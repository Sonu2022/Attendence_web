import streamlit as st
import csv
import os
from datetime import datetime
import pytz

FILE_NAME = "attendance.csv"

# ----------------- FILE SETUP ----------------- #
def create_file_if_not_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time", "Status"])

# ----------------- LOAD DATA ----------------- #
def load_data():
    data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) == 4:
                    data.append(row)
    return data

# ----------------- DUPLICATE CHECK ----------------- #
def already_marked_today(name, today):
    data = load_data()
    for row in data:
        if row[0].lower() == name.lower() and row[1] == today:
            return True
    return False

# ----------------- MARK ATTENDANCE ----------------- #
def mark_attendance(name, status):
    if name == "" or status == "":
        st.error("Please fill all fields")
        return

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    date_today = now.strftime("%d-%m-%Y")
    time_now = now.strftime("%H:%M:%S")

    if already_marked_today(name, date_today):
        st.warning("Attendance already marked for today")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, date_today, time_now, status])

    st.success("Attendance marked successfully")

# ----------------- DELETE RECORD ----------------- #
def delete_attendance(selected_row):
    with open(FILE_NAME, "r", newline="") as file:
        rows = list(csv.reader(file))

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Status"])
        for row in rows[1:]:
            if row != selected_row:
                writer.writerow(row)

    st.success("Attendance deleted successfully")

# ----------------- CLEAR ALL ----------------- #
def clear_all():
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Status"])
    st.experimental_rerun()

# ----------------- STREAMLIT UI ----------------- #
st.set_page_config(page_title="Attendance Management System", layout="centered")

st.title("📋 Attendance Management System")

create_file_if_not_exists()

name = st.text_input("Student Name")
status = st.selectbox("Status", ["", "Present", "Absent"])

if st.button("Mark Attendance"):
    mark_attendance(name, status)

st.markdown("---")
st.subheader("📄 Attendance Records")

data = load_data()

if data:
    for i, row in enumerate(data):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        col1.write(row[0])
        col2.write(row[1])
        col3.write(row[2])
        col4.write(row[3])
        if col5.button("Delete", key=f"del_{i}"):
            delete_attendance(row)
            st.experimental_rerun()
else:
    st.info("No attendance records found")

st.markdown("---")

# ----------------- ACTION BUTTONS ----------------- #
colA, colB = st.columns(2)

with colA:
    if st.button("🗑 Clear All Records"):
        clear_all()

with colB:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            st.download_button(
                label="⬇ Download CSV",
                data=f,
                file_name="attendance.csv",
                mime="text/csv"
            )

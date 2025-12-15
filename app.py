import streamlit as st
import csv
import os
from datetime import datetime
import pytz

FILE_NAME = "attendance.csv"

# -------------------- FILE SETUP -------------------- #
def create_file_if_not_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time", "Status"])

# -------------------- LOAD DATA -------------------- #
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

# -------------------- DUPLICATE CHECK -------------------- #
def already_marked_today(name, today):
    for row in load_data():
        if row[0].lower() == name.lower() and row[1] == today:
            return True
    return False

# -------------------- MARK ATTENDANCE -------------------- #
def mark_attendance(name, status):
    if not name or not status:
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
        csv.writer(file).writerow([name, date_today, time_now, status])

    st.success("Attendance marked successfully")

# -------------------- DELETE RECORD -------------------- #
def delete_attendance(row_to_delete):
    with open(FILE_NAME, "r", newline="") as file:
        rows = list(csv.reader(file))

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Status"])
        for row in rows[1:]:
            if row != row_to_delete:
                writer.writerow(row)

# -------------------- CLEAR ALL -------------------- #
def clear_all():
    with open(FILE_NAME, "w", newline="") as file:
        csv.writer(file).writerow(["Name", "Date", "Time", "Status"])
    st.rerun()

# -------------------- STREAMLIT UI -------------------- #
st.set_page_config("Attendance Management System", layout="centered")

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
        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
        c1.write(row[0])
        c2.write(row[1])
        c3.write(row[2])
        c4.write(row[3])

        if c5.button("Delete", key=f"del_{i}"):
            delete_attendance(row)
            st.success("Attendance deleted successfully")
            st.rerun()
else:
    st.info("No attendance records found")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑 Clear All Records"):
        clear_all()

with col2:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            st.download_button(
                "⬇ Download CSV",
                f,
                "attendance.csv",
                "text/csv"
            )

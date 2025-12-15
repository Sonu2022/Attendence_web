import streamlit as st
import csv
import os
from datetime import datetime

FILE_NAME = "attendance.csv"

# Ensure CSV file exists
def create_file_if_not_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time", "Status"])

# Mark attendance
def mark_attendance(name, status):
    if name == "" or status == "":
        st.error("Please fill all fields")
        return

    now = datetime.now()
    date_today = now.strftime("%d-%m-%Y")
    time_now = now.strftime("%H:%M:%S")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, date_today, time_now, status])

    st.success("Attendance marked successfully")

# Load attendance data
def load_data():
    data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) == 4:
                    data.append(row)
    return data

# Delete a record
def delete_attendance(selected_row):
    if not selected_row:
        st.warning("Select a record to delete")
        return

    with open(FILE_NAME, "r", newline="") as file:
        rows = list(csv.reader(file))

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Status"])
        for row in rows[1:]:
            if row != selected_row:
                writer.writerow(row)
    st.success("Attendance deleted successfully")

# ---------------- Streamlit UI ---------------- #

st.title("Attendance Management System")

create_file_if_not_exists()

# Input fields
name = st.text_input("Student Name")
status = st.selectbox("Status", ["", "Present", "Absent"])

if st.button("Mark Attendance"):
    mark_attendance(name, status)

st.markdown("---")
st.subheader("Attendance Records")

data = load_data()

if data:
    for i, row in enumerate(data):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        col1.write(row[0])
        col2.write(row[1])
        col3.write(row[2])
        col4.write(row[3])
        if col5.button("Delete", key=i):
            delete_attendance(row)
            st.experimental_rerun()
else:
    st.info("No attendance records found.")

# Download CSV
if st.button("Download CSV"):
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            st.download_button(
                label="Download Attendance CSV",
                data=f,
                file_name="attendance.csv",
                mime="text/csv"
            )
    else:
        st.error("No attendance data found")

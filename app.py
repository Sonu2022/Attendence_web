import streamlit as st
import csv
import os
from datetime import datetime
import pytz

# ---------- CONFIG ----------
DATA_DIR = "attendance_data"
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config("Attendance Management System", layout="centered")
st.title("📋 Attendance Management System")

# ---------- LOGIN ----------
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if not st.session_state.user_email:
    email = st.text_input("Enter your Email ID")
    if st.button("Login"):
        if email and "@" in email:
            st.session_state.user_email = email.lower()
            st.rerun()
        else:
            st.error("Please enter a valid email")
    st.stop()

# ---------- USER-SPECIFIC FILE ----------
safe_email = st.session_state.user_email.replace("@", "_").replace(".", "_")
USER_FILE = os.path.join(DATA_DIR, f"{safe_email}.csv")

# ---------- FILE CREATE ----------
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Date", "Time", "Status"])

# ---------- FUNCTIONS ----------
def load_data():
    with open(USER_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        return list(reader)

def mark_attendance(name, status):
    if not name or not status:
        st.error("Please fill all fields")
        return

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    with open(USER_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            name,
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S"),
            status
        ])

    st.success("Attendance marked")

def delete_attendance(row_to_delete):
    rows = load_data()
    with open(USER_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time", "Status"])
        for row in rows:
            if row != row_to_delete:
                writer.writerow(row)

# ---------- UI ----------
st.success(f"Logged in as: {st.session_state.user_email}")

name = st.text_input("Student Name")
status = st.selectbox("Status", ["", "Present", "Absent"])

if st.button("Mark Attendance"):
    mark_attendance(name, status)

st.markdown("---")
st.subheader("📄 My Attendance (Only My Data)")

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
            st.rerun()
else:
    st.info("No attendance records found")

st.markdown("---")

# ---------- DOWNLOAD ----------
with open(USER_FILE, "rb") as f:
    st.download_button(
        "⬇ Download My CSV",
        f,
        file_name="attendance.csv",
        mime="text/csv"
    )

# ---------- LOGOUT ----------
if st.button("🚪 Logout"):
    st.session_state.user_email = ""
    st.rerun()

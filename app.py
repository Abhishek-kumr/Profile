import streamlit as st
import pandas as pd
from datetime import date

# ----------------------------
# Initial Data
# ----------------------------
sites = {
    "Site A": {
        "manager": "manager_a",
        "guards": ["Ramesh", "Suresh"]
    },
    "Site B": {
        "manager": "manager_b",
        "guards": ["Amit", "Rahul"]
    }
}

# Initialize attendance data
if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(
        columns=["Date", "Site", "Guard", "Status"]
    )

# ----------------------------
# Login Section
# ----------------------------
st.title("🛡️ Attendance Management System")

st.sidebar.header("Login")

username = st.sidebar.text_input("Username")
role = st.sidebar.selectbox("Role", ["Site Manager", "Security Guard"])
site = st.sidebar.selectbox("Site", list(sites.keys()))

login_btn = st.sidebar.button("Login")

if login_btn:
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.role = role
    st.session_state.site = site

# ----------------------------
# Authorization Check
# ----------------------------
if "logged_in" in st.session_state:

    st.success(f"Logged in as {st.session_state.role}")

    # ----------------------------
    # Site Manager Dashboard
    # ----------------------------
    if st.session_state.role == "Site Manager":

        # Verify manager
        if st.session_state.username != sites[site]["manager"]:
            st.error("❌ You are not authorized as manager for this site.")
        else:
            st.subheader(f"📍 Managing Attendance for {site}")

            guard = st.selectbox(
                "Select Guard",
                sites[site]["guards"]
            )

            status = st.radio("Attendance Status", ["Present", "Absent"])
            today = date.today()

            if st.button("Update Attendance"):
                new_entry = {
                    "Date": today,
                    "Site": site,
                    "Guard": guard,
                    "Status": status
                }
                st.session_state.attendance = pd.concat(
                    [st.session_state.attendance, pd.DataFrame([new_entry])],
                    ignore_index=True
                )
                st.success("✅ Attendance updated successfully")

            st.subheader("📊 Attendance Records")
            st.dataframe(st.session_state.attendance)

    # ----------------------------
    # Security Guard Dashboard
    # ----------------------------
    elif st.session_state.role == "Security Guard":

        st.subheader("👮 Guard Attendance View")

        guard_name = st.text_input("Enter Your Name")

        if st.button("View Attendance"):
            guard_data = st.session_state.attendance[
                (st.session_state.attendance["Guard"] == guard_name) &
                (st.session_state.attendance["Site"] == site)
            ]

            if guard_data.empty:
                st.warning("No attendance records found.")
            else:
                st.dataframe(guard_data)

else:
    st.info("Please login from the sidebar.")

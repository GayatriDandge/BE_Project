import streamlit as st

# ------------------ INIT USERS (FIX ✅) ------------------
if "users" not in st.session_state:
    st.session_state["users"] = {
        "doctor@health.com": "1234"
    }

# ------------------ LOGIN ------------------
def login():
    st.markdown("## 🔐 Doctor Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.session_state["users"]

        if email in users and users[email] == password:
            st.success("Login successful")
            st.session_state["logged_in"] = True
            st.session_state["page"] = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")


# ------------------ SIGNUP ------------------
def signup():
    st.markdown("## 📝 Doctor Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if password != confirm:
            st.error("Passwords do not match")

        elif email in st.session_state["users"]:
            st.warning("User already exists")

        else:
            st.session_state["users"][email] = password
            st.success("Account created successfully")
            st.session_state["auth_page"] = "login"
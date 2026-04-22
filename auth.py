import streamlit as st
import json
import os

USER_FILE = "users.json"

# ---------- LOAD USERS ----------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# ---------- SAVE USERS ----------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------- LOGIN / SIGNUP UI ----------
def login_signup():
    st.sidebar.title("🔐 Authentication")

    choice = st.sidebar.selectbox("Select", ["Login", "Signup"])

    users = load_users()

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # ---------- LOGIN ----------
    if choice == "Login":
        if st.sidebar.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.sidebar.success(f"Welcome {username} 👋")
            else:
                st.sidebar.error("Invalid credentials")

    # ---------- SIGNUP ----------
    elif choice == "Signup":
        if st.sidebar.button("Create Account"):
            if username in users:
                st.sidebar.warning("User already exists")
            elif username == "" or password == "":
                st.sidebar.warning("Enter valid details")
            else:
                users[username] = password
                save_users(users)
                st.sidebar.success("Account created! Now login")

# ---------- CHECK LOGIN ----------
def check_login():
    return st.session_state.get("logged_in", False)
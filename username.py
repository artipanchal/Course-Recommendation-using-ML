import os
import streamlit as st

# Define the correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "password"

def main():
   
    st.title("STUDENT LOGIN")
    st.markdown(
    """
    <style>
        .stApp > header {
            background-color: transparent;
        }
        .css-16idsys p 
        {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 22px;
            font: bold;
        }
        .css-1n543e5 {
            width:90px;
            height:50px;
        }

        .stApp {
            color: green;
            background: hsla(208, 67%, 81%, 1);
            background: linear-gradient(90deg, hsla(208, 67%, 81%, 1) 0%, hsla(37, 65%, 85%, 1) 50%, hsla(301, 65%, 83%, 1) 100%);
            background: -moz-linear-gradient(90deg, hsla(208, 67%, 81%, 1) 0%, hsla(37, 65%, 85%, 1) 50%, hsla(301, 65%, 83%, 1) 100%);
            background: -webkit-linear-gradient(90deg, hsla(208, 67%, 81%, 1) 0%, hsla(37, 65%, 85%, 1) 50%, hsla(301, 65%, 83%, 1) 100%);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#AED1EF", endColorstr="#F2DFC1", GradientType=1);
            animation: my_animation 20s ease infinite;
            background-size: 200% 200%;
            background-attachment: fixed;
        }

        .login-header {
            color: Black;
        }

        @keyframes my_animation {
            0% {background-position: 0% 0%;}
            50% {background-position: 100% 100%;}
            100% {background-position: 0% 0%;}
        }
    </style>
    """,
    unsafe_allow_html=True
)

    username = st.text_input("Username", value="", key="username", help="")
    password = st.text_input("Password", value="", key="password", help="", type="password")

    if st.button("Login", key="login-button", help=""):
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.success("Logged in successfully!")
            # Set a session variable to indicate that the user is logged in
            st.session_state.logged_in = True
            # Redirect to the desired page
            open_main_page()
        else:
            st.write("<div class='error-message'>Invalid username or password</div>", unsafe_allow_html=True)

    st.write("</div>", unsafe_allow_html=True)

# Function to open the main page
def open_main_page():
    try:
        # Run main.py using os.system
        os.system("streamlit run main.py")
        st.success('Main page opened successfully!')
    except Exception as e:
        st.error(f'Error opening main page: {e}')

if __name__ == "__main__":
    main()

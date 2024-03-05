import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from PIL import Image

def load_image(image_path):
    return Image.open(image_path)


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>Smart Irrigation Tool</h1>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.sidebar.image(load_image("logo.png"), use_column_width=True)
        st.sidebar.image(load_image("logo2.png"), use_column_width=True)
        st.sidebar.markdown("<p style='text-align: center;'><a href='mailto:f.deoliveirasalles@agrifirm.com'>Contact: Filipe Salles</a></p>", unsafe_allow_html=True)

        
        if st.session_state.get("logged_in", False):
            # st.page_link("pages/page1.py", label="Secret Company Stuff", icon="🔒")
            # st.page_link("pages/page2.py", label="More Secret Stuff", icon="🕵️")
            if st.button("Log out"):
                logout()
        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")

            

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")


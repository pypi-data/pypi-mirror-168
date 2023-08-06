import textwrap
import streamlit as st


def hello_world():
    st.markdown(
        textwrap.dedent(
            """
            # RHDZMOTA Hello World!

            This is a simple streamlit hello-world application.
            """
        )
    )

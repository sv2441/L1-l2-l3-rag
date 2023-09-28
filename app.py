## import the CSV file and output the CSV file 

import streamlit as st

st.set_page_config(
    page_title="OP Generation",
    page_icon="👋",
)

st.image('logo.png')
st.title("👨‍💻 OP Generation")


embedded_code = """
<iframe width="560" height="315" src="https://www.youtube.com/embed/2LUJIUHLvhs?si=AcztUwcgaevRDP5n" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
"""
st.markdown(embedded_code, unsafe_allow_html=True)

## import the CSV file and output the CSV file 

import streamlit as st

st.set_page_config(
    page_title="OP Generation",
    page_icon="👋",
)

st.image('logo.png')
st.title("👨‍💻 OP Generation")


embedded_code = """
<iframe src="https://www.canva.com/design/DAFvushARmE/watch" width="768" height="432" frameborder="0" allowfullscreen="true"></iframe>
"""
st.markdown(embedded_code, unsafe_allow_html=True)


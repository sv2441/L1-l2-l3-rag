## import the CSV file and output the CSV file 

import streamlit as st

st.set_page_config(
    page_title="OP Generation",
    page_icon="👋",
)

st.image('logo.png')
st.title("👨‍💻 OP Generation")

embedded_code = """
<iframe width="768" height="432" src="https://miro.com/app/embed/uXjVMnDynt4=/?pres=1&frameId=3458764565130553333&embedId=649838642305" frameborder="0" scrolling="yes" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
"""
st.markdown(embedded_code, unsafe_allow_html=True)

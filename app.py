## import the CSV file and output the CSV file 

import streamlit as st

st.set_page_config(
    page_title="OP Generation",
    page_icon="👋",
)

st.image('logo.png')
st.title("👨‍💻 OP Generation")

embedded_code = """
<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVMnDynt4=/?moveToViewport=-1860,-498,1385,2042&embedId=630072882227" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
"""
st.markdown(embedded_code, unsafe_allow_html=True)

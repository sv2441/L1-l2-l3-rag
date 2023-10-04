## import the CSV file and output the CSV file 

import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
import csv
import os
import base64


load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
    
chat_llm = ChatOpenAI(temperature=0.6)
       
        
def get_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="PA-results.csv">Download CSV File</a>'
    return href

def convert_dict_to_csv(data_dict):
    with open('data11.csv', 'w', newline='') as csvfile:
        fieldnames = ['Pre/Post', 'Actionables']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty and write the header only if it's empty
        is_file_empty = csvfile.tell() == 0
        if is_file_empty:
            writer.writeheader()

        for key, value in data_dict.items():
            if isinstance(value, list):
                for item in value:
                    writer.writerow({'Pre/Post': key, 'Actionables': item})
            else:
                writer.writerow({'Pre/Post': key, 'Actionables': value})

def prompta_generator(df):
    
    #####output parser #############################################

    Action_schema = ResponseSchema(name="Actionable",
                                description="List of Actionable requirements from the text")

    response_schemas = [ Action_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    ###########################################################################

    title_template = """ \ You are an AI Governance bot.
                Extract actionable requirements from the "{topic}".
               {format_instructions}
                """
    prompt = ChatPromptTemplate.from_template(template=title_template)

##############################################################################################
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row['Regulatory text'], format_instructions=format_instructions)
        response = chat_llm(messages)
        response_as_dict = output_parser.parse(response.content)
        data = response_as_dict
        convert_dict_to_csv(data)
        test=pd.DataFrame(df.iloc[index]).T
        data11 = pd.read_csv(r'data11.csv',encoding='cp1252')
        results = pd.concat([test, data11], axis=1).fillna(0)
        # result.to_csv('final1.csv')
        # test=pd.DataFrame(df.iloc[0]).T
        # results = pd.concat([test, data11], axis=1).fillna(0)
        results.to_csv('PA-results.csv', mode='a', header=not os.path.isfile('PA-results.csv'), index=False)
    results=pd.read_csv("PA-results.csv" , usecols=["Regulatory text","Actionables"]
    st.subheader("OP's")
    st.dataframe(results)
    st.markdown(get_download_link(results), unsafe_allow_html=True)
    


def main():
    st.image('logo.png')
    st.title("👨‍💻 Extract Actionables")

    # File upload
    file = st.file_uploader("Upload a CSV file", type=["csv"])

    if file is not None:
        # Read CSV file
        df = pd.read_csv(file)

        # Display preview
        st.subheader("CSV File Preview")
        st.dataframe(df)

        # Button to process the file
        if st.button("Extract Actionable"):
            prompta_generator(df)
            
        
if __name__ == "__main__":
    main()

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
# chat_llm = ChatOpenAI(temperature=0.6)


def dict_to_csv(data, filename, append=False):
    mode = 'a' if append else 'w'
    with open(filename, mode, newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if not append:
            writer.writeheader()
        writer.writerow(data)

def dict_to_csv2(data, filename, append=False):
    mode = 'a' if append else 'w'
    with open(filename, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['L1 Intended Results'])
        if not append:
            writer.writeheader()
        writer.writerow({'L1 Intended Results': data})       
        
def get_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="PA-results.csv">Download CSV File</a>'
    return href

# def convert_dict_to_csv(data_dict):
#     with open('data11.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Pre/Post', 'Activity']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         # Check if the file is empty and write the header only if it's empty
#         is_file_empty = csvfile.tell() == 0
#         if is_file_empty:
#             writer.writeheader()

#         for key, value in data_dict.items():
#             if isinstance(value, list):
#                 for item in value:
#                     writer.writerow({'Pre/Post': key, 'Activity': item})
#             else:
#                 writer.writerow({'Pre/Post': key, 'Activity': value})

# def prompta_generator(df):
    
#     #####output parser #############################################

#     Action_schema = ResponseSchema(name="Actionable",
#                                 description="List of Actionable requirements from the text")

#     response_schemas = [ Action_schema]
#     output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#     format_instructions = output_parser.get_format_instructions()

#     ###########################################################################

#     title_template = """ \ You are an AI Governance bot.
#                 Extract actionable requirements from the "{topic}".
#                {format_instructions}
#                 """
#     prompt = ChatPromptTemplate.from_template(template=title_template)

# ##############################################################################################
    
#     for index, row in df.iterrows():
#         messages = prompt.format_messages(topic=row['Description'], format_instructions=format_instructions)
#         response = chat_llm(messages)
#         response_as_dict = output_parser.parse(response.content)
#         data = response_as_dict
#         convert_dict_to_csv(data)
#         test=pd.DataFrame(df.iloc[index]).T
#         data11 = pd.read_csv(r'data11.csv',encoding='cp1252')
#         results = pd.concat([test, data11], axis=1).fillna(0)
#         # result.to_csv('final1.csv')
#         # test=pd.DataFrame(df.iloc[0]).T
#         # results = pd.concat([test, data11], axis=1).fillna(0)
#         results.to_csv('PA-results.csv', mode='a', header=not os.path.isfile('PA-results.csv'), index=False)
#     st.subheader("OP's")
#     st.dataframe(results)


def description_generator(df):
    
    summary_schema = ResponseSchema(name="Description",
                                description="Description of Action Associated in Text in 30words.")

    response_schemas = [summary_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    title_template = """ \ You are an AI Governance bot.
            Generate actionable requirement IN 30 WORDS for "{topic}".
            using the following conditions
            1) One or two sentences description of the activity
            2) Provide a clear insight of what the activity is
            3) Provide a deeper understanding of what the activity entails
            4) Do not include expected outcome
            5) Do not include justification on why the activity should be implemented
            Use words like establish, define, create, execute, perform, provide, validate, approve, review, monitor as action words.
            {format_instructions}
            """
    prompt = ChatPromptTemplate.from_template(template=title_template)
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row["Actionables"], format_instructions=format_instructions)
        response = chat_llm(messages)
        response_as_dict = output_parser.parse(response.content)
        data = response_as_dict
        dict_to_csv(data, 'data12.csv', append=True)
    data12 = pd.read_csv('data12.csv', names=['L1 Description'])
    result = pd.concat([df, data12], axis=1)
    result.to_csv('PA-results.csv')
    st.subheader("Description Result")
    st.dataframe(result)
    
def l1_title_generator(df):
    
    Action_schema = ResponseSchema(name="Action",
                            description="Summarize actionable in max of 10 words")

    response_schemas = [ Action_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    title_template = """ \ You are an AI Governance bot.
                Summarize actionable in max of 10 words for "{topic}". Ensure that the output has an action word.
                
               {format_instructions}
                """
    prompt = ChatPromptTemplate.from_template(template=title_template)
   
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row['L1 Description'], format_instructions=format_instructions)
        response = chat_llm(messages)
        response_as_dict = output_parser.parse(response.content)
        data = response_as_dict
        # convert_dict_to_csv(data)
        dict_to_csv(data, 'data13.csv', append=True)
    data13 = pd.read_csv(r'data13.csv',encoding='cp1252',names=['L1 title'])
    results = pd.concat([df, data13], axis=1)
    results.to_csv("PA-results.csv")
    st.subheader("Description Result")
    st.dataframe(results)   

def intended_results_generator(df):
    intended_results_schema = ResponseSchema(name="Intended Results",
                                description="Summary of intended results.")

    response_schemas = [intended_results_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()


    title_template = """ \ You are an AI Governance bot.
                Provide two or three expected results of doing the "{topic}" as bullet points from a third person perspective for the following by adopting the conditions given below:
                (1) Intended results shall be specific to the activity.
                (2) Intended results details an expected outcome or result of the activity.
                (3) Intended result should not be a rationale / justification / motivation for the activity and it should not be general / generic.
                
                """
    prompt = ChatPromptTemplate.from_template(template=title_template)
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row["L1 Description"])
        response = chat_llm(messages)
        data = str(response.content)  # Convert data to string
        dict_to_csv2(data, 'data14.csv', append=True)

    data14 = pd.read_csv('data14.csv', names=['L1 Intended Results'])
    result = pd.concat([df, data14], axis=1)
    result.to_csv('PA-results.csv', index=False) 
    st.dataframe(result)
    # st.markdown(get_download_link(result), unsafe_allow_html=True)
    
    
def artefact_description_generator(df):
    Artefact_description_schema = ResponseSchema(name="Artefact Description",
                                description="Provide an artefact description.")

    response_schemas = [Artefact_description_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    title_template = """ \ You are an AI Governance bot.
                Determine basis the following "{topic}", whether an artefact as a documentation to evidence performance is required or not.
                If an artefact is required answer with "Yes", else with "no".
                Provide a name for the artefact.
                {format_instructions}"""
    prompt = ChatPromptTemplate.from_template(template=title_template)    
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row["L1 Description"], format_instructions=format_instructions)
        response = chat_llm(messages)
        response_as_dict = output_parser.parse(response.content)
        data = response_as_dict
        dict_to_csv2(data, 'data15.csv', append=True)
    data15 = pd.read_csv('data15.csv', names=['L1 Artefact Description'])
    result = pd.concat([df, data15], axis=1)
    result.to_csv('PA-results.csv')
    st.subheader("Artefact Description")
    st.dataframe(result)
    st.markdown(get_download_link(result), unsafe_allow_html=True)
    
    
def specifications_generator(df):
    Artefact_basis_schema = ResponseSchema(name="Specifications",
                                description="Provide a name for Specifications")

    response_schemas = [Artefact_basis_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    title_template = """ \ You are an AI Governance bot.
                List any specific conditions or considerations mentioned in the following "{topic}".
                Do not generalize. Do not exhibit any prior knowledge other than content provided above. Mention "no" in case there are no conditions.
                """

    prompt = ChatPromptTemplate.from_template(template=title_template)
    
    for index, row in df.iterrows():
        messages = prompt.format_messages(topic=row["L1 Description"])
        response = chat_llm(messages)
        data = str(response.content)  # Convert data to string
        dict_to_csv2(data, 'data16.csv', append=True)
    data16 = pd.read_csv('data16.csv', names=['L1 Specifications'])
    result = pd.concat([df, data16], axis=1)
    result.to_csv('PA-results.csv', index=False)  
    st.subheader("Specifications")
    st.dataframe(result)
    # final_result=pd.read_csv('PA-results.csv',usecols=['CO Level123 Code','Level','Code','Name','Description','Prompt A','L1 Description','L1 title','L1 Intended Results',' L1 Artefact Description','L1 Specifications'])
    
    st.markdown(get_download_link(result), unsafe_allow_html=True)
    


def main():
    st.image('logo.png')
    st.title("👨‍💻 L1 OP Generation")

    # File upload
    file = st.file_uploader("Upload a CSV file", type=["csv"])

    if file is not None:
        # Read CSV file
        L1_df = pd.read_csv(file)

        # Display preview
        st.subheader("CSV File Preview")
        st.dataframe(L1_df)

            
        if st.button("Generate Description"):
            description_generator(L1_df)
        
        if st.button("Generate Title"):
            l1_title_generator(pd.read_csv('PA-results.csv'))
       
        if st.button("Generate Intended Results"):
            intended_results_generator(pd.read_csv('PA-results.csv'))
            
        if st.button("Generate Artefact Description"):
            artefact_description_generator(pd.read_csv('PA-results.csv'))
            
        if st.button("Generate Specifications"):
            specifications_generator(pd.read_csv('PA-results.csv'))
            
        
if __name__ == "__main__":
    main()

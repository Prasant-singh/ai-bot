from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama  # Correct import from langchain_community

import streamlit as st
import os
import re
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  # Load environment variables

openai_api_key = os.getenv("OPENAI_API_KEY")
langchai_api_key = os.getenv("LANGCHAIN_API_KEY")

if not openai_api_key:
    st.error("OPENAI_API_KEY is not set. Please set it in your .env file.")
if not langchai_api_key:
    st.error("LANGCHAI_API_KEY is not set. Please set it in your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LANGCHAIN_API_KEY"] = langchai_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question: {question}")
    ]
)

# Streamlit framework
st.title("Langchain Demo with OPENAI API")
input_text = st.text_input("Search the topic you want")

# Initialize the Ollama model
try:
    llm = ollama.Ollama(model="mistral")  # Adjust based on the correct class name
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    if st.button("Submit"):
        if input_text:
            prompt_text = prompt.format(question=input_text)
            # Use invoke instead of run
            response = chain.invoke({"question": input_text})  # Pass inputs as a dictionary
            st.write(response)
            print("Response: ",response)
        else:
            st.error("Please enter a question.")
except Exception as e:
    st.error(f"An error occurred: {e}")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")  # Specify the path if it's not in the root directory


# Ensure the environment variables are loaded correctly
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

# OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    try:
        result = chain.invoke({"question": input_text})
        st.write(result)
    except Exception as e:
        st.error(f"An error occurred: {e}")



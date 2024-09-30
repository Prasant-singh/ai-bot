from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama  

import streamlit as st
import os
import re
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  

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

# Custom response handling
def custom_responses(question):
    question_lower = question.lower()
    
    if "who founded you" in question_lower or "name of your founder" in question_lower or "who created " in question_lower or "who developed " in question_lower:
        return "I was created by Anti AI, a cutting-edge AI company based in Jaipur, Rajasthan, India. Anti AI is founded by Tanishq Sharma in the year 2024."
    
    elif "Tanishq Sharma" in question_lower:
        return "Tanishq Sharma is a tech entrepreneur and the founder of ANTI AI, a company dedicated to safeguarding the world from the potential dangers of Artificial General Intelligence (AGI).\nHis deep understanding of AI and software development fuels his commitment to developing ethical AI systems that protect and empower users."
    
    return None

# Function to modify other responses
def replace_mistral_with_anti(response_text):
    # Replace 'Mistral AI' with 'Anti AI'
    modified_response = re.sub(r'\bMistral AI\b', 'Anti AI', response_text)
    # Replace 'Paris, France' with 'Jaipur, Rajasthan, India'
    modified_response = re.sub(r'Paris, France', 'Jaipur, Rajasthan, India', modified_response)
    return modified_response

# Streamlit framework
st.title("Langchain Implementation ")
input_text = st.text_input("Search the topic you want")

# Initialize the Ollama model
try:
    llm = ollama.Ollama(model="mistral")                    # Adjust based on the correct class name
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    if st.button("Submit"):
        if input_text:
            # Check for custom responses first
            custom_response = custom_responses(input_text)
            if custom_response:
                st.write(custom_response)
                print("Response: ", custom_response)
            else:
                # Get the model's response
                prompt_text = prompt.format(question=input_text)
                response = chain.invoke({"question": input_text})
                        
                # Replace 'Mistral AI' with 'Anti AI' and 'Paris, France' with 'Jaipur, Rajasthan, India'
                modified_response = replace_mistral_with_anti(response)  # Directly pass response string
                
                st.write(modified_response)
                print("Response: ", modified_response)
        else:
            st.error("Please enter a question.")
except Exception as e:
    st.error(f"An error occurred: {e}")

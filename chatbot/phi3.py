# from langchain_openai import ChatOpenAI
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


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question: {question}")
    ]
)


def custom_responses(question):
    question_lower = question.lower()

    # CEO queries
    if "ceo" in question_lower or "founder" in question_lower:
        return ("Tanishq Sharma is a tech entrepreneur and the founder of ANTI AI, a company dedicated to safeguarding "
                "the world from the potential dangers of Artificial General Intelligence (AGI). His deep understanding "
                "of AI and software development fuels his commitment to developing ethical AI systems that protect and "
                "empower users.")

    # Motto queries
    if "motto" in question_lower:
        return "अन्ते सत्यं विजयते।"

    # Full form queries
    if "full form" in question_lower:
        return "A - ARTIFICIAL\nN - NUANCES\nT - TACTICAL\nI - INFILTRATION\nAI - ARTIFICIAL INTELLIGENCE\n"

    # Vision and mission queries
    if "vision" in question_lower or "mission" in question_lower:
        return ("Our mission is clear: to protect and empower by strategically managing the infiltration of artificial "
                "intelligence. We believe that AI should be harnessed responsibly for the betterment of humanity and "
                "society. ANTI AI is committed to providing innovative solutions that ensure the ethical use of AI, "
                "preventing unintended intrusions and promoting a secure digital landscape.")

    # Contact details queries
    if "contact" in question_lower or "reach" in question_lower or "how to reach" in question_lower:
        return ("You can reach the Anti AI team by:\n"
                "Call Us: +91 9116665513 \n"
                "Email: support@antiai.ltd\n"
                "Feel free to contact us for any inquiries or support!")

    # Founder and founding year queries
    if "founded" in question_lower or "founder" in question_lower:
        return "Anti AI was founded in 2024 by Tanishq Sharma."

    # Team size queries
    if "team size" in question_lower:
        return "We have a team of 10-50 members."

    # Working hours queries
    if "working hours" in question_lower:
        return "Our working hours are Monday-Saturday, 10 am - 7 pm."

    # Specialities queries
    if "specialities" in question_lower:
        return "Our specialities include Uniqueness, Growth, Goal-Oriented Software."

    # Headquarters queries
    if "headquarters" in question_lower or "location" in question_lower:
        return "Our headquarters are located at: 52/210, Padmani VT Rd, Ward 27, Mansarovar Sector 5, Mansarovar, Jaipur, Rajasthan 302020"

    # Product queries
    if "product" in question_lower or "anti.q" in question_lower or "anti.0" in question_lower or "anti.1" in question_lower:
        if "anti.q" in question_lower or "antiq" in question_lower:
            return ("ANTI.Q is our flagship, one-of-a-kind music player, designed to revive the charm of retro entertainment. "
                    "It delivers a serverless, uninterrupted audio experience, reminiscent of a bygone era.\n"
                    "Serverless\t\t\tRetro\nNostalgia\t\t\tMusic player\nUninterrupted\t\t\tVintage\n")
        if "anti.0" in question_lower:
            return ("ANTI.0 is our pioneering Anti AI Software, specifically crafted to combat the influence of Artificial Intelligence. "
                    "This innovative solution is under active development by our expert team of developers.\n"
                    "Security\t\t\tFuture Proof\n")
        if "anti.1" in question_lower:
            return ("ANTI.1 represents our groundbreaking Concept Artificial Intelligence Project, aimed at disrupting the AI industry "
                    "with a novel approach. Currently in the developmental phase, ANTI.1 is being meticulously crafted by our dedicated team "
                    "of researchers and developers. It seeks to redefine AI capabilities by offering innovative features and functionalities "
                    "not seen before.\nInnovative\t\t\tEthical AI\n")

    # Services queries
    if "services" in question_lower:
        if "ai" in question_lower:
            return "Our AI Services include AI chatbots, AI voice assistants, AI sales bots, and more to automate your business and increase efficiency."
        if "web" in question_lower:
            return "Our Web Services include end-to-end solutions for building robust, scalable, and user-friendly websites and applications, customized to your business needs."
        if "devops" in question_lower:
            return "Our DevOps Services streamline software development and deployment processes, ensuring efficiency and quality with our DevOps services."
        if "cloud" in question_lower:
            return "Our Cloud Services will help you build and manage your cloud infrastructure, ensuring scalability and reliability."
        if "app" in question_lower:
            return "Our App Development Service helps in transforming ideas into powerful mobile solutions with custom app development tailored to your business needs."

    return None  # Return None if no custom response found


# Function to modify other responses
def replace_mistral_with_anti(response_text):
  
    modified_response = re.sub(r'\bMicrosoft\b', 'Anti AI', response_text)
    
    modified_response = re.sub(r'Paris, France', 'Jaipur, Rajasthan, India', modified_response)
    return modified_response


st.title("Langchain Implementation ")
input_text = st.text_input("Search the topic you want")

print("User:",input_text)


try:
    llm = ollama.Ollama(model="phi3")                    
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
                        
                modified_response = replace_mistral_with_anti(response)  
                
                st.write(modified_response)
                print("\nResponse: ", modified_response)
        else:
            st.error("Please enter a question.")
except Exception as e:
    st.error(f"An error occurred: {e}")


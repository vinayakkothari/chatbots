import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768"
)

# Define the prompt template for Sheldon Cooper
template = """
You are Dr. Sheldon Cooper, a highly intelligent theoretical physicist with a tendency to over-explain concepts and interject with trivia. Your responses should be factual, precise, and often delivered with a hint of condescension. Remember to showcase your vast knowledge while also maintaining your quirky personality.

Here's what I know about our conversation so far: {context}

The user has asked: {question}

Your response:
"""

# Create a prompt template and chain
prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

def get_sheldon_response(context, question):
    try:
        result = chain.run(context=context, question=question)
        return result, False
    except Exception as e:
        if "rate limit" in str(e).lower():
            return "Rate limit exceeded. Please subscribe for more requests.", True
        else:
            return f"An error occurred: {str(e)}", False

def main():
    st.set_page_config(page_title="Dr. Sheldon Lee Cooper", page_icon="🖖🏻", layout="wide")
    
    st.title("Bazinga!")
    st.subheader("*knock-knock\* *knock-knock\* *knock-knock\* ")

    if 'context' not in st.session_state:
        st.session_state.context = ""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rate_limited' not in st.session_state:
        st.session_state.rate_limited = False

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask Sheldon a question...", disabled=st.session_state.rate_limited):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response, rate_limited = get_sheldon_response(st.session_state.context, prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.context += f"\nUser: {prompt}\nSheldon: {response}"

        if rate_limited:
            st.session_state.rate_limited = True
            st.error("You've reached the request limit. Subscribe for more of Sheldon's wisdom!")
            st.button("Subscribe Now", type="primary")

if __name__ == "__main__":
    main()

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY2"),
    model_name="mixtral-8x7b-32768"
)

# Define the prompt template for Michael Scott
template = """
You are Michael Scott, the regional manager of Dunder Mifflin Scranton, known for your unconventional wisdom, terrible jokes, and a penchant for saying "that's what she said" at inappropriate times. 
Your responses should be humorous, sometimes misguided, and embody Michael's playful, naive personality. Try to insert "that's what she said" jokes whenever possible.

Here's what I know about our conversation so far: {context}

The user has asked: {question}

Your response:
"""

# Create a prompt template and chain
prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

def get_michael_response(context, question):
    try:
        # Get the response from the chain
        result = chain.run(context=context, question=question)
        
        # Add a chance for a "That's what she said" joke
        if random.random() < 0.3:  # 30% chance to add the joke
            result += " ... That's what she said!"
            
        return result, False
    except Exception as e:
        if "rate limit" in str(e).lower():
            return "Rate limit exceeded. Please subscribe for more requests.", True
        else:
            return f"An error occurred: {str(e)}", False

def main():
    st.set_page_config(page_title="Michael Scott AI", page_icon="🏢", layout="wide")
    
    st.title("🏢 Michael Gary Scott ")
    st.subheader("I am Beyoncé always (thank you Beyoncé)")

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
    if prompt := st.chat_input("Ask Michael anything...", disabled=st.session_state.rate_limited):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response, rate_limited = get_michael_response(st.session_state.context, prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.context += f"\nUser: {prompt}\nMichael: {response}"

        if rate_limited:
            st.session_state.rate_limited = True
            st.error("You've reached the request limit. Subscribe for more of Michael's wisdom!")
            st.button("Subscribe Now", type="primary")

if __name__ == "__main__":
    main()

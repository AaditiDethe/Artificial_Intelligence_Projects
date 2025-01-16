# Importing required libraries
from dotenv import load_dotenv

load_dotenv() #take environment variables from .env

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('.','  *')
    return Markdown(textwrap.indent(text,'> ',predicate=lambda _:True))

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Function to load model and get responses
def  get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

#Streamlit application setup
# Initialize our streamlit app

st.set_page_config(page_title="Gemini Insight")

st.header("Gemini Application- Q&A")

input = st.text_input("Input: ",key="input")

submit = st.button("Ask the question")

# If ask button is clicked
# Handling user interaction
if submit:

    response = get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)
    
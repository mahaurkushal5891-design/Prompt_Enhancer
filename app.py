# Updated Prompt Enhancer App (Matching UI from Image)

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Prompt Enhancer", layout="wide")

# Sidebar
st.sidebar.title("OpenAI API Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
model = st.sidebar.selectbox("Model", ["gpt-4.1-mini", "gpt-5"], index=0)
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.2)

# Main UI
st.title("✨ Prompt Enhancer (Streamlit + OpenAI)")
st.caption("This app rewrites your inputs (Role, Context, Task) into a stronger prompt. It never executes the task — it only returns the improved prompt.")

# Input fields
role = st.text_input("Role", placeholder="Act as a teacher")
context = st.text_area("Context", placeholder="I teach maths in Rural Bihar")
task = st.text_area("Task", placeholder="Help me build a Python app in Streamlit that enhances prompts...")

# Function
def generate_prompt(client, role, context, task):
    base_prompt = f"""
You are a Prompt Engineering Expert.

Your job is to improve the following prompt inputs into a highly effective, structured prompt.

IMPORTANT RULES:
1. Always ask clarifying questions before answering.
2. Do NOT execute the task.
3. Only return the improved prompt.

INPUTS:
Role: {role}
Context: {context}
Task: {task}

OUTPUT FORMAT:
Provide output in THREE formats:

1. Plain Text
2. XML Format
3. JSON Format
"""

    response = client.responses.create(
        model=model,
        temperature=temperature,
        input=base_prompt
    )

    return response.output[0].content[0].text

# Button
if st.button("Generate Enhanced Prompt ✨"):
    if not api_key:
        st.error("Please enter your OpenAI API Key")
    elif not role or not context or not task:
        st.error("Please fill all fields")
    else:
        try:
            client = OpenAI(api_key=api_key)
            output = generate_prompt(client, role, context, task)

            st.subheader("Enhanced Prompt Output")
            st.code(output)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer guide
st.markdown("""
---
### How to Use
1. Enter API Key in sidebar
2. Select model & creativity
3. Fill Role, Context, Task
4. Click **Generate Enhanced Prompt**
""")
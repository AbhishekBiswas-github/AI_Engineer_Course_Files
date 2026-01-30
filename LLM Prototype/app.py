from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Streamlit Chatbot", page_icon="💬")
st.title("Chatbot")

st.subheader("Prsonal Information", divider='rainbow')

name = st.text_input(label='Name', max_chars=None, placeholder="Enter your name")

experience = st.text_area(label='Experience', height=None, max_chars=None, placeholder="Enter your experience")

skills = st.text_area(label='Skills', height=None, max_chars=None, placeholder="Enter your Skills")

st.write(f"**Your Name:** {name}")
st.write(f"**Your Experience:** {experience}")
st.write(f"**Your Skills:** {skills}")

st.subheader("Company Position", divider="rainbow")

col1, col2 = st.columns(2)

with col1:
    level = st.radio(
        label="Choose Level",
        options=["Junior", "Mid Level", "Senior"],
        key="visibility"
    )

with col2:
    role = st.selectbox(
        label="Choose Role",
        options= ["Data Scientist", "Data Engineer", "ML Enigneer", "BI Analyst", "Financial Analist"]
    )

company = st.selectbox(
    label="Select Company",
    options=["Amazon", "Meta", "Google", "TCS", "Nvidia"]
)

st.write(f"**Your Information:** You are {level} in {role} at {company}")

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-4o'

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role':'system', 'content': f"You are an HR executive that interviews an interviewee called {name} with experience {experience} and skills {skills}. You should interview them for the {level}{role} at the company {company}"}]

for message in st.session_state.messages:
    if message['role'] != 'system':
        with st.chat_message(message['role']):
            st.markdown(message['content'])

if prompt := st.chat_input("Your Prompt"):
    st.session_state.messages.append({'role':'user', 'content': prompt})

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        stream = client.chat.completions.create(
            model= st.session_state['openai_model'],
            messages=[
                {'role': m['role'], 'content':m['content'] } for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({'role':'assistant', 'content':response})


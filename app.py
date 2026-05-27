import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Smart AI",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Smart AI")
st.markdown("### QnA Bot Based On Gemini")

# Load API Key
api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# Stop app if key missing
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found")
    st.info("Add your API key in .env or Streamlit Secrets")
    st.stop()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=api_key,
    temperature=0.7
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
query = st.chat_input("Ask anything...")

# Function to safely extract text
def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    parts.append(item["text"])
            else:
                parts.append(str(item))

        return " ".join(parts)

    return str(content)

# Process query
if query:

    # Exit commands
    if query.lower() in ["exit", "quit", "bye"]:
        st.session_state.messages.clear()

        with st.chat_message("assistant"):
            st.markdown("👋 Session ended. Refresh the page to start again.")

        st.stop()

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # Generate response
    try:
        with st.spinner("Thinking..."):

            res = llm.invoke(query)

            answer = extract_text(res.content)

        # Show assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Error: {str(e)}")
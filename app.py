import streamlit as st
import pandas as pd
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="Logistics BI Chatbot", page_icon="📦")
st.title("📦 Logistics BI Chatbot")
st.caption("Upload a CSV and ask questions about your logistics data")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Preview")
    st.dataframe(df)
    st.caption(f"✅ {len(df)} rows × {len(df.columns)} columns loaded — ask anything!")

    # Auto chart
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 1:
        st.subheader("📈 Quick Chart")
        st.bar_chart(df.set_index(df.columns[0])[numeric_cols])

    # Statistical summary
    st.subheader("📊 Statistical Summary")
    st.dataframe(df.describe())

    # CSV content for Claude
    csv_content = f"Dataset summary:\n{df.describe().to_string()}\n\nFirst 50 rows:\n{df.head(50).to_string()}"

    # Set up Claude ← MUST BE HERE before suggestions
    llm = ChatAnthropic(model="claude-haiku-4-5")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a logistics data analyst. Answer questions about this dataset:\n\n{data}"),
        ("human", "{question}")
    ])
    chain = prompt | llm

    # Suggestions
    st.subheader("💡 Try asking:")
    cols = st.columns(3)
    suggestions = [
        "What is the highest value?",
        "Give me an executive summary",
        "Which category needs attention?"
    ]
    for i, s in enumerate(suggestions):
        if cols[i].button(s):
            st.session_state.messages.append({"role": "user", "content": s})
            with st.spinner("Analysing..."):
                response = chain.invoke({"data": csv_content, "question": s})
                answer = response.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if question := st.chat_input("Ask a question about your data..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Analysing..."):
                response = chain.invoke({"data": csv_content, "question": question})
                answer = response.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # Clear chat button
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

else:
    st.info("👆 Upload a CSV file to get started!")
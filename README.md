# Logistics BI Chatbot

An AI-powered data chatbot that lets you upload any CSV file and ask questions about it in plain English — no SQL or coding required.

## Features
- Upload any CSV file
- Automatic data preview and statistical summary
- Auto-generated bar chart for numeric columns
- Chat with your data using natural language
- Powered by Claude AI (Anthropic) via LangChain

## Tech Stack
- Python
- Streamlit
- LangChain
- Claude API (claude-haiku-4-5)
- Pandas

## How to run locally
1. Clone the repo
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create a `.env` file with your Anthropic API key: ANTHROPIC_API_KEY=your_key_here
4. Run: `streamlit run app.py`

## Use case
Built as a portfolio project to demonstrate AI integration, no-code automation, and data analysis skills — relevant for logistics digitalization and AI product roles.
import pandas as pd
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Load CSV
df = pd.read_csv("logistics.csv")
csv_content = df.to_string()

# Set up Claude
llm = ChatAnthropic(model="claude-haiku-4-5")

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a logistics data analyst. Answer questions about this dataset:\n\n{data}"),
    ("human", "{question}")
])

chain = prompt | llm

# Chat loop
print("Logistics CSV Chatbot ready! Type 'quit' to exit.\n")
while True:
    question = input("Ask a question: ")
    if question.lower() == "quit":
        break
    response = chain.invoke({"data": csv_content, "question": question})
    print(f"\nAnswer: {response.content}\n")
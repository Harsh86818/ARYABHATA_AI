import os
import sympy
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key = os.getenv ("GROQ_API_KEY"))

def as_llm(question):
    response = client.chat.completions.create(
    model =  "openai/gpt-oss-120b",
    messages = [{
    "role": "system", "content":"You are a SymPy code writer. The user will ask a math question. You must write Python code that solves it using the sympy library.\n\nRules:\n- Import sympy as sp at the start of the code.\n- Define symbols with sp.Symbol() as needed.\n- Use print() to display the final answer.\n- Output ONLY the Python code, no explanations, no markdown, no backticks.\n- The code should be complete and ready to run."
    },
    {"role": "user", "content": question}]

)
    return response.choices[0].message.content.strip()

question = input("Write the question:")
code = as_llm(question)
print(code)
print("output")
exec(code)
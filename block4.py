import os
import sympy as sp
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))


def extract_equation(question):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages = [
            {"role": "system", "content":"You extract math equations. Reply with ONLY the equation in Python format, nothing else. Use ** for powers and * for multiplication. Do NOT include '== 0' or '= 0'. Just the expression, no equals sign." },
            {"role": "user", "content" : question }


        ]

    )

    return response.choices[0].message.content.strip()

def solve_equation(equation):
    x = sp.Symbol ('x')
    
    expr = sp.sympify(equation)
    solution = sp.solve(expr, x)

    return solution


question = input("Write the math question:")
equation = extract_equation(question)
print("Extracted equation:", equation)
answer = solve_equation(equation)
print("The answer is:", answer)
solve_equation(equation)
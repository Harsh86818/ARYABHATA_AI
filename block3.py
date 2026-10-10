import os 
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()
client = Groq(api_key = os.getenv   ("GROQ_API_KEY"))


def extract (question):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b" ,
        messages = [{"role": "system", "content": "You extract math equations. Reply with ONLY the equation in Python format, nothing else. Use ** for powers and * for multiplication. No 'x=' or 'solve for x', just the expression."},
            {"role": "user", "content": question}
        
    ]
        
)

    return response.choices[0].message.content.strip()

question = "solve x^2 - 5x + 6 = 0"
equation = extract(question)
print(equation)
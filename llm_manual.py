from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="سلام! خودت را در یک جمله معرفی کن."
)

print(response.output_text)
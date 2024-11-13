import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file REPLACE WITH YOUR PATH
load_dotenv(dotenv_path=r"C:\Users\tsmia\Downloads\Acne\DTM_CTP2024\Gemini\.env")

# Retrieve the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_acne_treatments(acne_types):
    treatments = {}
    for acne_type in acne_types:
        prompt = f"Suggest treatment options for acne type: {acne_type}. Provide clear steps and product recommendations."
        response = model.generate_content(prompt)
        treatments[acne_type] = response.text
    return treatments

# Example list of acne types
acne_types = [
    "blackheads",
    "whiteheads",
    "cystic acne",
    "papules",
    "pustules",
    "nodular acne"
]

# Get treatments for each acne type
treatment_recommendations = get_acne_treatments(acne_types)

# Print the recommendations
for acne_type, treatment in treatment_recommendations.items():
    print(f"Acne Type: {acne_type}\nTreatment: {treatment}\n")

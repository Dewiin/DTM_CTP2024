import google.generativeai as genai
from dotenv import load_dotenv
import os

# Retrieve the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# def get_acne_treatments(acne_types):
#     treatments = {}
#     for acne_type in acne_types:
#         prompt = f"Suggest treatment options for acne type: {acne_type}. Provide clear steps and product recommendations."
#         response = model.generate_content(prompt, stream=True)
#         treatments[acne_type] = response.text
#     return treatments   

def stream_response(prompt):
    # Request streaming response
    response = model.generate_content(prompt, stream=True)
    
    # Process streamed parts
    for part in response:
        yield part.text

prompt = "Explain the benefits of using sunscreen for skincare."
for text_chunk in stream_response(prompt):
    print(text_chunk)  # Print each chunk of the streamed response in real-time

# # Example list of acne types
# acne_types = [
#     "blackheads",
#     "whiteheads",
#     "cystic acne",
#     "papules",
#     "pustules",
#     "nodular acne"
# ]

# # Get treatments for each acne type
# treatment_recommendations = get_acne_treatments(acne_types)

# # Print the recommendations
# for acne_type, treatment in treatment_recommendations.items():
#     print(f"Acne Type: {acne_type}\nTreatment: {treatment}\n")

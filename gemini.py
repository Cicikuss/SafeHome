import os
import google.generativeai as genai
from dotenv import load_dotenv


class geminiAI():
    @classmethod
    def __init__(self):
        load_dotenv()
        self.prompt = "Give only the hassan index only number if you cant calculate give me the null"
        self.GOOGLE_API_KEY = os.getenv("API")
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    @classmethod
    def send(self, image):
        response = self.model.generate_content([self.prompt, image], stream=False)
        return response.text

import os
import google.generativeai as genai
import asyncio
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with the appropriate model ID for Gemini

    async def generate_response(self, prompt):
        try:
            # Start a new chat
            chat = self.model.start_chat()
            # Send the message asynchronously
            response = await asyncio.to_thread(chat.send_message, prompt)
            ai_response = response.text
            return ai_response
        except Exception as e:
            logger.error(f"Error generating response from Gemini API: {e}", exc_info=True)
            raise e

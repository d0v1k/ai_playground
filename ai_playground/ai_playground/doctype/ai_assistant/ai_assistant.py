from frappe.model.document import Document
import frappe
import requests
from .report_dispatcher import handle_report_request  # Updated to use the new dispatcher

class AIAssistant(Document):
    @frappe.whitelist()
    def send_message(self):
        user_input = self.message
        report_response = handle_report_request(user_input)
        if report_response != "Report type not recognized.":
            return report_response
        else:
            return self.get_chatgpt_response(user_input)

    def get_chatgpt_response(self, text):
        api_url = "https://api.openai.com/v1/chat/completions"
        api_key = "your api key here"  # Use environment variables or secure storage for production
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        }
        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {e}"
            frappe.log_error(error_msg, 'AI Assistant API Error')
            return "Failed to get response from ChatGPT. Please check error log for details."

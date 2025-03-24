import os
import random
import string
from flask import Flask, request, render_template
from google.cloud import dialogflow_v2 as dialogflow

# Set up your Dialogflow API credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\risha\.vscode\Projects\AI Chat-bot\MC-Dialogflow-API-Key.json"

#Initialize the Flask app
app = Flask(__name__)

#Initialize the Dialogflow client
client = dialogflow.SessionsClient()


project_id = "heisenbergai-pnyk" 

def generate_random_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Detect intent function
def detect_intent_texts(user_input, session_id, language_code='en'):
    session = client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=user_input, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    session_id = generate_random_session_id()  # Generate random session ID for each interaction
    bot_response = detect_intent_texts(user_input, session_id)
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)

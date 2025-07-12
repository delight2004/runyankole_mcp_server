# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS # Required for cross-origin requests from web clients
import requests
import os # For environment variables
from dotenv import load_dotenv
load_dotenv()
import asyncio # For running async functions in a sync context

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes. In a production environment, you might restrict this
# to specific origins (e.g., your web app's domain) for security.
CORS(app)

# --- Configuration for Gemini API ---
# It's crucial to load your API key from an environment variable for security.
# Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual API key, or set it as an
# environment variable before running the app (recommended).
# Example for setting environment variable (in terminal before running app.py):
# export GEMINI_API_KEY="your_actual_api_key_from_google_ai_studio" (Linux/macOS)
# set GEMINI_API_KEY="your_actual_api_key_from_google_ai_studio" (Windows CMD)
# $env:GEMINI_API_KEY="your_actual_api_key_from_google_ai_studio" (Windows PowerShell)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Gemini API endpoint (using gemini-2.0-flash model, which is good for speed)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Placeholder for your Runyakole/Rukiga Language Knowledge Base ---
# Initially, we'll load this from a simple text file.
# In future steps, we can make this more sophisticated (e.g., a database,
# dynamic loading based on query, or even directly from NotebookLM exports).
LANGUAGE_KNOWLEDGE_BASE_FILE = 'runyakole_rukiga_data.txt'
language_data_content = ""

def load_language_knowledge_base():
    """
    Loads the Runyakole/Rukiga language data from a text file.
    """
    global language_data_content
    try:
        with open(LANGUAGE_KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
            language_data_content = f.read()
        print(f"Successfully loaded language data from {LANGUAGE_KNOWLEDGE_BASE_FILE}")
    except FileNotFoundError:
        print(f"WARNING: '{LANGUAGE_KNOWLEDGE_BASE_FILE}' not found. Please create this file and add your language data.")
        language_data_content = "No language data loaded yet. Please add your Runyakole/Rukiga dictionary, grammar, and phrases to the 'runyakole_rukiga_data.txt' file."
    except Exception as e:
        print(f"Error loading language data: {e}")
        language_data_content = f"Error loading language data: {e}. Please check '{LANGUAGE_KNOWLEDGE_BASE_FILE}'."

# Load the knowledge base when the server starts
load_language_knowledge_base()


# --- Helper function to call the Gemini API ---
async def call_gemini_api(prompt_text):
    """
    Makes an asynchronous call to the Google Gemini API to generate content.
    """
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("WARNING: Gemini API key is not set. Using a placeholder response.")
        return "Placeholder response: Please set your GEMINI_API_KEY environment variable. Once set, I can teach you Runyakole/Rukiga!"

    headers = {
        'Content-Type': 'application/json',
    }
    # Construct the payload for the Gemini API request
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    try:
        # Make the POST request to the Gemini API
        # The 'requests' library is synchronous. For a production server,
        # consider using an aiohttp client for truly asynchronous requests
        # if performance is critical. For this example, it's fine.
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        # Extract the generated text from the response
        if result and result.get('candidates') and len(result['candidates']) > 0 and \
           result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts') and \
           len(result['candidates'][0]['content']['parts']) > 0:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        else:
            print(f"Error: Unexpected Gemini API response structure: {result}")
            return "Error: Could not get a valid response from the LLM. Please check the API response structure."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error: Failed to connect to LLM. Details: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: An unexpected issue occurred. Details: {e}"

# --- API Endpoint for Language Learning Queries ---
@app.route('/teach_me_runyakole', methods=['POST'])
def teach_me_runyakole():
    """
    Receives a query related to Runyakole/Rukiga, combines it with the
    language knowledge base, and sends it to the LLM.
    """
    # Ensure the request content type is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "Missing 'query' in request. Please ask a question about Runyakole/Rukiga."}), 400

    # --- MCP Logic: Combine Knowledge Base with User Query ---
    # This is the core of your MCP. We instruct the LLM to act as a language tutor
    # and use the provided knowledge base.
    full_prompt = f"""
You are a helpful Runyakole/Rukiga language tutor. Your goal is to teach the user based on the provided language data.
Always refer to the provided 'Language Knowledge Base' for information and examples.
If the answer is not in the 'Language Knowledge Base', state that you don't have enough information from the provided text.

Language Knowledge Base:
---
{language_data_content}
---

User's Question: {user_query}

Your Answer:
"""
    
    if not full_prompt.strip():
        return jsonify({"error": "No valid query or language data to process."}), 400

    # Call the Gemini API (using a synchronous call here for Flask's default handler)
    llm_response = asyncio.run(call_gemini_api(full_prompt))

    # Return the LLM's response to the client
    return jsonify({"runyakole_tutor_response": llm_response})

# --- Endpoint to reload the knowledge base (useful during development) ---
@app.route('/reload_knowledge_base', methods=['POST'])
def reload_knowledge_base():
    """
    Reloads the language knowledge base from the file.
    Call this after you've updated 'runyakole_rukiga_data.txt'.
    """
    load_language_knowledge_base()
    return jsonify({"status": "Language knowledge base reloaded successfully!"}), 200


# --- Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    """
    A simple health check endpoint to ensure the server is running.
    """
    return jsonify({"status": "Runyakole/Rukiga MCP server is running!"}), 200

# --- Main execution block ---
if __name__ == '__main__':
    # Run the Flask app
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    # Set host='0.0.0.0' to make the server accessible from other devices on your network.
    # For local development, '127.0.0.1' or 'localhost' is usually fine.
    print("Starting Runyakole/Rukiga MCP server...")
    print("Access the health check at http://127.0.0.1:5000/health")
    print("Send POST requests to http://127.0.0.1:5000/teach_me_runyakole")
    print(f"Your language data file is: {LANGUAGE_KNOWLEDGE_BASE_FILE}")
    app.run(debug=True, host='0.0.0.0', port=5000)

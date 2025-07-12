# 🗣️ Runyakole/Rukiga Language Tutor Server

## 🚀 Overview

This project is a **Model Context Protocol (MCP)** server designed to be a personalized AI tutor for learning **Runyakole/Rukiga**. It uses your custom language data to provide highly accurate and contextualized explanations via **Google Gemini**, tackling the scarcity of digital resources for less commonly spoken languages.

---

## ✨ Features

- 🔤 **Customizable Knowledge Base**: Load your own Runyakole/Rukiga dictionary, grammar, and phrases from `runyakole_rukiga_data.txt`.
- 🧠 **Intelligent Context Management**: Combines your language data with user queries for targeted LLM prompts.
- ⚙️ **Google Gemini Integration**: Leverages Gemini for AI-powered explanations and learning.
- 🔌 **RESTful API**: Clear endpoints for easy integration with front-end apps or mobile clients.
- 🔐 **Secure API Key Handling**: Uses `.env` for storing your Gemini API key safely.
- ♻️ **Reloadable Data**: Update your language data without restarting the server.

---

## 🛠️ Technologies

- Python 3.x  
- [Flask](https://flask.palletsprojects.com/) (Web Framework)  
- Flask-CORS (CORS handling)  
- Requests (HTTP client)  
- python-dotenv (Environment variables)  
- [Google Gemini API](https://aistudio.google.com/) (LLM)

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/delight2004/runyankole_mcp_server.git
cd runyankole_mcp_server

2. Install Dependencies

pip install Flask Flask-CORS requests python-dotenv
# OR
pip install -r requirements.txt

3. Get Gemini API Key

Sign in to Google AI Studio

Generate and copy your Gemini API key.


4. Configure Environment Variable

Create a .env file in the project root:

GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

> ✅ Note: .env is already in .gitignore and will not be pushed to GitHub.



5. Create Language Knowledge Base

Create runyakole_rukiga_data.txt in the root directory and add your custom language knowledge.

Example:

--- Runyakole/Rukiga Language Knowledge Base ---

Greetings:
- Hello (singular): Oraire ota
- Hello (plural): Muraire muta
- I am fine: Ndi kurungi

Basic Vocabulary:
- Person: Omuntu (singular), Abantu (plural)
- Water: Amaizi

Grammar Notes:
- Noun Classes: 'Om-'/'Ab-' for people (e.g., Omuntu, Abantu).


---

🚀 Running the Server

python app.py

The server will be live at:
http://127.0.0.1:5000


---

🌐 API Endpoints

POST /teach_me_runyakole

Description: Query the AI tutor with a language-related question.

Request Body:

{
  "query": "How do I say 'thank you'?"
}

Example cURL:

curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "What does 'Amaizi' mean?"}' \
     http://127.0.0.1:5000/teach_me_runyakole

Response:

{
  "runyakole_tutor_response": "The AI's answer based on your knowledge base."
}


---

POST /reload_knowledge_base

Description: Reloads runyakole_rukiga_data.txt without restarting the server.

Example cURL:

curl -X POST http://127.0.0.1:5000/reload_knowledge_base


---

GET /health

Description: Checks if the server is running.

Example cURL:

curl http://127.0.0.1:5000/health


---

➡️ Next Steps (Ideas 💡)

🖥️ Web UI: Build a simple front-end for smoother interaction.

🧠 Advanced Context: Add semantic search or embeddings.

⏰ Spaced Repetition: Track learning progress over time.

🔊 Text-to-Speech: Add audio pronunciation with TTS.

☁️ Deployment: Host the server on Google Cloud Run, Render, etc.



---

📚 Happy Learning!

Let’s preserve and modernize our local languages, one prompt at a time ✨

---

Let me know if you'd like a badge pack (e.g., `Made with Python`, `Built with Gemini`, `Powered by MCP`) or a license section added!


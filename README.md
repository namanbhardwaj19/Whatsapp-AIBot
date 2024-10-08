**AI Agent with OpenAI and Twilio WhatsApp Integration**

**Project Overview**
This project develops an AI agent using the OpenAI Assistant API that integrates with Twilio's WhatsApp functionality. 
The AI agent responds to user queries in real time through WhatsApp by leveraging a provided knowledge base for contextually 
relevant answers.

**Features**
- Real-time user interactions via WhatsApp.
- AI agent developed using OpenAI's gpt-4.0 model.
- Knowledge base integration for accurate responses.
- Session management to maintain conversation context for multiple users.
- FastAPI: Backend framework for handling API requests and integrating OpenAI with Twilio.
- OpenAI API: Powers the AI agent for generating intelligent responses.
- Twilio API: Handles WhatsApp messaging functionality.
- Python: Core programming language for the entire project.


**Clone the repository:**
git clone https://github.com/your-repo/your-project.git

**Install the required dependencies:**
pip install -r requirements.txt

**Set up the Twilio API:**

Create a Twilio account.
Get your Twilio WhatsApp sandbox number.
Configure your conversation service webhook to point to your FastAPI app endpoint.

**Set up OpenAI API:**
Create a OpenAI account.
Create an Assistant and provide knowledge base and prompt as System Instructions.
Get your OpenAI API key from the OpenAI platform.
Set your API key in your environment variables or directly in the code.

**Run the FastAPI server:**
uvicorn main:app --reload

**Expose your local development server using ngrok for Twilio to access your webhook:**

**Install ngrok**
Set auth token in ngrok config
RUN ngrok http 8000
Configuration

Add your OpenAI API key and Twilio credentials in the project’s .env file or as environment variables.

**Usage:**
Once the server is up and running, users can interact with the AI agent via WhatsApp. 
The agent will respond based on the conversation context and the knowledge base.



**CODE STRUCTURE**

1. Main Application (main.py):
This is the entry point of the FastAPI server. It creates the app and routes the incoming requests from Twilio to /whatsapp endpoint.
Run run.py to start the server

2. API Handlers:
The src/routes/init.py file has /whatsapp endpoint to receives WhatsApp messages.
This function processes the user's message, sends it to the OpenAI API, and returns a response.

3. OpenAI Integration:
The /whatsapp endpoint uses helper functions in services/ai_response.py to sends the user message to the OpenAI API to 
generate a response using the provided knowledge base and prompt.
The response is then formatted and sent back to the FastAPI handler.

5. Session Management:
The project tracks conversations per user by managing user session data in redis.
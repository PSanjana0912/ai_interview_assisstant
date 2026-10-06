# AI Interview Assistant

A beginner-friendly command-line application built with Python and the OpenAI API to help users prepare for technical interviews.

## Features

- Generate five interview questions by topic and difficulty
- Explain technical topics with examples
- Conduct a five-question mock interview
- Evaluate answers and provide scores out of 10
- Display feedback and overall interview score
- Handle invalid input and API errors
- Use colored terminal output

## Technologies

- Python
- OpenAI Python SDK
- OpenAI API
- python-dotenv
- Colorama

## Project Structure

```text
ai_interview_assistant/
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

Setup

Create a virtual environment:
python -m venv .venv       -windows
python3 -m venv .venv       -MacOS
Activate virtual environment
.venv\Scripts\Activate.ps1    -windows powershell
.venv\Scripts\Activate.bat     -windows command prompt



Install dependencies:
pip install -r requirements.txt

Create a .env file in the project directory:
OPENAI_API_KEY=your_api_key_here

Never commit or share your API key.

Run the Application
python main.py  -windows
python3 main.py   -MacOS

The application provides these options:
1. Generate Interview Questions
2. Explain a Technical Topic
3. Mock Interview
4. Exit

During a mock interview, type menu to return to the main menu.


#Learning Goals
This project demonstrates:

OpenAI API integration
Environment variables
Prompt construction
System instructions and user input
Response handling
Error handling
Basic prompt engineering
Multi-step LLM workflows


#Future Improvements
Structured JSON responses
Interview history
RAG with FAISS
AI agents with tools
React and Flask frontend/backend
Database support
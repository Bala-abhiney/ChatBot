ChatBot Interview Assistant
Overview
A Streamlit-based chatbot that helps conduct technical interviews by:

Collecting candidate information

Generating technical questions based on the candidate's skills

Evaluating responses using AI

Storing results for recruitment review

Features
Candidate Profile Collection – Name, email, experience, etc.
Tech Skill Input – Enter your skills (comma-separated)
AI-Generated Questions – Custom questions based on your tech stack
Answer Validation – AI-powered evaluation of responses
Duplicate Prevention – Prevents multiple submissions with the same email

Installation
Clone the repository

bash
git clone
cd
Install dependencies

bash
pip install streamlit
Run the app

bash
streamlit run app.py
How It Works
Start → Click "Start" to begin.

Fill Profile → Enter your details (all fields required).

Enter Skills → List technologies you know (e.g., Python, SQL, AWS).

Answer Questions → Respond to generated technical questions.

Get Results → AI evaluates answers and provides feedback.

File Structure
project/
├── app.py # Main Streamlit app
├── question_generator.py # Generates skill-based questions
├── validate_answer.py # Validates answers using AI
├── candidate_email.py # Manages candidate data & prevents duplicates
└── README.md # This guide
Note
All form fields are mandatory.

Email must be unique (prevents duplicate submissions).

Responses are stored for recruitment review.

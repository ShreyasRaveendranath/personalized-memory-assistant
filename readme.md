Personalized Memory Assistant:


A Streamlit web app that simulates personalized, memory-aware responses using Phi-3-mini-4k-instruct.

The app extracts “stable memories” from up to 30 past user messages and generates two versions of the response:

 1) Neutral personalized response
 2) Personality-styled response (Calm Mentor, Witty Friend, Therapist)

Features:
1) Memory Extraction:

Uses a structured JSON-only extraction prompt to detect:
User preferences
Emotional patterns
Stable facts

2) Two Response Modes:

a) Without Personality – neutral and helpful

b) With Personality – same content but stylized according to selected persona


3) Clean Streamlit Interface

Enter messages
Enter current question
Choose personality
View extracted memories and generated responses 

Installation:
1) Clone the repository

2) Create a Python environment
a) Create a virtual environment 
b) Activate it
c) Then install the libraries using pip install -r requirements.tx

Running the App:

a) streamlit run stream.py

b) Then open your browser at: http://localhost:8501


Project Structure:

.├── app.py                     
├── stream.py                   
├── requirements.txt

└── README.md







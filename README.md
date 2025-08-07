This github repo is intended to be future workspace for code integration and promosing development of the AvaSec chatbot!

Steps for launching the server on your local machine:

-- If you want to ensure you do not have any conflicting dependacies (just for safety) on Linux/Linux-like systems, run the following commands:

   1. python -m venv venv
   2. source venv/Scripts/activate

-- Use requirements.txt to install all dependacies:

   3. pip install -r requirements.txt

-- Put your OpenAI key in the .env file:
   4. OPENAI_API_KEY="your_openai_api_key_here"

-- Run the server:

   5. uvicorn api_server:app --port=8090 --reload

-- Start php server:

   6. php -S localhost:8090

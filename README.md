This github repo is intended to be future workspace for code integration and promosing development of the AvaSec chatbot!

Steps for launching the server on your local machine:

-- If you want to ensure you do not have any conflicting dependacies (just for safety) on Linux/Linux-like systems, run the following commands:

   1. python -m venv venv
   2. source venv/Scripts.activate
-- Use requirements.txt to install all dependacies:

   1. pip install -r requirements.txt
-- Run the server:

   1. uvicorn api_server:app --port=8090 --reload
-- Start php server:

   1. php -S localhost:8090

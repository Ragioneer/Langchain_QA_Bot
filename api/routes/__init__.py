from flask import Flask, url_for, request, render_template, redirect
from api.parameters import PDF_Loader
from api.parameters.LLM import agent
import os

app = Flask(__name__)
messages = []  # List to store chat history messages
conversation = []  # List to store chat conversation messages

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if 'file_path' in request.files:
            # Extract file and call PDF_Loader
            uploaded_file = request.files['file_path']
            delete_flag = request.form.get('delete', False)  # Check for delete flag
            file_path = os.path.join(os.getcwd(), 'datasets', uploaded_file.filename)

            if delete_flag:
                # Handle file deletion before uploading new one (if necessary)
                PDF_Loader.delete_file(file_path)  # Call delete function from PDF_Loader
                messages.append(f"File deleted: {file_path}")
            else:
                uploaded_file.save(file_path)
                vectorstore = PDF_Loader.Load_PDF(file_path=file_path)
                messages.append(f"PDF uploaded successfully: {file_path}")

        else:
            query = request.form.get('query')
            response = agent.run(str(query))
            conversation.append(f"You: {query}")
            conversation.append(f"Bot: {response['result']}")

    return render_template("index.html", messages=messages, conversation=conversation)

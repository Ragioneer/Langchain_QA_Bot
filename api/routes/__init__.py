from flask import Flask, url_for, request, render_template, redirect
from api.parameters import PDF_Loader
from api.parameters.LLM import qa
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
      file_path = os.path.join(os.getcwd(), 'datasets', uploaded_file.filename)
      uploaded_file.save(file_path)
      PDF_Loader.Load_PDF(file_path=file_path)
      messages.append(f"PDF uploaded successfully: {file_path}")
      return redirect(url_for('index'))  # Redirect to avoid duplicate file upload
    else:
      query = request.form.get('query')
      response = qa.invoke({'query': str(query)})
      conversation.append(f"You: {query}")
      conversation.append(f"Bot: {response['result']}")
      # Update messages and conversation lists on server-side
      return render_template("index.html", messages=messages, conversation=conversation)

  return render_template("index.html", messages=messages, conversation=conversation)

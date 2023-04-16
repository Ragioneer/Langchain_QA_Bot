from flask import Flask, url_for, request, render_template, redirect
from LLM import qa

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        response = qa.run(query)
        return redirect(url_for("index",result=response))   
    
    result = request.args.get('result')  
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
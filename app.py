from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Mentorship & Research Collaboration Database is running!"

if __name__ == '__main__': 
    app.run(debug=True)
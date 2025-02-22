from flask import Flask
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# Load MySQL configuration
app.config['MYSQL_HOST'] = config.Config.MYSQL_HOST
app.config['MYSQL_USER'] = config.Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.Config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def home():
    return "Mentorship & Research Collaboration Database is running!"

@app.route('/test_db')
def test_db():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES;")  # Check if we can access the database
    result = cur.fetchall()
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)

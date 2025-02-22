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
    try:
        cur = mysql.connection.cursor()
        cur.execute("USE mentorship_db;")  # Ensure correct database is selected
        cur.execute("SHOW TABLES;")  # List tables
        result = cur.fetchall()
        return f"Tables: {result}" if result else "No tables found."
    except Exception as e:
        return f"Database error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

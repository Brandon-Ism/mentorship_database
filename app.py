from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL
import config
import os 
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load MySQL configuration
app.config['MYSQL_HOST'] = config.Config.MYSQL_HOST
app.config['MYSQL_USER'] = config.Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.Config.MYSQL_DB

mysql = MySQL(app)

    
# Upload settings
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    


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


def allowed_file(filename):
    """Check if the uploaded file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    cur = mysql.connection.cursor()

    # Fetch user info
    cur.execute("""
        SELECT u.id, u.name, u.academic_position, u.institution, u.department, 
               u.bio, u.interested_in, u.headshot_path
        FROM users u 
        ORDER BY u.name ASC
    """)
    users = cur.fetchall()

    # Fetch all research interests for users
    user_interests = {}
    for user in users:
        user_id = user[0]
        cur.execute("""
            SELECT ri.name FROM research_interests ri
            JOIN user_research_interests uri ON ri.id = uri.interest_id
            WHERE uri.user_id = %s
        """, (user_id,))
        interests = [row[0] for row in cur.fetchall()]
        user_interests[user_id] = interests

    cur.close()
    return render_template('home.html', profiles=users, user_interests=user_interests)


from flask import send_from_directory

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        academic_position = request.form.get('academic_position')
        institution = request.form.get('institution')
        department = request.form.get('department')
        bio = request.form.get('bio')
        interested_in = request.form.getlist('interested_in')  # Multi-select checkbox
        interested_in_str = ",".join(interested_in) if interested_in else "N/A"

        # Handle research interests
        selected_interests = request.form.getlist('research_interests')
        new_interest = request.form.get('new_research_interest')

        # Insert new research interest if provided
        if new_interest:
            cur.execute("INSERT IGNORE INTO research_interests (name) VALUES (%s)", (new_interest,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM research_interests WHERE name = %s", (new_interest,))
            new_interest_id = cur.fetchone()[0]
            selected_interests.append(str(new_interest_id))  # Add new interest to selected list

        # Handle file upload
        file = request.files.get('headshot')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save file to static/uploads/
            headshot_path = file_path
        else:
            headshot_path = "static/uploads/default.jpg"

        # Insert user into database
        cur.execute("""
            INSERT INTO users (name, email, academic_position, institution, department, bio, interested_in, headshot_path) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, academic_position, institution, department, bio, interested_in_str, headshot_path))
        mysql.connection.commit()

        # Get the newly created user ID
        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

        # Insert selected research interests
        for interest_id in set(selected_interests):  # remove duplicates just in case
            cur.execute("INSERT IGNORE INTO user_research_interests (user_id, interest_id) VALUES (%s, %s)", (user_id, interest_id))

        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))

    # Fetch all existing research interests
    cur.execute("SELECT id, name FROM research_interests ORDER BY name ASC")
    research_interests = cur.fetchall()
    cur.close()

    return render_template('create_profile.html', research_interests=research_interests)



@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        email = request.form.get('email')

        # Find user by email
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if not user:
            cur.close()
            return render_template('update_profile.html', error="No profile found for that email.")

        # Fetch research interests for this user
        cur.execute("""
            SELECT interest_id FROM user_research_interests WHERE user_id = %s
        """, (user[0],))
        selected_interests = [row[0] for row in cur.fetchall()]

        # Fetch all available interests
        cur.execute("SELECT id, name FROM research_interests ORDER BY name ASC")
        all_interests = cur.fetchall()

        cur.close()

        return render_template('edit_profile.html', user=user, selected_interests=selected_interests, research_interests=all_interests)

    return render_template('update_profile.html')


# Handle profile update POST request
@app.route('/edit_profile/<int:user_id>', methods=['POST'])
def edit_profile(user_id):
    cur = mysql.connection.cursor()

    name = request.form.get('name')
    academic_position = request.form.get('academic_position')
    institution = request.form.get('institution')
    department = request.form.get('department')
    bio = request.form.get('bio')
    interested_in = request.form.getlist('interested_in')
    interested_in_str = ",".join(interested_in) if interested_in else "N/A"

    # Handle file upload
    file = request.files.get('headshot')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        headshot_path = file_path
        cur.execute("""
            UPDATE users SET name=%s, academic_position=%s, institution=%s, 
            department=%s, bio=%s, interested_in=%s, headshot_path=%s 
            WHERE id=%s
        """, (name, academic_position, institution, department, bio, interested_in_str, headshot_path, user_id))
    else:
        cur.execute("""
            UPDATE users SET name=%s, academic_position=%s, institution=%s, 
            department=%s, bio=%s, interested_in=%s 
            WHERE id=%s
        """, (name, academic_position, institution, department, bio, interested_in_str, user_id))

    mysql.connection.commit()

    # Update research interests
    cur.execute("DELETE FROM user_research_interests WHERE user_id = %s", (user_id,))
    selected_interests = request.form.getlist('research_interests')
    new_interest_input = request.form.get('new_research_interest')

    if new_interest_input:
        new_interests = [s.strip() for s in new_interest_input.split(',') if s.strip()]
        for interest in new_interests:
            cur.execute("INSERT IGNORE INTO research_interests (name) VALUES (%s)", (interest,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM research_interests WHERE name = %s", (interest,))
            new_interest_id = cur.fetchone()[0]
            selected_interests.append(str(new_interest_id))

    for interest_id in set(selected_interests):
        cur.execute("INSERT IGNORE INTO user_research_interests (user_id, interest_id) VALUES (%s, %s)", (user_id, interest_id))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
    
    
    

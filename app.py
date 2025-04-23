from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL
import config
import os 
from werkzeug.utils import secure_filename



app = Flask(__name__)


# Load MySQL configuration and establish connection
app.config['MYSQL_HOST'] = config.Config.MYSQL_HOST
app.config['MYSQL_USER'] = config.Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.Config.MYSQL_DB

mysql = MySQL(app)

    
# Upload settings
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # only images allowed for headshots
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    

# Test conenction to database by listing all tables
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


# Check if the uploaded file is of an allowed types
def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: Fix homepage SQL query to exclude email and align fields to table headers



@app.route('/')

def home():
    # Dynamically sort all user profiles by name

    sort_by = request.args.get('sort_by', 'name') # check if user choses a sort option, if not sort by name
    #sorting only allowed on valid columns
    valid_sort_columns = {
        'name': 'u.name',
        'institution': 'u.institution',
        'interested_in': 'u.interested_in'
    }

    order_clause = valid_sort_columns.get(sort_by, 'u.name')

    # Open cursor to execute sql commands
    cur = mysql.connection.cursor()

    # Store all basic user info into a tuple with sorting
    cur.execute(f"""
        SELECT u.id, u.name, u.academic_position, u.institution, u.department,
               u.bio, u.interested_in, u.headshot_path
        FROM users u
        ORDER BY {order_clause} ASC
    """)
    users = cur.fetchall() # store as tuple

    # Create dictionary to map user_id and list of interest name
    user_interests = {}

    # Loop over every user
    for user in users:
        user_id = user[0]
        # Query interests for user_i by joining reserch_interests and user_research_interestss
        cur.execute("""
            SELECT ri.name FROM research_interests ri
            JOIN user_research_interests uri ON ri.id = uri.interest_id
            WHERE uri.user_id = %s
        """, (user_id,))

        # Map user_id and list of interests
        user_interests[user_id] = [row[0] for row in cur.fetchall()]

    cur.close()
    # To display results on hompepage
    return render_template('home.html', profiles=users, user_interests=user_interests, sort_by=sort_by)






from flask import send_from_directory

# Serve file from uploads folder for profile images
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
        new_interest_input = request.form.get('new_research_interest')

        # Support multiple comma-separated new interests
        if new_interest_input:
            new_interests = [s.strip() for s in new_interest_input.split(',') if s.strip()]
            for interest in new_interests:
                cur.execute("INSERT IGNORE INTO research_interests (name) VALUES (%s)", (interest,))
                mysql.connection.commit()
                cur.execute("SELECT id FROM research_interests WHERE name = %s", (interest,))
                new_interest_id = cur.fetchone()[0]
                selected_interests.append(str(new_interest_id))


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
    
    # User has submitted their email in the form
    if request.method == 'POST':
        email = request.form.get('email')

        # Find user by email and return full user record
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        # If no profile found with that email, notify user
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

        # Send profile and interests selctions to html form
        return render_template('edit_profile.html', user=user, selected_interests=selected_interests, research_interests=all_interests)



    return render_template('update_profile.html')






# Profile update POST request
@app.route('/edit_profile/<int:user_id>', methods=['POST'])

def edit_profile(user_id):
    cur = mysql.connection.cursor()

    # Collect basic user fileds user may have edited
    name = request.form.get('name')
    academic_position = request.form.get('academic_position')
    institution = request.form.get('institution')
    department = request.form.get('department')
    bio = request.form.get('bio')
    interested_in = request.form.getlist('interested_in')
    interested_in_str = ",".join(interested_in) if interested_in else "N/A"

    # Handle file upload
    file = request.files.get('headshot')
    # If the headshot was updated, updated the path
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        headshot_path = file_path

        # Update the entire profile with the new headshot path
        cur.execute("""
            UPDATE users SET name=%s, academic_position=%s, institution=%s, 
            department=%s, bio=%s, interested_in=%s, headshot_path=%s 
            WHERE id=%s
        """, (name, academic_position, institution, department, bio, interested_in_str, headshot_path, user_id))
    
    else:
        # If no new file uploaded, update all other fields
        cur.execute("""
            UPDATE users SET name=%s, academic_position=%s, institution=%s, 
            department=%s, bio=%s, interested_in=%s 
            WHERE id=%s
        """, (name, academic_position, institution, department, bio, interested_in_str, user_id))

    mysql.connection.commit()


    # Delete old research inrerests to allow for new ones
    cur.execute("DELETE FROM user_research_interests WHERE user_id = %s", (user_id,))
    # Get the selected and new interests from the form
    selected_interests = request.form.getlist('research_interests')
    new_interest_input = request.form.get('new_research_interest')

    # Handle new, custom interests without allowing duplicates 
    if new_interest_input:
        new_interests = [s.strip() for s in new_interest_input.split(',') if s.strip()] # separate intersts with comma
        for interest in new_interests:
            # Add to research_interests table
            cur.execute("INSERT IGNORE INTO research_interests (name) VALUES (%s)", (interest,))
            mysql.connection.commit()

            cur.execute("SELECT id FROM research_interests WHERE name = %s", (interest,))
            new_interest_id = cur.fetchone()[0]
            selected_interests.append(str(new_interest_id))

    # Insert all current interests with a set to remove duplicates
    for interest_id in set(selected_interests):
        cur.execute("INSERT IGNORE INTO user_research_interests (user_id, interest_id) VALUES (%s, %s)", (user_id, interest_id))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home'))





# Delete_profile. Show deletion form and process request to delete user
@app.route('/delete_profile', methods=['GET', 'POST'])

def delete_profile():
    message = None

    # Check if user selects to delete profile
    if request.method == 'POST':
        email = request.form.get('email') # get user email
        confirm = request.form.get('confirm') # if checkbox checked, a requirement

        # If both email entered and checkbox
        if confirm == 'on':
            cur = mysql.connection.cursor()
            # Find user by email
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cur.fetchone() # if found, user is tuple

            if user:
                user_id = user[0]
                # Delete from related tables 
                cur.execute("DELETE FROM user_research_interests WHERE user_id = %s", (user_id,)) # delete from many to many table first
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

                mysql.connection.commit()
                cur.close()
                message = "Profile deleted successfully."

            else:
                message = "No profile found with that email."
        else:
            # Email and checkbox not both entered
            message = "You must confirm deletion to proceed."

    return render_template('delete_profile.html', message=message)
    




## Mentorship Matching

@app.route('/find_matches', methods=['GET', 'POST'])

def find_matches():
    matches = [] # to store all compatible users and interests
    message = None # return feedback

    # Form to match is submitted
    if request.method == 'POST':
        email = request.form.get('email')

        cur = mysql.connection.cursor()
        # Lookup user
        cur.execute("SELECT id, name, interested_in FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        # If email does not match any current profiles
        if not user:
            cur.close()
            message = "No profile found for that email."
            return render_template('find_matches.html', message=message)


        user_id, user_name, user_interest_tags = user
        user_tags = set(user_interest_tags.split(',')) # create a set from their intents

        # Get rhe set of research interests IDs for user
        cur.execute("SELECT interest_id FROM user_research_interests WHERE user_id = %s", (user_id,))
        user_interest_ids = {row[0] for row in cur.fetchall()}

        # Look at all other users (except current) and compare
        cur.execute("SELECT id, name, email, academic_position, institution, department, bio, interested_in, headshot_path FROM users WHERE id != %s", (user_id,))
        others = cur.fetchall()

        # Loop through users
        # Extract interested_in tags for user and convert to set
        for other in others:
            other_id = other[0]
            other_tags = set(other[7].split(','))

            # Match logic. collaboration to collaboration, or mentor to mentee
            def is_match(user_tags, other_tags):
                return (
                    ('Collaboration' in user_tags and 'Collaboration' in other_tags) or
                    ('Providing Mentorship' in user_tags and 'Receiving Mentorship' in other_tags) or
                    ('Receiving Mentorship' in user_tags and 'Providing Mentorship' in other_tags)
                )

            # Skip to next user if no match
            if not is_match(user_tags, other_tags):
                continue

            # Check shared interests
            cur.execute("SELECT interest_id FROM user_research_interests WHERE user_id = %s", (other_id,))
            other_interest_ids = {row[0] for row in cur.fetchall()}

            # Compute intersection to get common interests with user
            shared_interests = user_interest_ids.intersection(other_interest_ids)

            if shared_interests:
                # Get interest names for each shared interest ID
                shared = []
                for iid in shared_interests:
                    cur.execute("SELECT name FROM research_interests WHERE id = %s", (iid,))
                    result = cur.fetchone()
                    if result:
                        shared.append(result[0])

                # Store user's full profile tuple and a list of shared interests
                matches.append((other, shared))

        cur.close()

        if not matches:
            message = "No strong matches found. Try updating your interests."

    # Render matches, and display message if needed
    return render_template('find_matches.html', matches=matches, message=message)





# Search route
@app.route('/search_profiles', methods=['GET', 'POST'])

def search_profiles():
    # Store matching profiles, list of interest names
    results = []
    user_interests = {}
    query = ""

    if request.method == 'POST':
        query = request.form.get('query', '').lower().strip() # To be user entered
        search_type = request.form.get('search_type') # type of entry

        cur = mysql.connection.cursor()

        if search_type in ['position', 'interested_in']:
            options = request.form.getlist('query')
            placeholders = ','.join(['%s'] * len(options))

            if search_type == 'position':
                cur.execute(f"""
                    SELECT id, name, email, academic_position, institution, department, bio, interested_in, headshot_path
                    FROM users
                    WHERE academic_position IN ({placeholders})
                """, tuple(options))

            elif search_type == 'interested_in':
                conditions = ' OR '.join(["FIND_IN_SET(%s, REPLACE(interested_in, ', ', ',')) > 0" for _ in options])
                cur.execute(f"""
                    SELECT id, name, email, academic_position, institution, department, bio, interested_in, headshot_path
                    FROM users
                    WHERE {conditions}
                """, tuple(options))


            results = cur.fetchall()

        elif search_type in ['name', 'institution', 'department', 'bio']:
            cur.execute(f"""
                SELECT id, name, email, academic_position, institution, department, bio, interested_in, headshot_path
                FROM users
                WHERE LOWER({search_type}) LIKE %s
            """, (f'%{query}%',))
            results = cur.fetchall()

        elif search_type == 'interests':
            cur.execute("""
                SELECT DISTINCT u.id, u.name, u.email, u.academic_position, u.institution, u.department, u.bio, u.interested_in, u.headshot_path
                FROM users u
                JOIN user_research_interests uri ON u.id = uri.user_id
                JOIN research_interests ri ON ri.id = uri.interest_id
                WHERE LOWER(ri.name) LIKE %s
            """, (f'%{query}%',))
            results = cur.fetchall()

        for profile in results:
            user_id = profile[0]
            cur.execute("""
                SELECT ri.name FROM research_interests ri
                JOIN user_research_interests uri ON ri.id = uri.interest_id
                WHERE uri.user_id = %s
            """, (user_id,))
            user_interests[user_id] = [row[0] for row in cur.fetchall()]

        cur.close()


    return render_template('search_profiles.html', profiles=results, user_interests=user_interests, query=query)


####


if __name__ == '__main__':
    app.run(debug=True)
    
    
    

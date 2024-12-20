from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)  

@app.route('/')
def index():
    return render_template('login.html') 

@app.route('/register_user')
def register_user():
    return render_template('register_user.html')  


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    
    
    print(f"Received data - Name: {name}, Email: {email}")

    
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="puja@123",
        database="project"
    )
    cursor = conn.cursor()

    try:
        # Check if user details exist in the database
        query = "SELECT * FROM newuser WHERE name = %s AND email = %s"
        cursor.execute(query, (name, email))
        user = cursor.fetchone()  # Fetch one matching record
    
        if user:
            # If user exists, redirect to the home page
            return redirect(url_for('home'))
        else:
            # If no match found, display an error message
            flash("Invalid credentials. Please try again.")
    except Exception as e:  # Fixed syntax error in exception handling
        flash(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

    # Render the form again with a flashed error message
    return redirect(url_for('index'))

# Home page route
@app.route('/home')
def home():
    return render_template('home.html')   

# @app.route('/registerUser')    #login register button
# def register_user():
#     return render_template('register_user.html')

@app.route('/register', methods=['POST'])
def add_user():
    try:
        # Get JSON data from the client
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        password = request.form['password']

        # SQL query and database operation
        query = "INSERT INTO newuser(name, email, phone, role, password) VALUES (%s, %s, %s, %s, %s)"
        values = (name, email, phone, role, password)

        conn = pymysql.connect(
        host="localhost",
        user="root",
        password="puja@123",
        database="project"
    )
        cursor = conn.cursor()
 
        cursor.execute(query, values)
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return 'User added successfully!'
    except Exception as e:
        print(e)
        return 'error'


if __name__ == '__main__':
    app.run(debug=True)
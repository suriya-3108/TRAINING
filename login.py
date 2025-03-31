# Import required libraries
from flask import Flask, request, redirect, url_for
import json
import logging
import re
import sys

# Initialize Flask app
app = Flask(__name__)

# Set up logging to save logs in 'app.log' AND display in terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to file
        logging.StreamHandler(sys.stdout)  # Log to terminal
    ]
)

# File to store user data
USER_DATA_FILE = 'users.json'

# Load existing users or start with an empty list
try:
    with open(USER_DATA_FILE, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = []

# Function to validate password
def validate_password(password):
    # Check if password is at least 8 characters and meets complexity requirements
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # Check for uppercase
        return False
    if not re.search(r'[a-z]', password):  # Check for lowercase
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Check for special characters
        return False
    return True

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Log the form submission
        logging.info(f"Received form submission: {request.form}")

        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate form fields
        if not name or not email or not password:
            logging.error("Missing fields")
            return "All fields are required", 400

        if not validate_password(password):
            logging.error("Invalid password")
            return "Password must be 8+ characters with uppercase, lowercase, and special characters", 400

        # Check if email already exists
        if any(user['email'] == email for user in users):
            logging.error("Email already exists")
            return "Email already exists", 400

        # Add new user to the list
        new_user = {
            "name": name,
            "email": email,
            "password": password  # Note: In real apps, hash the password
        }
        users.append(new_user)

        # Save updated user list to JSON file
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

        logging.info(f"User added: {new_user}")
        return redirect(url_for('index'))

    # Display the form for GET requests
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Registration</title>
    </head>
    <body>
        <h1>User Details</h1>
        <form action="/" method="POST">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>

            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br><br>

            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <small>Password must be 8+ characters with uppercase, lowercase, and special characters.</small><br><br>

            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''

# Run the app
if __name__ == '__main__':
    # Log the port details to the terminal
    logging.info("Starting Flask app...")
    app.run(debug=True)
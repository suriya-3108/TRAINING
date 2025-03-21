# Import the necessary modules from Flask
from flask import Flask, request

# Create an instance of the Flask class
app = Flask(__name__)

@app.route('/')
def home():
    # Return an HTML form for user input
    return """
    <h1>Welcome to the Arithmetic Calculator!</h1>
    <form action="/calculate" method="post">
        <label for="value1">Value 1:</label>
        <input type="text" id="value1" name="value1" required><br><br>
        <label for="value2">Value 2:</label>
        <input type="text" id="value2" name="value2" required><br><br>
        <label for="operation">Operation:</label>
        <select id="operation" name="operation" required>
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
            <option value="divide">Divide</option>
            <option value="modulus">Modulus</option>
            <option value="power">Power</option>
        </select><br><br>
        <input type="submit" value="Calculate">
    </form>
    """

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data from the request
    value1 = request.form.get('value1')
    value2 = request.form.get('value2')
    operation = request.form.get('operation')

    # Check if all required parameters are provided
    if value1 is None or value2 is None or operation is None:
        return "Missing parameters. Required: value1, value2, operation", 400

    # Convert values to floats (handle invalid input)
    try:
        value1 = float(value1)
        value2 = float(value2)
    except ValueError:
        return "Invalid input values. value1 and value2 must be numbers.", 400

    # Perform the requested operation
    result = None
    if operation == 'add':
        result = value1 + value2
    elif operation == 'subtract':
        result = value1 - value2
    elif operation == 'multiply':
        result = value1 * value2
    elif operation == 'divide':
        if value2 == 0:
            return "Division by zero is not allowed.", 400
        result = value1 / value2
    elif operation == 'modulus':
        if value2 == 0:
            return "Modulus by zero is not allowed.", 400
        result = value1 % value2
    elif operation == 'power':
        result = value1 ** value2
    else:
        return "Invalid operation. Allowed operations: add, subtract, multiply, divide, modulus, power", 400

    # Return the result as plain text
    return f"Result: {result}"

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
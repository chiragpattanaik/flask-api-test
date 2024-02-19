from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def perform_operation(operation, num1, num2):
    try:
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return "Error: Division by zero is not allowed."
            result = num1 / num2
        else:
            return "Invalid operation."
        return f"The result of {operation}ing {num1} and {num2} is {result}."
    except Exception as e:
        return f"Error: {str(e)}"

# @app.route('/', methods=['GET', 'POST'])
# def home_page():
#     return render_template('D:\Python\Flask code\templates\index.html')

@app.route('/math', methods=['POST'])
def math_operation():
    if request.method == 'POST':
        operation = request.form['operation']
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        result = perform_operation(operation, num1, num2)
        # return render_template('D:\Python\Flask code\templates\results.html', result=result)
        return jsonify(result=result)

@app.route('/via_postman', methods=['POST'])
def math_operation_via_postman():
    if request.method == 'POST':
        data = request.get_json()
        operation = data['operation']
        num1 = int(data['num1'])
        num2 = int(data['num2'])
        result = perform_operation(operation, num1, num2)
        return jsonify(result=result)


@app.route('/chirag1', methods=['POST'])
def math_chirag1():
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        personcontact = request.json['phone_number']
        return jsonify(name + email + personcontact)

@app.route('/url_testing')
#Write this thing in the browser address bar for the result:-
#http://127.0.0.1:5000/url_testing?val1=100&val2=120
def url_test():
    test1 = request.args.get('val1')
    test2 = request.args.get('val2')
    test3 = int(test1) + int(test2)
    return '''<h1>my result is: {}</h1>'''.format(test3)
if __name__ == '__main__':
    app.run()

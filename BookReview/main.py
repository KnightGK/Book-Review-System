from website import create_app
from flask import request

app = create_app()

@app.route('/get_message', methods=['POST'])
def get_message():
    name = request.form['name']
    message = f"Hello, {name}!"
    return message


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_name():
    return 'Hello !'

if __name__ == '__main__':
    app.run(debug=True)

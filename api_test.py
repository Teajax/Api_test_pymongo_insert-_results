from flask import Flask
import json

app = Flask(__name__)

@app.get('/test/')
def home():
    with open("./api_data.json") as data_file:
        data = data_file.read()
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
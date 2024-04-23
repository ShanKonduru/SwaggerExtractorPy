from flask import Flask, Response

app = Flask(__name__)

@app.route('/swagger')
def send_swagger_spec():
    with open('swagger.yaml', 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)

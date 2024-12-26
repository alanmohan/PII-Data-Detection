from flask import Flask, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def run_script():
    # Ensure that the parameter is included in the request
    if 'text' not in request.form:
        return "text not found", 400

    # Get the parameter from the request
    parameter = request.form['text']
#     return """[{"token": "Waseem", "label": "B-NAME_STUDENT"}, {"token": "Mabunda", "label": "I-NAME_STUDENT"}, {"token":
# "410.526.1667", "label": "B-ID_NUM"}, {"token": "vpi@mn.nlMind", "label": "B-ID_NUM"}]"""

    if not parameter:
        return "Parameter is empty or not provided", 400
    try:
        # Call the Python script with the parameter using subprocess
        result = subprocess.run(['python', 'testing/scriipt.py',parameter], capture_output=True, text=True, check=True)

        # Get the output of the script
        output = result.stdout
        # text after ### is the output of the script
        output = output.split('###')[1]
        return output
    except subprocess.CalledProcessError as e:
        # If there's an error calling the script, return an error message
        return f"Error calling script: {e.stderr}", 500  # Internal server error

if __name__ == '__main__':
    app.run(debug=True, port=1235)

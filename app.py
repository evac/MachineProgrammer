from flask import Flask, render_template, request
from main import ga, asm
import json
import pusher

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/run_program", methods=["GET", "POST"])
def run_program():

    inputs = request.form.get("inputs")
    test = []
    data = json.loads(inputs)
    for i in data:
        variables = tuple(i[0])
        test.append((variables, i[1]))


    asm.add_inputs(test)
    ga.main()

    return "HEllo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
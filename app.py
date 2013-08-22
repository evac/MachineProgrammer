from flask import Flask, render_template, request
from main import ga
import json

app = Flask(__name__)

SETTINGS = {
    "population": 80,
    "max_generations": 1
}


# initialize and start evolution
def init_evolution(inputs):
    input_len = len(inputs[0][0])
    ga.add_settings(SETTINGS)
    ga.add_inputs(inputs)
    ga.init_population(input_len)
    ga.init_algorithms()
    ga.main()

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/run_program", methods=["GET", "POST"])
def run_program():
    args = request.form.get("inputs")
    data = json.loads(args)

    # convert arrays of inputs to tuples
    inputs = []
    for i in data:
        variables = tuple(i[0])
        inputs.append((variables, i[1]))

    # start evolution
    init_evolution(inputs)

    return "Success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
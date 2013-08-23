from flask import Flask, render_template, request
from main import ga, push
import json
import string
import random

app = Flask(__name__)
SETTINGS = {
    "population": 100,
    "max_generations": 10,
    "pusher_settings": {
        "channel": "evolution",
        "app_id": '52211',
        "key": '9eb76d1f686de8651d46',
        "secret": '975144a7f85eced304f6'
    }
}


def generate_str(size=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))


# initialize and start evolution
def init_evolution(inputs):
    input_len = len(inputs[0][0])

    push.add_settings(SETTINGS["pusher_settings"])
    ga.add_settings(SETTINGS)
    ga.add_inputs(inputs)
    ga.init_population(input_len)
    ga.init_algorithms()
    ga.main()


@app.route("/")
def main():
    pusher = SETTINGS["pusher_settings"]
    channel = pusher["channel"]
    key = pusher["key"]
    return render_template("main.html", key=key, channel=channel)


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


@app.route("/exit_program", methods=["GET", "POST"])
def exit_program():

    # Log exit
    ga.EXIT_PROGRAM = True
    return "Success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
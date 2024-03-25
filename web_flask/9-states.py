#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown application context
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """
    Display a HTML page showing a list of states
    """
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """
    Display a HTML page showing cities of a state
    """
    state = storage.get("State", id)
    if state is None:
        return render_template('9-not_found.html')

    return render_template('9-states_cities.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

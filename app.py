from flask import Flask, Response
from parser import get_crossword

app = Flask(__name__)

cached = {}

@app.route('/guardiancross/<type>/<id>')
def return_guardian_crossword(type, id):

    try:
        data = cached[type][id]
    except KeyError:

        data = get_crossword(id, type)

        if data is None:
            return 'Crossword not found', 404

        try:
            cached[type][id] = data
        except KeyError:
            cached[type] = {}
            cached[type][id] = data

    return Response(data, mimetype='text/xml')

if __name__ == "__main__":
    app.run()

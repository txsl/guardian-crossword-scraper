from flask import Flask, Response

from parser import get_crossword

app = Flask(__name__)

@app.route('/guardiancross/<type>/<id>')
def return_guardian_crossword(type, id):
    
    data = get_crossword(id, type)
    
    return Response(data, mimetype='text/xml')

app.run()
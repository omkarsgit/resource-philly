import os
import json
import flask
import speech2text
from flask import request, jsonify, render_template, redirect

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('voice-html.html')


@app.route('/api/v1/text', methods=['GET', 'POST'])
def api_text():
    if 'text' not in request.args:
        return jsonify({'status' : 0})
    # return jsonify({'status': 1, 'intent': speech2text.get_intent(request.args['text'])[0], 'score': speech2text.get_intent(request.args['text'])[1]})
    return redirect('https://dev-link-love.pantheonsite.io/services/' + speech2text.get_intent(request.args['text'])[0])

app.run(host = '0.0.0.0', port = '9002')


# Reference:
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

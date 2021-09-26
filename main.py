from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

cooks = [{"PersonalID": 1, "Name": "Gordon Ramsay"}, {"PersonalID": 2, "Name": "Jamie Oliver"}]


@app.route('/hall_data')
def hello_world():
    url = "http://172.18.0.3:8080/app?id=1"
    return requests.get(url).text


@app.route('/app')
def id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "unknown request"

    result = []

    for person in cooks:
        if person['PersonalID'] == id:
            result.append(person)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

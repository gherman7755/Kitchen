import sys
from flask import Flask, request, jsonify
import requests
import random

cooks = []
names = ["Asma Millington", "Mariya Lynn", "Lewie Johnston", "Minnie Huber", "Katharine Finch"]
catch_phrases = ["I'll be back!", "Hasta la vista, baby", "I love the smell of napalm in the morning",
                 "Say hello to my little friend", "42"]

ID_HASH = 0
number_of_cooks = 2


class Cooks:
    def __init__(self, rank, proficiency, name, catch_phrase):
        self.rank = rank
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase


foods = [{"id": 1, "name": "pizza", "preparation-time": 20, "complexity": 2, "cooking-apparatus": "oven"},
         {"id": 2, "name": "salad", "preparation-time": 10, "complexity": 1, "cooking-apparatus": None},
         {"id": 3, "name": "zeama", "preparation-time": 7, "complexity": 1, "cooking-apparatus": "stove"},
         {"id": 4, "name": "Scallop", "preparation-time": 32, "complexity": 3, "cooking-apparatus": None},
         {"id": 5, "name": "Island Duck", "preparation-time": 35, "complexity": 3, "cooking-apparatus": "oven"},
         {"id": 6, "name": "Waffles", "preparation-time": 10, "complexity": 1, "cooking-apparatus": "stove"},
         {"id": 7, "name": "Aubergine", "preparation-time": 20, "complexity": 2, "cooking-apparatus": None},
         {"id": 8, "name": "Lasagna", "preparation-time": 30, "complexity": 2, "cooking-apparatus": "oven"},
         {"id": 9, "name": "Burger", "preparation-time": 15, "complexity": 1, "cooking-apparatus": "oven"},
         {"id": 10, "name": "Gyros", "preparation-time": 15, "complexity": 1, "cooking-apparatus": None}]

seed_value = random.randrange(sys.maxsize)
random.seed(seed_value)

gordon = Cooks(3, 3, "Gordon Ramsay", "My gran could do better! And she’s dead!")
cooks.append(gordon)

for i in range(1, number_of_cooks):
    rank = random.randint(1, 2)
    proficiency = random.randint(1, 3)
    name = random.choice(names)
    catch_phrase = random.choice(catch_phrases)
    t = Cooks(rank, proficiency, name, catch_phrase)
    cooks.append(t)


app = Flask(__name__)

global input_json
input_json = dict()


@app.route('/hall_data')
def hello_world():
    url = "http://172.17.0.3:80/app?id=1"
    return requests.get(url).text


hash_map = dict()


@app.route('/get_order', methods=["POST", "GET"])
def get_posted_order():
    if request.method == "POST":
        input_json = request.get_json(force=True)
        global hash_map
        global ID_HASH
        hash_map[ID_HASH] = input_json
        ID_HASH += 1
        return jsonify(input_json)
    else:
        return jsonify(hash_map)


@app.route('/read_order', methods=["GET"])
def output():
    input_json = {1: "a", 2: "b", 3: "c"}
    return jsonify(input_json)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

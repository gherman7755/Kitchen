import sys
from flask import Flask, request, jsonify
import requests
import random
import time
import concurrent.futures
from threading import Lock, Thread

cooks = []
names = ["Asma Millington", "Mariya Lynn", "Lewie Johnston", "Minnie Huber", "Katharine Finch"]
catch_phrases = ["I'll be back!", "Hasta la vista, baby", "I love the smell of napalm in the morning",
                 "Say hello to my little friend", "42"]

ID_HASH = 0
number_of_cooks = 2
SPENT_TIME = 0


class Cooks:
    def __init__(self, rank, proficiency, name, catch_phrase):
        self.rank = rank
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase
        self.dishes_to_prepare = []

    def choose_order(self):
        global order_list
        max_priority = 0
        can_take = self.proficiency
        for id in order_list:
            if max_priority < order_list[id]["priority"]:
                max_priority = order_list[id]["priority"]

        for id in order_list:
            if order_list[id]["priority"] == max_priority:
                if len(order_list[id]["items"]) == 0:
                    mutex = Lock()
                    mutex.acquire()
                    try:
                        self.send_order_back(order_list[id])
                        del order_list[id]
                        break
                    finally:
                        mutex.release()

                for item in order_list[id]["items"]:
                    if foods[item - 1]["complexity"] == self.rank or foods[item - 1]["complexity"] == self.rank - 1:
                        self.dishes_to_prepare.append(foods[item - 1])
                        order_list[id]["items"].remove(item)
                        can_take -= 1
                        if can_take == 0:
                            break
            if can_take == 0:
                break

        if len(self.dishes_to_prepare) != 0:
            self.start_cooking()

    def start_cooking(self):
        max_wait_time = max([dish["preparation-time"] for dish in self.dishes_to_prepare])
        # time.sleep(max_wait_time)
        self.dishes_to_prepare = []

    def send_order_back(self, order):
        res = requests.post('http://172.17.0.3:80/serve_order', json=order)


foods = [{"id": 1, "name": "pizza", "preparation-time": 20, "complexity": 2, "cooking-apparatus": "oven"},
         {"id": 2, "name": "salad", "preparation-time": 10, "complexity": 1, "cooking-apparatus": None},
         {"id": 3, "name": "zeama", "preparation-time": 7, "complexity": 1, "cooking-apparatus": "stove"},
         {"id": 4, "name": "Scallop", "preparation-time": 32, "complexity": 3, "cooking-apparatus": None},
         {"id": 5, "name": "Island Duck", "preparation-time": 35, "complexity": 3, "cooking-apparatus": "oven"},
         {"id": 6, "name": "Waffles", "preparation-time": 10, "complexity":      1, "cooking-apparatus": "stove"},
         {"id": 7, "name": "Aubergine", "preparation-time": 20, "complexity": 2, "cooking-apparatus": None},
         {"id": 8, "name": "Lasagna", "preparation-time": 30, "complexity": 2, "cooking-apparatus": "oven"},
         {"id": 9, "name": "Burger", "preparation-time": 15, "complexity": 1, "cooking-apparatus": "oven"},
         {"id": 10, "name": "Gyros", "preparation-time": 15, "complexity": 1, "cooking-apparatus": None}]

seed_value = random.randrange(sys.maxsize)
random.seed(seed_value)

gordon = Cooks(3, 3, "Gordon Ramsay", "My gran could do better! And she’s dead!")
cooks.append(gordon)
rank = 3

"""
For custom cooks
cooker = Cooks(rank, proficiency, random.choice(names), random.choice(catch_phrases))
cooks.append(cooker)
"""

for i in range(1, number_of_cooks):
    rank -= 1
    proficiency = random.randint(1, 3)
    name = random.choice(names)
    catch_phrase = random.choice(catch_phrases)
    t = Cooks(rank, proficiency, name, catch_phrase)
    cooks.append(t)


app = Flask(__name__)

global input_json
input_json = dict()


def start(cook):
    if order_list is not None:
        cook.choose_order()
        return "ok"
    return "Order list empty"


def change_priorities():
    now = time.time()
    for ident in order_list:
        if order_list[ident]["priority"] == 4 and now - order_list[ident]["time"] > 2:
            order_list[ident]["priority"] += 1
        elif order_list[ident]["priority"] == 3 and now - order_list[ident]["time"] > 5:
            order_list[ident]["priority"] += 1
        elif order_list[ident]["priority"] == 2 and now - order_list[ident]["time"] > 9:
            order_list[ident]["priority"] += 1
        elif order_list[ident]["priority"] == 1 and now - order_list[ident]["time"] > 13:
            order_list[ident]["priority"] += 1


order_list = dict()


@app.route('/get_order', methods=["POST", "GET"])
def get_posted_order():
    if request.method == "POST":
        global SPENT_TIME
        input_json = request.get_json(force=True)
        SPENT_TIME = time.time()
        global order_list
        global ID_HASH
        order_list[ID_HASH] = input_json
        order_list[ID_HASH]["time"] = time.time()
        ID_HASH += 1
        return jsonify(input_json)
    else:
        return jsonify(order_list)


@app.route('/start_kitchen')
def start_kitchen():
    threads = []
    while True:
        for i in range(len(cooks)):
            t = Thread(target=start, args=[cooks[i]])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        change_priorities()
        break
    return jsonify(order_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, make_response, jsonify, request, g
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.before_request
def load_data():
    with open("db.json") as f:
        g.data: dict = json.load(f)
# opening JSON file saving it to g- like a global variable object 


@app.after_request
def save_data(response):
    with open('db.json', 'w') as f:
        json.dump(g.data, f, indent=4)
    return response

@app.route("/")
def root():
    print("doing request")
    return "<h1>Welcome to the simple json server<h1>"

# same as @app.route('/langs', methods=['GET'])
@app.get("/ducks")
def get_ducks():
    return g.data['ducks']

@app.get('/ducks/<int:id>')
def get_duck_by_id(id):
    for duck in g.data['ducks']:
        if duck['id'] == id:
            return duck
    return "<h1>error! duck not found</h1>"

@app.patch('/ducks/<int:id>')
def patch_duck(id):
    print(request.json)
    for duck in g.data['ducks']:
        if duck['id'] == id:
            duck['likes'] = request.json['likes']
            return duck
    return "<h1>error! duck not found</h1>"

@app.post('/ducks')
def post_duck():
    new_duck = request.json
    #find the highest id of g.data['ducks']
    # duck_list = g.data['ducks']
    all_ids = [duck['id'] for duck in g.data['ducks']]
    new_duck['id'] = max(all_ids) + 1 
    g.data['ducks'].append(new_duck)
    return new_duck

    #add new id incremented by 1 to request.json
    #return the posted duck (request.json)
    #append that duck to g.data['ducks']

@app.delete('/ducks/<int:id>')
def delete_duck(id):
    # data = g.data['ducks'] # list of objects
    g.data['ducks'] = [duck for duck in g.data['ducks'] if duck['id'] != id]
    # get duck by id
    # filter that duck out of the list
    # return the filtered list 
    return {}


if __name__ == "__main__":
    app.run(port=5555, debug=True)

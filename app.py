from flask import Flask, jsonify, request
from itertools import count

app = Flask(__name__)

# our in-memory db

items = {}
next_id = count(1)

@app.get("/health")
def health():
    """Readiness endpoint"""
    return jsonify(status="ok"), 200

@app.get("/api/items")
def list_items():
    return jsonify(items=list(items.values())), 200

@app.get("/api/items/<int:item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify(error="Item not found"), 404
    return jsonify(item), 200

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify(error="Please include a name"), 400
    
    item_id = next(next_id)
    item = {"id": item_id, "name": data["name"]}
    items[item_id]=item
    
    return jsonify(item), 200 

@app.put("/api/items/<int:item_id>")
def edit_item(item_id):
    item = items.get(item_id)
    
    if item is None:
        return jsonify(error="Item not found"), 404
    
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify(error="Please include a name"), 400
    
    items[name]=data[name]
    
    return jsonify(item), 200 


@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    item = items.pop(item_id, None)
    if item is None:
        return jsonify(error="Item not found"), 404
    return jsonify(status="Item removed"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
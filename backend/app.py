import base64
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from PIL import Image
import imagehash

app = Flask(__name__)
CORS(app)

# Connect to MongoDB (adjust connection string if needed)
client = MongoClient('mongodb://localhost:27017/')
db = client['zk_handsign_auth']
users_collection = db['users']

def decode_image_to_pil(image_data):
    """
    Decode a base64-encoded image to a PIL Image.
    """
    encoded_data = image_data.split(",")[1]  # Remove the header
    image_bytes = base64.b64decode(encoded_data)
    return Image.open(io.BytesIO(image_bytes))

def compute_phash(image):
    """
    Compute the perceptual hash (pHash) for a PIL image.
    """
    return imagehash.phash(image)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    image_data = data["image"]
    user_id = "test_user"  # For simplicity, using a fixed user id
    image = decode_image_to_pil(image_data)
    phash = compute_phash(image)
    stored_hash = str(phash)  # Save the hash as a string
    print(f"[REGISTER] User: {user_id}")
    print(f"[REGISTER] pHash: {stored_hash}")
    
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"phash": stored_hash}},
        upsert=True
    )
    return jsonify({"message": "Gesture registered with perceptual hash!"})

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    image_data = data["image"]
    user_id = "test_user"
    image = decode_image_to_pil(image_data)
    current_hash = compute_phash(image)
    
    user_record = users_collection.find_one({"user_id": user_id})
    stored_hash_str = user_record.get("phash") if user_record else None
    if stored_hash_str is None:
        return jsonify({"success": False, "message": "No registered gesture found."}), 400
    
    stored_hash = imagehash.hex_to_hash(stored_hash_str)
    hamming_distance = current_hash - stored_hash
    print(f"[AUTHENTICATE] User: {user_id}")
    print(f"[AUTHENTICATE] Current pHash: {current_hash}")
    print(f"[AUTHENTICATE] Stored pHash: {stored_hash}")
    print(f"[AUTHENTICATE] Hamming Distance: {hamming_distance}")
    
    # Choose a threshold for the Hamming distance (tweak as needed)
    threshold = 10
    if hamming_distance <= threshold:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True)

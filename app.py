from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

app = Flask(__name__)


# Initialize the limiter with default limits
limiter = Limiter(
    get_remote_address,  # This is the correct way to pass the key_func
    app=app,
    default_limits=["1000 per day", "50 per hour"]
)


def load_dua():
    try:
        with open('Duas.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

@app.route('/', methods=['GET'])
@limiter.limit("1000 per day, 50 per hour", error_message='You have exceeded the rate limit.')
def get_dua():
    duas = load_dua()
    return jsonify(duas)

@app.route('/api/health', methods = ['GET'])
def health_check():
    return jsonify({"Status": "success" , "message": "API is running"}),200 


@app.errorhandler(429)
def reatelimit_error(e):
    return jsonify(error="ratelimit exceeded", message="You have exceeded your request limit. Please try again later."), 429

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "not Found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug= True)
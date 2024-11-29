import os
import time
import random
from flask import Flask, jsonify
from requests import Session

app = Flask(__name__)

def generate_log():
    logs = [
        "Success",
        "Created",
        "Failed",
    ]
    return random.choice(logs)

@app.route('/api_1')
def api_call():
    log_message = generate_log()
    print(f"Operation log: {log_message}")
    time.sleep(0.5)  # Wait for half a second
    return f"completed: {log_message}"

@app.route('/download_external_logs')
def download_external_logs():
    # retry_strategy = Retry(
    #     total=3,
    #     backoff_factor=1,
    #     status_forcelist=[500, 502, 503, 504],
    #     allowed_methods=['GET']
    # )
    external_key = os.getenv('EXTERNAL_INTGERATION_KEY')
    data_api_url = os.getenv("DATA_API_PORT").replace("tcp", "http")
    # return jsonify({"new": data_api_url})

    with Session() as session:
        # adapter = HTTPAdapter(max_retries=retry_strategy)
        # session.mount('http://', adapter)
        try:
            response = session.get(f'{data_api_url}/')
            response.raise_for_status()

            return jsonify(response.text)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Not able to communicate with data api"}), 500



@app.route("/health")
def liveness_probe():
    return jsonify({"status": "OK"})

@app.route("/ready")
def readiness_probe():
    return jsonify({"status": "ready"})



if __name__ == '__main__':
    app.run(debug=True)

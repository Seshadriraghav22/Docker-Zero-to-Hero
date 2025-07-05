from prometheus_client import Counter, Gauge, Histogram, generate_latest
from flask import Flask, Response
import time
import random

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
IN_PROGRESS = Gauge('http_requests_in_progress', 'In-progress HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency in seconds', ['endpoint'])

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with IN_PROGRESS.track_inprogress():
        start_time = time.time()
        time.sleep(random.uniform(0.1, 0.4))  # Simulate work
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint='/').observe(duration)
        return "Hello, Prometheus!"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, jsonify, render_template
from routes import page
from init_db import setup_db
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.register_blueprint(page)

@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})



# -------- RUN TABLE CREATION ON STARTUP ----------
setup_db()



if __name__ == "__main__":
    app.run(debug=True)

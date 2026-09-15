import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]
routers = db["routers"]
interface_status = db["interface_status"]

app = Flask(__name__)


@app.route("/")
def main():
    data = routers.find()
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add_comment():
    routerId = request.form.get("routerId")
    username = request.form.get("username")
    password = request.form.get("password")
    routers.insert_one(
        {"routerId": routerId, "username": username, "password": password}
    )
    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        routers.delete_one({"routerId": idx})
    except Exception:
        pass
    return redirect(url_for("main"))


@app.route("/router/<ip>")#help
def router_detail(ip):
    record = interface_status.find_one(
        {"router_ip": ip},
        sort=[("timestamp", -1)],
    )
    return render_template("router_detail.html", ip=ip, record=record)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

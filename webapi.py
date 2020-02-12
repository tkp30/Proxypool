import flask
import random
from database import DB
from config import config
app=flask.Flask("ProxyPool",static_url_path="/static",static_folder='statics',)
db=DB()
@app.route("/")
def api_index():
    return '''<h2>Welcome to Proxy pool System</h2>\n<h4>There is the REST API:</h4>\n<p><a href="/api/random">Random</a></p>\n<p><a href="/api/all">All</a></p>\n<p><a href="/api/count">Count</a></p><p><a href="/api/tqdl?limit=30">Extract</a></p>'''
@app.route("/api/random")
def get():
    choice=random.choice(db.getall())
    return flask.jsonify({"error":"","ip":choice,"century":db.getdbcontury(choice)})
@app.route("/api/all")
def all():
    return flask.jsonify({"error":"","list":db.getall()})
@app.route("/api/count")
def count():
    return flask.jsonify({"error":"","count":len(db.getall())})
@app.route("/api/tqdl")
def tqdl():
    if flask.request.args.get("limit",0)==0:
        return flask.jsonify({"error":"missing param limit"})
    elif not flask.request.args.get("limit").isdigit():
        return flask.jsonify({"error":"param limit's type is invaild"})
    elif int(flask.request.args.get("limit"))<1:
        return flask.jsonify({"error":"param limit's type is invaild"})
    else:
        li=[]
        while len(li)!=int(flask.request.args.get("limit")):
            c=random.choice(db.getall())
            if c not in li:
                li.append(c)
        return flask.jsonify({"error":"","list":li})
def run():
    app.run(config["web"]["ip"],config["web"]["port"])

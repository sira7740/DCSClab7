##
from flask import Flask, request, Response
import jsonpickle, pickle
import platform
import io, os, sys
import pika, redis
import hashlib, requests
import json
import base64

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

##
## You provide this
##
app = Flask(__name__)

@app.route('/scan/image/<X>', methods=['POST'])
def test(X):
    print(X)
    r = request
    try:
        m = hashlib.md5()
        m.update(r.data)
        q = m.hexdigest()
        response = {
            "hash" : q
        }
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(response)
        message = pickle.dumps([X,q,r.data])
        #credentials=pika.PlainCredentials('guest','guest')
        #parameters = pika.ConnectionParameters('rabbitmq', 15672, '/', credentials)
        #connection = pika.BlockingConnection(parameters)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='work')
        channel.basic_publish(exchange ='',routing_key='work', body = message)
        print(" [x] Sent Data ")
        connection.close()
    except:
        response = {
           "hash" : 0
        }

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/scan/url', methods=['POST'])
def test1():
    r = request
    X = r.json['url']

    #X = r.data
    #print(X)
    #X1 = json.loads(r.data)
    #X2 = X1.url
    print("printing url")
    print(X)

    try:
        r1 = requests.get(X, allow_redirects=True)
        m = hashlib.md5()
        m.update(r1.content)
        q = m.hexdigest()
        response = {
            "hash" : q
        }
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(response)
        message = pickle.dumps([X,q,r1.content])
        print("Printing type of sent data")
        print(type(X))
        print(type(q))
        print(type(r1.content))
        #credentials=pika.PlainCredentials('guest','guest')
        #parameters = pika.ConnectionParameters('rabbitmq', 15672, '/', credentials)
        #connection = pika.BlockingConnection(parameters)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='work')
        channel.basic_publish(exchange ='',routing_key='work', body = message)
        print(" [x] Sent Data ")
        connection.close()
    except:
        response = {
           "hash" : 0
        }

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/match/<X>', methods=['GET'])
def getvalue(X):
    r = redis.Redis(host=redisHost, db=5)
    print("printing X")
    print(type(X))
    print(X)
    val1 = []
    for i in r.smembers(X):
        print(i)
        val1.append((str(i)))
    v = r.smembers(X)
    print(type(v))
    response = {
        "value": val1
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

app.run(host="localhost", port=5000)
app.debug = True

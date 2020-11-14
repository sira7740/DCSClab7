#
# Worker server
#
import pickle
import platform
from PIL import Image
import io
import os
import sys
import pika
import redis
import hashlib
import json
import face_recognition



hostname = platform.node()

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

##
## You provide this
##

#credentials=pika.PlainCredentials('guest','guest')
#parameters = pika.ConnectionParameters('rabbitmq', 15672, '/', credentials)
#connection = pika.BlockingConnection(parameters)
#channel = connection.channel()



#credentials = pika.PlainCredentials('guest','guest')
#parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
#connection = pika.BlockingConnection(parameters)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='work')

print("connected to rabbitmq local")

def callback(ch, method, properties, body):
	obj1,obj2,obj3 = pickle.loads(body)

	print("printing type of obj1 obj2 obj3")
	print(type(obj1))
	print(type(obj2))
	print(type(obj3))

	redisNameToHash = redis.Redis(host=redisHost, db=1)
	redisNameToHash.set(obj1, obj2)
	print("Redis get by Name")
	print(obj1)
	val1 = redisNameToHash.get(obj1)
	print(val1)

	redisHashToName = redis.Redis(host=redisHost, db=2)
	redisHashToName.set(obj2, obj1)
	print("Redis get by Hash Value")
	print(obj2)
	val2 = redisHashToName.get(obj2)
	print(val2)

	img1 = io.BytesIO(obj3)
	img = face_recognition.load_image_file(img1)
	unknown_face_encodings = face_recognition.face_encodings(img)
	print("printing unknown faceencoding")
	print(unknown_face_encodings)

	redisHashToFaceRec = redis.Redis(host=redisHost, db=3)
	for each_face in unknown_face_encodings:
		redisHashToFaceRec.sadd(obj2, pickle.dumps(each_face))
		print("printing for DATABASE3")
		print(type(obj2))
		print(obj2)
		print(type(pickle.dumps(each_face)))
		print(pickle.dumps(each_face))
	print("Redis get by Hash Value for face encoding")
	print(obj2)
	val3 = []
	for i in redisHashToFaceRec.smembers(obj2):
		val3.append(pickle.loads(i))
	#val3 = pickle.loads(redisHashToFaceRec.smembers(obj2))
	print(val3)
	

	redisHashToHashSet = redis.Redis(host=redisHost, db=5)

	#keys_db3 = redisHashToFaceRec.keys()
	for each_key in redisHashToFaceRec.keys(pattern='*'):
		print("printing each key for DB4")
		print(type(each_key))
		print(each_key)
		face_array = []
		for i in redisHashToFaceRec.smembers(each_key):
			face_array.append(pickle.loads(i))
		#face_array = pickle.loads(redisHashToFaceRec.smembers(each_key))
		print("printing face array")
		print(type(face_array))
		print(face_array)
		for each_unknown in unknown_face_encodings:
			result = face_recognition.compare_faces(face_array, each_unknown)
			if result[0]:
				#print(pickle.loads(each_key))
				#each_key = pickle.loads(each_key)
				print("printing for DATABASE4")
				print(type(obj2))
				print(obj2)
				print(type((each_key)))
				print((each_key))
				redisHashToHashSet.sadd(obj2, pickle.dumps(each_key))
				break



channel.basic_consume(
    queue='work', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
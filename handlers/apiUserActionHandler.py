import json

import tornado.web
import tornado.gen

from common.sentry import sentry
from common.web import requestsManager
from objects import glob
from constants import exceptions

class handler(requestsManager.asyncRequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	@sentry.captureTornado
	def asyncGet(self):
		statusCode = 400
		data = {"message": "unknown error"}
		try:
			if "u" in self.request.arguments:
				userID = int(self.get_argument("u"))
			else:
				raise exceptions.invalidArgumentsException()

			if glob.redis.exists("peppy:actions:{}".format(str(userID))):
				data.update(json.loads(glob.redis.get("peppy:actions:{}".format(str(userID))).decode("utf-8")))
				data["action"]["online"] = 1
			else: 
				data["action"] = {}
				data["action"]["online"] = 0

			# Status code and message
			statusCode = 200
			data["message"] = "ok"

		except exceptions.invalidArgumentsException:
			statusCode = 400
			data["message"] = "missing required arguments"

		finally:
			# Add status code to data
			data["status"] = statusCode
			# Send response
			self.add_header("Access-Control-Allow-Origin", "*")
			self.add_header("Content-Type", "application/json")

			# Send response
			self.write(json.dumps(data))
			self.set_status(statusCode)


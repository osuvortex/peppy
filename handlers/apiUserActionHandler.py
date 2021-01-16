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
			if "id" in self.request.arguments:
				username = int(self.get_argument("id"))
			else:
				raise exceptions.invalidArgumentsException()


			if glob.redis.exists("peppy:actions:" + str(username) + ":actionid"):
				data["action"] = {}
				data["action"]["id"] = int(glob.redis.get("peppy:actions:" + str(username) + ":actionid"))
				data["action"]["text"] = str(glob.redis.get("peppy:actions:" + str(username) + ":actiontext"))

				data["action"]["beatmap"] = {}
				data["action"]["beatmap"]["md5"] = str(glob.redis.get("peppy:actions:" + str(username) +":actionmd5"))
				data["action"]["beatmap"]["id"] = int(glob.redis.get("peppy:actions:" + str(username) +":beatmapid"))
			else: 
				data["action"] = {}

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
			self.write(json.dumps(data))
			self.set_status(statusCode)

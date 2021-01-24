from common.log import logUtils as log
from common.ripple import bancho
from common.redis import generalPubSubHandler
from objects import glob
from constants import serverPackets


class handler(generalPubSubHandler.generalPubSubHandler):
	def __init__(self):
		super().__init__()
		self.structure = {
			"user_id": 0,
			"relax": 0
		}

	def handle(self, data):
		data = super().parseData(data)
		if data is None:
			return
		targetToken = glob.tokens.getTokenFromUserID(data["user_id"])
		if targetToken:
			currentRelax = glob.db.fetch(
				"SELECT is_relax FROM users WHERE id = %s LIMIT 1",
				(data["user_id"],)
			)
			if currentRelax["is_relax"] == data["relax"]:
				return
			glob.db.execute("UPDATE users SET is_relax = %s WHERE id = %s", [data["relax"], data["user_id"]])
			bancho.notification(
				data["user_id"],
				f"You are currently on {'Relax' if data["relax"] == 1 else 'Classic'} leaderboard"
			)
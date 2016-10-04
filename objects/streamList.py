from objects import stream

class streamList:
	def __init__(self):
		self.streams = {}

	def add(self, name):
		"""
		Create a new stream list if it doesn't already exist

		:param name: stream name
		:return:
		"""
		if name not in self.streams:
			self.streams[name] = stream.stream(name)
		print(str(self.streams))

	def remove(self, name):
		"""
		Removes an existing stream and kick every user in it

		:param name: stream name
		:return:
		"""
		if name in self.streams:
			for i in self.streams[name].clients:
				i.leaveStream(name)
			self.streams.pop(name)

	def broadcast(self, streamName, data):
		"""
		Send some data to all clients in a stream

		:param streamName: stream name
		:param data: data to send
		:return:
		"""
		if streamName not in self.streams:
			return
		self.streams[streamName].broadcast(data)

	def getClients(self, streamName):
		"""
		Get all clients in a stream

		:param streamName: name of the stream
		:return:
		"""
		if streamName not in self.streams:
			return
		return self.streams[streamName].clients

	def join(self, streamName, client):
		"""
		Add a client to a stream

		:param streamName: stream name
		:param client: client (osuToken) object
		:return:
		"""
		if streamName not in self.streams:
			return
		self.streams[streamName].addClient(client)

	def leave(self, streamName, client):
		"""
		Remove a client from a stream

		:param streamName: stream name
		:param client: client (osuToken) object
		:return:
		"""
		if streamName not in self.streams:
			return
		self.streams[streamName].removeClient(client)
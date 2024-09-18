import requests
import json
from utils.log import logger

class Requester:
    def __init__(self, url, method, data=None, header=None):
        self.url = url
        self.method = method
        self.data = data
        self.header = header

    def sendRequest(self):
        try:
            if self.method == "GET":
                result = requests.get(self.url, headers=self.header)
            elif self.method == "POST":
                result = requests.post(self.url, data=json.dumps(self.data), headers=self.header)
            elif self.method == "DELETE":
                result = requests.delete(self.url, data=json.dumps(self.data), headers=self.header)
            elif self.method == "PUT":
                result = requests.put(self.url, data=json.dumps(self.data), headers=self.header)

            return result
        except Exception as e:
            logger.error("Error : ", type(e).__name__, e.args)
            logger.error(
                f"url : {self.url}, parameter : {self.data}")
            
    def setData(self, data):
        self.data = data

    def setHeader(self, header):
        self.header = header

    def getAuth(self):
        pass
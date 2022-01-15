APP_ID = "KTJG6T-QRX67TR7LU"
#Taken from https://developer.wolframalpha.com/portal/myapps/
#Help https://www.geeksforgeeks.org/python-create-a-simple-assistant-using-wolfram-alpha-api/?ref=lbp

import wolframalpha
  

class BotAssistant:
    def __init__(self):
        self._client = wolframalpha.Client(APP_ID)
        pass

    def answerQ(self, question):
        res = self._client.query(question)
        answer = next(res.results).text
        return answer


import requests
import json
from datetime import date
import logging

# Logging file initialization
logging.basicConfig(filename='log/veztia.log',
                    format='[%(asctime)s-%(levelname)s-%(funcName)s-%(lineno)d]: %(message)s', level=logging.INFO)
requestResultList = []


# recursive function to get all request from Postman Collection
def recGetAllRequestFromPostmanCollection(data):
    if 'item' in data.keys():
        for i in range(len(data['item'])):
            recGetAllRequestFromPostmanCollection(data['item'][i])
    else:
        requestResultList.append(data)


def sendRequest(url, method, dataObj):
    headObj = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJpZFwiOlwiYzg3ZDU0ZDQtYzI0OS0xMWVjLWE4OWYtM2YzMWMzN2E5MmVlXCIsXCJmaXJzdE5hbWVcIjpcIkFiZHVsXCIsXCJsYXN0TmFtZVwiOlwiUm91ZlwiLFwiZW1haWxcIjpcImFiZHVscm91ZkBtYWRyYXNhaC5rZW1lbmFnLmdvLmlkXCIsXCJwcm9maWxlUGljdHVyZUlkXCI6bnVsbCxcInByb2ZpbGVQaWN0dXJlXCI6bnVsbCxcImNvbXBvbmVudElkXCI6XCJlYzA3YjJhMi03NDQ1LTExZWMtOTYwMC0wMjQyYWMxMTAwMTBcIixcImNvbXBvbmVudFwiOntcImlkXCI6XCJlYzA3YjJhMi03NDQ1LTExZWMtOTYwMC0wMjQyYWMxMTAwMTBcIixcImNvZGVcIjpcIjQuNFwiLFwiZGVzY3JpcHRpb25cIjpcIlVuaXQgUGVuZ2Vsb2xhIFByb3lla1wiLFwiY3JlYXRlZEF0XCI6XCIxMy0wMS0yMDIyIDE0OjUzOjQwXCIsXCJ1cGRhdGVkQXRcIjpcIjEzLTAxLTIwMjIgMTQ6NTM6NDBcIn0sXCJwcm92aW5jZUlkXCI6XCJjNDA3NzQ5ZS1iZWRkLTExZWMtODRjNS0xMzcyYWEwMzJhZjNcIixcInByb3ZpbmNlXCI6e1wiaWRcIjpcImM0MDc3NDllLWJlZGQtMTFlYy04NGM1LTEzNzJhYTAzMmFmM1wiLFwibmFtZVwiOlwiTGFpbm55YVwiLFwiY29kZVwiOlwiSUQ5NVwiLFwiY3JlYXRlZEF0XCI6XCIxOC0wNC0yMDIyIDEzOjA3OjAyXCIsXCJ1cGRhdGVkQXRcIjpcIjE4LTA0LTIwMjIgMTM6MDc6MDJcIn0sXCJyb2xlc1wiOlt7XCJpZFwiOlwiYzY5NGMwOTAtYzI1Mi0xMWVjLWE5MTAtNWZlODhlYzVhNmYyXCIsXCJ1c2VySWRcIjpcImM4N2Q1NGQ0LWMyNDktMTFlYy1hODlmLTNmMzFjMzdhOTJlZVwiLFwicm9sZUlkXCI6XCJlMTRhMDMwOC05MWY4LTExZWMtOGFkMC0xN2JhY2EyY2VkYTBcIixcInJvbGVcIjp7XCJpZFwiOlwiZTE0YTAzMDgtOTFmOC0xMWVjLThhZDAtMTdiYWNhMmNlZGEwXCIsXCJuYW1lXCI6XCJDb29yZGluYXRvclwiLFwiY29kZVwiOlwiRVwiLFwic3VwZXJ2aXNpb3JJZFwiOm51bGwsXCJjcmVhdGVkQXRcIjpcIjIwLTAyLTIwMjIgMDk6NTc6NDVcIixcInVwZGF0ZWRBdFwiOlwiMjAtMDItMjAyMiAwOTo1Nzo0NVwifSxcImNyZWF0ZWRBdFwiOlwiMjItMDQtMjAyMiAyMjo0MjoxMVwiLFwidXBkYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIyOjQyOjExXCJ9LHtcImlkXCI6XCJhYThmNDVmZS1jMjUzLTExZWMtYTk0OC1mYjhjMGU0ZjNlZjlcIixcInVzZXJJZFwiOlwiYzg3ZDU0ZDQtYzI0OS0xMWVjLWE4OWYtM2YzMWMzN2E5MmVlXCIsXCJyb2xlSWRcIjpcImVmZmYzODI4LTEwNWMtMTFlYy05MjBjLWRiZDIwODUwMzIwOVwiLFwicm9sZVwiOntcImlkXCI6XCJlZmZmMzgyOC0xMDVjLTExZWMtOTIwYy1kYmQyMDg1MDMyMDlcIixcIm5hbWVcIjpcIkFkbWluaXN0cmF0b3JcIixcImNvZGVcIjpcIkZcIixcInN1cGVydmlzaW9ySWRcIjpudWxsLFwiY3JlYXRlZEF0XCI6XCIxMS0wMi0yMDIyIDE1OjAzOjMyXCIsXCJ1cGRhdGVkQXRcIjpcIjExLTAyLTIwMjIgMTU6MDM6MzJcIn0sXCJjcmVhdGVkQXRcIjpcIjIyLTA0LTIwMjIgMjI6NDg6MzRcIixcInVwZGF0ZWRBdFwiOlwiMjItMDQtMjAyMiAyMjo0ODozNFwifV0sXCJyZXNvdXJjZXNJZFwiOlwiYWNlNmYyZTItYzI0YS0xMWVjLWE4ZDctYjM1Y2IxODliZWQxXCIsXCJyZXNvdXJjZXNcIjp7XCJpZFwiOlwiYWNlNmYyZTItYzI0YS0xMWVjLWE4ZDctYjM1Y2IxODliZWQxXCIsXCJwaG9uZU51bWJlclwiOlwiKzYyODEyODA1OTQyMjlcIixcInBvc2l0aW9uSWRcIjpcIjJmMWZmMzkwLWVlMmQtMTFlYy1hODIxLWJhMjMyN2VkNzU4N1wiLFwicG9zaXRpb25cIjp7XCJpZFwiOlwiMmYxZmYzOTAtZWUyZC0xMWVjLWE4MjEtYmEyMzI3ZWQ3NTg3XCIsXCJ1bml0SWRcIjpcImI5MjQ2ZmYwLWVkMjItMTFlYy04NjhjLTY3YjQ3YjZiNGJjM1wiLFwidW5pdFwiOntcImlkXCI6XCJiOTI0NmZmMC1lZDIyLTExZWMtODY4Yy02N2I0N2I2YjRiYzNcIixcIm5hbWVcIjpcIlBNVVwiLFwiY3JlYXRlZEF0XCI6XCIxNi0wNi0yMDIyIDEwOjE2OjMzXCIsXCJ1cGRhdGVkQXRcIjpcIjE2LTA2LTIwMjIgMTA6MTY6MzNcIn0sXCJuYW1lXCI6XCJQcm9qZWN0IE1hbmFnZW1lbnQgVW5pdCBDaGFpclwiLFwiY3JlYXRlZEF0XCI6XCIxNy0wNi0yMDIyIDExOjAzOjU3XCIsXCJ1cGRhdGVkQXRcIjpcIjE3LTA2LTIwMjIgMTE6MDM6NTdcIn0sXCJzdXBlcnZpc2lvcklkXCI6bnVsbCxcImNyZWF0ZWRBdFwiOlwiMjItMDQtMjAyMiAyMTo0NDoxMlwiLFwidXBkYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIxOjQ0OjEyXCJ9LFwibHNwSWRcIjpudWxsLFwibHNwXCI6bnVsbCxcImxhc3RMb2dpblwiOlwiMTAtMDctMjAyMiAxOToyOToxNVwiLFwiY3JlYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIxOjM3OjQ5XCIsXCJ1cGRhdGVkQXRcIjpcIjIyLTA0LTIwMjIgMjE6Mzc6NDlcIixcImFjdGl2ZVwiOnRydWV9IiwiYXVkIjoidXNlci1hZG1pbiIsImV4cCI6MTY1ODMyMDE1NX0.mc24hGTwcBKw8NsvdypODwQN3tECaAU8Ud5lOhNd721ioFinL9jBRCvAt9zhgX1FH6N01PFLd3CAlGV7T3F-CQ'
    }

    if method == "GET":
        req = requests.get(url, headers=headObj)
    elif method == "POST":
        req = requests.post(url, data=json.dumps(dataObj), headers=headObj)
    elif method == "DELETE":
        req = requests.delete(url, data=json.dumps(dataObj), headers=headObj)
    elif method == "PUT":
        req = requests.put(url, data=json.dumps(dataObj), headers=headObj)
    else:
        return 0

    return req


def sendAttack(parameterList, requestURL, requestMethod, resultList):
    # if requestMethod == "POST" or requestMethod == "PUT":
    if requestMethod == "DELETE":
        for parameter in parameterList:
            print(f"Sending request to : {requestURL}")
            print(f"Parameter : {parameter}")
            try:
                result = sendRequest(
                    requestURL, requestMethod, parameter)
                resultList.append(createResultDict(
                    requestURL, parameter, result.status_code, result.json()))
            except Exception as e:
                logging.error(e)
                logging.error(
                    f"url : {requestURL}, parameter : {parameter}")
                # print("This error", requestURL, parameter)
                continue


# For POST method
def createResultDict(requestURL, parameter, statusCode, response):
    resultDict = {
        "url": requestURL,
        "parameter": parameter,
        "statusCode": statusCode,
        "response": response
    }

    return resultDict


# For GET method
def getQueryListtoDict(queryList):
    queryDict = {}
    for query in queryList:
        key = query["key"]
        value = query["value"]
        queryDict[key] = value

    return queryDict


def parameterProductList(parameterDict, payloadContent):
    parameterList = []
    for key in parameterDict:
        # refrence
        tempParameterDict = parameterDict.copy()
        for payload in payloadContent:
            tempParameterDict[key] = payload
            parameterList.append(tempParameterDict.copy())

    return parameterList


def automateAttack(payloadFile, requestFile):
    payloadType = payloadFile.split(".")[0]

    resultList = []

    # load payload from file
    with open("payload/"+payloadFile, "r") as file:
        payloadContent = file.readlines()
        payloadContent = [line.rstrip() for line in payloadContent]

    # load postman collection
    with open(requestFile, 'r') as fh:
        requestDictList = json.loads(fh.read())

    for requestDict in requestDictList:
        requestMethod = requestDict["request"]["method"]
        requestURL = requestDict["request"]["url"]
        # if requestMethod == "POST":
        #     try:
        #         parameterDict = json.loads(
        #             requestDict["request"]["body"]["raw"])
        #         parameterList = parameterProductList(
        #             parameterDict, payloadContent)
        #         sendAttack(parameterList, requestURL,
        #                    requestMethod, resultList)
        #     except Exception as e:
        #         logging.error(e, requestURL)

        # if requestMethod == "GET":
        #     try:
        #         if (dict == type(requestURL)):
        #             host = f"{requestURL['host'][0]}"
        #             for path in requestURL["path"]:
        #                 host += f"/{path}"
        #             host += "?"
        #             parameterDict = getQueryListtoDict(requestURL["query"])
        #             parameterList = parameterProductList(
        #                 parameterDict, payloadContent)
        #             for parameter in parameterList:
        #                 # print("parameter ", parameter)
        #                 tempHost = host
        #                 for key, val in parameter.items():
        #                     tempHost += f"{key}={val}&"
        #                 # print(tempHost)
        #                 result = sendRequest(tempHost,
        #                                      requestMethod, [])
        #                 resultList.append(createResultDict(
        #                     tempHost, "null", result.status_code, result.json()))
        #     except Exception as e:
        #         logging.error(e, tempHost)

        # if requestMethod == "PUT":
        #     try:
        #         parameterDict = json.loads(
        #             requestDict["request"]["body"]["raw"])
        #         parameterList = parameterProductList(
        #             parameterDict, payloadContent)
        #         sendAttack(parameterList, requestURL,
        #                    requestMethod, resultList)
        #     except Exception as e:
        #         logging.error(e, requestURL)

        if requestMethod == "DELETE":
            try:
                parameterDict = json.loads(
                    requestDict["request"]["body"]["raw"])
                parameterList = parameterProductList(
                    parameterDict, payloadContent)
                sendAttack(parameterList, requestURL,
                           requestMethod, resultList)
            except Exception as e:
                logging.error(e, requestURL)

        with open(f"reports/{str(date.today())}-{payloadType}.json", "w") as fileRes:
            fileRes.write(json.dumps(resultList, indent=4))


if __name__ == "__main__":
    injectionAttackFile = ["sqli.txt", "command_injection_linux.txt",
                           "command_injection_windows.txt"]

    # injectionAttackFile = ["sqli.txt"]

    logging.info("=============== Starting veZtia ===============")
    for attackFile in injectionAttackFile:
        try:
            logging.info(f"using {attackFile}")
            automateAttack(attackFile, "result.json")
        except Exception as e:
            logging.error(e)
    logging.info("=============== Successfully running veZtia ===============")

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
        'Authorization': 'Bearer '
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
    headObj = {
        'Content-Type': 'application/json',
        'Authorization': ''
    }

    if requestMethod == "POST":
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

        if requestMethod == "GET":
            try:
                if (dict == type(requestURL)):
                    host = f"{requestURL['host'][0]}"
                    for path in requestURL["path"]:
                        host += f"/{path}"
                    host += "?"
                    parameterDict = getQueryListtoDict(requestURL["query"])
                    parameterList = parameterProductList(
                        parameterDict, payloadContent)
                    # print((parameterList[2]))
                    for parameter in parameterList:
                        # print(parameter)
                        tempHost = host

                        for key, val in parameter.items():
                            tempHost += f"{key}={val}&"

                        # print(tempHost)
                        result = sendRequest(tempHost,
                                             requestMethod, [])
                        resultList.append(createResultDict(
                            tempHost, "null", result.status_code, result.json()))
            except Exception as e:
                logging.error(e, tempHost)

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

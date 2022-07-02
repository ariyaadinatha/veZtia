import requests
import json
from datetime import date
import logging

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


def sendRequest(url, method, dataObj, headObj):
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


def automateAttack(payloadFile, requestFile):
    payloadType = payloadFile.split(".")[0]

    resultList = []
    with open("payload/"+payloadFile, "r") as file:
        payloadContent = file.readlines()
        payloadContent = [line.rstrip() for line in payloadContent]

    with open(requestFile, 'r') as fh:
        requestDictList = json.loads(fh.read())

    headObj = {
        'Content-Type': 'application/json',
        'Authorization': ''
    }

    for requestDict in requestDictList:
        resultDict = {}
        requestMethod = requestDict["request"]["method"]
        requestURL = requestDict["request"]["url"]
        if requestMethod == "POST":
            try:
                parameterDict = json.loads(
                    requestDict["request"]["body"]["raw"])
                for key in parameterDict:
                    tempParameterDict = parameterDict.copy()
                    for payload in payloadContent:
                        print("URL", requestURL)
                        print("Parameter", tempParameterDict)
                        tempParameterDict[key] = payload
                        try:
                            result = sendRequest(
                                requestURL, requestMethod, tempParameterDict, headObj)
                        except Exception as e:
                            logging.error(e)
                            logging.error(
                                f"url : {requestURL}, parameter : {tempParameterDict}")
                            continue
                        resultDict["url"] = requestURL
                        resultDict["payload"] = payload
                        resultDict["parameter"] = tempParameterDict
                        resultDict["statusCode"] = result.status_code
                        resultDict["response"] = result.json()
                        resultList.append(resultDict)
            except Exception as e:
                logging.error(e, requestURL)

        with open(f"reports/{str(date.today())}-{payloadType}.json", "w") as fileRes:
            fileRes.write(json.dumps(resultList, indent=4))


if __name__ == "__main__":
    injectionAttackFile = ["sqli.txt", "command_injection_linux.txt",
                           "command_injection_windows.txt"]

    logging.info("=============== Starting veZtia ===============")
    for attackFile in injectionAttackFile:
        try:
            logging.info(f"using {attackFile}")
            automateAttack(attackFile, "result.json")
        except Exception as e:
            logging.error(e)
    logging.info("=============== Successfully running veZtia ===============")

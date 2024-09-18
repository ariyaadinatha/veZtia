import requests
import json
from datetime import date



from utils.log import logger
import time

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
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJpZFwiOlwiYzg3ZDU0ZDQtYzI0OS0xMWVjLWE4OWYtM2YzMWMzN2E5MmVlXCIsXCJmaXJzdE5hbWVcIjpcIlVzZXJcIixcImxhc3ROYW1lXCI6XCJBZG1pbmlzdHJhdG9yXCIsXCJlbWFpbFwiOlwiYWJkdWxyb3VmQG1hZHJhc2FoLmtlbWVuYWcuZ28uaWRcIixcInByb2ZpbGVQaWN0dXJlSWRcIjpudWxsLFwicHJvZmlsZVBpY3R1cmVcIjpudWxsLFwiY29tcG9uZW50SWRcIjpcImVjMDdiMmEyLTc0NDUtMTFlYy05NjAwLTAyNDJhYzExMDAxMFwiLFwiY29tcG9uZW50XCI6e1wiaWRcIjpcImVjMDdiMmEyLTc0NDUtMTFlYy05NjAwLTAyNDJhYzExMDAxMFwiLFwiY29kZVwiOlwiNC40XCIsXCJkZXNjcmlwdGlvblwiOlwiVW5pdCBQZW5nZWxvbGEgUHJveWVrXCIsXCJjcmVhdGVkQXRcIjpcIjEzLTAxLTIwMjIgMTQ6NTM6NDBcIixcInVwZGF0ZWRBdFwiOlwiMTMtMDEtMjAyMiAxNDo1Mzo0MFwifSxcInByb3ZpbmNlSWRcIjpcImM0MDc3NDllLWJlZGQtMTFlYy04NGM1LTEzNzJhYTAzMmFmM1wiLFwicHJvdmluY2VcIjp7XCJpZFwiOlwiYzQwNzc0OWUtYmVkZC0xMWVjLTg0YzUtMTM3MmFhMDMyYWYzXCIsXCJuYW1lXCI6XCJMYWlubnlhXCIsXCJjb2RlXCI6XCJJRDk1XCIsXCJjcmVhdGVkQXRcIjpcIjE4LTA0LTIwMjIgMTM6MDc6MDJcIixcInVwZGF0ZWRBdFwiOlwiMTgtMDQtMjAyMiAxMzowNzowMlwifSxcInJvbGVzXCI6W3tcImlkXCI6XCJjNjk0YzA5MC1jMjUyLTExZWMtYTkxMC01ZmU4OGVjNWE2ZjJcIixcInVzZXJJZFwiOlwiYzg3ZDU0ZDQtYzI0OS0xMWVjLWE4OWYtM2YzMWMzN2E5MmVlXCIsXCJyb2xlSWRcIjpcImUxNGEwMzA4LTkxZjgtMTFlYy04YWQwLTE3YmFjYTJjZWRhMFwiLFwicm9sZVwiOntcImlkXCI6XCJlMTRhMDMwOC05MWY4LTExZWMtOGFkMC0xN2JhY2EyY2VkYTBcIixcIm5hbWVcIjpcIkNvb3JkaW5hdG9yXCIsXCJjb2RlXCI6XCJFXCIsXCJzdXBlcnZpc2lvcklkXCI6bnVsbCxcImNyZWF0ZWRBdFwiOlwiMjAtMDItMjAyMiAwOTo1Nzo0NVwiLFwidXBkYXRlZEF0XCI6XCIyMC0wMi0yMDIyIDA5OjU3OjQ1XCJ9LFwiY3JlYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIyOjQyOjExXCIsXCJ1cGRhdGVkQXRcIjpcIjIyLTA0LTIwMjIgMjI6NDI6MTFcIn0se1wiaWRcIjpcImFhOGY0NWZlLWMyNTMtMTFlYy1hOTQ4LWZiOGMwZTRmM2VmOVwiLFwidXNlcklkXCI6XCJjODdkNTRkNC1jMjQ5LTExZWMtYTg5Zi0zZjMxYzM3YTkyZWVcIixcInJvbGVJZFwiOlwiZWZmZjM4MjgtMTA1Yy0xMWVjLTkyMGMtZGJkMjA4NTAzMjA5XCIsXCJyb2xlXCI6e1wiaWRcIjpcImVmZmYzODI4LTEwNWMtMTFlYy05MjBjLWRiZDIwODUwMzIwOVwiLFwibmFtZVwiOlwiQWRtaW5pc3RyYXRvclwiLFwiY29kZVwiOlwiRlwiLFwic3VwZXJ2aXNpb3JJZFwiOm51bGwsXCJjcmVhdGVkQXRcIjpcIjExLTAyLTIwMjIgMTU6MDM6MzJcIixcInVwZGF0ZWRBdFwiOlwiMTEtMDItMjAyMiAxNTowMzozMlwifSxcImNyZWF0ZWRBdFwiOlwiMjItMDQtMjAyMiAyMjo0ODozNFwiLFwidXBkYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIyOjQ4OjM0XCJ9XSxcInJlc291cmNlc0lkXCI6XCJhY2U2ZjJlMi1jMjRhLTExZWMtYThkNy1iMzVjYjE4OWJlZDFcIixcInJlc291cmNlc1wiOntcImlkXCI6XCJhY2U2ZjJlMi1jMjRhLTExZWMtYThkNy1iMzVjYjE4OWJlZDFcIixcInBob25lTnVtYmVyXCI6XCIrNjI4MTI4MDU5NDIyOVwiLFwicG9zaXRpb25JZFwiOlwiMmYxZmYzOTAtZWUyZC0xMWVjLWE4MjEtYmEyMzI3ZWQ3NTg3XCIsXCJwb3NpdGlvblwiOntcImlkXCI6XCIyZjFmZjM5MC1lZTJkLTExZWMtYTgyMS1iYTIzMjdlZDc1ODdcIixcInVuaXRJZFwiOlwiYjkyNDZmZjAtZWQyMi0xMWVjLTg2OGMtNjdiNDdiNmI0YmMzXCIsXCJ1bml0XCI6e1wiaWRcIjpcImI5MjQ2ZmYwLWVkMjItMTFlYy04NjhjLTY3YjQ3YjZiNGJjM1wiLFwibmFtZVwiOlwiUE1VXCIsXCJjcmVhdGVkQXRcIjpcIjE2LTA2LTIwMjIgMTA6MTY6MzNcIixcInVwZGF0ZWRBdFwiOlwiMTYtMDYtMjAyMiAxMDoxNjozM1wifSxcIm5hbWVcIjpcIlByb2plY3QgTWFuYWdlbWVudCBVbml0IENoYWlyXCIsXCJjcmVhdGVkQXRcIjpcIjE3LTA2LTIwMjIgMTE6MDM6NTdcIixcInVwZGF0ZWRBdFwiOlwiMTctMDYtMjAyMiAxMTowMzo1N1wifSxcInN1cGVydmlzaW9ySWRcIjpudWxsLFwiY3JlYXRlZEF0XCI6XCIyMi0wNC0yMDIyIDIxOjQ0OjEyXCIsXCJ1cGRhdGVkQXRcIjpcIjE2LTA3LTIwMjIgMjI6MzA6MjdcIn0sXCJsc3BJZFwiOm51bGwsXCJsc3BcIjpudWxsLFwibGFzdExvZ2luXCI6XCIyNS0wNy0yMDIyIDAwOjQ1OjU3XCIsXCJjcmVhdGVkQXRcIjpcIjIyLTA0LTIwMjIgMjE6Mzc6NDlcIixcInVwZGF0ZWRBdFwiOlwiMTYtMDctMjAyMiAyMjozMDoyNlwiLFwiYWN0aXZlXCI6dHJ1ZX0iLCJhdWQiOiJ1c2VyLWFkbWluIiwiZXhwIjoxNjU5NTQ4NzU4fQ.l-O8Wu3IPpIJWH_9hFFNUHMUA_tQ7VaEghJKTC4aGRDKAS-V6eAOSKhxH0aIhQ8oMrdLUOnp_LWW0ACSPV7Isg'
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
    if requestMethod == "DELETE" or requestMethod == "POST" or requestMethod == "PUT":
        for parameter in parameterList:
            print(f"Sending request to : {requestURL}")
            print(f"Parameter : {parameter}")
            try:
                result = sendRequest(
                    requestURL, requestMethod, parameter)
                resultList.append(createResultDict(
                    requestURL, parameter, result.status_code, result.json()))
            except json.JSONDecodeError:
                return 0
            except requests.exceptions.InvalidSchema:
                return 0
            except Exception as e:
                logger.error("Error : ", type(e).__name__, e.args)
                logger.error(
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

        if requestMethod == "POST":
            try:
                parameterDict = json.loads(
                    requestDict["request"]["body"]["raw"])
                parameterList = parameterProductList(
                    parameterDict, payloadContent)
                sendAttack(parameterList, requestURL,
                           requestMethod, resultList)
            except Exception as e:
                logger.error("Error : ", type(e).__name__, e.args, requestURL)
                # logger.error(e, requestURL)

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
                    for parameter in parameterList:
                        # print("parameter ", parameter)
                        tempHost = host
                        for key, val in parameter.items():
                            tempHost += f"{key}={val}&"
                        # print(tempHost)
                        result = sendRequest(tempHost,
                                             requestMethod, [])
                        resultList.append(createResultDict(
                            tempHost, "null", result.status_code, result.json()))
            except Exception as e:
                # logger.error(e, tempHost)
                logger.error("Error : ", type(e).__name__, e.args, tempHost)

        if requestMethod == "PUT":
            try:
                parameterDict = json.loads(
                    requestDict["request"]["body"]["raw"])
                parameterList = parameterProductList(
                    parameterDict, payloadContent)
                sendAttack(parameterList, requestURL,
                           requestMethod, resultList)
            except Exception as e:
                logger.error("Error : ", type(e).__name__, e.args, requestURL)
                # logger.error(e, requestURL)

        if requestMethod == "DELETE":
            try:
                parameterDict = json.loads(
                    requestDict["request"]["body"]["raw"])
                parameterList = parameterProductList(
                    parameterDict, payloadContent)
                sendAttack(parameterList, requestURL,
                           requestMethod, resultList)
            except Exception as e:
                logger.error("Error : ", type(e).__name__, e.args, requestURL)
                # logger.error(e, requestURL)

        with open(f"reports/{str(date.today())}-{payloadType}.json", "w") as fileRes:
            fileRes.write(json.dumps(resultList, indent=4))


if __name__ == "__main__":
    logger.info("=============== Starting broken access detection ===============")
    startTime = time.time()

    # code here
    print("test")

    logger.info(f"Execution time: {(time.time() - startTime)}")
    logger.info("=============== Finished broken access detection ===============")



# if __name__ == "__main__":
if __name__ == "a":
    injectionAttackFile = ["sqli.txt", "command_injection_linux.txt",
                           "command_injection_windows.txt"]

    # injectionAttackFile = ["sqli.txt"]

    logger.info("=============== Starting veZtia ===============")
    for attackFile in injectionAttackFile:
        try:
            logger.info(f"using {attackFile}")
            automateAttack(attackFile, "result.json")
        except Exception as e:
            logger.error("Error : ", type(e).__name__, e.args)
            # logger.error(e)
    logger.info("=============== Successfully running veZtia ===============")

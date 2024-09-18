


# recursive function to get all request from Postman Collection
def recGetAllRequestFromPostmanCollection(data):
    if 'item' in data.keys():
        for i in range(len(data['item'])):
            recGetAllRequestFromPostmanCollection(data['item'][i])
    else:
        requestResultList.append(data)
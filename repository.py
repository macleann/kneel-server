'''A dictionary of keys containing lists. Each list holds unique dictionaries relevant to the overarching key.'''
DATABASE = {
    "METALS": [
        {"id": 1, "metal": "Sterling Silver", "price": 12.42},
        {"id": 2, "metal": "14K Gold", "price": 736.4},
        {"id": 3, "metal": "24K Gold", "price": 1258.9},
        {"id": 4, "metal": "Platinum", "price": 795.45},
        {"id": 5, "metal": "Palladium", "price": 1241.0}
    ],
    "ORDERS": [
        {
            "id": 1,
            "metalId": 1,
            "sizeId": 2,
            "styleId": 3,
            "timestamp": 1614659931693
        },
        {
            "id": 2,
            "metalId": 2,
            "sizeId": 3,
            "styleId": 1,
            "timestamp": 1616333988188
        },
        {
            "id": 3,
            "metalId": 3,
            "sizeId": 1,
            "styleId": 2,
            "timestamp": 1616334884289
        },
        {
            "id": 4,
            "metalId": 1,
            "sizeId": 3,
            "styleId": 2,
            "timestamp": 1616334980694
        }
    ],
    "SIZES": [
        {"id": 1, "carets": 0.5, "price": 405},
        {"id": 2, "carets": 0.75, "price": 782},
        {"id": 3, "carets": 1, "price": 1470},
        {"id": 4, "carets": 1.5, "price": 1997},
        {"id": 5, "carets": 2, "price": 3638}
    ],
    "STYLES": [
        {"id": 1, "style": "Classic", "price": 500},
        {"id": 2, "style": "Modern", "price": 710},
        {"id": 3, "style": "Vintage", "price": 965}
    ]
}


def all(resource):
    """Returns all dictionaries of any given resource for a GET method

    Args:
        resource (str): the path specified by the GET call's URL

    Returns:
        list: a list of dictionaries from the matching string in the DATABASE 
    """
    return DATABASE[resource.upper()]


def retrieve(resource, id, query_params):
    """Returns a single dictionary of any given resource for a GET method

    Args:
        resource (str): the path specified by the GET call's URL
        id (int): the id for the needed dictionary 
        query_params (???): not too sure yet tbh

    Returns:
        dict: the requested dictionary
    """
    requested_resource = None

    for single_resource in DATABASE[resource.upper()]:
        if single_resource["id"] == id:
            requested_resource = single_resource.copy()

    if resource == "orders":
        metal_price = DATABASE["METALS"][requested_resource["metalId"] - 1]["price"]
        style_price = DATABASE["STYLES"][requested_resource["styleId"] - 1]["price"]
        size_price = DATABASE["SIZES"][requested_resource["sizeId"] - 1]["price"]
        requested_resource["total_price"] = metal_price + style_price + size_price

    if query_params:
        for single_query in query_params:
            if single_query.upper() in DATABASE:
                single_query_singular = single_query[:-1]
                matching_query_id = single_query_singular + "Id"
                requested_resource[single_query_singular] = DATABASE[single_query.upper()][requested_resource[matching_query_id] - 1]
                requested_resource.pop(matching_query_id, None)

    return requested_resource


def create(resource, new_resource):
    """Adds a provided dictionary to the appropriate list in DATABASE for a POST method

    Args:
        resource (str): the path specified by the POST call's URL
        new_resource (dict): the dictionary that needs to be added

    Returns:
        dict: the modified dictionary that was posted with a unique id assigned
    """
    max_id = [DATABASE[resource.upper()]][-1]["id"]
    new_id = max_id + 1
    new_resource["id"] = new_id
    DATABASE[resource.upper()].append(new_resource)
    return new_resource


def update(resource, id, new_resource):
    """Updates a single, existing dictionary in the appropriate list in DATABASE for a PUT method

    Args:
        resource (str): the path specified by the PUT call's URL
        id (int): the id of the dictionary needing to be updated
        new_resource (dict): the updated contents of the specified dictionary
    """
    for index, single_resource in enumerate(DATABASE[resource.upper()]):
        if single_resource["id"] == id:
            DATABASE[resource.upper()][index] = new_resource
            break

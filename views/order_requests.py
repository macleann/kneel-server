from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

ORDERS = [
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
]

def get_all_orders():
    return ORDERS

def get_single_order(id):
    requested_order = None
    
    for order in ORDERS:
        if order["id"] == id:
            requested_order = order
            requested_order["metal"] = get_single_metal(requested_order["metalId"])
            requested_order["style"] = get_single_style(requested_order["styleId"])
            requested_order["size"] = get_single_size(requested_order["sizeId"])
            requested_order.pop("metalId", None)
            requested_order.pop("styleId", None)
            requested_order.pop("sizeId", None)
            return requested_order
        
def create_order(order):
    if len(ORDERS) == 0:
        max_id = 0
    else:
        max_id = ORDERS[-1]["id"]
    new_id = max_id + 1
    order["id"] = new_id
    ORDERS.append(order)
    return order

def update_order(id, new_order):
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            ORDERS[index] = new_order
            break

def delete_order(id):
    order_index = -1
    
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            order_index = index
            
    if order_index >= 0:
        ORDERS.pop(order_index)
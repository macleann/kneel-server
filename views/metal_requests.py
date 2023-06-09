METALS = [
    { "id": 1, "metal": "Sterling Silver", "price": 12.42 },
    { "id": 2, "metal": "14K Gold", "price": 736.4 },
    { "id": 3, "metal": "24K Gold", "price": 1258.9 },
    { "id": 4, "metal": "Platinum", "price": 795.45 },
    { "id": 5, "metal": "Palladium", "price": 1241.0 }
]

def get_all_metals():
    return METALS

def get_single_metal(id):
    requested_metal = None

    for metal in METALS:
        if metal["id"] == id:
            requested_metal = metal
            return requested_metal
        
def create_metal(metal):
    max_id = METALS[-1]["id"]
    new_id = max_id + 1
    metal["id"] = new_id
    METALS.append(metal)
    return metal

def update_metal(id, new_metal):
    for index, metal in enumerate(METALS):
        if metal["id"] == id:
            METALS[index] = new_metal
            break

def delete_metal(id):
    metal_index = -1
    
    for index, metal in enumerate(METALS):
        if metal["id"] == id:
            metal_index = index
            
    if metal_index >= 0:
        METALS.pop(metal_index)
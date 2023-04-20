class Order():
    
    def __init__(self, id, timestamp, metal_id, style_id, size_id):
        self.id = id
        self.timestamp = timestamp
        self.metal_id = metal_id
        self.style_id = style_id
        self.size_id = size_id
        self.metal = None
        self.style = None
        self.size = None
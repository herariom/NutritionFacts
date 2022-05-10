class Product:

    def __init__(self, name: str, img_path: str, url: str):
        self.name = name
        self.img_path = img_path
        self.url = url
        self.facts = {'Calories': 0, 'Fat': 0, 'Carbohydrates': 0, 'Protein': 0}

    def __hash__(self) -> int:
        return hash((self.name, self.facts))

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, Product):
            return NotImplemented
        return (self.name, self.facts) == (obj.name, obj.facts)

    def __str__(self):
        return "Name: " + self.name + ", Image Path: " + self.img_path + "Nutrition Facts: " + str(self.facts)

import random


class Dado:
    def __init__(self, faces: int = 6):
        self.faces = faces

    def rolar(self) -> int:
        return random.randint(1, self.faces)

    def to_dict(self) -> dict:
        return {"faces": self.faces}

    @classmethod
    def from_dict(cls, data: dict) -> "Dado":
        return cls(faces=data.get("faces", 6))

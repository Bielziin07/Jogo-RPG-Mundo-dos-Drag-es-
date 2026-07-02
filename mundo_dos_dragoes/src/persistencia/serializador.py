import json
import os
from ..models.jogo import Jogo

SAVES_DIR = "saves"


def salvar(jogo: Jogo, caminho: str = "saves/save.json") -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(jogo.to_dict(), f, indent=2, ensure_ascii=False)


def carregar(caminho: str = "saves/save.json") -> Jogo:
    with open(caminho, "r", encoding="utf-8") as f:
        return Jogo.from_dict(json.load(f))


def existe_save(caminho: str = "saves/save.json") -> bool:
    return os.path.exists(caminho)

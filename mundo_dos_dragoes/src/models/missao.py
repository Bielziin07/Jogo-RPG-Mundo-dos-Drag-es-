from __future__ import annotations
from typing import List
from .inimigo import Inimigo


# --------- Fábricas de inimigos ---------
def goblin_fraco():   return Inimigo("Goblin Fraco", 10, 3, tipo="goblin")
def goblin_forte():   return Inimigo("Goblin Forte", 20, 5, tipo="goblin")
def goblin_gigante(): return Inimigo("Goblin Gigante", 20, 7, tipo="goblin")
def rei_goblin():     return Inimigo("Rei Goblin", 50, 5, tipo="chefe")
def dragao_rebelde(): return Inimigo("Dragão Rebelde", 30, 10, tipo="dragao")
def dragao_normal():  return Inimigo("Dragão da Vila", 40, 12, tipo="dragao")
def dragao_especial(): return Inimigo("Dragão Especial", 50, 15, tipo="dragao")
def dragao_supremo(): return Inimigo("Dragão Supremo", 150, 20, tipo="chefe-final")


class Missao:
    def __init__(self, nome_missao: str, hordas: List[List[Inimigo]],
                 recompensa: dict | None = None, chave: str = ""):
        self.nome_missao = nome_missao
        self.chave = chave  # identificador para diálogos/lore
        self.concluida = False
        self.horda_atual = 0
        self._hordas = hordas
        self.recompensa = recompensa or {}

    def iniciar_missao(self) -> List[Inimigo]:
        self.horda_atual = 0
        self.concluida = False
        return list(self._hordas[0]) if self._hordas else []

    def avancar_horda(self) -> List[Inimigo]:
        self.horda_atual += 1
        if self.horda_atual >= len(self._hordas):
            self.concluida = True
            return []
        return list(self._hordas[self.horda_atual])

    def verificar_conclusao(self) -> bool:
        return self.concluida

    def to_dict(self) -> dict:
        return {
            "nomeMissao": self.nome_missao,
            "chave": self.chave,
            "concluida": self.concluida,
            "hordaAtual": self.horda_atual,
            "hordas": [[i.to_dict() for i in h] for h in self._hordas],
            "recompensa": self.recompensa,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Missao":
        hordas = [[Inimigo.from_dict(i) for i in h] for h in data.get("hordas", [])]
        m = cls(
            nome_missao=data["nomeMissao"],
            hordas=hordas,
            recompensa=data.get("recompensa", {}),
            chave=data.get("chave", ""),
        )
        m.concluida = data.get("concluida", False)
        m.horda_atual = data.get("hordaAtual", 0)
        return m


def missoes_padrao() -> List[Missao]:
    """Roteiro fiel à lore: 5 missões + 2 objetivos."""
    return [
        # M1
        Missao(
            "Aventura Inicial — Emboscada na Floresta",
            [[goblin_fraco(), goblin_fraco(), goblin_fraco()]],
            recompensa={"ouro": 10, "forca": 1, "item_narrativo": "ovo+mapa1"},
            chave="m1_floresta",
        ),
        # M2 (caminho do meio — canônico)
        Missao(
            "Exploração da Caverna",
            [[goblin_gigante(), goblin_fraco(), goblin_fraco(), goblin_fraco()]],
            recompensa={"ouro": 20, "forca": 2, "item_narrativo": "mapa2+aprimorador"},
            chave="m2_caverna",
        ),
        # M3 — dungeon da vila goblin
        Missao(
            "Vila dos Goblins",
            [
                [goblin_fraco()] * 6,
                [goblin_forte(), goblin_forte(), goblin_fraco(), goblin_fraco(), goblin_fraco()],
                [goblin_forte(), goblin_forte(), rei_goblin()],
            ],
            recompensa={"ouro": 50, "forca": 2, "item_narrativo": "aprimorador+ovo_choca"},
            chave="m3_vila_goblin",
        ),
        # Objetivo 1 — defesa da vila
        Missao(
            "Objetivo I — Defesa da Vila",
            [
                [goblin_forte(), goblin_forte(), goblin_fraco(), goblin_fraco()],
                [goblin_forte(), goblin_forte(), goblin_forte()],
                [goblin_forte(), goblin_forte()] + [goblin_fraco()] * 5,
            ],
            recompensa={"ouro": 30, "forca": 1},
            chave="obj1_defesa",
        ),
        # M4
        Missao(
            "Chegada ao Mundo dos Dragões",
            [[dragao_rebelde(), dragao_rebelde(), dragao_rebelde()]],
            recompensa={"ouro": 30, "forca": 2, "item_narrativo": "aprimorador"},
            chave="m4_mundo_dragoes",
        ),
        # M5
        Missao(
            "Vila dos Dragões",
            [[dragao_normal(), dragao_normal(), dragao_especial()]],
            recompensa={"ouro": 40, "forca": 2, "item_narrativo": "aprimorador"},
            chave="m5_vila_dragoes",
        ),
        # Objetivo 2 — chefe final
        Missao(
            "Objetivo II — O Dragão Supremo",
            [
                [dragao_normal(), dragao_normal(), dragao_normal()],
                [dragao_especial(), dragao_normal(), dragao_normal()],
                [dragao_supremo()],
            ],
            recompensa={"ouro": 100, "forca": 5},
            chave="obj2_supremo",
        ),
    ]

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personagem import Personagem


class Inimigo:
    def __init__(self, nome: str, pontos_de_vida: int, dano_base: int, tipo: str = "goblin"):
        self.nome = nome
        self.pontos_de_vida = pontos_de_vida
        self.dano_base = dano_base
        self.tipo = tipo

    def atacar(self, p: "Personagem") -> int:
        dano_real = max(1, self.dano_base - p.mitigar_dano())
        p.receber_dano(dano_real)
        return dano_real

    def receber_dano(self, dano: int) -> None:
        self.pontos_de_vida = max(0, self.pontos_de_vida - dano)

    def esta_vivo(self) -> bool:
        return self.pontos_de_vida > 0

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "pontosDeVida": self.pontos_de_vida,
            "danoBase": self.dano_base,
            "tipo": self.tipo,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Inimigo":
        return cls(
            nome=data["nome"],
            pontos_de_vida=data["pontosDeVida"],
            dano_base=data["danoBase"],
            tipo=data.get("tipo", "goblin"),
        )

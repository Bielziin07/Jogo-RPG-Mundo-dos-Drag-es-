from __future__ import annotations
from typing import Optional
from .personagem import Personagem


class Jogador:
    def __init__(self, nome_jogador: str, id_controle: int,
                 personagem: Optional[Personagem] = None):
        self.nome_jogador = nome_jogador
        self.id_controle = id_controle
        self.personagem: Optional[Personagem] = personagem

    def escolher_acao(self, acao: str) -> str:
        return acao

    def entrar_na_sessao(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {
            "nomeJogador": self.nome_jogador,
            "idControle": self.id_controle,
            "personagem": self.personagem.to_dict() if self.personagem else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Jogador":
        pers = Personagem.from_dict(data["personagem"]) if data.get("personagem") else None
        return cls(
            nome_jogador=data["nomeJogador"],
            id_controle=data["idControle"],
            personagem=pers,
        )

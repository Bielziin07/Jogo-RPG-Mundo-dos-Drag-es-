from __future__ import annotations
from typing import List
from .jogador import Jogador
from .missao import Missao, missoes_padrao


class Jogo:
    """Agregação de Jogadores (1..3) e composição de Missões."""

    def __init__(self, nome: str = "Mundo dos Dragões"):
        self.nome = nome
        self.estado_atual = "MENU"
        self.jogadores: List[Jogador] = []
        self.missoes: List[Missao] = missoes_padrao()
        self.missao_atual_idx = 0

    def iniciar_jogo(self) -> None:
        if not self.jogadores:
            raise RuntimeError("É preciso ao menos 1 jogador.")
        self.estado_atual = "EM_ANDAMENTO"
        self.missao_atual_idx = 0

    def encerrar_jogo(self) -> None:
        self.estado_atual = "ENCERRADO"

    def adicionar_jogador(self, j: Jogador) -> None:
        if len(self.jogadores) >= 3:
            raise RuntimeError("Máximo de 3 jogadores (UML: 1..3).")
        self.jogadores.append(j)

    def missao_atual(self) -> Missao:
        return self.missoes[self.missao_atual_idx]

    def avancar_missao(self) -> bool:
        self.missao_atual_idx += 1
        if self.missao_atual_idx >= len(self.missoes):
            self.estado_atual = "VITORIA"
            return False
        return True

    def grupo_derrotado(self) -> bool:
        return all(
            not j.personagem or not j.personagem.esta_vivo()
            for j in self.jogadores
        )

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "estadoAtual": self.estado_atual,
            "jogadores": [j.to_dict() for j in self.jogadores],
            "missoes": [m.to_dict() for m in self.missoes],
            "missaoAtualIdx": self.missao_atual_idx,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Jogo":
        g = cls(nome=data.get("nome", "Mundo dos Dragões"))
        g.estado_atual = data.get("estadoAtual", "MENU")
        g.jogadores = [Jogador.from_dict(j) for j in data.get("jogadores", [])]
        g.missoes = [Missao.from_dict(m) for m in data.get("missoes", [])]
        g.missao_atual_idx = data.get("missaoAtualIdx", 0)
        return g

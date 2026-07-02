from typing import List, Tuple
from .dado import Dado


class TesteHabilidade:
    """Realiza rolagem de 3d6 e classifica o resultado."""

    def __init__(self, tipo_de_acao: str):
        self.tipo_de_acao = tipo_de_acao
        self.dados: List[Dado] = [Dado() for _ in range(3)]

    def executar_teste(self) -> Tuple[int, List[int]]:
        rolagens = [d.rolar() for d in self.dados]
        return sum(rolagens), rolagens

    def avaliar_resultado(self, soma: int) -> str:
        if soma == 3:
            return "DESASTRE"
        if 4 <= soma <= 6:
            return "FALHA"
        if 7 <= soma <= 14:
            return "SUCESSO"
        if 15 <= soma <= 18:
            return "CRITICO"
        return "INVALIDO"

    def to_dict(self) -> dict:
        return {"tipoDeAcao": self.tipo_de_acao}

    @classmethod
    def from_dict(cls, data: dict) -> "TesteHabilidade":
        return cls(tipo_de_acao=data.get("tipoDeAcao", ""))

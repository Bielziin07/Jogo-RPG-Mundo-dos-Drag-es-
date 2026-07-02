from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personagem import Personagem


# tipos: "arma" (equipável, some no bonus_dano quando equipado)
#        "consumivel" (usado em batalha, aplica bonus_cura e some do inventário)
#        "acessorio" (equipável, dá bônus passivos)
class Item:
    def __init__(self, nome_item: str, preco_ouro: int = 0,
                 bonus_dano: int = 0, bonus_cura: int = 0,
                 tipo: str = "arma", efeito_especial: str = ""):
        self.nome_item = nome_item
        self.preco_ouro = preco_ouro
        self.bonus_dano = bonus_dano
        self.bonus_cura = bonus_cura
        self.tipo = tipo
        self.efeito_especial = efeito_especial  # "pesca_segura" | "biblioteca_segura"

    @property
    def equipavel(self) -> bool:
        return self.tipo in ("arma", "acessorio")

    @property
    def consumivel(self) -> bool:
        return self.tipo == "consumivel"

    def usar(self, p: "Personagem") -> str:
        """Usa o item (consumível). Retorna descrição do efeito."""
        if self.bonus_cura:
            p.recuperar_saude(self.bonus_cura)
            return f"{p.nome_personagem} usou {self.nome_item} e recuperou {self.bonus_cura} PV."
        return f"{self.nome_item} não teve efeito."

    def to_dict(self) -> dict:
        return {
            "nomeItem": self.nome_item,
            "precoOuro": self.preco_ouro,
            "bonusDano": self.bonus_dano,
            "bonusCura": self.bonus_cura,
            "tipo": self.tipo,
            "efeitoEspecial": self.efeito_especial,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(
            nome_item=data["nomeItem"],
            preco_ouro=data.get("precoOuro", 0),
            bonus_dano=data.get("bonusDano", 0),
            bonus_cura=data.get("bonusCura", 0),
            tipo=data.get("tipo", "arma"),
            efeito_especial=data.get("efeitoEspecial", ""),
        )


def _novo(nome: str) -> Item:
    """Fábrica utilizada pela loja (cada compra gera uma nova instância)."""
    return {
        "Poção de Vida": lambda: Item("Poção de Vida", 10, bonus_cura=20, tipo="consumivel"),
        "Espada Dourada": lambda: Item("Espada Dourada", 50, bonus_dano=15, tipo="arma"),
        "Vara de Pesca Dourada": lambda: Item("Vara de Pesca Dourada", 60,
                                              bonus_dano=10, tipo="arma",
                                              efeito_especial="pesca_segura"),
        "Livro Mágico": lambda: Item("Livro Mágico", 30, bonus_dano=12, tipo="arma",
                                     efeito_especial="biblioteca_segura"),
    }[nome]()


CATALOGO_LOJA = [
    _novo("Poção de Vida"),
    _novo("Espada Dourada"),
    _novo("Vara de Pesca Dourada"),
    _novo("Livro Mágico"),
]

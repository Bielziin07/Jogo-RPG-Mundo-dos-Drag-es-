from __future__ import annotations
from typing import List, Optional
from .item import Item
from .inimigo import Inimigo
from .teste_habilidade import TesteHabilidade


CLASSES_RPG = {
    "Guerreiro": {"forca": 10, "inteligencia": 4,  "saude": 6},
    "Pescador":  {"forca": 6,  "inteligencia": 3,  "saude": 10},
    "Doutor":    {"forca": 3,  "inteligencia": 10, "saude": 6},
}

PONTOS_PERSONALIDADE = 10  # rigidez + carisma == 10


class Personagem:
    def __init__(self, nome_personagem: str, classe_rpg: str,
                 rigidez: int = 5, carisma: int = 5):
        if classe_rpg not in CLASSES_RPG:
            raise ValueError(f"Classe inválida: {classe_rpg}")
        if rigidez + carisma != PONTOS_PERSONALIDADE:
            raise ValueError(
                f"rigidez + carisma deve somar {PONTOS_PERSONALIDADE} "
                f"(recebido {rigidez + carisma})."
            )
        if not (0 <= rigidez <= 10 and 0 <= carisma <= 10):
            raise ValueError("rigidez e carisma devem estar entre 0 e 10.")

        base = CLASSES_RPG[classe_rpg]
        self.nome_personagem = nome_personagem
        self.classe_rpg = classe_rpg
        self.forca = base["forca"]
        self.inteligencia = base["inteligencia"]
        self.saude = base["saude"]
        self.rigidez = rigidez
        self.carisma = carisma
        self.pontos_de_vida = self.pv_max()
        self.ouro = 0
        # inventário
        self.inventario: List[Item] = []           # itens que possui mas não estão equipados
        self.itens_equipados: List[Item] = []      # itens equipados (armas/acessórios)
        self.dragao_vivo = False

    # ---------- status derivado ----------
    def pv_max(self) -> int:
        return 20 + (self.saude // 3) * 10

    def bonus_dano_equipado(self) -> int:
        return sum(i.bonus_dano for i in self.itens_equipados)

    def forca_efetiva(self) -> int:
        return self.forca + self.bonus_dano_equipado()

    def efeito_ativo(self, chave: str) -> bool:
        return any(i.efeito_especial == chave for i in self.itens_equipados)

    # ---------- inventário ----------
    def adicionar_item(self, item: Item, equipar: bool = True) -> None:
        """Adiciona item ao personagem. Auto-equipa armas se equipar=True."""
        if item.equipavel and equipar:
            self.itens_equipados.append(item)
        else:
            self.inventario.append(item)

    def equipar(self, item: Item) -> bool:
        if item not in self.inventario or not item.equipavel:
            return False
        self.inventario.remove(item)
        self.itens_equipados.append(item)
        return True

    def desequipar(self, item: Item) -> bool:
        if item not in self.itens_equipados:
            return False
        self.itens_equipados.remove(item)
        self.inventario.append(item)
        return True

    def usar_consumivel(self, item: Item) -> Optional[str]:
        """Usa item consumível do inventário. Retorna descrição ou None."""
        if item not in self.inventario or not item.consumivel:
            return None
        msg = item.usar(self)
        self.inventario.remove(item)
        return msg

    # ---------- combate ----------
    def atacar(self, i: Inimigo) -> dict:
        teste = TesteHabilidade("ataque")
        soma, rolagens = teste.executar_teste()
        resultado = teste.avaliar_resultado(soma)
        dano_causado = 0
        contra_ataque = 0
        base = self.forca_efetiva()

        if resultado == "CRITICO":
            dano_causado = base * 2
            i.receber_dano(dano_causado)
        elif resultado == "SUCESSO":
            dano_causado = base
            i.receber_dano(dano_causado)
        elif resultado == "FALHA":
            pass
        elif resultado == "DESASTRE":
            bruto = i.dano_base * 2
            contra_ataque = max(1, bruto - self.mitigar_dano())
            self.receber_dano(contra_ataque)

        return {
            "rolagens": rolagens,
            "soma": soma,
            "resultado": resultado,
            "dano_causado": dano_causado,
            "dano_recebido": contra_ataque,
        }

    def receber_dano(self, dano: int) -> None:
        self.pontos_de_vida = max(0, self.pontos_de_vida - dano)

    def mitigar_dano(self) -> int:
        return self.rigidez ** 2

    def recuperar_saude(self, cura: int) -> None:
        self.pontos_de_vida = min(self.pv_max(), self.pontos_de_vida + cura)

    def esta_vivo(self) -> bool:
        return self.pontos_de_vida > 0

    # ---------- loja ----------
    def desconto_loja(self, preco: int) -> int:
        desconto = (self.inteligencia // 3) * 5
        return max(1, preco - desconto)

    def comprar_item(self, item: Item) -> bool:
        preco = self.desconto_loja(item.preco_ouro)
        if self.ouro < preco:
            return False
        self.ouro -= preco
        # consumíveis vão para o inventário; equipáveis: auto-equipa se ainda não tem
        if item.consumivel:
            self.inventario.append(item)
        else:
            self.adicionar_item(item, equipar=True)
        return True

    # ---------- serialização ----------
    def to_dict(self) -> dict:
        return {
            "nomePersonagem": self.nome_personagem,
            "classeRPG": self.classe_rpg,
            "forca": self.forca,
            "inteligencia": self.inteligencia,
            "saude": self.saude,
            "rigidez": self.rigidez,
            "carisma": self.carisma,
            "pontosDeVida": self.pontos_de_vida,
            "ouro": self.ouro,
            "inventario": [i.to_dict() for i in self.inventario],
            "itensEquipados": [i.to_dict() for i in self.itens_equipados],
            "dragaoVivo": self.dragao_vivo,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Personagem":
        p = cls(
            nome_personagem=data["nomePersonagem"],
            classe_rpg=data["classeRPG"],
            rigidez=data.get("rigidez", 5),
            carisma=data.get("carisma", 5),
        )
        p.forca = data.get("forca", p.forca)
        p.inteligencia = data.get("inteligencia", p.inteligencia)
        p.saude = data.get("saude", p.saude)
        p.pontos_de_vida = data.get("pontosDeVida", p.pontos_de_vida)
        p.ouro = data.get("ouro", p.ouro)
        p.inventario = [Item.from_dict(i) for i in data.get("inventario", [])]
        p.itens_equipados = [Item.from_dict(i) for i in data.get("itensEquipados", [])]
        p.dragao_vivo = data.get("dragaoVivo", False)
        return p

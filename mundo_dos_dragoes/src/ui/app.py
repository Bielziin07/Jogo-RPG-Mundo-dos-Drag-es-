import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from copy import deepcopy

from ..models import Jogo, Jogador, Personagem, lore
from ..models.personagem import CLASSES_RPG, PONTOS_PERSONALIDADE
from ..models.item import CATALOGO_LOJA, _novo
from ..persistencia import serializador


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mundo dos Dragões")
        self.geometry("1000x720")
        self.jogo: Jogo = Jogo()
        self.jogador_ativo_idx = 0
        self.inimigos_horda: list = []
        self._so_explorar = False
        self._montar_menu_inicial()

    # ---------- utilitários ----------
    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

    def _label(self, parent, text, **kw):
        return ttk.Label(parent, text=text, wraplength=940, justify="left", **kw)

    def _jogador_ativo(self) -> Jogador:
        return self.jogo.jogadores[self.jogador_ativo_idx]

    def _dialogo(self, titulo: str, texto: str):
        top = tk.Toplevel(self)
        top.title(titulo)
        top.geometry("640x380")
        top.grab_set()
        ttk.Label(top, text=titulo, font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        frame = ttk.Frame(top, padding=15); frame.pack(expand=True, fill="both")
        txt = tk.Text(frame, wrap="word", height=12, width=70)
        txt.insert("1.0", texto); txt.config(state="disabled")
        txt.pack(expand=True, fill="both")
        ttk.Button(top, text="Continuar", command=top.destroy).pack(pady=8)
        self.wait_window(top)

    # ---------- menu inicial ----------
    def _montar_menu_inicial(self):
        self._limpar()
        f = ttk.Frame(self, padding=40); f.pack(expand=True)
        self._label(f, "🐉 MUNDO DOS DRAGÕES 🐉",
                    font=("TkDefaultFont", 16, "bold")).pack(pady=10)
        self._label(f, "RPG cooperativo local (1 a 3 jogadores)").pack(pady=5)
        ttk.Button(f, text="Novo Jogo", command=self._nova_partida).pack(pady=5, fill="x")
        if self.jogo.jogadores:
            ttk.Button(f, text="Personagens (party atual)",
                       command=lambda: self._tela_personagens(volta=self._montar_menu_inicial)).pack(pady=5, fill="x")
            ttk.Button(f, text="Continuar Aventura",
                       command=self._tela_hub).pack(pady=5, fill="x")
        if serializador.existe_save():
            ttk.Button(f, text="Carregar Jogo", command=self._carregar).pack(pady=5, fill="x")
        ttk.Button(f, text="Sair", command=self.destroy).pack(pady=5, fill="x")

    def _nova_partida(self):
        self._dialogo("Prólogo", lore.INTRODUCAO)
        self._tela_criar_jogadores()

    # ---------- criação ----------
    def _tela_criar_jogadores(self):
        self._limpar()
        self._dialogo("Criação de Personagem", lore.CRIACAO_PERSONAGEM)
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        self._label(f, "Quantos jogadores? (1 a 3)").pack(pady=10)
        qtd_var = tk.IntVar(value=1)
        ttk.Spinbox(f, from_=1, to=3, textvariable=qtd_var, width=5).pack()

        def prosseguir():
            self.jogo = Jogo()
            for i in range(qtd_var.get()):
                if not self._criar_jogador_dialog(i + 1):
                    return
            if self.jogo.jogadores:
                self.jogo.iniciar_jogo()
                self._tela_hub(primeira_vez=True)

        ttk.Button(f, text="Continuar", command=prosseguir).pack(pady=15)
        ttk.Button(f, text="Voltar", command=self._montar_menu_inicial).pack()

    def _criar_jogador_dialog(self, idx: int) -> bool:
        nome = simpledialog.askstring("Jogador", f"Nome do Jogador {idx}:", parent=self) or f"Jogador{idx}"
        nome_p = simpledialog.askstring("Personagem", "Nome do personagem:", parent=self) or "Herói"

        top = tk.Toplevel(self); top.title(f"Personagem — Jogador {idx}"); top.grab_set()
        ttk.Label(top, text="Classe:").pack(pady=(10, 2))
        classe_var = tk.StringVar(value="Guerreiro")
        for c, atr in CLASSES_RPG.items():
            txt = f"{c}  (FOR {atr['forca']} / INT {atr['inteligencia']} / SAU {atr['saude']})"
            ttk.Radiobutton(top, text=txt, variable=classe_var, value=c).pack(anchor="w", padx=20)

        ttk.Label(top, text=f"\nDistribua {PONTOS_PERSONALIDADE} pontos entre Rigidez e Carisma:").pack()
        rig_var = tk.IntVar(value=5); car_var = tk.IntVar(value=5)
        soma_lbl = ttk.Label(top, text="Soma: 10"); soma_lbl.pack()
        def atualiza(*_): soma_lbl.config(text=f"Soma: {rig_var.get() + car_var.get()}")
        rig_var.trace_add("write", atualiza); car_var.trace_add("write", atualiza)

        row = ttk.Frame(top); row.pack(pady=5)
        ttk.Label(row, text="Rigidez:").grid(row=0, column=0)
        ttk.Spinbox(row, from_=0, to=10, textvariable=rig_var, width=5).grid(row=0, column=1, padx=5)
        ttk.Label(row, text="Carisma:").grid(row=0, column=2)
        ttk.Spinbox(row, from_=0, to=10, textvariable=car_var, width=5).grid(row=0, column=3, padx=5)

        ok_flag = {"ok": False}
        def confirmar():
            if rig_var.get() + car_var.get() != PONTOS_PERSONALIDADE:
                messagebox.showwarning("Atributos",
                    f"Rigidez + Carisma deve somar exatamente {PONTOS_PERSONALIDADE}.")
                return
            try:
                pers = Personagem(nome_p, classe_var.get(),
                                  rigidez=rig_var.get(), carisma=car_var.get())
            except ValueError as e:
                messagebox.showerror("Erro", str(e)); return
            self.jogo.adicionar_jogador(Jogador(nome, idx, personagem=pers))
            ok_flag["ok"] = True; top.destroy()
        ttk.Button(top, text="Confirmar", command=confirmar).pack(pady=10)
        self.wait_window(top)
        return ok_flag["ok"]

    # ---------- tela: seleção de personagens / inventário ----------
    def _tela_personagens(self, volta=None):
        self._limpar()
        volta = volta or self._tela_hub
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        self._label(f, "👥 Personagens do Grupo",
                    font=("TkDefaultFont", 14, "bold")).pack(pady=8)
        for j in self.jogo.jogadores:
            p = j.personagem
            row = ttk.LabelFrame(f, text=f"{j.nome_jogador} → {p.nome_personagem}",
                                 padding=10)
            row.pack(fill="x", pady=4)
            self._label(row,
                f"Classe: {p.classe_rpg} | PV: {p.pontos_de_vida}/{p.pv_max()} | "
                f"FOR {p.forca}(+{p.bonus_dano_equipado()})={p.forca_efetiva()} | "
                f"INT: {p.inteligencia} | SAU: {p.saude} | "
                f"RIG: {p.rigidez} | CAR: {p.carisma} | Ouro: {p.ouro}"
            ).pack(anchor="w")
            ttk.Button(row, text="🎒 Abrir inventário",
                       command=lambda pers=p: self._tela_inventario(pers, volta)).pack(pady=4, anchor="w")
        ttk.Button(f, text="⬅ Voltar", command=volta).pack(pady=15)

    def _tela_inventario(self, p: Personagem, volta):
        self._limpar()
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        self._label(f, f"🎒 Inventário de {p.nome_personagem} ({p.classe_rpg})",
                    font=("TkDefaultFont", 13, "bold")).pack(pady=6)
        self._label(f,
            f"PV: {p.pontos_de_vida}/{p.pv_max()} | "
            f"Força efetiva: {p.forca_efetiva()} (base {p.forca} + itens {p.bonus_dano_equipado()}) | "
            f"Ouro: {p.ouro}"
        ).pack(pady=4)

        eq_box = ttk.LabelFrame(f, text="Equipados (efeitos ativos)", padding=10)
        eq_box.pack(fill="x", pady=6)
        if not p.itens_equipados:
            self._label(eq_box, "(nenhum item equipado)").pack(anchor="w")
        for it in list(p.itens_equipados):
            linha = ttk.Frame(eq_box); linha.pack(fill="x", pady=2)
            self._label(linha,
                f"⚔ {it.nome_item} — dano+{it.bonus_dano}"
                + (f" | efeito: {it.efeito_especial}" if it.efeito_especial else "")
            ).pack(side="left")
            ttk.Button(linha, text="Desequipar",
                       command=lambda i=it, per=p: (p.desequipar(i), self._tela_inventario(per, volta))
                       ).pack(side="right")

        inv_box = ttk.LabelFrame(f, text="Inventário (não equipados)", padding=10)
        inv_box.pack(fill="x", pady=6)
        if not p.inventario:
            self._label(inv_box, "(vazio)").pack(anchor="w")
        for it in list(p.inventario):
            linha = ttk.Frame(inv_box); linha.pack(fill="x", pady=2)
            desc = f"{it.nome_item}"
            if it.bonus_dano: desc += f" — dano+{it.bonus_dano}"
            if it.bonus_cura: desc += f" — cura+{it.bonus_cura}"
            if it.efeito_especial: desc += f" — efeito: {it.efeito_especial}"
            desc += f"  [{it.tipo}]"
            self._label(linha, desc).pack(side="left")
            if it.equipavel:
                ttk.Button(linha, text="Equipar",
                           command=lambda i=it, per=p: (p.equipar(i), self._tela_inventario(per, volta))
                           ).pack(side="right")
            elif it.consumivel:
                ttk.Button(linha, text="Usar",
                           command=lambda i=it, per=p: self._usar_consumivel_inv(per, i, volta)
                           ).pack(side="right")

        ttk.Button(f, text="⬅ Voltar", command=volta).pack(pady=10)

    def _usar_consumivel_inv(self, p: Personagem, item, volta):
        msg = p.usar_consumivel(item)
        if msg:
            messagebox.showinfo("Item usado", msg)
        self._tela_inventario(p, volta)

    # ---------- Hub ----------
    def _tela_hub(self, primeira_vez: bool = False):
        if primeira_vez:
            self._dialogo("Sua vila", lore.HUB_PRIMEIRA_VEZ)
        self._limpar()
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        m = self.jogo.missao_atual()
        self._label(f, f"🏘️  Vila — próxima missão: {m.nome_missao}",
                    font=("TkDefaultFont", 12, "bold")).pack(pady=8)
        self._painel_status(f)

        ttk.Button(f, text="⚔️  Explorar / Iniciar Missão",
                   command=self._iniciar_missao).pack(fill="x", pady=3)

        st = "normal" if not self._so_explorar else "disabled"
        ttk.Button(f, text="🎣  Pescar no Mar",
                   command=lambda: self._selecionar_para_atividade("pescar"),
                   state=st).pack(fill="x", pady=3)
        ttk.Button(f, text="📚  Estudar na Biblioteca",
                   command=lambda: self._selecionar_para_atividade("estudar"),
                   state=st).pack(fill="x", pady=3)
        ttk.Button(f, text="🛒  Visitar a Loja",
                   command=self._selecionar_comprador, state=st).pack(fill="x", pady=3)

        ttk.Button(f, text="👥  Personagens / Inventário",
                   command=lambda: self._tela_personagens(volta=self._tela_hub)).pack(fill="x", pady=3)
        ttk.Button(f, text="💾  Salvar", command=self._salvar).pack(fill="x", pady=3)
        ttk.Button(f, text="Menu principal",
                   command=self._montar_menu_inicial).pack(fill="x", pady=3)

    def _painel_status(self, parent):
        box = ttk.LabelFrame(parent, text="Grupo", padding=10)
        box.pack(fill="x", pady=8)
        for j in self.jogo.jogadores:
            p = j.personagem
            eq = ", ".join(i.nome_item for i in p.itens_equipados) or "—"
            self._label(box,
                f"{j.nome_jogador} — {p.nome_personagem} ({p.classe_rpg}) | "
                f"PV: {p.pontos_de_vida}/{p.pv_max()} | "
                f"FOR:{p.forca_efetiva()} INT:{p.inteligencia} SAU:{p.saude} "
                f"RIG:{p.rigidez} CAR:{p.carisma} | Ouro:{p.ouro} | Equip: {eq}"
            ).pack(anchor="w")

    # ---------- seleção multi-jogador ----------
    def _selecionar_jogadores(self, titulo: str, texto: str,
                              min_sel: int = 1, permitir_multi: bool = True) -> list[int]:
        top = tk.Toplevel(self); top.title(titulo); top.grab_set()
        ttk.Label(top, text=texto, wraplength=380).pack(padx=15, pady=10)
        vars_ = []
        for idx, j in enumerate(self.jogo.jogadores):
            if not j.personagem.esta_vivo():
                continue
            v = tk.BooleanVar(value=False)
            ttk.Checkbutton(top,
                text=f"[{idx}] {j.nome_jogador} — {j.personagem.nome_personagem} "
                     f"({j.personagem.classe_rpg}, PV {j.personagem.pontos_de_vida})",
                variable=v).pack(anchor="w", padx=15)
            vars_.append((idx, v))
        escolha: list[int] = []
        def ok():
            sel = [i for i, v in vars_ if v.get()]
            if not permitir_multi and len(sel) > 1:
                messagebox.showwarning("Seleção", "Escolha apenas 1 personagem."); return
            if len(sel) < min_sel:
                messagebox.showwarning("Seleção",
                    f"Selecione pelo menos {min_sel} personagem(ns)."); return
            escolha.extend(sel); top.destroy()
        ttk.Button(top, text="OK", command=ok).pack(pady=10)
        self.wait_window(top)
        return escolha

    # ---------- atividades ----------
    def _selecionar_para_atividade(self, tipo: str):
        texto = ("Selecione um ou mais personagens para "
                 + ("pescar no mar" if tipo == "pescar" else "estudar na biblioteca")
                 + " (cada um rolará seus dados):")
        alvos = self._selecionar_jogadores(
            titulo="Quem realiza a ação?", texto=texto, permitir_multi=True)
        if not alvos:
            return
        for idx in alvos:
            self.jogador_ativo_idx = idx
            self._atividade(tipo)
            if self.jogo.grupo_derrotado():
                return
        self._tela_hub()

    def _atividade(self, tipo: str):
        from ..models.teste_habilidade import TesteHabilidade
        p = self._jogador_ativo().personagem
        self._dialogo(f"Ação de {p.nome_personagem}", lore.ATIVIDADE[f"{tipo}_inicio"])

        teste = TesteHabilidade(tipo)
        soma, rolagens = teste.executar_teste()
        res = teste.avaliar_resultado(soma)

        if res == "DESASTRE":
            if (tipo == "pescar" and p.efeito_ativo("pesca_segura")) or \
               (tipo == "estudar" and p.efeito_ativo("biblioteca_segura")):
                res = "FALHA"

        header = f"({p.nome_personagem}) 🎲 Dados: {rolagens} (soma {soma})\n\n"

        if tipo == "pescar":
            if res == "CRITICO":
                p.saude += 2; p.pontos_de_vida += 10
                self._dialogo("Pesca", header + lore.ATIVIDADE["pescar_critico"])
            elif res == "SUCESSO":
                p.saude += 1; p.pontos_de_vida += 5
                self._dialogo("Pesca", header + lore.ATIVIDADE["pescar_sucesso"])
            elif res == "FALHA":
                self._dialogo("Pesca", header + lore.ATIVIDADE["pescar_falha"])
            elif res == "DESASTRE":
                self._dialogo("Pesca", header + lore.ATIVIDADE["pescar_desastre"])
                from ..models.inimigo import Inimigo
                self.inimigos_horda = [Inimigo("Monstro Marinho", 30, 8, tipo="oceano")]
                self._tela_combate(retorno_hub=True); return
        else:  # estudar
            if res == "CRITICO":
                p.inteligencia += 2
                self._dialogo("Estudo", header + lore.ATIVIDADE["estudar_critico"])
            elif res == "SUCESSO":
                p.inteligencia += 1
                self._dialogo("Estudo", header + lore.ATIVIDADE["estudar_sucesso"])
            elif res == "FALHA":
                self._dialogo("Estudo", header + lore.ATIVIDADE["estudar_falha"])
            elif res == "DESASTRE":
                self._dialogo("Estudo", header + lore.ATIVIDADE["estudar_desastre"])
                from ..models.inimigo import Inimigo
                self.inimigos_horda = [Inimigo("Aranha Gigante", 30, 10, tipo="aracnideo")]
                self._tela_combate(retorno_hub=True); return

    # ---------- loja (com seleção de comprador) ----------
    def _selecionar_comprador(self):
        alvos = self._selecionar_jogadores(
            titulo="Comprador",
            texto="Qual personagem vai à loja?",
            permitir_multi=False)
        if not alvos: return
        self.jogador_ativo_idx = alvos[0]
        self._tela_loja()

    def _tela_loja(self):
        self._limpar()
        self._dialogo("Loja", lore.ATIVIDADE["loja_boas_vindas"])
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        p = self._jogador_ativo().personagem
        self._label(f, f"🛒 Loja — {p.nome_personagem} tem {p.ouro} de ouro",
                    font=("TkDefaultFont", 12, "bold")).pack(pady=8)

        for item in CATALOGO_LOJA:
            preco = p.desconto_loja(item.preco_ouro)
            desc = f"{item.nome_item} — {preco} ouro | tipo: {item.tipo}"
            if item.bonus_dano: desc += f" | dano+{item.bonus_dano}"
            if item.bonus_cura: desc += f" | cura+{item.bonus_cura}"
            if item.efeito_especial: desc += f" | efeito: {item.efeito_especial}"
            ttk.Button(f, text=desc, command=lambda it=item: self._comprar(it)).pack(fill="x", pady=2)

        ttk.Button(f, text="Voltar", command=self._tela_hub).pack(pady=10)

    def _comprar(self, item_ref):
        # cria uma nova instância do item (senão a loja compartilharia efeitos)
        novo_item = _novo(item_ref.nome_item)
        p = self._jogador_ativo().personagem
        if p.comprar_item(novo_item):
            messagebox.showinfo("Loja",
                f"Você comprou {novo_item.nome_item}!"
                + (" (equipado)" if novo_item.equipavel else " (adicionado ao inventário)"))
        else:
            messagebox.showwarning("Loja", "Ouro insuficiente.")
        self._tela_loja()

    # ---------- combate ----------
    def _iniciar_missao(self):
        m = self.jogo.missao_atual()
        texto = lore.MISSOES.get(m.chave, {}).get("inicio", f"Iniciando: {m.nome_missao}")
        self._dialogo(m.nome_missao, texto)
        self.inimigos_horda = m.iniciar_missao()
        self.jogador_ativo_idx = 0
        while not self._jogador_ativo().personagem.esta_vivo():
            self.jogador_ativo_idx = (self.jogador_ativo_idx + 1) % len(self.jogo.jogadores)
        self._tela_combate()

    def _tela_combate(self, retorno_hub: bool = False):
        self._limpar()
        f = ttk.Frame(self, padding=20); f.pack(expand=True, fill="both")
        m = self.jogo.missao_atual()
        titulo = "⚔️  Encontro Inesperado" if retorno_hub else \
                 f"⚔️  {m.nome_missao} — Horda {m.horda_atual + 1}"
        self._label(f, titulo, font=("TkDefaultFont", 12, "bold")).pack(pady=6)
        self._painel_status(f)

        box = ttk.LabelFrame(f, text="Inimigos", padding=10); box.pack(fill="x", pady=6)
        for i, inim in enumerate(self.inimigos_horda):
            self._label(box, f"[{i}] {inim.nome} — PV:{inim.pontos_de_vida} — dano:{inim.dano_base}").pack(anchor="w")

        j = self._jogador_ativo(); p = j.personagem
        self._label(f, f"➤ Vez de: {j.nome_jogador} ({p.nome_personagem}) — "
                       f"Força efetiva: {p.forca_efetiva()}",
                    font=("TkDefaultFont", 10, "bold")).pack(pady=4)

        alvo_var = tk.IntVar(value=0)
        row = ttk.Frame(f); row.pack()
        ttk.Label(row, text="Alvo:").grid(row=0, column=0)
        ttk.Spinbox(row, from_=0, to=max(0, len(self.inimigos_horda) - 1),
                    textvariable=alvo_var, width=5).grid(row=0, column=1, padx=5)
        ttk.Button(f, text="⚔ Atacar",
                   command=lambda: self._acao_atacar(alvo_var.get(), retorno_hub)).pack(pady=4)

        # Uso de poção em batalha
        consumiveis = [i for i in p.inventario if i.consumivel]
        if consumiveis:
            pot_row = ttk.LabelFrame(f, text="Usar item em batalha", padding=8)
            pot_row.pack(fill="x", pady=6)
            for it in consumiveis:
                ttk.Button(pot_row,
                    text=f"🧪 Usar {it.nome_item} (cura+{it.bonus_cura})",
                    command=lambda i=it: self._usar_pocao_batalha(i, retorno_hub)
                ).pack(anchor="w", pady=2)

    def _usar_pocao_batalha(self, item, retorno_hub):
        p = self._jogador_ativo().personagem
        msg = p.usar_consumivel(item)
        if msg:
            self._dialogo("Item usado em batalha", msg)
        # inimigos contra-atacam (ação consome turno)
        self._contra_ataque(p)
        if self.jogo.grupo_derrotado():
            self._tela_fim(vitoria=False); return
        self._proximo_jogador(); self._tela_combate(retorno_hub=retorno_hub)

    def _contra_ataque(self, p):
        for i in self.inimigos_horda:
            if not p.esta_vivo(): break
            bruto = i.dano_base
            dano = max(1, bruto - p.mitigar_dano())
            p.receber_dano(dano)
            self._dialogo("Contra-ataque",
                f"{i.nome} atacou {p.nome_personagem} — dano {dano} "
                f"(bruto {bruto}, mitigado {p.mitigar_dano()}).")

    def _proximo_jogador(self):
        n = len(self.jogo.jogadores)
        for _ in range(n):
            self.jogador_ativo_idx = (self.jogador_ativo_idx + 1) % n
            if self._jogador_ativo().personagem.esta_vivo():
                return

    def _acao_atacar(self, idx_alvo: int, retorno_hub: bool):
        if idx_alvo < 0 or idx_alvo >= len(self.inimigos_horda):
            messagebox.showwarning("Combate", "Alvo inválido."); return
        p = self._jogador_ativo().personagem
        alvo = self.inimigos_horda[idx_alvo]
        res = p.atacar(alvo)
        self._dialogo("Rolagem de Ataque",
            f"🎲 Dados: {res['rolagens']} (soma {res['soma']}) → {res['resultado']}\n\n"
            f"Dano causado em {alvo.nome}: {res['dano_causado']}\n"
            f"Dano recebido: {res['dano_recebido']}")

        self.inimigos_horda = [i for i in self.inimigos_horda if i.esta_vivo()]
        self._contra_ataque(p)

        if self.jogo.grupo_derrotado():
            self._tela_fim(vitoria=False); return

        if retorno_hub and not self.inimigos_horda:
            self._tela_hub(); return

        if not self.inimigos_horda:
            self._recompensar_horda()
            proxima = self.jogo.missao_atual().avancar_horda()
            if not proxima:
                self._concluir_missao(); return
            self.inimigos_horda = proxima
            self._dialogo("Nova horda!", "Reforços chegam. Prepare-se!")

        self._proximo_jogador()
        self._tela_combate(retorno_hub=retorno_hub)

    def _recompensar_horda(self):
        for j in self.jogo.jogadores:
            if j.personagem.esta_vivo():
                j.personagem.ouro += 5

    def _concluir_missao(self):
        m = self.jogo.missao_atual()
        rec = m.recompensa
        for j in self.jogo.jogadores:
            if not j.personagem.esta_vivo(): continue
            j.personagem.ouro += rec.get("ouro", 0)
            j.personagem.forca += rec.get("forca", 0)

        fim = lore.MISSOES.get(m.chave, {}).get("fim", "Missão concluída!")
        self._dialogo(f"Fim: {m.nome_missao}", fim)

        if m.chave == "m3_vila_goblin":
            for j in self.jogo.jogadores:
                j.personagem.dragao_vivo = True
        if m.chave == "obj1_defesa":
            self._so_explorar = True
        if m.chave == "m4_mundo_dragoes":
            self._so_explorar = False

        if not self.jogo.avancar_missao():
            self._tela_fim(vitoria=True); return
        self._tela_hub()

    # ---------- fim ----------
    def _tela_fim(self, vitoria: bool):
        self._limpar()
        if vitoria:
            self._dialogo("Final", lore.MISSOES["obj2_supremo"]["fim"])
        else:
            self._dialogo("Fim de jogo", lore.FIM_DERROTA)
        f = ttk.Frame(self, padding=40); f.pack(expand=True)
        self._label(f, "🏆 VITÓRIA!" if vitoria else "💀 DERROTA",
                    font=("TkDefaultFont", 14, "bold")).pack(pady=20)
        ttk.Button(f, text="Menu Inicial", command=self._montar_menu_inicial).pack()

    # ---------- persistência ----------
    def _salvar(self):
        serializador.salvar(self.jogo)
        messagebox.showinfo("Salvar", "Jogo salvo em saves/save.json")

    def _carregar(self):
        self.jogo = serializador.carregar()
        self.jogador_ativo_idx = 0
        messagebox.showinfo("Carregar", "Jogo carregado.")
        self._tela_hub()

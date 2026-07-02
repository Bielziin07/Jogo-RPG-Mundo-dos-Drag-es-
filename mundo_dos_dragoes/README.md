# Mundo dos Dragões — RPG (Nível 2 / 3 / 4)

Jogo de RPG cooperativo local (até 4 jogadores) com sistema de 3d6, implementado em **Python + Tkinter**. Estrutura de classes fiel à UML entregue no Nível I.

## Requisitos
- Python 3.10+
- Tkinter (já vem com a instalação padrão do Python)

## Instalação
```bash
git clone <repo>
cd mundo_dos_dragoes
pip install -r requirements.txt
```

## Execução
```bash
python main.py
```

## Estrutura do projeto (conforme UML)
```
mundo_dos_dragoes/
├── main.py                       # Ponto de entrada
├── requirements.txt
├── saves/                        # Serialização (JSON) dos jogos salvos
└── src/
    ├── models/                   # Classes do domínio (UML)
    │   ├── jogo.py               # Jogo   (composição Missao, agregação Jogador)
    │   ├── jogador.py            # Jogador (controla 1 Personagem)
    │   ├── personagem.py         # Personagem (possui Itens, enfrenta Inimigos)
    │   ├── dado.py               # Dado (faces = 6)
    │   ├── teste_habilidade.py   # TesteHabilidade (instancia 3 Dados)
    │   ├── missao.py             # Missao (hordas)
    │   ├── inimigo.py            # Inimigo
    │   └── item.py               # Item
    ├── persistencia/
    │   └── serializador.py       # Salvar/carregar em JSON
    └── ui/
        └── app.py                # Interface Tkinter
```

## Regras (3d6)
- **3** → Desastre (dobro de dano do contra-ataque)
- **4–6** → Falha
- **7–14** → Sucesso Normal
- **15–18** → Sucesso Crítico (dano multiplicado)

## Classes / Multiplayer
- Guerreiro — Força alta
- Pescador — Saúde alta
- Doutor — Inteligência alta (descontos na loja)

Cooperativo local com 1..3 Jogadores (conforme UML).

## Testes / Roteiro de avaliação
Ver `docs/roteiro_teste.md` e `docs/ficha_avaliacao.md`.

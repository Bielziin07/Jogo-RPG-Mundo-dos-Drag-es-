# Roteiro de Teste — Mundo dos Dragões (Nível 3)

## Preparação
1. Instalar Python 3.10+.
2. `pip install -r requirements.txt`
3. `python main.py`

## Cenários

### C1 — Fluxo básico
- Iniciar Novo Jogo com 1 jogador (Guerreiro).
- Verificar tela de Vila (Hub).
- Iniciar Missão "Emboscada na Floresta".
- Atacar até derrotar a horda.
- **Esperado:** ao vencer, ganha ouro e avança horda/missão.

### C2 — Sistema 3d6
- Rolar vários ataques e conferir se os resultados exibidos ficam entre 3 e 18.
- Confirmar as faixas: 3 (desastre), 4–6 (falha), 7–14 (sucesso), 15–18 (crítico).

### C3 — Atividades da vila
- Pescar 5 vezes. Observar mensagens de ganho / monstro marinho no desastre.
- Estudar 5 vezes. Observar aumento de inteligência / aranha gigante.

### C4 — Loja
- Comprar poção com Doutor e Guerreiro. Verificar desconto do Doutor.

### C5 — Cooperativo local (2–3 jogadores)
- Criar time com Guerreiro + Pescador + Doutor.
- Verificar alternância de turnos entre jogadores.
- Confirmar derrota apenas quando **todos** morrem.

### C6 — Persistência
- Salvar durante Hub.
- Fechar aplicativo.
- Reabrir → Carregar Jogo → conferir estado (PV, ouro, missão).

### C7 — Vitória / Derrota
- Vitória: concluir todas as 3 missões.
- Derrota: deixar PV do grupo chegar a zero.

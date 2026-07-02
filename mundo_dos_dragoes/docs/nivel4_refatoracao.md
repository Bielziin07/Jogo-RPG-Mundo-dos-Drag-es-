# Nível IV — Refatoração baseada em testes com usuários reais

Modelo para preencher após receber a ficha de avaliação do Nível III.

## 1. Resumo dos testes realizados (Nível III)
Descreva quem testou, quando, qual a versão do jogo, ambiente utilizado.

## 2. Relação de sugestões, críticas e problemas
| # | Origem (grupo) | Categoria | Descrição |
|---|---|---|---|
| 1 |   | UX/Bug/Regra |   |

## 3. Análise crítica e decisões
Utilizar o formato:

**Sugestão recebida:** "..."
**Decisão:** Aceita / Parcialmente aceita / Rejeitada / Problema corrigido / Problema não corrigido
**Justificativa:** (técnica)
**Alteração realizada:** (o que mudou no código)
**Evidência:** (screenshot / commit / trecho de código)

### Exemplo
**Sugestão:** "A tela de combate mostra informações demais."
**Decisão:** Aceita.
**Justificativa:** Usuários se perderam ao localizar PV e resultado da rolagem.
**Alteração:** Reorganização de `src/ui/app.py::_tela_combate` destacando PV do grupo e resultado do teste.
**Evidência:** commit `abcd1234`, screenshot `docs/img/combate_v2.png`.

## 4. Lista final de alterações implementadas
- [ ] ...

## 5. Evidências
Capturas, vídeos, diagramas atualizados, histórico de commits.

## 6. UML atualizada
Se houve mudança estrutural, atualizar `docs/uml/MdD.drawio`.

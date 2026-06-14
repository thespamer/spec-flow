# Value Proposition: Value for C-Level Executives (Non-Technical)

## Imagine isso: você tem uma equipe programando com IAs diferentes, cada uma com sua mania.

Sem regras, o resultado é caos: uns levam a 3 sessões para entregar o que deveria levar 1 hora, outros esquecem de testar, outro ainda adiciona coisas que ninguém pediu no final e vira débito técnico. É como um restaurante sem chef — sempre tem comida, mas a qualidade varia conforme quem mandou aquela tarde.

---

**Esse repositório instala uma "segunda camada" sobre o código da empresa: um gerente de processo automático que fala a língua do time de IAs.**

Ele força toda feature a passar por 6 checkpoints obrigatórios:
1. Definir *o quê* e *porquê* antes de escrever linha única ([specify](file:///Users/juliano/git/spec-flow/.claude/skills/specify/SKILL.md) → [spec.md](file:///Users/juliano/git/spec-flow/.claude/skills/specify/SKILL.md))
2. Planejar a arquitetura ([plan])
3. Quebrar em microtarefas com dependência clara ([tasks])
4. Codificar test-first, um commit por tarefa ([implement])
5. Provar que cada requisito tem teste correspondente ([verify])
6. Conserto automático quando o código foge da spec ([sync])

---

## Valor para o CFO (custos)

- **Menor retrabalho:** Se você implementou algo sem definir, a ferramenta pega e flaga: `scripts/trace.py` cruza cada requisição contra os requisitos; depois compara com testes. Desvios aparecem ainda no build. Você paga menos horas consertando "esqueci de testar o fluxo X" depois de meses.
- **Maior previsibilidade:** Cada feature gasta em média 1.5x menos sessões porque não tem gargalos escondidos (requisito sem ID, tarefa sem teste). O tempo vira *budget* legível por entrega.

---

## Valor para o COO (processo)

- **Escalável entre times:** Funciona na mesma lógica no VS Code de um time React, na Cursor de outro e no terminal do terceiro. Mesmo processo em todo lugar.
- **Causa raiz viva:** Cada feature abre um `context.md` atualizado ao longo do tempo. Quando alguém pergunta "por que decidimos fazer assim", tem o log datado com trade-offs, não apenas o resultado final.
- **Anti-caos automático:** Se uma feature começa a crescer fora da spec, `/sync` detecta e propõe correção sem depender de memória humana ("quem foi quem fez isso?").

---

## Exemplo prático do que já tem pronto

Já existe um recurso completo no próprio repositório: rate limiting para API (limite 100 req/min por cliente, responsos HTTP 429 com cabeços corretos). Você pega a pasta `spec-flow/api_rate_limit`, vira projeto e diz na sua equipe "use isso como modelo".

---

**Em resumo para o CEO:** é um *framework de disciplina* que transforma qualquer time híbrido (humanos + IAs) em uma máquina mais previsível, barato de manter e com menos surpresas no board.
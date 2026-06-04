# AN NIGHTMARE

**THE OX** é um jogo de terror psicológico em primeira pessoa desenvolvido em Python utilizando a técnica de *Raycasting*. O jogador é submetido a um experimento científico que deu terrivelmente errado, prendendo-o em uma dimensão de pesadelo onde o tempo é sua única moeda de sobrevivência.

## 📖 História

Você foi recrutado para participar de um experimento clínico envolvendo uma nova pílula experimental. A promessa era simples: uma noite de sono perfeita e um despertar revigorante. No entanto, algo deu errado durante o processo de sedação. 

Ao invés do descanso, sua consciência foi fragmentada e enviada para o **OX**, um labirinto finito gerado pelo seu próprio subconsciente. Agora, você está preso em um ciclo de pesadelos onde a realidade se distorce e o relógio trabalha contra sua existência.

## 🎯 Objetivo

O objetivo principal é escapar de cada nível antes que o tempo se esgote.

*   **Coleta de Arquivos:** Você deve encontrar e coletar os "arquivos" (files) espalhados pelo mapa. Cada arquivo coletado descriptografa partes da sua memória e concede **tempo extra** ao seu cronômetro de vida.
*   **Sobrevivência:** Gerencie sua vida e defesa enquanto navega por corredores estreitos.
*   **O Limbo:** Se o tempo chegar a zero antes de você completar a coleta, você não morre imediatamente; você é banido para o **Nível 8 (O Vazio)**, uma arena onde a entidade definitiva o caçará.

## 👤 Criaturas (Entidades)

O experimento manifestou três tipos de entidades baseadas em seus medos primordiais:

### 1. Stalker (O Perseguidor)
*   **Comportamento:** Uma entidade agressiva que se teleporta aleatoriamente pelo labirinto.
*   **Perigo:** Ele drena sua sanidade e vida instantaneamente se você mantiver contato visual direto com ele. 
*   **Estratégia:** Se você o vir, desvie o olhar imediatamente.

### 2. Looker (O Observador)
*   **Comportamento:** Uma criatura paralisante. Quando você entra no campo de visão dela, ela exerce uma força gravitacional sobre sua consciência.
*   **Perigo:** Ela **trava sua visão**, forçando você a encará-la. Enquanto estiver sob o efeito do Looker, você fica vulnerável e incapaz de navegar livremente.
*   **Estratégia:** Tente antecipar sua posição e evite ser pego de surpresa em corredores longos.

### 3. Timer (A Entidade do Tempo)
*   **Comportamento:** A manifestação física do fim. Ele aparece no Nível 7 ou quando o tempo do jogador se esgota.
*   **Perigo:** Diferente dos outros, ele não se teleporta; ele flutua implacavelmente em sua direção. Sua presença causa **tremores violentos** na realidade (tela).
*   **Estratégia:** É inevitável. Se ele te tocar, o experimento termina permanentemente.

## 🎮 Controles

*   **W, A, S, D:** Movimentação
*   **Mouse:** Olhar/Rotacionar
*   **Espaço:** Pular
*   **Shift:** Correr
*   **ESC:** Pausar o pesadelo

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Biblioteca Gráfica:** Pygame (SDL)
*   **Técnica:** Raycasting (Motor pseudo-3D inspirado em Wolfenstein 3D)
*   **Otimização:** Sistema de Cache de Texturas e Tabelas Trigonométricas pré-calculadas.

---
*Desenvolvido por Heitor Pessoa.*

# Backlog do projeto

Controle compartilhado das implementações, validações e entregas do Citizen Assist AI. Este arquivo é versionado, **permanece na entrega acadêmica e não deve entrar no `.gitignore`**. As tarefas concluídas permanecem como histórico, com evidências.

## Ponto de partida — 12/11/2026

A etapa inicial conduzida por Danilo Fernandes disponibilizou o protótipo e sua documentação. Este registro organiza o trabalho futuro; não atribui autoria individual retroativa a cada arquivo.

| Disponível | Evidência e limite |
|---|---|
| Assistente textual em Python, três estratégias de busca, navegação e condições | [Programa](../src/sistema.py) e [arquitetura](projeto.md); a busca ainda apresenta o erro V15 |
| Base com 23 registros em 5 temas e sinônimos editáveis | [Base](../data/base.json); revisão humana integral das orientações ainda pendente |
| Avaliação com 40 perguntas de teste, 15 de validação e 12 verificações de robustez | [Resultados](resultados_testes.md); híbrida: 39/40 e 11/15, robustez: 12/12; não comprova usabilidade nem validade jurídica |
| Dois modelos de prompt, gerador e validador estrutural | [Prompts](prompts.md); comparação experimental pendente e sem integração com IA generativa |
| Proposta, relatório em Markdown e declaração de uso de IA | [Proposta](projeto.md), [relatório](relatorio.md) e [uso de IA](uso_ia.md); PDF, vídeo e submissão ainda pendentes |

## Como acompanhar

1. Confirme o aceite da frente e escolha uma tarefa pelo identificador.
2. Atualize o status: **A fazer**, **Em andamento**, **Bloqueado** ou **Concluído**. Em bloqueios, registre o motivo e a dependência.
3. Trabalhe em uma branch própria e abra um PR citando a tarefa, as mudanças e a validação realizada.
4. Marque os passos executados com `[x]`. Peça revisão a outro integrante; conclua a tarefa após integração e conferência dos critérios.
5. Preencha a evidência com link do PR/commit e do resultado, quando aplicável. Não marque uma atividade como executada apenas porque existe um formulário ou código para ela.

Este é o controle oficial de tarefas da equipe. Outros documentos apresentam os resultados e podem apontar para cá. Registre evidências sem dados pessoais dos participantes, credenciais ou cópias dos materiais privados do curso.

## Frentes e aceite

As responsabilidades abaixo são propostas e dependem de aceite dos integrantes. A etapa inicial de Danilo é o ponto de partida; as pendências são distribuídas nas três frentes.

- [ ] Alexandre Niewelt aceita a frente **Base e busca**.
- [ ] Renato Nascimento aceita a frente **Validação e interação**.
- [ ] Renato Valle aceita a frente **Documentação e entrega**.

## Base e busca — Alexandre Niewelt

### BAS-01 — Revisar fontes e orientações

**Responsável proposto:** Alexandre Niewelt · **Status:** A fazer

- [ ] Conferir os 23 registros contra as fontes oficiais e registrar, por identificador, fonte consultada, data e conclusão no relatório técnico.
- [ ] Corrigir conteúdo, referência, linguagem e data quando necessário; sinalizar o que continuar sem confirmação.
- [ ] Alinhar a apresentação de “Verificado em” ao que foi efetivamente revisado, evitando transmitir uma verificação inexistente.

**Critério de conclusão:** todos os registros têm revisão rastreável; orientações sem respaldo foram corrigidas ou retiradas da resposta disponível. Datas cadastradas não são usadas como prova isolada de revisão.

**Evidência:** a preencher — registro de revisão no relatório e PR.

### BUS-01 — Corrigir associação entre academia e telecomunicações

**Responsável proposto:** Alexandre Niewelt · **Status:** A fazer

- [ ] Reproduzir V15 e identificar por que a busca seleciona DB20.
- [ ] Corrigir a seleção e acrescentar casos de regressão para academia e cancelamento de telecomunicações.
- [ ] Executar a avaliação completa e explicar diferenças nas classificações e nos indicadores.

**Critério de conclusão:** a pergunta sobre academia não recebe a orientação de telecomunicações; consultas legítimas de telecomunicações continuam atendidas e regressões são resolvidas ou explicitamente documentadas.

**Evidência:** a preencher — PR, perguntas de regressão e resultados.

**Nota de avaliação:** V15 já é conhecido e orienta esta correção. Não apresentar o desempenho posterior nesse mesmo caso como validação inédita; reservar novas perguntas que não tenham orientado os ajustes.

## Validação e interação — Renato Nascimento

### VAL-01 — Verificar fluxos, condições e privacidade

**Responsável proposto:** Renato Nascimento · **Status:** A fazer

- [ ] Testar menu, opção inexistente, entrada vazia, símbolos, ambiguidade, ausência de resposta e navegação por relacionados.
- [ ] Verificar condições com sim, não e não sei nas três situações disponíveis, incluindo respostas inválidas.
- [ ] Verificar mascaramento com CPF, telefone, e-mail e cartão fictícios, registrando os limites observados.
- [ ] Conferir BUS-01 e os resultados da avaliação após as mudanças; registrar falhas e repetir os cenários corrigidos.

**Critério de conclusão:** cenários têm esperado, obtido e resultado registrados; falhas remanescentes estão identificadas, sem confundir cobertura parcial com garantia integral.

**Evidência:** a preencher — PR e registro dos cenários no relatório técnico.

### UX-01 — Avaliar usabilidade e acessibilidade

**Responsável proposto:** Renato Nascimento · **Status:** A fazer

- [ ] Realizar teste com pelo menos uma pessoa e preencher o formulário de usabilidade do relatório, sem identificar o participante.
- [ ] Avaliar navegação por teclado e leitura da interface com leitor de tela, registrando ferramenta e ambiente.
- [ ] Registrar dificuldades, pelo menos duas melhorias ou limitações e verificar novamente qualquer ajuste realizado.

**Critério de conclusão:** há observação real das tarefas, evidências anonimizadas e limites de acessibilidade explícitos; um teste isolado não é apresentado como certificação.

**Evidência:** a preencher — seção de usabilidade do relatório e PR.

### IA-01 — Comparar experimentalmente os prompts

**Responsável proposto:** Renato Nascimento · **Status:** A fazer

- [ ] Executar o protocolo de cinco perguntas dos modelos A e B em conversas novas, registrando modelo, data e condições de execução.
- [ ] Registrar as respostas e preencher a comparação em [prompts.md](prompts.md), conferindo fontes e recusas.
- [ ] Atualizar o uso de IA e descrever os limites do validador, que não comprova fidelidade semântica.

**Critério de conclusão:** comparação sustentada por execuções reais, com resultados inspecionáveis; expectativas e observações estão diferenciadas.

**Evidência:** a preencher — respostas, tabela de comparação e PR.

## Documentação e entrega — Renato Valle

### DOC-01 — Consolidar documentação e relatório PDF

**Responsável proposto:** Renato Valle · **Status:** A fazer

- [ ] Preparar a estrutura do relatório e conferir requisitos, arquitetura e referências acadêmicas pertinentes.
- [ ] Incorporar os resultados de BAS-01, BUS-01, VAL-01, UX-01 e IA-01, conferindo evidências e coerência com o README.
- [ ] Gerar `docs/relatorio.pdf` com 4 a 8 páginas e conferir legibilidade, links, conteúdo e número de páginas.

**Critério de conclusão:** PDF e documentação refletem a mesma versão do projeto e os resultados reais, com limitações e uso de IA declarados.

**Dependência:** a estrutura pode avançar imediatamente; a versão final depende dos resultados das outras frentes.

**Evidência:** a preencher — PR, PDF e registro da conferência.

### ENT-01 — Preparar vídeo e concluir a entrega

**Responsável proposto:** Renato Valle · **Status:** A fazer

- [ ] Preparar roteiro, gravar e revisar a demonstração da versão final, incluindo funcionamento e limitações.
- [ ] Publicar o vídeo como Não Listado após autorização aplicável e atualizar [link_video.txt](link_video.txt).
- [ ] Confirmar que o repositório está público; se estiver privado, obter autorização do responsável antes de mudar a visibilidade.
- [ ] Preparar o `.txt` contendo somente os links do repositório público e do vídeo, um por linha, e conferir acesso sem autenticação.
- [ ] Conferir o pacote final e registrar a confirmação de submissão no portal quando realizada pela equipe autorizada, sem expor dados pessoais.

**Critério de conclusão:** entregáveis acessíveis e coerentes com a versão demonstrada, com confirmação efetiva de submissão; preparar arquivos não equivale a entregar no portal.

**Dependência:** DOC-01 e versão final conferida pelas demais frentes.

**Evidência:** a preencher — PR, links finais e registro sanitizado da submissão.

## Conhecimentos de apoio e limites de escopo

Os [requisitos consolidados da GS](projeto.md) orientam a entrega. Os materiais das fases 05–07 apoiam as decisões, e fontes externas podem complementá-los. A consulta ao acervo não significa aplicar todos os seus conteúdos nem transplantar requisitos de outros projetos.

| Apoio acadêmico | Aplicação nas tarefas |
|---|---|
| Fase 05: arquivos e dados estruturados; prompts, cadeias e lógica | BAS-01, VAL-01 e IA-01: validar registros, conferir condições e comparar respostas estruturadas |
| Fase 06: complexidade, avaliação de desempenho e assistentes | BUS-01 e VAL-01: comparar buscas, tempos, erros e comportamento em perguntas novas |
| Fase 07: tratamento de exceções, integração e cidadania digital | VAL-01, UX-01 e DOC-01: tratar falhas, avaliar privacidade, inclusão e transparência |

Ao aprofundar uma associação no relatório, consultar o PDF individual correspondente e registrar fase, capítulo e páginas efetivamente conferidas. Guias de estudo são apoio derivado. Não anexar PDFs privados nem exigir acesso ao acervo local para entender as tarefas.

- **Requisitos da GS:** protótipo, base, fontes, comparação de prompts, testes e indicadores, usabilidade e entregáveis descritos na proposta.
- **Decisões de qualidade da equipe:** corrigir V15, ampliar verificação de fluxos e privacidade, avaliar com leitor de tela e usar revisão por PR.
- **Melhorias opcionais:** incluir power bank, ampliar cobertura ou integrar outros canais/modelos. Exigem tarefa e aceite próprios; não fazem parte desta rodada de organização.

Na entrega, manter este backlog e seus registros concluídos. Pendências ou melhorias futuras continuam visíveis com status honesto, sem serem marcadas como feitas para encerrar o documento.

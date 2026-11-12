# Proposta do projeto — Citizen Assist AI

## Desafio e recorte adotado

O case Citizen Assist AI, da Global Solution 2026.2 — CitizenTech, propõe construir um protótipo funcional que organize informações verificadas sobre serviços, documentos, direitos e orientações comunitárias, facilitando o acesso por meio de um assistente digital introdutório.

O projeto adota um recorte: **direitos do consumidor em situações cotidianas**, para pessoas de todas as idades sem formação jurídica. O objetivo é transformar a consulta em uma orientação utilizável no atendimento, com referência e indicação dos canais adequados.

Os requisitos abaixo foram consolidados do enunciado fornecido ao projeto. A [página oficial da atividade](https://on.fiap.com.br/mod/assign/view.php?id=684386) é a referência acadêmica; a [divulgação CitizenTech](https://experience.fiap.com.br/global-solution-citizen-tech) contextualiza o tema.

## Requisitos da atividade

### Funcionalidades e cuidados

- Receber uma pergunta em texto livre ou uma escolha de menu e buscar por pergunta ou assunto.
- Consultar uma base em JSON, TXT ou CSV, editável sem mudanças no código.
- Listar temas e exibir orientação, fonte e aviso de limitação.
- Informar quando não houver informação suficiente; tratar entrada vazia ou inválida, opção inexistente e dúvidas não previstas.
- Validar campos e tratar arquivo ausente ou vazio.
- Não solicitar dados pessoais desnecessários nem se apresentar como canal oficial do governo.

### Tecnologia, estruturas e prompts

- Usar Python, com entrada principal em `src/sistema.py`. A interface textual é suficiente; interface gráfica ou web é opcional.
- Usar listas e dicionários; ler a base com Python e explicar a estratégia de busca e o tratamento de múltiplas correspondências.
- Organizar temas em hierarquia ou grafo simples e permitir navegação entre pelo menos três assuntos relacionados.
- Documentar e comparar pelo menos dois modelos de prompt.
- APIs pagas, LangChain e n8n não são obrigatórios.

Os conteúdos acadêmicos associados incluem estruturas de dados, arquivos, prompts e cadeias, saídas estruturadas, lógica booleana e De Morgan, comparação de algoritmos e métricas. Essa relação de conteúdos não significa que todos sejam funcionalidades implementadas.

### Base mínima

São exigidos pelo menos **15 registros em 3 temas**, contendo identificador, tema, pergunta ou palavras-chave, orientação resumida, referência e data de verificação.

### Avaliação

- Pelo menos 12 perguntas, incluindo perguntas diretas, reformulações e consultas fora do tema.
- Pelo menos três situações-limite: entrada vazia, consulta ambígua e pergunta sem resposta confiável.
- Registro de resposta esperada, obtida, acerto ou erro e tempo por consulta, com taxa de acerto e tempo médio.
- Teste de usabilidade com pelo menos uma pessoa e identificação de pelo menos duas melhorias ou limitações.

### Entregáveis acadêmicos

| Artefato | Conteúdo requerido |
|---|---|
| `README.md` | Identificação da equipe e RMs; problema, público e temas; base, estruturas e busca; regras, prompts e limitações; testes e indicadores; execução, exemplos, cuidados, vídeo e conclusões |
| `src/sistema.py` | Programa principal, executado com `python src/sistema.py` |
| Base em `data/` | Pelo menos 15 orientações |
| `docs/relatorio.pdf` | Relatório de 4 a 8 páginas com problema, público, arquitetura, fontes, prompts, testes, indicadores, limitações e impacto social |
| `docs/link_video.txt` | Link do vídeo de apresentação |
| `docs/uso_ia.md` | Registro do uso de IA, quando aplicável |

A submissão na plataforma exige um único arquivo `.txt`, contendo somente dois links, um por linha: o repositório GitHub público da equipe e o vídeo no YouTube como Não Listado. A tabela descreve os entregáveis exigidos, sem afirmar que todos já foram produzidos.

## Escolhas de implementação

### Orientações e base de conhecimento

A implementação contém 23 registros em cinco temas: mercado e lojas; compras pela internet; bares, restaurantes e lazer; bancos, contas e telefone; viagens e transporte.

Cada resposta pode apresentar orientação resumida, frase pronta para o atendimento, passos, prazo, canais de reclamação, referência, data cadastrada de verificação e limitações. Esses campos adicionais são escolhas do projeto.

| Campo da base JSON | Uso |
|---|---|
| `identificador`, `tema` | Identificação e organização do registro |
| `pergunta_ou_palavras_chave` | Perguntas de exemplo e palavras-chave usadas na busca |
| `orientacao_resumida` | Texto principal da orientação |
| `referencia` | Norma e endereço da fonte |
| `data_de_verificacao` | Data declarada no cadastro, em formato AAAA-MM-DD |
| `frase_pronta`, `passos`, `prazo`, `onde_reclamar`, `limitacoes` | Orientação para agir e cuidados aplicáveis |
| `relacionados` | Ligações com outros assuntos |
| `condicoes` | Perguntas opcionais para verificar a aplicabilidade da orientação |

A leitura valida campos, datas, temas e identificadores. Registros inválidos são ignorados com aviso; arquivo ausente, vazio ou JSON inválido recebe tratamento de erro. Referências a assuntos inexistentes geram avisos. O sistema sinaliza registros com mais de 180 dias desde a data cadastrada; não consulta as fontes automaticamente.

### Fluxo e estruturas

```text
Texto ou menu
  -> mascaramento de padrões de dados pessoais
  -> normalização e busca
  -> resposta, esclarecimento ou aviso de informação insuficiente
  -> navegação por assuntos relacionados e verificação de condições
```

Os registros ficam em um dicionário por identificador; os temas formam uma hierarquia e os assuntos relacionados, um grafo não direcionado com conjuntos de adjacência. Listas e tuplas organizam o ranking; `Counter` apoia o cálculo do TF-IDF. Há busca em largura (BFS) para obter caminhos entre assuntos.

### Busca e decisão

O texto passa por conversão para minúsculas, remoção de acentos, substituição de sinônimos, descarte de palavras vazias e radical por prefixo de seis letras. As palavras de negação relevantes são mantidas. A lista de sinônimos também é editável em JSON.

Três estratégias são comparadas: palavras-chave e frases, TF-IDF com similaridade do cosseno e a média das duas, denominada híbrida e usada por padrão.

Entradas vazias, inválidas ou fora do tema recebem mensagens próprias. Notas abaixo do limiar geram aviso de informação insuficiente. Quando há múltiplas correspondências próximas ou palavras isoladas ambíguas, o sistema oferece até três opções. Nos demais casos, apresenta o registro com maior nota. Essa decisão pode selecionar um registro inadequado e não equivale a uma compreensão jurídica da pergunta.

### Condições e prompts

Arrependimento, meia-entrada e passagem interestadual para pessoa idosa possuem perguntas de condições, com respostas sim, não e não sei. As regras usam lógica de três valores e De Morgan para explicar condições não atendidas.

As respostas do programa são recuperadas da base, sem chamadas a modelos de linguagem. Dois prompts são documentados como estudo: A, direto; B, ancorado no registro, com saída JSON. A cadeia proposta é classificar, redigir e validar. O gerador de prompts e o validador estrutural existem, mas não executam essa integração. O validador confere JSON, estado, fonte e data; não comprova fidelidade semântica. Consulte as [estratégias de prompt](prompts.md).

## Evidências e limitações

O avaliador utiliza 40 perguntas de teste, 15 de validação e 12 verificações de robustez. Os [resultados detalhados](resultados_testes.md) incluem indicadores e erros por estratégia. Na híbrida, os acertos são 39/40 no teste e 11/15 na validação; o erro V15 associa academia a telecomunicações.

A cobertura se restringe à base. Vocabulário novo, radicalização por prefixos e regras locais são limitações. A revisão humana das fontes é necessária; as datas cadastradas não comprovam essa revisão. A comparação experimental dos prompts e o teste com usuário ainda não possuem resultados registrados. O [relatório técnico](relatorio.md) reúne a análise e o formulário de usabilidade.

O texto busca clareza e oferece navegação por códigos, sem emojis. O uso com leitores de tela ainda precisa ser avaliado. As consultas não são persistidas, e padrões reconhecidos de dados pessoais são mascarados, sem garantia de detectar todo dado sensível. O assistente é informativo e não substitui os canais oficiais.

## Impacto pretendido

A proposta busca facilitar o acesso à informação de consumo e aos canais de reclamação, com relação aos ODS 10 (redução das desigualdades) e 11 (cidades sustentáveis). ODS 16 é uma conexão complementar escolhida pelo projeto, pelo acesso à informação e à justiça. O impacto pretendido ainda depende de avaliação com usuários.

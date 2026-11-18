# Citizen Assist AI

**Global Solution 2026.2 · CitizenTech · FIAP — Ciência da Computação**

O desafio Citizen Assist AI propõe um assistente digital introdutório que facilite o acesso a informações sobre serviços, documentos, direitos e orientações comunitárias. Este projeto aplica o desafio aos **direitos do consumidor no dia a dia**, com um assistente textual em Python.

A pessoa descreve uma situação e recebe uma orientação da base, uma frase pronta para usar no atendimento, os próximos passos, os canais de reclamação e a referência consultada. O programa funciona localmente, sem dependências externas ou chamadas a IA generativa.

## Integrantes

| Nome | GitHub | Matrícula |
|---|---|---|
| Alexandre Niewelt | [@QTAlox](https://github.com/QTAlox) | RM 570614 |
| Danilo Fernandes | [@dandgsf](https://github.com/dandgsf) | RM 570057 |
| Renato Nascimento | [@renascience](https://github.com/renascience) | RM 570266 |
| Renato Valle | [@renatolvalle](https://github.com/renatolvalle) | RM 572352 |

## Problema e público

Informações sobre consumo estão espalhadas em leis e páginas institucionais, muitas vezes em linguagem técnica. O projeto busca facilitar a consulta por pessoas sem formação jurídica, diante de problemas como cobrança indevida, compras pela internet ou atraso de voo.

O público inclui pessoas de todas as idades que precisam entender uma situação de consumo e encontrar os canais adequados para resolvê-la.

## Temas atendidos

A base contém **23 situações em 5 temas**:

| Tema | Exemplos de situações |
|---|---|
| Mercado e lojas | Preço divergente, produto com defeito, venda casada e atendimento prioritário |
| Compras pela internet | Arrependimento, entrega atrasada e produto não solicitado |
| Bares, restaurantes e lazer | Taxa de serviço, consumação mínima, perda de comanda e meia-entrada |
| Bancos, contas e telefone | Golpe no Pix, cobrança indevida, corte de luz e cancelamento de telecomunicações |
| Viagens e transporte | Atraso de voo e passagem interestadual para pessoa idosa |

## Como funciona

1. A entrada passa pela detecção de padrões de dados pessoais e pela normalização do texto.
2. A busca compara a pergunta com os registros por palavras-chave, TF-IDF ou pela média das duas estratégias, usada por padrão, filtrando candidatos incompatíveis com setores regulados antes de montar respostas ou opções de ambiguidade.
3. O sistema apresenta uma resposta, pede esclarecimento em casos ambíguos ou informa que não encontrou informação suficiente.
4. A resposta inclui a fonte, a data cadastrada de verificação e o aviso de limitação. É possível navegar por assuntos relacionados e verificar condições em situações específicas.

A base JSON pode ser editada sem alterar o código. A arquitetura usa dicionários para os registros, uma hierarquia de temas e um grafo de assuntos relacionados. O detalhamento está na [proposta do projeto](docs/projeto.md).

## Como executar

Requer **Python 3.10 ou superior**, apenas com a biblioteca padrão.

```bash
git clone https://github.com/dandgsf/gs-citizen-assist-ai.git
cd gs-citizen-assist-ai
python src/sistema.py
```

Outras formas de uso:

```bash
python src/sistema.py --pergunta "perdi a comanda"
python src/sistema.py --explicar
python src/sistema.py --estrategia tfidf
python src/sistema.py --simples
python src/avaliar.py
```

No menu, use `1` para temas, `2` para informações, `3` para alternar a explicação da busca, `m` para voltar ao menu e `0` para sair. Após uma resposta, `r1`, `r2` e seguintes abrem assuntos relacionados; `v` aparece quando há condições a verificar.

## Exemplos de consultas

| Pergunta | Comportamento do sistema |
|---|---|
| "o garçom botou os dez por cento sem me perguntar" | Apresenta a orientação cadastrada sobre taxa de serviço, com frase pronta e referência |
| "cobrança" | Solicita a escolha entre situações relacionadas |
| "fui demitido, quanto recebo de FGTS?" | Informa que o assunto está fora do escopo |
| "a loja não quis me dar nota fiscal" | Informa que não encontrou resposta confiável na base |

## Prompts e regras de resposta

As respostas exibidas são recuperadas da base. O projeto documenta dois modelos de prompt: um direto e outro ancorado em um registro, com saída JSON e validação de fonte e data. A integração com um modelo de linguagem é uma proposta; o script apenas gera os prompts.

A [documentação de prompts](docs/prompts.md) contém a comparação conceitual e o protocolo experimental. A validação estrutural de uma saída não comprova a fidelidade de seu conteúdo à fonte.

## Testes e resultados

O avaliador compara as três estratégias com **60 perguntas de teste e regressão** (`data/perguntas_teste.json`), **17 perguntas reservadas de validação** e **2 regressões conhecidas (`V15` e `V17`)** (`data/perguntas_validacao.json`), além de **14 verificações de robustez e gravidade**, incluindo entradas vazias, ambiguidade, ausência de resposta, leitura de arquivos, validação de saída estruturada e classificação de candidatos proibidos.

| Estratégia | Acerto (teste + regressão) | Acerto (validação inédita) | Erros perigosos (corpus avaliado) |
|---|---|---|---|
| Palavras-chave | 59/60 (98,3%) | 14/17 (82,4%) | 0 |
| TF-IDF | 58/60 (96,7%) | 12/17 (70,6%) | 0 |
| Híbrida (padrão) | 59/60 (98,3%) | 14/17 (82,4%) | 0 |

As três estratégias se abstêm para a academia em `V15` e recuperam a orientação de cancelamento de internet em `V17`. A contagem de `0` erros perigosos refere-se ao corpus avaliado na estratégia indicada e não garante ausência de falhas fora dele.

Execute `python -m unittest discover -s tests -v` para conferir as respostas e os atalhos de cancelamento na CLI, incluindo a confirmação da contratação. O [relatório de testes](docs/resultados_testes.md) registra resposta esperada, obtida, candidatos exibidos, acerto ou erro, tempos de consulta e robustez. O teste com usuário e a comparação experimental de prompts ainda não têm resultados registrados.

## Limitações e cuidados

- A cobertura se restringe às situações cadastradas; vocabulário novo não mapeado em sinônimos, radicalização por prefixos e regras locais podem levar o sistema a abster-se (como ocorre nos erros seguros da validação inédita) ou falhar em formulações não previstas fora do corpus.
- Os 23 registros foram revisados manualmente em 16/11/2026 contra as normas citadas, mas não há conferência automática das fontes; a revisão humana periódica permanece necessária, apoiada pelo aviso de registros com mais de 180 dias.
- O assistente é informativo, não é canal oficial e não substitui Procon, Defensoria ou advogado.
- As consultas não são persistidas. A detecção de CPF, telefone, e-mail e cartão cobre padrões específicos, sem garantir a remoção de todo dado sensível. Evite dados pessoais também nos argumentos do terminal.
- A interface usa linguagem simples, texto sem emojis e navegação por códigos. A acessibilidade com leitores de tela ainda precisa ser avaliada.

## Documentação e vídeo

- [Backlog da equipe: tarefas, responsáveis e evidências](docs/BACKLOG.md). É versionado, permanece na entrega acadêmica e não deve ser incluído no `.gitignore`.
- [Proposta, arquitetura e requisitos acadêmicos](docs/projeto.md)
- [Relatório técnico](docs/relatorio.md)
- [Estratégias de prompt](docs/prompts.md)
- [Resultados dos testes](docs/resultados_testes.md)
- [Uso de IA](docs/uso_ia.md)
- [Vídeo de apresentação](docs/link_video.txt): link ainda não informado.

## Conclusão

O protótipo demonstra a organização e recuperação de orientações de consumo em uma base editável. A avaliação evidencia a diferença entre perguntas de calibração, regressões setoriais e perguntas inéditas; ampliar o vocabulário de sinônimos e a cobertura de setores continuam como melhorias prioritárias. A proposta se relaciona aos ODS 10 e 11, com conexão complementar ao ODS 16 pelo acesso à informação e aos canais de reclamação.

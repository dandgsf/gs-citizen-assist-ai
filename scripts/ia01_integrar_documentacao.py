#!/usr/bin/env python3
"""Integra a IA-01 ao repositório, sem modificar evidências originais.

Requer data/ia01/* contendo as 10 respostas e a avaliação.
Alterações: docs/prompts.md (tabela e nota), docs/uso_ia.md (seção marcada),
docs/BACKLOG.md (bloco IA-01, sem alterar outras tarefas).
Pode ser executado mais de uma vez sem duplicar conteúdo.
"""
from pathlib import Path
import csv, json, re, hashlib

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data/ia01'
DOCS=ROOT/'docs'
START='<!-- IA01_PR2026_INICIO -->'
END='<!-- IA01_PR2026_FIM -->'
WORD_RE=re.compile(r"\b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b",re.UNICODE)
TABLE_HEAD='| # | Modelo | Fonte verificável | Inventou algo | Recusou quando devia | Formato OK | Palavras |'
VALUES={'sim':'Sim','nao':'Não','n/a':'n/a','pendente':'Pendente'}


def stop(message): raise SystemExit('ERRO: '+message)

def read(path):
    if not path.is_file(): stop('Arquivo ausente: '+str(path.relative_to(ROOT)))
    return path.read_text(encoding='utf-8')

def replace_marked(text,body):
    block=START+'\n'+body.strip()+'\n'+END
    if START in text and END in text:
        a=text.index(START);b=text.index(END,a)+len(END)
        return text[:a]+block+text[b:]
    if START in text or END in text: stop('Marcador de seção parcial encontrado; nada foi alterado')
    return text.rstrip()+'\n\n'+block+'\n'

def main():
    # Validar tudo ANTES de escrever um único documento
    m=json.loads(read(DATA/'manifesto.json'))
    with (DATA/'avaliacao_manual.csv').open('r',encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    ratings={(r['teste'],r['modelo']):r for r in rows}
    if len(rows)!=10 or len(ratings)!=10: stop('CSV precisa de exatamente dez casos únicos')
    out=[]
    for i in range(1,6):
        for model in 'AB':
            test=f'IA-T{i:02d}';key=(test,model)
            if key not in ratings: stop('Ausente no CSV: '+str(key))
            row=ratings[key]
            for field in ('fonte_verificavel','inventou_algo','recusou_quando_devia'):
                if row[field] not in VALUES: stop('Avaliação inválida: '+str(key)+' '+field)
            text=read(DATA/'respostas'/f'{test}_{model}.txt')
            if not text.strip():stop('Resposta vazia '+str(key))
            if model=='B':
                try: parsed=json.loads(text)
                except json.JSONDecodeError: stop('JSON inválido '+str(key))
                fields=('status','resposta_simples','frase_pronta','fonte','data_verificacao','aviso')
                if not isinstance(parsed,dict) or not set(fields).issubset(parsed):stop('Campos ausentes '+str(key))
                count=len(WORD_RE.findall(parsed['resposta_simples']))
                fmt='Sim' if (parsed['status'] in ('ok','sem_informacao') and all(isinstance(parsed[f],str) for f in fields if f!='status') and count<=80) else 'Não'
            else:
                count=len(WORD_RE.findall(text));fmt='n/a'
            out.append('| '+' | '.join([str(i),model,VALUES[row['fonte_verificavel']],VALUES[row['inventou_algo']],VALUES[row['recusou_quando_devia']],fmt,str(count)])+' |')
    source=read(DOCS/'prompts.md')
    lines=source.splitlines()
    hits=[i for i,line in enumerate(lines) if line.strip()==TABLE_HEAD]
    if len(hits)!=1:stop('Cabeçalho de tabela esperado não localizado unicamente em docs/prompts.md')
    i=hits[0];j=i+1
    while j<len(lines) and lines[j].lstrip().startswith('|'):j+=1
    lines[i:j]=[TABLE_HEAD,'|---|---|---|---|---|---|---|',*out]
    note='> **Execução IA-01 (19/11/2026):** 10 respostas originais registradas, comparação preenchida. T01_B/T03_B tiveram `data_verificacao` ajustada manualmente nos prompts individuais; T02_B devolveu data diferente daquela fornecida. Consulte [resultado e auditoria](ia01_resultados.md) e [uso de IA](uso_ia.md). JSON válido não significa aceitação pelo validador nem fidelidade jurídica.'
    match=[i for i,l in enumerate(lines) if l.startswith(('> **Pendente:**','> **Execução experimental:**','> **Execução parcialmente registrada:**','> **Experimento IA-01','> **Execução IA-01'))]
    if len(match)>1:stop('Múltiplas notas de execução na tabela; revisar manualmente')
    if match:lines[match[0]]=note
    else:lines.extend(['',note])
    prompts='\n'.join(lines)+'\n'
    prompts=prompts.replace('Essas diferenças descrevem os prompts e hipóteses de projeto, sem resultados experimentais.', 'A tabela de expectativas anterior descreve hipóteses de projeto; os resultados experimentais reais estão registrados mais abaixo.')
    uso=read(DOCS/'uso_ia.md')
    uso=uso.replace('A pesquisa inicial não substitui a revisão humana contra as fontes oficiais. As datas cadastradas na base não comprovam que essa revisão foi concluída.', 'A pesquisa inicial não substitui a revisão humana contra as fontes oficiais. As datas cadastradas na base não comprovam que essa revisão foi concluída.')
    uso=uso.replace('A equipe é responsável por revisar fontes e linguagem, avaliar o sistema com usuários e conferir os resultados dos testes. O teste de usabilidade, a revisão humana integral das fontes e a comparação experimental dos prompts ainda não têm conclusão registrada.', 'A equipe é responsável por revisar fontes e linguagem, avaliar o sistema com usuários e conferir os resultados dos testes. A revisão humana integral das fontes permanece necessária; o experimento IA-01 está registrado abaixo, com ressalvas. A situação do teste de usabilidade é documentada separadamente.')
    body=f"""## IA-01 — Comparação experimental real de prompts

- **Condições informadas:** 19/11/2026; ChatGPT; modelo {m.get('modelo_ia','não informado')}; 10 conversas novas e independentes declaradas. O ZIP comprova os textos capturados, não comprova externamente a configuração nem o isolamento das conversas.
- **Procedimento:** cinco perguntas, prompt A (livre) e prompt B (ancorado no registro), com dez saídas originais preservadas em `data/ia01/respostas/`.
- **Observações:** B produziu 5/5 JSONs válidos, 5/5 textos `resposta_simples` de até 80 palavras e 2/2 abstenções esperadas sem registro. A respondeu a 5/5 perguntas, inclusive duas sem cobertura na base. O operador declarou editar manualmente as datas em T01_B/T03_B; em T02_B a IA mudou a data recebida.
- **Limite de validação:** `validar_saida_ia()` verifica JSON, `status`, `fonte` e `data_verificacao`; **não** confere adequação do registro recuperado, fidelidade semântica, veracidade jurídica, completude de todos os campos ou o limite de palavras. `sem_informacao` é rejeitado para uso da saída gerada, acionando o retorno ao texto da base (fallback).
- **Integridade:** data do teste e `data_verificacao` da fonte são conceitos distintos. A edição manual de prompts é declarada, e a atualização da base só pode ser reivindicada com conferência efetiva das normas. A saída T02_B falha ao copiar a data do prompt individual. Nenhuma evidência foi corrigida retroativamente.
- **Evidências:** [comparação, análise e fontes](ia01_resultados.md) · [protocolo e tabela preenchida](prompts.md).
"""
    uso=replace_marked(uso,body)
    back=read(DOCS/'BACKLOG.md')
    start=back.find('### IA-01 — Comparar experimentalmente os prompts')
    if start<0:stop('Seção IA-01 ausente no backlog')
    end=back.find('\n## ',start+4)
    if end<0:end=len(back)
    block=back[start:end]
    block=re.sub(r'\*\*Status:\*\*[^\n]+','**Status:** Experimento e documentação registrados; preparado para PR com ressalvas',block,count=1)
    patterns=[
      r'- \[[ x]\] Executar o protocolo de cinco perguntas dos modelos A e B em conversas novas, registrando modelo, data e condições de execução\.',
      r'- \[[ x]\] Registrar as respostas e preencher a comparação em \[prompts\.md\]\(prompts\.md\), conferindo fontes e recusas\.',
      r'- \[[ x]\] Atualizar o uso de IA e descrever os limites do validador, que não comprova fidelidade semântica\.'
    ]
    for pat in patterns:
        block,n=re.subn(pat,lambda m:m.group(0).replace('- [ ]','- [x]'),block,count=1)
        if n!=1:stop('Checkbox do backlog inesperado; nenhuma alteração aplicada')
    block=re.sub(r'\*\*Evidência:\*\*[^\n]+',
      '**Evidência:** [respostas e prompts](../data/ia01/) · [comparação em prompts.md](prompts.md) · [relatório IA-01](ia01_resultados.md) · [uso de IA](uso_ia.md) · PR de IA-01 (link a acrescentar após abertura). **Ressalva:** duas datas editadas manualmente; uma divergência de data gerada em T02_B.',block,count=1)
    back=back[:start]+block+back[end:]
    # gravação de três documentos somente após verificações
    (DOCS/'prompts.md').write_text(prompts,encoding='utf-8')
    (DOCS/'uso_ia.md').write_text(uso,encoding='utf-8')
    (DOCS/'BACKLOG.md').write_text(back,encoding='utf-8')
    print('OK: docs/prompts.md — tabela IA-01 atualizada (10 linhas)')
    print('OK: docs/uso_ia.md — seção IA-01 adicionada/atualizada')
    print('OK: docs/BACKLOG.md — 3 critérios documentados, ressalvas visíveis')
    print('As dez respostas e prompts originais foram preservados.')

if __name__=='__main__': main()

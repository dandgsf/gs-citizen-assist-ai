# Como aplicar — pacote final IA-01

Este ZIP inclui os arquivos de evidência enviados (`ia01(1).zip`) e novos arquivos de auditoria. **Não substitui `src/prompts.py`, `data/base.json` nem o sistema principal.**

1. Confirme `git status -sb` na branch `test/ia-01-comparacao-prompts`.
2. Na raiz do repositório, extraia o ZIP: `unzip -o ~/Downloads/IA01_PR_final.zip -d .`.
3. Execute `python3 scripts/ia01_integrar_documentacao.py` para atualizar **somente** as seções IA-01 de `docs/prompts.md`, `docs/uso_ia.md` e `docs/BACKLOG.md`.
4. Revise `docs/ia01_resultados.md`, `git diff --check`, `git status -sb`, `git diff --stat`.
5. Confira todos os arquivos novos de `data/ia01` — se estiverem ignorados no `.gitignore`, use `git check-ignore -v data/ia01/manifesto.json` e adicione explicitamente com `git add -f -- data/ia01/...` apenas se necessário.
6. Adicione os caminhos aprovados, crie commit, faça push e abra Draft PR para `main`.
7. Copie o texto do arquivo separado `IA01_descricao_PR.md` para o corpo do PR.

As 10 respostas foram mantidas exatamente como recebidas. A data alterada manualmente nos prompts T01_B/T03_B e a falha de data em T02_B são descritas sem correção retroativa.

# Price Radar

Monitora precos de perifericos e eletronicos. O GitHub confere os precos a cada 3 h e manda alerta no celular quando cai.

## Ligar (uma vez)
1. Repo **publico** `price-radar`.
2. Settings > Secrets > Actions: crie `NTFY_TOPIC` com um nome longo e aleatorio (ex: `radar-k3j9x2m8q7`).
3. Actions > "Gerar APK" > Run workflow. Depois baixe `app-debug.apk` em Releases, no celular, e instale.
4. No celular, instale o app **ntfy** e assine o mesmo topico. E ele que toca o alerta.

## Usar
- Adicionar item: botao "+ Adicionar item" no app (edita `docs/items.json`, campos `name`, `url`, `target` opcional).
- Buscar outro produto: caixa de busca no app (Zoom, KaBuM, Pichau, Amazon, Mercado Livre).
- Testar agora: Actions > "Conferir precos" > Run workflow.

Limite: lojas podem bloquear o robo do GitHub. O log do Actions mostra `erro` ou `sem preco` nesses casos.

## Catálogo multi-loja
Na seção "Catálogo" do app: digite um produto (ou toque numa categoria), filtre por marca, loja e preço, e toque em **Rastrear** para adicionar ao monitor.
Os resultados vêm do Zoom (agrega KaBuM, Amazon e outras lojas). O botão Rastrear precisa de um token fine-grained do GitHub (só o repo price-radar, Contents: read/write), colado em "Configurar botão Rastrear".

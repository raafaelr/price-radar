# Price Radar

Monitora precos de perifericos e eletronicos. O GitHub confere os precos a cada 3 h e manda alerta no celular quando cai.

## Ligar (uma vez)
1. Repo **publico** `price-radar`. Settings > Pages > Source: `main`, pasta `/docs`.
2. Settings > Secrets > Actions: crie `NTFY_TOPIC` com um nome longo e aleatorio (ex: `radar-k3j9x2m8q7`).
3. Actions > "Gerar APK" > Run workflow. Depois baixe `app-debug.apk` em Releases, no celular, e instale.
4. No celular, instale o app **ntfy** e assine o mesmo topico. E ele que toca o alerta.

## Usar
- Adicionar item: botao "+ Adicionar item" no app (edita `docs/items.json`, campos `name`, `url`, `target` opcional).
- Buscar outro produto: caixa de busca no app (Zoom, KaBuM, Pichau, Amazon, Mercado Livre).
- Testar agora: Actions > "Conferir precos" > Run workflow.

Limite: lojas podem bloquear o robo do GitHub. O log do Actions mostra `erro` ou `sem preco` nesses casos.

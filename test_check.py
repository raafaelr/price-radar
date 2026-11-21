from check import alert, parse_price

assert parse_price('<span class="a-offscreen">R$ 1.599,90</span>') == 1599.90
assert parse_price('{"offers":{"priceCurrency":"BRL","price":739.99}}') == 739.99
assert parse_price('<meta property="product:price:amount" content="829.99">') == 829.99
assert parse_price('<b>por R$ 599,00 no cartao</b>') == 599.00
assert parse_price("sem preco aqui") is None

assert alert([], 500, None) is None                      # primeira leitura nao avisa
assert alert([[0, 700]], 650, None) == "caiu de R$ 700,00 para R$ 650,00"
assert alert([[0, 700]], 695, None) is None              # queda menor que 1% e ignorada
assert alert([[0, 700]], 590, 600).endswith("meta de R$ 600,00")
assert alert([[0, 590]], 580, 600).startswith("caiu")    # ja estava abaixo da meta: so queda normal
print("ok")

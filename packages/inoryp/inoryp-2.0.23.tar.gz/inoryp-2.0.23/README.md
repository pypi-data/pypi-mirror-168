## Instalar & Importar
* import inoryp
* from inoryp import classico

## Como usar a funcao classica?
* inoryp.classico(0) # IP
* inoryp.classico(1) # Codigo (Status code)
* inoryp.classico(2) # Dicionario (Dictionary/JSON)

## Como usar o classico com Proxies?
* inoryp.classico(0, "localhost:9150", "socks5") # IP (using proxy)
* inoryp.classico(0, "localhost:9150", "socks5") # Codigo (using proxy)
* inoryp.classico(0, "localhost:9150", "socks5") # Dicionario (using proxy)

## Como usar as novas fucoes?
* inoryp.getIP() # IP
* inoryp.getCode() # Codigo (Status code)
* inoryp.getJSON() # Dicionario (Dictionary/JSON)

* inoryp.RetornarIP() # IP
* inoryp.RetornarCodigo() # Codigo (Status code)
* inoryp.RetornarJSON() # Dicionario (Dictionary/JSON)

## Como usar proxy com as novas funcoes?
* inoryp.RetornarIP("localhost:9050", "socks5") # IP (using proxy)
* inoryp.RetornarCodigo("localhost:9050", "socks5") # Codigo (Status code  using proxy)
* inoryp.RetornarJSON("localhost:9050", "socks5") # Dicionario (Dictionary/JSON using proxy)

## Suporte para os metodos
* HTTP
* HTTPS
* SOCKS4
* SOCKS5

## Exemplo sem Proxy!
```

import inoryp

InformaIP = inoryp.classico(0)
print("Seu IP: " + InformaIP)

```
``` Seu IP: 1.1.1.1 ```

## Exemplo com Proxy!
```

import inoryp

InformaIP = inoryp.classico(0, "localhost:9150", "socks5")
print(" Seu IP: " + InformaIP)

```
``` Seu IP: 45.12.32.1```

## Segundo exemplo, com proxy:
```

import inoryp

informaIP_Proxy = inoryp.getIP("localhost:9150", "socks5")
print(" Seu IP: " + informaIP_Proxy)

```
``` Seu IP: 45.12.32.1 ```

## Terceiro exemplo, com proxy:
```

import inoryp

informaIP_Proxy = inoryp.RetornarIP("localhost:9150", "socks5")
print(" Seu IP: " + informaIP_Proxy)

```
``` Seu IP: 45.12.32.1 ```

## Registro de Alteracoes:
* Adicionado: Novas funcoes como: "RetornarIP, RetornarCodigo e RetornarJSON";
* Adicionado: Sistema de identificacao de idiomas;
* Adicionado: Traducao para os idiomas Portugues(Portugueses), Russo(Russian), Ingles(English);
* Corrigido: Alguns bugs foram resolvido da versao anterior; 
* Corrigido: Foi renomeado a duplicata da funcao "inoryp" e ajustado para "classico";
* Corrigido: A resposta de cada funcao foi refeita para melhorar o desempenho do codigo;
* Removido: Foi removido uma unidade da versao como 1.0.2.6 para 2.0.16

# Saiba mais:
* Discord: https://discord.gg/CHsnjZB3Ec
* Desenvolvidor: R0htg0r
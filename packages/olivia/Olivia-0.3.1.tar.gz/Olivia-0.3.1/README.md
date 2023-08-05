# Olivia

**Uma simples, amigável e poderosa assistente para requisições HTTP**

- Olivia utiliza a biblioteca *requests*, tornando sua execução mais intuitiva.

## Instalação
    pip install olivia

## Métodos
Na versão *0.3.0*, Olivia assite aos métodos *POST, GET, DELETE*

# Modo de Usar
## POST

``` python

from olivia import Olivia

infos = {
    "rua": "Verde",
    "numero": "29"
}

dados = Olivia("http://url@url.com", infos)
dados.olivia_salva()

```
# Olivia

from requests import post, get, delete


class Olivia:
    def __init__(self):
        self.item = None
        self.dados = None
        self.url = None

    def olivia_salva(self, url, dados):
        self.url = url
        self.dados = dados

        post(url, dados)
        print('Dados Salvos!')

    def olivia_ler(self, url):
        self.url = url

        lendo = get(url)
        return lendo

    def olivia_apaga(self, url, item):
        self.url = url
        self.item = item
        url_formatada = url + item
        delete(url_formatada)
        print('Item Excluido')

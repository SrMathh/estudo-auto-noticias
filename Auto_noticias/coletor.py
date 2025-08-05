import requests

class Coletor:
    def __init__(self, news_key):
        if not news_key:
            raise ValueError("Chave de API para NewsAPI não fornecida.")
        self.news_key = news_key
        self.url = "https://newsapi.org/v2/everything"

    def buscar_noticias_por_tempo(self, termo_busca, tamanho=5):
        print(f"Buscando notícias sobre '{termo_busca}'...")
        params = {
                'q': termo_busca,
                'language': 'pt',
                'sortBy': 'publishedAt',
                'pageSize': tamanho,
                'apiKey': self.news_key
            }
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            dados_noticias = response.json()
            artigos = dados_noticias.get('articles', [])
            print(f"{len(artigos)} notícias encontradas.")
            return artigos
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar notícias: {e}")
            return []

            

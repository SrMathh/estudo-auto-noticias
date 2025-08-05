import requests
from coletor import Coletor
from analisador import AnalisadorNoticias
from banco_dados import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

news_key = os.getenv("api_key_newsapi")
openai_key = os.getenv("openai_key")

TERMOS_DE_BUSCA = {
    'bitcoin': '"bitcoin"',
    'ethereum': '"ethereum" OR "ETH"',
    'tether': '"tether" OR "USDT"',
    'binancecoin': '"binance coin" OR "BNB"', 
    'ripple': '"ripple" AND ("XRP" OR "cripto")', 
    'solana': '"solana" AND ("cripto" OR "SOL")',
    'usd-coin': '"usd coin" OR "USDC"',
    'staked-ether': '"staked ether" OR "stETH"',
    'tron': '"tron" AND ("cripto" OR "TRX")',
    'dogecoin': '"dogecoin"'
}

class Orquestrador:
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3/"

    def buscar_top_10_moedas(self):
        print("Buscando as 10 principais moedas...")
        try:    
            url = f"{self.url}coins/markets"
            params = {
                'vs_currency': 'brl',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                }
            response = requests.get(url,params=params)
            response.raise_for_status()
            dados_cripto = response.json()
            nomes_cripto = [moeda['id'] for moeda in dados_cripto]
            print("Top 10 moedas encontradas:")
            return nomes_cripto
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar as moedas: {e}")
            return []

if __name__ == "__main__":

    try:
        if not news_key:
            raise ValueError("Chave de API para NewsAPI não fornecida.")
        else:
            db = DatabaseManager('noticias.db')
            db.criar_tabela()
            orquestrador = Orquestrador()
            coletor = Coletor(news_key=news_key)
            analisador = AnalisadorNoticias(openai_key=openai_key)
            top_10_moedas = orquestrador.buscar_top_10_moedas()

        if top_10_moedas:
            print("\nLista das Top 10 Criptomoedas:")
            for moeda in top_10_moedas:
                termos_busca = TERMOS_DE_BUSCA.get(moeda, moeda)
                noticias_encontradas = coletor.buscar_noticias_por_tempo(termos_busca)

                if noticias_encontradas:
                    for noticia in noticias_encontradas:
                        titulo = noticia['title']
                        conteudo = noticia['description'] or noticia['content']
                        resumo_ia = analisador.criar_resumo(titulo, conteudo)
                        url_noticia = noticia['url']
                        db.inserir_resumo(ativo_pesquisado=moeda, titulo_noticia=titulo, resumo_ia=resumo_ia, url_noticia=url_noticia)

                print("-" * 50)
        print("Busca de notícias concluída.")

    except Exception as e:
        print(f"Erro inesperado: {e}")

    finally:
        db.fechar_conexao()
        

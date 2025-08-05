import openai

class AnalisadorNoticias:
    def __init__(self, openai_key):
        if not openai_key:
            raise ValueError("Chave de API para OpenAI não fornecida.")
        self.client = openai.OpenAI(api_key=openai_key)

    def criar_resumo(self, titulo, conteudo):

        print(f"Criando resumo para a notícia: {titulo}")
        prompt = """
        Você é um analista financeiro para um portal de notícias, especializado em resumos rápidos e diretos.
        Sua tarefa é ler o título e o conteúdo de uma notícia e criar um resumo em um único parágrafo, com no máximo 3 frases.
        Seja objetivo e foque no impacto principal da notícia. Não dê conselhos de investimento.
        """
        try:
            response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Título: {titulo}\nConteúdo: {conteudo}\nResumo:"}
                ],
                temperature=0.3,
            )
            resumo = response.choices[0].message.content
            return resumo.strip()
        except Exception as e:
            print(f"Erro ao criar resumo: {e}")
            return "Resumo não disponível devido a um erro."
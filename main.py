import s3fs
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import openai

NPS_ZONES = ['Crítico', 'Aperfeiçoamento', 'Qualidade', 'Excelência']
NPS_VALUES = [-100, 0, 50, 75, 100]
NPS_COLORS = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4']

class Feedback:
    def __init__(self, nota, comentario):
        self.nota = nota
        self.comentario = comentario

class AnalisadorFeedback:
    def __init__(self, feedbacks):
        self.feedbacks = feedbacks
    
    # O NPS é calculado como a diferença entre o percentual de promotores (nota >= 9) e detratores (nota <= 6), multiplicada por 100.
    def calcular_nps(self):
        detratores = sum(1 for feedback in self.feedbacks if feedback.nota <= 6)
        promotores = sum(1 for feedback in self.feedbacks if feedback.nota >= 9)

        return (promotores - detratores) / len(self.feedbacks) * 100

    def criar_grafico_nps(self, nps):
        fig, ax = plt.subplots(figsize=(10, 2))
        
        for i, zone in enumerate(NPS_ZONES):
            ax.barh([0], width=NPS_VALUES[i+1] - NPS_VALUES[i], left=NPS_VALUES[i], color = NPS_COLORS[i])
        
        ax.barh([0], width=0.7, left=nps, color='black') # Plota a posição do nps 
        ax.set_yticks([]) # Remove índices do eixo y
        ax.set_xlim(-100, 100) # Limita gráfico entre -100 e 100]
        ax.set_xticks(NPS_VALUES) # Mostra apenas os índices das zonas nps

        plt.text(nps, 0, f'NPS = {nps:.2f}', ha='center', va='center', color='white', bbox=dict(facecolor='black')) # Caixinha no entorno do nps
        
        patches = [mpatches.Patch(color=NPS_COLORS[i], label=NPS_ZONES[i]) for i in range(len(NPS_ZONES))] # Cria a caixa de legendas
        plt.legend(handles=patches, bbox_to_anchor=(1,1)) # Posiciona o box de legendas

        plt.title('Gráfico de NPS')
        plt.show()

    # Analisa feedbacks usando gpt-4
    def analisar_sentimentos(self, feedbacks):
        comentarios_formatados = "\n".join([f"- Nota {feedback.nota}! {feedback.comentario}" for feedback in feedbacks])
        prompt = f'Sintetize uma análise geral sobre os seguintes comentarios: {comentarios_formatados}'

        repostaAPI = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um modelo de análise de sentimentos com foco em feedbacks sobre experiências educacionais."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return repostaAPI.choices[0].message.content

# Access key e secret key para acessar o AWS S3
with open('elvin-sentimental-data-analysis-user_accessKeys.csv', 'r') as csv_file:
    arquivo = csv.reader(csv_file)

    next(arquivo) # Ignora cabeçalho
    aws_access_key, aws_secret_key = next(arquivo)

# Secret key para utilizar os serviços da openai
with open('secret_key.txt', 'r') as file:
    secret_key = file.read()
    openai.api_key = secret_key

# Carregando feedbacks em um DataFrame pandas
fs = s3fs.S3FileSystem(key=aws_access_key, secret=aws_secret_key)
with fs.open('s3://analise-dados-sentimentos/feedbacks.csv', 'rb') as s3_file:
    dados = pd.read_csv(s3_file, delimiter=';')

# Lista de objetos Feedback
feedbacks = [Feedback(linha['nota'], linha['comentario']) for i, linha in dados.iterrows()]

analisador = AnalisadorFeedback(feedbacks)
nps = analisador.calcular_nps()

# analisador.criar_grafico_nps(nps)

insights = analisador.analisar_sentimentos(feedbacks)
print(insights)
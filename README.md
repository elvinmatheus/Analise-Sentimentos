# Análise de Sentimentos usando Python e IA

Este documento descreve o projeto de um analisador de sentimentos com IA. O projeto tem como objetivo coletar dados de um questionário fictício, tratar os dados com a biblioteca `pandas`, calcular o Net Promoter Score (NPS), visualizar o gráfico do NPS usando `matplotlib` e analisar os comentários usando O `GPT-4`. O projeto foi desenvolvido durante a Ifood Dev Week, da plataforma DIO.

## Organização do projeto

1. **Geração dos dados:** Os dados com as notas e avaliações do bootcamp fictício foram gerados com auxílio do chatGPT. As respostas foram agrupadas em um arquivo .CSV e exportadas para um bucket no `Amazon S3`.

2. **Coleta de dados:** Os dados são coletados do S3 usando a biblioteca `s3fs` e carregados em um DataFrame `pandas`.

3. **Tranformação dos dados:** Cada linha do DataFrame são convertidos em objetos Feedback, para que sejam utilizados posteriormente na análise dos dados.

4. **Cálculo do NPS:** O NPS é calculado como a diferença entre o percentual de promotores (nota >= 9) e detratores (nota <= 6), multiplicada por 100.

5. **Visualização do gráfico NPS:** Um gráfico é desenhado a partir do NPS obtido anteriormente. Utilizamos a biblioteca `matplotlib` para a visualização dos dados.

![Gráfico NPS](https://github.com/elvinmatheus/Analise-Sentimentos/blob/main/images/NPS.png)

6. **Análise dos sentimentos:** Com base nos comentários dos participantes do bootcamp fictício, utilizamos a biblioteca `openai` para decifrar os sentimentos e as emoções presentes nos textos.
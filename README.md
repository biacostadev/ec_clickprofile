# ClickProfile: Do clique ao perfil. Seu passageiro em 360º.

**ClickProfile**, é uma solução de inteligência de dados que visa transformar dados de comportamento de compra em insights valiosos. Nosso principal objetivo é revelar o comportamento dos passageiros para ajudar na criação de experiências personalizadas e no impulsionamento de resultados.

## Os 3 Desafios

### 1\. Perfil de Compra (Modelo de Clusterização)

  * **Objetivo:** Segmentar os clientes em grupos distintos com base em seu histórico de compras para guiar ações estratégicas e campanhas de marketing direcionadas.

  * **Abordagem:**

    1.  Utilizamos a **Análise RFM (Recência, Frequência e Valor Monetário)** para calcular as features principais que definem o perfil de cada cliente.
    2.  Aplicamos o **algoritmo K-Means** para agrupar os clientes em 4 clusters, com base nos resultados do Método do Cotovelo.
    3.  Nomeamos os clusters com base em seus comportamentos: **Clientes Inativos**, **Clientes Novos**, **Clientes Comuns** e **Clientes Premium**.

  * **Resultado:** O modelo gerou uma base de dados consolidada que classifica cada cliente em um dos perfis. Além disso, foi criado um dashboard no Power BI para visualização do comportamento de compra e consumo de cada grupo.

-----

### 2\. Previsão da Próxima Compra (Modelo de Classificação)

  * **Objetivo:** Prever se um cliente realizará uma nova compra na plataforma dentro dos próximos 30 dias, resolvendo um problema de classificação binária.

  * **Abordagem:**

    1.  Focamos a análise nos **Clientes Comuns** por apresentarem um histórico de compra consistente e alto potencial de previsibilidade.
    2.  Treinamos um modelo de **classificação binária XGBoost** para lidar com o desbalanceamento das classes, ajustando parâmetros como `scale_pos_weight`, `learning_rate` e `max_depth`.
    3.  Ajustamos o `threshold` do modelo para priorizar o **recall**, garantindo que a maior parte dos clientes que realmente iriam comprar fosse identificada, mesmo com a diminuição da precisão.

  * **Resultado:** O modelo final alcançou uma acurácia geral de 74,4%, com um recall de 79% e uma precisão de 54%. A curva ROC apresentou uma AUC de 83,76%, confirmando a excelente capacidade do modelo em distinguir entre os clientes que compram e os que não compram.

-----

### 3\. Previsão do Próximo Trecho (Modelo de Recomendação)

  * **Objetivo:** Prever qual trecho (par origem-destino) um cliente tem a maior probabilidade de comprar em sua próxima viagem.

  * **Abordagem:**

    1.  Construímos um sistema de recomendação com múltiplas camadas de lógica para garantir que sempre haja uma recomendação relevante.
    2.  O modelo usa uma **lógica sequencial**, que analisa a última viagem do cliente e recomenda os próximos trechos mais comprados por outros usuários que fizeram a mesma rota.
    3.  Foram criadas três camadas de `fallback` para garantir recomendações mesmo para clientes novos ou sem histórico.

  * **Resultado:** O modelo foi avaliado com a métrica `Hit Rate @5`. Ele obteve um `Hit Rate @5` de **52,56%**, uma performance considerada excelente, já que a estratégia de fallback se mostrou essencial para garantir cobertura total.

## Tecnologias

O projeto foi construído usando as seguintes tecnologias:

  * **Databricks:** Plataforma de dados e inteligência artificial unificada para transformar, processar e armazenar dados brutos de maneira acessível e escalável.
  * **Python:** Linguagem principal para o desenvolvimento dos modelos de machine learning e feature engineering.
  * **Power BI:** Solução para visualização dos resultados e criação dos dashboards de consumo e comportamento.
  * **Streamlit:** Aplicativo online onde o Produto de Dados é disponibilizado para visualização e consulta interativa.
  * **GitHub:** Repositório que contém todo o código do projeto.
  * **Lucidchart:** Ferramenta utilizada para a construção do Modelo de Entidade de Relacionamento do projeto.

## Equipe

  * Ana Beatriz Costa de Oliveira
  * Hygor Abrantes
  * Igor Vignola

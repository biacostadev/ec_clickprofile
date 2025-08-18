import os
from databricks import sql
import streamlit as st
import pandas as pd

DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
DATABRICKS_WAREHOUSE_ID = os.getenv('DATABRICKS_WAREHOUSE_ID')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

if not DATABRICKS_HOST:
    st.error("DATABRICKS_HOST must be set in your environment variables.")
    st.stop()
if not DATABRICKS_WAREHOUSE_ID:
    st.error("DATABRICKS_WAREHOUSE_ID must be set in your environment variables.")
    st.stop()
if not DATABRICKS_TOKEN:
    st.error("DATABRICKS_TOKEN must be set in your environment variables.")
    st.stop()


def sqlQuery(query: str) -> pd.DataFrame:
    """
    Executes a SQL query on Databricks and returns the result as a DataFrame.
    """
    try:
        with sql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=f"/sql/1.0/warehouses/{DATABRICKS_WAREHOUSE_ID}",
            access_token=DATABRICKS_TOKEN
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        raise Exception(f"Erro durante a conexão ou consulta SQL: {e}")

st.set_page_config(layout="wide", page_title="ClickProfile", page_icon="https://raw.githubusercontent.com/biacostadev/ec_clickprofile/refs/heads/main/streamlit/img/icone_1.png")

tabelas = {
    "Produtos de Dados": [
        "estudo.default.tcluster_cli_gold",
        "estudo.default.tprev_compra_cli_gold"
    ],
    "Insumos Dashboard Cluster": [
        "estudo.default.tcluster_dash_geral_gold",
        "estudo.default.tcluster_dash_temporal_ticket_dia_semana_gold",
        "estudo.default.tcluster_dash_temporal_compras_mes_gold",
        "estudo.default.tcluster_dash_temporal_compras_hora_gold",
        "estudo.default.tcluster_dash_temporal_compras_estacao_gold",
        "estudo.default.tcluster_dash_temporal_compras_dia_gold",
        "estudo.default.tcluster_dash_temporal_compras_rota_gold"
    ]
}

logo_col, title_col = st.columns([0.15, 1])
with logo_col:
    st.image("https://raw.githubusercontent.com/biacostadev/ec_clickprofile/refs/heads/main/streamlit/img/icone_2.png")
with title_col:
    st.title("Visualizador de Tabelas ClickProfile")

st.write("Este aplicativo carrega e exibe as tabelas do Produto de Dados Analítico e os Insumos para Dashboard do Cluster, permitindo que você visualize os dados de forma interativa e execute consultas SQL personalizadas.")

def get_columns_from_table(table_name):
    """
    Fetches column names from a table using a metadata query.
    """
    try:
        query = f"SHOW COLUMNS FROM {table_name}"
        columns_df = sqlQuery(query)
        return columns_df['col_name'].tolist()
    except Exception as e:
        st.error(f"Não foi possível obter as colunas da tabela `{table_name}`. Erro: {e}")
        return []

def getData_tcluster_cli_gold():
    """
    Allows the user to select a group, table, and columns, then loads and displays a data preview.
    """
    # Criando dois contêineres para as caixas de seleção
    select_col1, select_col2 = st.columns(2)

    with select_col1:
        grupo_selecionado = st.selectbox(
            "Escolha o grupo da tabela:",
            list(tabelas.keys()),
            index=None,
            placeholder="Por favor, selecione um grupo..."
        )
    
    tabela_completa = None
    with select_col2:
        if grupo_selecionado:
            tabela_completa = st.selectbox(
                f"Escolha a tabela de '{grupo_selecionado}':",
                tabelas[grupo_selecionado],
                index=None,
                placeholder="Por favor, selecione uma tabela..."
            )
    
    # Restante da lógica de exibição
    if tabela_completa:
        st.header(f"Tabela selecionada: `{tabela_completa}`")
        query = f"SELECT * FROM {tabela_completa} limit 5"
        
        try:
            st.info("Tentando conectar e buscar os dados...")
            df = sqlQuery(query)
            st.success("Dados carregados com sucesso!")
            st.dataframe(df, hide_index=True, use_container_width=True)
        except Exception as query_error:
            st.error(f"Falha ao consultar a tabela `{tabela_completa}`. Erro: {query_error}")
            st.warning("Verifique se o SQL Warehouse está em execução e se as credenciais de acesso estão corretas.")
    else:
        st.info("Por favor, selecione um grupo e uma tabela.")

    # Query Personalizada
    st.markdown("---")
    st.header("Execute Sua Query SQL Personalizada")
    st.write("Lembre-se que este aplicativo foi criado pensando em ser uma solução que possibilite a visualização das informações para conhecimento e análise dos dados de saída do projeto ClickProfile. Para garantir a melhor usabilidade inclua em sua consulta um `LIMIT` ou agregue os dados (ex: `COUNT`, `SUM`).")

    colunas_selecionadas = None
    if tabela_completa:
        todas_colunas = get_columns_from_table(tabela_completa)
        if todas_colunas:
            colunas_selecionadas = st.multiselect(
                "Selecione as colunas para a sua query:",
                options=todas_colunas,
                default=todas_colunas
            )

    default_query = ""
    if tabela_completa and colunas_selecionadas:
        colunas_str = ", ".join(colunas_selecionadas)
        default_query = f"SELECT {colunas_str} FROM {tabela_completa} LIMIT 10"
        
    custom_query = st.text_area(
        "Digite sua consulta SQL aqui:",
        value=default_query,
        height=150,
        placeholder="Exemplo: SELECT DISTINCT fk_contact, ds_cluster FROM estudo.default.tcluster_cli_gold LIMIT 10"
    )
    
    if st.button("Executar Query"):
        if custom_query:
            try:
                st.info("Executando sua consulta...")
                df = sqlQuery(custom_query)
                st.success("Consulta executada com sucesso!")
                st.dataframe(df, hide_index=True, use_container_width=True)
            except sql.exc.Error as query_error:
                st.error(f"Erro de Conexão ou Tamanho de Mensagem. Erro: {query_error}")
                st.warning("A consulta retornou um volume de dados muito grande. Por favor, ajuste a consulta para incluir um `LIMIT` ou para agregar os dados (ex: `COUNT`, `SUM`).")
            except Exception as query_error:
                st.error(f"Falha ao executar sua consulta. Erro: {query_error}")
                st.warning("Verifique se a sintaxe SQL está correta e se você tem permissões.")
        else:
            st.warning("Por favor, digite uma consulta SQL para executar.")

if __name__ == "__main__":
    try:
        getData_tcluster_cli_gold()
    except AssertionError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Falha geral na aplicação: {e}")

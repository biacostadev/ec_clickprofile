from pyspark.sql import SparkSession, DataFrame

def escrita_tabela(df: DataFrame, destino: str):
    df.write.mode("overwrite").saveAsTable(destino)
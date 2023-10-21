from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_aeronaves.sql") as f:
            self.query_relatorio_aeronaves = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_voos.sql") as f:
            self.query_relatorio_voos = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_total_aeronave.sql") as f:
            self.query_relatorio_total_aeronave = f.read()    

    def get_relatorio_aeronaves(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_aeronaves))
        input("Pressione Enter para Sair do Relatório de Aeronaves")

    def get_relatorio_voos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_voos))
        input("Pressione Enter para Sair do Relatório de Voos")

    def get_relatorio_total_aeronave(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_total_aeronave))
        input("Pressione Enter para Sair do Relatório Total de Aeronaves")
from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_aeronaves = config.QUERY_COUNT.format(tabela="tbl_aeronaves")
        self.qry_total_voos = config.QUERY_COUNT.format(tabela="tbl_voos")

        # Nome(s) do(s) criador(es)
        self.created_by = "Matheus Gomes Montovani, Bruna Torres, Kevin Camara, Murilo Martins, João Degasperi, Alejandro Cristh"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_total_aeronaves(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_aeronaves)["total_tbl_aeronaves"].values[0]

    def get_total_voos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_voos)["total_tbl_voos"].values[0]


    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE CONTROLE DE VOOS                    
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - AERONAVES:         {str(self.get_total_aeronaves()).rjust(5)}
        #      2 - VOOS:              {str(self.get_total_voos()).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """
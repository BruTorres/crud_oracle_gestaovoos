from model.aeronaves import Aeronave
from conexion.oracle_queries import OracleQueries

class AeronaveController:
    def __init__(self):
        pass
        
    def adicionar_aeronave(self) -> Aeronave:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigoCalda = input("Código calda: ")
            
        nomeAeronave = input("Nome: ")

        oracle.write(f"insert into tbl_aeronaves values ('{codigoCalda}', '{nomeAeronave}')")
        
        df_aeronave = oracle.sqlToDataFrame(f"select cd_calda, nm_aeronave from tbl_aeronaves where cd_calda = '{codigoCalda}'")
        
        nova_aeronave = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
        
        print(nova_aeronave.to_string())
        
        return nova_aeronave

    def atualizar_aeronave(self) -> Aeronave:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigoCalda = (input("O código calda da aeronave que você deseja alterar: "))

        if not self.verifica_existencia_aeronave(oracle, codigoCalda ):
            
            novo_nome = input("Nome (Novo): ")

            oracle.write(f"update tbl_aeronaves set nm_aeronave = '{novo_nome}' where cd_calda  = '{codigoCalda }'")
           
            df_aeronave = oracle.sqlToDataFrame(f"select cd_calda, nm_aeronave from tbl_aeronaves where cd_calda = '{codigoCalda}'")
            
            aeronave_atualizado = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
           
            print(aeronave_atualizado.to_string())
            
            return aeronave_atualizado
        else:
            print(f"O Código calda {codigoCalda} não existe.")
            return None

    def excluir_aeronave(self):
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        
        codigoCalda = int(input("Digite o código calda da aeronave que deseja excluir: "))        

        
        if not self.verifica_existencia_aeronave(oracle, codigoCalda):            
            
            df_aeronave = oracle.sqlToDataFrame(f"select cd_calda, nm_aeronave from tbl_aeronaves where cd_calda = '{codigoCalda}'")
            
            oracle.write(f"delete from tbl_aeronaves where cd_calda = '{codigoCalda}'")            
            
            aeronave_excluido = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
            
            print("Aeronave Removida com Sucesso!")
            print(aeronave_excluido.to_string())
        else:
            print(f"O código calda {codigoCalda} não existe.")

    def verifica_existencia_aeronave(self, oracle:OracleQueries, codigoCalda:str=None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_aeronave = oracle.sqlToDataFrame(f"select cd_calda, nm_aeronave from tbl_aeronaves where cd_calda = '{codigoCalda}'")
        return df_aeronave.empty
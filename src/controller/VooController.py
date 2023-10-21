from pydoc import cli
from model.voos import Voo
from controller.AeronaveController import AeronaveController
from model.aeronaves import Aeronave
from conexion.oracle_queries import OracleQueries
from datetime import date
import datetime

class VooController:
    def __init__(self):
        self.ctrl_aeronave = AeronaveController()
        pass
        
    def inserir_voo(self) -> Voo:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        oracle = OracleQueries()
        
        dt_voo_str = input("Digite a data do voo (yyyy-mm-dd): ")

        self.listar_aeronaves(oracle, need_connect=True)
        cd_calda = input("Digite o código calda da aeronave que você deseja: ")
        aeronave = self.valida_aeronave(oracle, cd_calda)
        if aeronave == None:
            return None

        cursor = oracle.connect()
        
        output_value = cursor.var(int)

        # data = dict(nr_voo=output_value, dt_voo=dt_voo_str, cd_calda=cd_calda)
        data = dict(nr_voo=output_value, dt_voo=dt_voo_str, cd_calda=aeronave.get_codigoCalda())

        cursor.execute("""
        begin
            :nr_voo := SEQ_TBL_VOOS.NEXTVAL;
            insert into tbl_voos values(:nr_voo, TO_DATE(:dt_voo, 'DD/MM/YYYY'), :cd_calda);
        end;
        """, data)
       
        nr_voo = output_value.getvalue()
        
        oracle.conn.commit()
        
        df_voo = oracle.sqlToDataFrame(f"select nr_voo, dt_voo, cd_calda from tbl_voos where nr_voo = '{nr_voo}'")
        
        print(df_voo)

        novo_voo = Voo(df_voo.nr_voo.values[0], df_voo.dt_voo.values[0], df_voo.cd_calda[0])
        
        print(novo_voo.to_string())
        
        return novo_voo

    def atualizar_voo(self) -> Voo:
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        
        nr_voo = int(input("Digite o número do voo que será alterado: "))        

        
        if not self.verifica_existencia_voo(oracle, nr_voo):

            self.listar_aeronaves(oracle)
            cd_calda = str(input("Digite o código calda da aeronave que você deseja: "))
            aeronave = self.valida_aeronave(oracle, cd_calda)
            if aeronave == None:
                return None

            dt_voo_str = input("Digite a data do voo (yyyy-mm-dd): ")
        

            oracle.write(f"update tbl_voos set cd_calda = '{aeronave.get_codigoCalda()}', dt_voo = to_date('{dt_voo_str}', 'yyyy-mm-dd') where nr_voo = '{nr_voo}'")
            
            df_voo = oracle.sqlToDataFrame(f"select nr_voo, cd_calda, dt_voo from tbl_voos where nr_voo = {nr_voo}")
            
            voo_atualizado = Voo(df_voo.nr_voo.values[0], df_voo.cd_calda.values[0], df_voo.dt_voo.values[0])
            
            print(voo_atualizado.to_string())
            
            return voo_atualizado
        else:
            print(f"O número do voo {nr_voo} não existe.")
            return None


    def excluir_voo(self):
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        nr_voo = int(input("Digite o número do voo que será excluido: "))           

        if not self.verifica_existencia_voo(oracle, nr_voo):            
            
            df_voo = oracle.sqlToDataFrame(f"select nr_voo, dt_voo, cd_calda from tbl_voos where nr_voo = '{nr_voo}'")
           
            oracle.write(f"delete from tbl_voos where nr_voo = '{nr_voo}'")            
            
            voo_excluido = Voo(df_voo.nr_voo.values[0], df_voo.cd_calda.values[0], df_voo.dt_voo.values[0])
            
            print("Voo removido com sucesso!")
            print(voo_excluido.to_string())
        else:
            print(f"O número do voo {nr_voo} não existe.")

    def verifica_existencia_voo(sself, oracle:OracleQueries, nr_voo:int=None) -> bool:
        
        df_voo = oracle.sqlToDataFrame(f"select nr_voo, dt_voo, cd_calda from tbl_voos where nr_voo = '{nr_voo}'")
        return df_voo.empty
    
    def listar_aeronaves(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                SELECT a.CD_CALDA
                    , a.NM_AERONAVE
                FROM TBL_AERONAVES a
                ORDER BY a.NM_AERONAVE
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_aeronave(self, oracle:OracleQueries, cd_calda:str=None) -> Aeronave:
        if self.ctrl_aeronave.verifica_existencia_aeronave(oracle, cd_calda):
            print(f"O ódigo calda {cd_calda} informado não existe.")
            return None
        else:
            oracle.connect()
            df_aeronave = oracle.sqlToDataFrame(f"select cd_calda, nm_aeronave from tbl_aeronaves where cd_calda = '{cd_calda}'")
            aeronave = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
            return aeronave
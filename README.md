# example_crud_oracle_voos
# Exemplo de Sistema em Python fazendo CRUD no Oracle

Esse sistema de exemplo é composto por um conjunto de tabelas que representam sistema de gerenciamento de voos, contendo tabelas como: voos e aeronaves

O sistema exige que as tabelas existam, então basta executar o script Python a seguir para criação das tabelas e preenchimento de dados de exemplos:
```shell
~$ python create_tables_and_records.py
```

Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```

Para que possa testar as conexões com o banco de dados Oracle e o módulo Conexion desenvolvido para esse projeto, basta executar o script Python a seguir:
```shell
~$ python test.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/DIAGRAMA_SISTEMAVOOS.pdf) (lógico) do sistema.
    * O sistema possui duas entidades: AERONAVES E VOOS
- [sql](sql): Nesse diretório estão os scripts para criação das tabelas e inserção de dados fictícios para testes do sistema
    * Certifique-se de que o usuário do banco possui todos os privilégios antes de executar os scripts de criação, caso ocorra erro, execute o comando a seguir com o superusuário via SQL Developer: `GRANT ALL PRIVILEGES TO LABDATABASE;`
    * [create_tables.sql](sql/create_tables.sql): script responsável pela criação das tabelas, relacionamentos e criação de permissão no esquema LabDatabase.
    * [insert_table.sql](sql/insert_table.sql): script responsável pela inserção dos registros fictícios para testes do sistema.
- [src](src): Nesse diretório estão os scripts do sistema
    * [conexion](src/conexion): Nesse repositório encontra-se o [módulo de conexão com o banco de dados Oracle](src/conexion/oracle_queries.py). Esse módulo possui algumas funcionalidades úteis para execução de instruções DML e DDL, sendo possível obter JSON, Matriz e Pandas DataFrame.
      - Exemplo de utilização para consultas simples:

        ```python
        def listar_aeronaves(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                SELECT a.CD_CALDA
                    , a.NM_AERONAVE
                FROM TBL_AERONAVES a
                ORDER BY a.NM_AERONAVE;
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))
        ```
      - Exemplo de utilização para alteração de registros

        ```python
         def inserir_voo(self) -> Voo:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        oracle = OracleQueries()
        
        cursor = oracle.connect()
        
        output_value = cursor.var(int)

        dt_voo_str = input("Digite a data do voo (dd/mm/aaaa): ")

        try:
            dt_voo = datetime.datetime.strptime(dt_voo_str, "%d/%m/%Y")
        except ValueError:
            print("Data inválida! Por favor, insira a data no formato dd/mm/aaaa.")
            return None
        

        self.listar_aeronaves(oracle, need_connect=True)
        cd_calda = input("Digite o código calda da aeronave que você deseja: ")
        aeronave = self.valida_cliente(oracle, cd_calda)
        if aeronave == None:
            return None

        data = dict(nr_voo=output_value, dt_voo=dt_voo, cd_calda=cd_calda)

        cursor.execute("""
        begin
            :nr_voo := SEQ_TBL_VOOS.NEXTVAL;
            insert into tbl_voos values(:nr_voo, :dt_voo, :cd_calda);
        end;
        """, data)
       
        codigo_voo = output_value.getvalue()
        
        oracle.conn.commit()
        
        df_voo = oracle.sqlToDataFrame(f"select nr_voo, dt_voo, cd_calda from tbl_voos where nr_voo = {codigo_voo}")
        
        novo_voo = Voo(df_voo.nr_voo.values[0], df_voo.dt_voo.values[0], df_voo.cd_calda.values[0])
        
        print(novo_voo.to_string())
        
        return novo_voo
        ```
      - Outros exemplos: [test.py](src/test.py)
      - Caso esteja utilizando na máquina virtual antiga, você precisará alterar o método connect de:
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString()
                                  )
          ```
        Para:
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString(in_container=True)
                                  )
          ```
    * [controller](src/controller/): Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.
    * [model](src/model/): Nesse diretório encontram-ser as classes das entidades descritas no [diagrama relacional](diagrams/DIAGRAMA_SISTEMAVOOS.pdf)
    * [reports](src/reports/) Nesse diretório encontra-se a [classe](src/reports/relatorios.py) responsável por gerar todos os relatórios do sistema
    * [sql](src/sql/): Nesse diretório encontram-se os scripts utilizados para geração dos relatórios a partir da [classe relatorios](src/reports/relatorios.py)
    * [utils](src/utils/): Nesse diretório encontram-se scripts de [configuração](src/utils/config.py) e automatização da [tela de informações iniciais](src/utils/splash_screen.py)
    * [create_tables_and_records.py](src/create_tables_and_records.py): Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script [principal.py](src/principal.py) para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`

### Instalando Oracle InstantClient
- Baixe a versão do [InstantClient](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html) de acordo com a versão do Banco de Dados
- Caso esteja utilizando uma distribuição Linux baseado em Debian, será necessário executar o comando a seguir para converter o arquivo .rpm para .deb.
  ```shell
  sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
  ```
- Descompacte o arquivo e será gerado um diretório em um diretório de fácil acesso.
- Mova os diretórios lib e share para dentro do diretório do InstantClient
  ```shell
  sudo mv lib /usr/local/oracle/instantclient_18_5/
  ```
  
  ```shell
  sudo mv share instantclient_18_5/
  ```
- Edite o arquivo `.bash_profile` incluindo as linhas a seguir ao final do arquivo:
  ```shell
  export ORACLE_HOME=/usr/local/oracle/instantclient_18_5/lib/oracle/18.5/client64
  export LD_LIBRARY_PATH=$ORACLE_HOME/lib
  export PATH=$PATH:$ORACLE_HOME/bin
  export PATH
  ```

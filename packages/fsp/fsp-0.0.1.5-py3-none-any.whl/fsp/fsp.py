import mysql.connector
class FSP():
    """
    Cria um objeto de conexão com um banco de dados no sistema de gerenciamento de dados MySQL.
    :args:
        nomeBancoDeDados: Nome do banco de dados a ser conectado
        enderecoDoBancoDeDados: Endereço do banco de dados, por padrão é definido como localhost.
        nomeUsuarioDoBancoDeDados: Nome do usuário que deseja conectar ao banco de dados, por padrão é definido como root.
        senhaDoBancoDeDados: Senha do usuário que deseja se conectar ao banco de dados, por padrão é definido como uma string vazia.
    :returns: Retorna uma um objeto capaz de manipular o banco de dados selecionado, caso não seja possível a conexão retorna o valor booleano False.
    """
    def __init__(self,nomeBancoDeDados,enderecoDoBancoDeDados='localhost',nomeUsuarioDoBancoDeDados='root',senhaDoBancoDeDados=''):
        self.conexao = self.conectarBD(nomeBancoDeDados,enderecoDoBancoDeDados,nomeUsuarioDoBancoDeDados,senhaDoBancoDeDados)
        
    def conectarBD(self,nomeBancoDeDados,enderecoDoBancoDeDados,nomeUsuarioDoBancoDeDados,senhaDoBancoDeDados):
        """
        Tenta criar um objeto conectado ao banco de dados informado, e cria umm atributo cursor para realizar as operações no banco.
        :args:
            nomeBancoDeDados: Nome do banco de dados a ser conectado
            enderecoDoBancoDeDados: Endereço do banco de dados, por padrão é definido como localhost.
            nomeUsuarioDoBancoDeDados: Nome do usuário que deseja conectar ao banco de dados, por padrão é definido como root.
            senhaDoBancoDeDados: Senha do usuário que deseja se conectar ao banco de dados, por padrão é definido como uma string vazia.
        :returns: Retorna uma um objeto capaz de manipular o banco de dados selecionado, caso não seja possível a conexão retorna o valor booleano False.
        """
        try:
            conexao = mysql.connector.connect(host=enderecoDoBancoDeDados,database=nomeBancoDeDados,user=nomeUsuarioDoBancoDeDados,password=senhaDoBancoDeDados)
            if conexao.is_connected():
                self.cursor = conexao.cursor()
                return conexao
            else:
                print(F"Falha ao conectar ao banco de dados {nomeBancoDeDados}")
                return False
        except:
            print("Erro na passagem de parâmetros")
            return False

    def criarTabela(self,nomeTabela,nomeChavePrimaria):
        """
        Cria uma tabela no banco de dados selecionado, a tabela é criada com uma chave primária.
        :args:
            nomeTabela: Nome da tabela a ser criada.
            nomeChavePrimaria: Nome da chave primária da tabela.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            self.cursor.execute(F'''CREATE TABLE IF NOT EXISTS {nomeTabela}(
	                                    {nomeChavePrimaria} int NOT NULL AUTO_INCREMENT,
	                                    PRIMARY KEY({nomeChavePrimaria})
                                    );''')
            return True
        except:
            print(F"Erro ao criar tabela {nomeTabela}")
            return False

    def limparDadosTabela(self,nomeTabela):
        """
        Limpa as infomações da tabela selecionada no banco de dados, a estrutura da tabela não é alterada.
        :args:
            nomeTabela: Nome da tabela a ter seus dados apagados.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            self.cursor.execute(F'''TRUNCATE TABLE {nomeTabela};''')
            return True
        except:
            print(F"Erro ao limpar a tabela {nomeTabela}")
            return False
    
    def excluirTabelaComDados(self,nomeTabela):
        """
        Exclui uma tabela selecionada no banco de dados, a estrutura e dados da tabela são apagados.
        :args:
            nomeTabela: Nome da tabela a ser criada.
            nomeChavePrimaria: Nome da chave primária da tabela.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            self.cursor.execute(F'''DROP TABLE {nomeTabela};''')
            return True
        except:
            print(F"Erro ao excluir a tabela {nomeTabela}")
            return False
    
    def adicionarColunaTabela(self, nomeTabela, nomeNovaColuna, stringComCaracteristicas,aposColuna=''):
        """
        Adiciona uma coluna na tabela selecionada.
        :args:
            nomeTabela: Nome da tabela onde a coluna será adicionada.
            nomeNovaColuna: Nome da coluna que será adicionada.
            stringComCaracterísticas: Atributos que a nova coluna possui.
            aposColuna: Indica após que coluna existente a nova coluna será adicionada, por padrão é definido como uma string vazia.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            stringComCaracteristicas = stringComCaracteristicas.split(' ')
        except:
            print(stringComCaracteristicas)
            print("Atributos devem ser separados por espaço. Se o erro persistir cheque o conteúdo passado.")
            return False
        try:
            if aposColuna:
                sql = F'''ALTER TABLE {nomeTabela} ADD COLUMN {nomeNovaColuna}'''
                for atributo in stringComCaracteristicas:
                    sql += F" {atributo}"
                if aposColuna.upper() == "FIRST":
                    sql += F" FIRST;"
                else:
                    sql += F" AFTER {aposColuna};"
            else:
                sql = F'''ALTER TABLE {nomeTabela} ADD COLUMN {nomeNovaColuna}'''
                for atributo in stringComCaracteristicas:
                    sql += F" {atributo}"
                sql += ";"
            self.cursor.execute(sql)
            return True
        except:
            print(F"Erro ao adicionar uma nova coluna a tabela {nomeTabela}, verifique as características passadas.")
            return False

    def inserirDadosNaTabela(self,nomeTabela,colunas='',inserirValores=''):
        """
        Insere dados na tabela selecionada.
        :args:
            nomeTabela: Nome da tabela onde os dados serão adicionados.
            colunas: Colunas que receberão novos dados.
            inserirValores: Valores a ser adicionados nas colunas selecionadas.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            if colunas:
                colunas = colunas.split(',')
                sql = F'''INSERT INTO {nomeTabela}('''
                for coluna in colunas:
                    sql += F"{coluna},"
                sql = sql[:-1]
                sql += ") VALUES("
                inserirValores = inserirValores.split(',')
                for valor in inserirValores:
                    sql += F"{valor},"
                sql = sql[:-1]
                sql += ");"
            else:
                sql = F'''INSERT INTO {nomeTabela} VALUES ('''
                for valores in inserirValores:
                    sql += valores
                sql += ');'
            self.cursor.execute(sql)
            return True
        except:
            print("ERRO: Cheque a passagem de parâmetros.")
            return False

    def atualizarDadosNaTabela(self,nomeTabela, colunaAlterada,novoValor,identificadorLinha,condicao,valorIdentificado):
        """
        Atualiza dados em uma coluna na tabela selecionada.
        :args:
            nomeTabela: Nome da tabela onde o dado será alterado.
            colunaAlterada: Nome da coluna em que o dado será alterado.
            novoValor: Novo valor da linha selecionada.
            identificadorLinha: Nome de da coluna para ser usada na condição para atualizar o valor.
            condicao: Operador relacional a ser usada para fazer a condição para atualizar o valor.
            valorIdentificado: Valor usado como referência para alterar o valor de uma linha.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            if isinstance(nomeTabela,str):
                sql = F"UPDATE {nomeTabela} SET {colunaAlterada} = '{novoValor}' WHERE {identificadorLinha} {condicao} {valorIdentificado}"
            else:
                sql = F"UPDATE {nomeTabela} SET {colunaAlterada} = {novoValor} WHERE {identificadorLinha} {condicao} {valorIdentificado}"
            print(sql)
            self.cursor.execute(sql)
            return True
        except:
            print("Erro: cheque a passagem de parâmetros.")
            return False

    def deletarDadosNaTabela(self, nomeTabela,colunaIdentificadora,condicaoFiltragem,valorFiltragem):
        """
        Deleta linhas de uma tabela selecionada.
        :args:
            nomeTabela: Nome da tabela onde a linha será alterada.
            colunaIdentificadora: Nome de da coluna para ser usada na condição para deletar a linha.
            condicaoFiltragem: Operador relacional a ser usada para fazer a condição para deletar a linha.
            stringComCaracterísticas: Atributos que a nova coluna possui.
            valorIdentificado: Valor usado como referência para deletar uma linha.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            sql = F"DELETE FROM {nomeTabela} WHERE {colunaIdentificadora} {condicaoFiltragem} {valorFiltragem};"
            self.cursor.execute(sql)
            return True
        except:
            print("Erro: cheque a passagem de parâmetros.")
            return False

    def verTabelaCompleta(self,nomeTabela,colunasExibidas='*',filtrar=False,colunaFiltragem=None,condicaoFiltragem=None,valorFiltragem=None):
        """
        Permite a vizualização dos dados de uma tabela selecionada.
        :args:
            nomeTabela: Nome da tabela a ter os dados retornados.
            colunasExibidas: Colunas da tabela a ser retornadas, por padrão definido como *.
            filtrar: Permite fazer uma filtragem nas linhas da tabela, por padrão definido como False.
            colunaFiltragem: Nome de da coluna para ser usada na condição para encontrar linhas a ser retornadas.
            condicaoFiltragem: Operador relacional a ser usada para fazer a condição para retornar a linha.
            valorFiltragem: Valor usado como referência para retornar uma linha.
        :returns:Retorna True caso a operação seja executada com sucesso, caso contrário retorna False.
        """
        try:
            sql = F"SELECT "
            if colunasExibidas != '*':
                colunasExibidas = colunasExibidas.split(',')
                for colunas in colunasExibidas:
                    sql += F"{colunas},"
                sql = sql[:-1]
            else:
                sql += "*"
            sql += F" FROM {nomeTabela};"

            if filtrar:
                sql = sql[:-1]
                sql += F" WHERE {colunaFiltragem} {condicaoFiltragem} {valorFiltragem};"
            print(sql)
            self.cursor.execute(sql)
            dados = self.cursor.fetchall()
            return dados
        except:
            print("Erro: cheque a passagem de parâmetros.")
            return False
if __name__ == '__main__':
    teste = FSP('fsp')
    """print(teste.conexao)
    teste.cursor.execute("SELECT DATABASE();")
    t = teste.cursor.fetchone()
    print(t)"""
    #teste.inserirDadosNaTabela('teste','numeros,nome','23,"Wanderlei"')
    #teste.adicionarColunaTabela('teste','nome','varchar(30)','')
    #teste.atualizarDadosNaTabela('teste','nome','Jose Wanderlei','id','>',9)
    print(teste.verTabelaCompleta('teste','id,nome',True,'numeros','>',9))   
    print(teste.verTabelaCompleta('teste'))
    teste.deletarDadosNaTabela('teste','id','=','8')
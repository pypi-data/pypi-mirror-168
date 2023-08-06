
"""
Funções para facilitar a implementação de um ETL, subindo o nível de abstração
para um job de carga de dados.
"""

import blipy.tabela_entrada as te
import blipy.tabela_saida as ts
import blipy.func_transformacao as ft

from enum import Enum, auto


# Tipos de estratégias de gravação no banco
class TpEstrategia(Enum):
    DELETE  = auto()
    INSERT  = auto()


def importa_tabela_por_sql(conn_entrada, conn_saida, sql_entrada,
        nome_tabela_saida, cols_saida, estrategia=TpEstrategia.DELETE):
    """
    Importação do resultado de uma consulta sql para o banco de dados. A
    tabela de destino é limpa e carregada de novo (considera-se que são poucas
    linhas). Qualquer erro dispara uma exceção.

    Args:
    :param conn_entrada: conexão com o esquema de entrada de dados (geralmente
    o staging)
    :param conn_saida: conexão com o esqumea de saída (geralmente a produção)
    :param sql_entrada: consulta sql que irá gerar os dados de entrada
    :param nome_tabela_saida: nome da tabela de saida
    :param cols_saida: lista das colunas que serão gravadas na tabela 
    de saida, com o nome da coluna, seu tipo e a função de transformanção
    a ser aplicada (opcional; se não informado, faz só uma cópia do dado)
    :param estrategia: estratégia de gravação que será utilizada (enum
    TpEstrategia)
    """

    tab_entrada = te.TabelaEntrada(conn_entrada)
    tab_entrada.carrega_dados(sql_entrada)

    __grava_tabela( tab_entrada, 
                    conn_saida, 
                    nome_tabela_saida, 
                    cols_saida, 
                    estrategia)


def importa_tabela_por_nome(conn_entrada, conn_saida, nome_tabela_entrada, 
        nome_tabela_saida, cols_entrada, cols_saida, 
        estrategia=TpEstrategia.DELETE):
    """
    Importação de uma tabela para o banco de dados. A tabela de destino é limpa
    e carregada de novo (considera-se que são poucas linhas). Qualquer erro
    dispara uma exceção.

    Args:
    :param conn_entrada: conexão com o esquema de entrada de dados (geralmente
    o staging)
    :param conn_saida: conexão com o esqumea de saída (geralmente a produção)
    :param nome_tabela_entrada: nome da tabela de entrada
    :param nome_tabela_saida: nome da tabela de saida
    :param cols_entrada: lista dos nomes das colunas que serão buscadas na 
    tabela de entrada
    :param cols_saida: lista das colunas que serão gravadas na tabela 
    de saida, com o nome da coluna, seu tipo e a função de transformanção
    a ser aplicada (opcional; se não informado, faz só uma cópia do dado)
    :param estrategia: estratégia de gravação que será utilizada (enum
    TpEstrategia)
    """

    tab_entrada = te.TabelaEntrada(conn_entrada)
    tab_entrada.carrega_dados(nome_tabela_entrada, cols_entrada)

    __grava_tabela( tab_entrada, 
                    conn_saida, 
                    nome_tabela_saida, 
                    cols_saida, 
                    estrategia)


def __grava_tabela(tab_entrada, conn_saida, nome_tabela_saida, cols_saida, estrategia):
    """
    Grava uma tabela no banco de dados.

    Args:
    :param tab_entrada: a tabela de entrada dos dados
    :param conn_saida: conexão com o esqumea de saída (geralmente a produção)
    :param nome_tabela_saida: nome da tabela de saida
    :param cols_saida: lista das colunas que serão gravadas na tabela 
    de saida, com o nome da coluna, seu tipo e a função de transformanção
    a ser aplicada (opcional; se não informado, faz só uma cópia do dado)
    :param estrategia: estratégia de gravação que será utilizada (enum
    TpEstrategia)
    """

    cols = {}
    for item in cols_saida:
        if len(item) == 2:
            # função de transformanção não informada, faz só uma cópia do dado
            cols[item[0]] = ts.Coluna(item[0], item[1], ft.f_copia)
        else:
            # usa a função de transformanção informada
            cols[item[0]] = ts.Coluna(item[0], item[1], item[2])

    tab_saida = ts.TabelaSaida(nome_tabela_saida, cols, conn_saida)

    if estrategia == TpEstrategia.DELETE:
        conn_saida.apaga_registros(nome_tabela_saida)
    elif estrategia == TpEstrategia.INSERT:
        pass
    else:
        raise NotImplementedError

    while True:
        registro = tab_entrada.le_prox_registro()
        if registro is None:
            break

        i = 0
        for k in cols.keys():
            tab_saida.col[k].calcula_valor( (registro[i],) )
            i += 1

        tab_saida.grava_registro()



import sys
sys.path.append('..')

from blipy.conexao_bd import ConexaoBD

# from blipy.job import Job
# from blipy.enum_tipo_col_bd import TpColBD as tp


if __name__ == "__main__":
    # job = Job("Teste Carga")

    try:
        conn_stg, conn_prd, conn_corp = ConexaoBD.from_json()
    except:
        sys.exit()

    print(conn_stg)
    print(conn_prd)
    print(conn_corp)

    # # dimensão LOCAL_HOSPEDAGEM
    # cols_entrada = ["ID_LOCAL_HOSPEDAGEM",
    #                 "NO_LOCAL_HOSPEDAGEM"]
    # cols_saida = [  ["ID_LOCAL_HOSPEDAGEM", tp.NUMBER],
    #                 ["NO_LOCAL_HOSPEDAGEM", tp.STRING]]
    # job.importa_tabela_por_nome(   
    #         conn_stg, 
    #         conn_prd, 
    #         "MVW_LOCAL_HOSPEDAGEM", 
    #         "LOCAL_HOSPEDAGEM",
    #         cols_entrada, 
    #         cols_saida)


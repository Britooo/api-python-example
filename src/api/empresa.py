from http import HTTPStatus
from flask import g, Blueprint

empresa = Blueprint(name='empresas', import_name=__name__, url_prefix='/api/empresas')

@empresa.route('medicao/<string:medicao>')
def get_by_ponto_medicao(medicao):
    """Filtra uma lista de empresas com base em um ponto de medição 
    ---
    parameters:
      - name: medicao
        in: path
        type: string
        required: true
    definitions:
      Empresa:
        type: object
        properties:
          nCdEmpresa:
            type: number
          sNrCnpj:
            type: string
          sNmEmpresa:
            type: string
          sNmFantasia:
            type: string
          sNmApelido:
            type: string
      ListaEmpresa:
        type: object
        properties:
            empresas:
                type: array
                items:
                    $ref: '#/definitions/Empresa'
    responses:
      200:
        description: Lista de empresas
        schema:
          $ref: '#/definitions/ListaEmpresa'
    """

    cursor = g.wbc_db.cursor()
    cursor.execute("""
        SELECT
            EMPR.nCdEmpresa,
            EMPR.sNrCnpj,
            EMPR.sNmEmpresa,
            EMPR.sNmFantasia,
            EMPR.sNmApelido
        FROM EMPRESA AS EMPR
        INNER JOIN CE_PONTO_MEDICAO AS PMED
           ON EMPR.nCdEmpresa = PMED.nCdEmpresa
        WHERE PMED.sCdImportacaoPontoMedicao = %s
    """, (medicao))
    
    response = { 'empresas': cursor.fetchall() }

    cursor.close()
    
    return response, HTTPStatus.OK


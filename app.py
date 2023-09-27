from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, session
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Peca
from logger import logger
#from models.base import Base
from schemas import *
from flask_cors import CORS

info = Info(title="Componente_C", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
peca_tag = Tag(name="Pecas", description="Adição, visualização e remoção de peças à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/peca', tags=[peca_tag],
          responses={"200": PecaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_peca(form: PecaSchema):
    """Adiciona uma nova peça à base de dados

    Retorna uma representação das peças.
    """
    print(form)
    peca = Peca(
        nome_peca=form.nome_peca,
        modelo_peca=form.modelo_peca,
        cod_peca=form.cod_peca
    )
    logger.info(f"Adicionando peças de nome: '{peca.nome_peca}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando uma peça
        session.add(peca)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado peça: %s"% peca)
        return apresenta_material(peca), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Peça de mesmo nome e marca já salvo na base :/"
        logger.warning(f"Erro ao adicionar peça '{peca.nome_peca}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova peça :/"
        logger.warning(f"Erro ao adicionar peça '{peca.nome_peca}', {error_msg}")
        return {"mesage": error_msg}, 400


#@app.get('/peca', tags=[peca_tag],
#         responses={"200": PecaViewSchema, "404": ErrorSchema})
#def get_peca(query: PecaBuscaPorIDSchema):
#    """Faz a busca por uma peça a partir do seu id.
#
#    Retorna uma representação das peças.
#    """
#    peca_id = query.id
#    logger.info(f"Coletando dados sobre a peça #{peca_id}")
#    # criando conexão com a base
#    session = Session()
#    # fazendo a busca
#    peca = session.query(Peca).filter(Peca.id == peca_id).first()
#
#    if not peca:
#        # se a peça não for encontradada
#        error_msg = "Peça não encontrada na base :/"
#        logger.warning(f"Erro ao buscar a peça '{peca_id}', {error_msg}")
#        return {"mesage": error_msg}, 404
#    else:
#        logger.info("Peça encontrada: %s" % peca)
#        # retorna a representação da peça
#        return apresenta_material(peca), 200


@app.delete('/peca', tags=[peca_tag],
            responses={"200": PecaDelSchema, "404": ErrorSchema})
def del_peca(query: PecaBuscaPorIDSchema):
    """Deleta uma peça a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    peca_id = query.id
    logger.info(f"Deletando dados sobre a peça #{peca_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Peca).filter(Peca.id == peca_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Peça deletada #{peca_id}")
        return {"mesage": "Peça removida", "id": peca_id}
    else:
        # se a peça não for encontradada
        error_msg = "Peça não encontrada na base :/"
        logger.warning(f"Erro ao deletar a peça #'{peca_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/busca_peca', tags=[peca_tag],
         responses={"200": ListagemPecaSchema, "404": ErrorSchema})
def busca_peca(query: PecaBuscaPorNomeSchema):
    """Faz a busca por peças usando um termo qualquer a partir de seu id.

    Retorna uma representação das peças.
    """
    termo = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome com o termo: {termo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção

    pecas = session.query(Peca).filter(Peca.nome_peca.ilike(f"%{termo}%")).all()
    # pecas = session.query(Suprimento, Peca).join(Suprimento.nome_suprimento, Peca.nome_veiculo).all()
    
    print(pecas)
    
    if not pecas:
        # se não há peças cadastradas
        return {"peças": []}, 200
    else:
        logger.info(f"%d peças econtradas" % len(pecas))
        # retorna a representação da peça
        return apresenta_materiais(pecas), 200


@app.put('/updatePeca', tags=[peca_tag],
          responses={"200": UpdatePecaSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_peca(form: UpdatePecaSchema):
    """Edita uma peça já salva na base de dados

    Retorna uma representação das peças.
    """
    nome_peca = form.id
    session = Session()

    try:
        query = session.query(Peca).filter(Peca.id == nome_peca)
        print(query)
        db_peca = query.first()
        if not db_peca:
            # se peça não for encontrada
            error_msg = "Peça não encontrada na base :/"
            logger.warning(f"Erro ao buscar a peça '{nome_peca}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            if form.nome_peca:
                db_peca.nome_peca = form.nome_peca
            if form.modelo_peca:  
                db_peca.modelo_peca = form.modelo_peca
            if form.cod_peca:
                db_peca.cod_peca=form.cod_peca
            
            session.add(db_peca)
            session.commit()
            logger.debug(f"Editada peça de id: '{db_peca.id}'")
            return apresenta_material(db_peca), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar a peça '{db_peca.id}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/pecasapi', tags=[peca_tag],
         responses={"200": ListagemPecaSchema, "404": ErrorSchema})
def get_pecas():     
    """Faz a busca por todos as peças cadastradas no banco de dados.

    Retorna uma representação da lista de peças.
    """

    logger.debug(f"Coletando peças ")
    # criando conexão com a base
    session = Session()
    pecas = session.query(Peca).order_by(Peca.nome_peca.asc()).all()
    

    if not pecas:
        # se não há peças cadastradas
        return {"pecas": []}, 200
    else:
        logger.debug(f"%d peças encontradas" % len(pecas))
        # retorna a representação da peça
        print(pecas)
        return apresenta_materiais(pecas), 200
    

@app.get('/pecas', tags=[peca_tag],
         responses={"200": PecaViewSchema, "404": ErrorSchema})
def get_mercadoria(query: PecaBuscaSchema):
    """Faz a busca por uma peca a partir do seu nome.

    Retorna uma representação dos pecas.
    """
    nome_mercadoria = query.nome_peca
    logger.debug(f"Coletando dados sobre peca #{nome_mercadoria}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    mercadoria = session.query(Peca).filter(Peca.nome_peca == nome_mercadoria).first()

    if not mercadoria:
        # se o fornecedor não foi encontrado
        error_msg = "Peca não localizado no banco :/"
        logger.warning(f"Erro ao buscar o usuario '{nome_mercadoria}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pecas encontradas: '{mercadoria.nome_peca}'") 
        # retorna a representação de fornecedor
        return apresenta_material(mercadoria), 200
from sqlalchemy import Column, String, Integer

from  models import Base


class Peca(Base):

    __tablename__ = 'pecas'

    id = Column("pk_cod_pecas", Integer, primary_key=True)
    nome_peca = Column(String(50))
    modelo_peca = Column(String(20))
    cod_peca = Column(String(20))
    
    

    def __init__(self, nome_peca:str, modelo_peca:str, cod_peca:str):
        """
        Cria uma Peça

        Arguments:
            nome_peca: nome da Peça.
            modelo_peca: identificação do tipo de peça
            cod_peca: numero de identificação da peça
        """
        self.nome_peca = nome_peca
        self.modelo_peca = modelo_peca
        self.cod_peca = cod_peca
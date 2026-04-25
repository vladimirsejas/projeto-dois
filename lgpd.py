from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, text
from datetime import datetime

# Conexão com o banco
engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2")
metadata = MetaData()

# Estrutura da tabela (já existe no banco, mas definimos para o SQLAlchemy reconhecer)
usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

# Funções de anonimização
def anonimizar_nome(nome):
    partes = nome.split()
    if len(partes) > 0:
        partes[0] = partes[0][0] + "*" * (len(partes[0]) - 1)
    return " ".join(partes)

def anonimizar_cpf(cpf):
    return cpf[:3] + ".***.***-**"

def anonimizar_email(email):
    usuario, dominio = email.split("@")
    return usuario[0] + "*" * (len(usuario) - 1) + "@" + dominio

def anonimizar_telefone(telefone):
    return telefone[-4:]

# Função LGPD ajustada
def LGPD(row):
    id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on = row
    nome = anonimizar_nome(nome)
    cpf = anonimizar_cpf(cpf)
    email = anonimizar_email(email)
    telefone = anonimizar_telefone(telefone)
    return (id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on)

# Teste só roda se você executar diretamente este arquivo
if __name__ == "__main__":
    users = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
        for row in result:
            row = LGPD(row)
            users.append(row)

    for user in users:
        print(user)

from lgpd import LGPD, engine  # importa a função LGPD e a conexão
import pandas as pd
from sqlalchemy import text

def exportar_por_ano():
    users = []
    # Consulta todos os registros do banco
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;"))
        for row in result:
            row = LGPD(row)  # aplica anonimização
            users.append(row)

    # Cria DataFrame com os registros anonimizados
    df = pd.DataFrame(users, columns=[
        "id", "nome", "cpf", "email", "telefone", 
        "data_nascimento", "created_on", "updated_on"
    ])

    # Converte a coluna para datetime (garante que .dt.year funcione)
    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"])

    # Exporta por ano de nascimento
    for ano in df["data_nascimento"].dt.year.unique():
        df_ano = df[df["data_nascimento"].dt.year == ano]
        df_ano.to_csv(f"{ano}.csv", index=False)
        print(f"Arquivo {ano}.csv criado com {len(df_ano)} registros.")

if __name__ == "__main__":
    exportar_por_ano()

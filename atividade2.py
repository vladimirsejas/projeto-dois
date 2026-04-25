from lgpd import LGPD, engine
from atividade4 import medir_tempo
import pandas as pd
from sqlalchemy import text

@medir_tempo
def exportar_por_ano():
    users = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;"))
        for row in result:
            row = LGPD(row)
            users.append(row)

    df = pd.DataFrame(users, columns=[
        "id", "nome", "cpf", "email", "telefone",
        "data_nascimento", "created_on", "updated_on"
    ])

    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"])

    for ano in df["data_nascimento"].dt.year.unique():
        df_ano = df[df["data_nascimento"].dt.year == ano]
        df_ano.to_csv(f"{ano}.csv", index=False)
        print(f"Arquivo {ano}.csv criado com {len(df_ano)} registros.")

if __name__ == "__main__":
    exportar_por_ano()
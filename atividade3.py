from lgpd import engine
from atividade4 import medir_tempo
import pandas as pd
from sqlalchemy import text

@medir_tempo
def exportar_todos():
    users = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT nome, cpf FROM usuarios;"))
        for row in result:
            users.append(row)

    df = pd.DataFrame(users, columns=["nome", "cpf"])
    df.to_csv("todos.csv", index=False)
    print(f"Arquivo todos.csv criado com {len(df)} registros.")

if __name__ == "__main__":
    exportar_todos()
import time
import logging
from functools import wraps

logging.basicConfig(
    filename="tempo_execucao.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        duracao = fim - inicio
        logging.info(f"Função {func.__name__} executada em {duracao:.2f} segundos")
        print(f"Função {func.__name__} executada em {duracao:.2f} segundos")
        return resultado
    return wrapper
import time
import sys
print(sys.path)
from lgpd import (
    anonimizar_nome,
    anonimizar_cpf,
    anonimizar_email,
    anonimizar_telefone,
    LGPD,
)
from atividade4 import medir_tempo


# =========================
# TESTES — anonimizar_nome
# =========================

class TestAnonimizarNome:
    def test_primeira_letra_preservada(self):
        resultado = anonimizar_nome("Vladimir Sejas")
        assert resultado.startswith("V")

    def test_nome_unico_anonimizado(self):
        resultado = anonimizar_nome("Maria")
        assert resultado == "M****"

    def test_nome_vazio(self):
        resultado = anonimizar_nome("")
        assert resultado == ""


# =========================
# TESTES — anonimizar_cpf
# =========================

class TestAnonimizarCpf:
    def test_formato_correto(self):
        resultado = anonimizar_cpf("123.456.789-00")
        assert resultado == "123.***.***-**"


# =========================
# TESTES — anonimizar_email
# =========================

class TestAnonimizarEmail:
    def test_email_mascarado(self):
        resultado = anonimizar_email("teste@email.com")
        assert resultado.endswith("@email.com")
        assert resultado[0] == "t"


# =========================
# TESTES — anonimizar_telefone
# =========================

class TestAnonimizarTelefone:
    def test_ultimos_4_digitos(self):
        resultado = anonimizar_telefone("(19) 99999-1234")
        assert resultado == "1234"


# =========================
# TESTES — LGPD (integração)
# =========================

class TestLGPD:
    def test_lgpd(self):
        from datetime import date, datetime

        row = (
            1,
            "Vladimir Sejas",
            "123.456.789-00",
            "vladimir@gmail.com",
            "(19) 99999-1234",
            date(1990, 5, 15),
            datetime(2024, 1, 1),
            datetime(2024, 6, 1),
        )

        resultado = LGPD(row)

        assert resultado[0] == 1
        assert resultado[1].startswith("V")
        assert resultado[2] == "123.***.***-**"
        assert resultado[4] == "1234"


# =========================
# TESTES — decorador
# =========================

class TestDecorador:
    def test_decorador(self):
        @medir_tempo
        def soma(a, b):
            return a + b

        assert soma(2, 3) == 5

    def test_kwargs(self):
        @medir_tempo
        def cumprimento(nome="mundo"):
            return f"Olá, {nome}!"

        assert cumprimento(nome="FATEC") == "Olá, FATEC!"


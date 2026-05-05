import pytest
from services.stock_service import validar_cantidad_positiva


class TestValidarCantidadPositivaLimites:

    def test_cantidad_cero_no_es_valida(self):
        """Valor límite: 0 está justo en la frontera inferior y es inválido"""
        assert validar_cantidad_positiva(0) is False

    def test_cantidad_negativa_no_es_valida(self):
        """Valor inmediatamente inferior al límite: -1 debe ser rechazado"""
        assert validar_cantidad_positiva(-1) is False

    def test_cantidad_uno_es_valida(self):
        """Primer valor entero positivo después del límite: 1 es válido"""
        assert validar_cantidad_positiva(1) is True

import pytest
from services.stock_service import validar_salida_stock


class TestValidarSalidaStockEquivalencia:

    def test_salida_menor_al_stock_es_permitida(self):
        """Clase válida: cantidad < stock disponible"""
        assert validar_salida_stock(10, 5) is True

    def test_salida_mayor_al_stock_es_rechazada(self):
        """Clase inválida: cantidad > stock disponible"""
        assert validar_salida_stock(10, 15) is False

    def test_salida_con_cantidad_cero_es_rechazada(self):
        """Clase inválida: cantidad = 0 no debe permitirse"""
        assert validar_salida_stock(10, 0) is False

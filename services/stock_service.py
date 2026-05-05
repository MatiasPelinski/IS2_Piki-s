def validar_salida_stock(stock_actual: int, cantidad_salida: int) -> bool:
    """
    Retorna True si la salida es permitida (stock suficiente y cantidad positiva).
    """
    if stock_actual < 0 or cantidad_salida <= 0:
        return False
    if cantidad_salida > stock_actual:
        return False
    return True


def validar_cantidad_positiva(cantidad: int) -> bool:
    """
    Retorna True si la cantidad es mayor que 0.
    """
    return cantidad > 0

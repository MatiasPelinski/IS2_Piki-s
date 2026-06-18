from decimal import Decimal, ROUND_HALF_UP


def calcular_precio_ipc(precio_actual, porcentaje_ipc):
    precio = Decimal(str(precio_actual))
    ipc = Decimal(str(porcentaje_ipc))

    factor = Decimal('1') + (ipc / Decimal('100'))
    precio_nuevo = precio * factor

    return precio_nuevo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def test_actualizacion_ipc_5_por_ciento():
    assert calcular_precio_ipc('2500', '5') == Decimal('2625.00')
    assert calcular_precio_ipc('25', '5') == Decimal('26.25')
    assert calcular_precio_ipc('8500', '5') == Decimal('8925.00')


def test_actualizacion_ipc_3_5_por_ciento():
    assert calcular_precio_ipc('10000', '3.5') == Decimal('10350.00')


def test_actualizacion_ipc_redondeo_a_dos_decimales():
    assert calcular_precio_ipc('99.99', '3.5') == Decimal('103.49')


def test_actualizacion_ipc_no_modifica_precio_cero():
    assert calcular_precio_ipc('0', '5') == Decimal('0.00')
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import mysql.connector
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from config import DB_CONFIG


ipc_bp = Blueprint('ipc', __name__)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def usuario_puede_actualizar_precios():
    return session.get('usuario_rol') in ['encargado', 'admin']


def convertir_decimal(valor):
    if valor is None:
        return Decimal('0.00')

    return Decimal(str(valor))


def calcular_precio_ipc(precio_actual, porcentaje_ipc):
    precio = convertir_decimal(precio_actual)
    ipc = convertir_decimal(porcentaje_ipc)

    factor = Decimal('1') + (ipc / Decimal('100'))
    precio_nuevo = precio * factor

    return precio_nuevo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def validar_porcentaje_ipc(valor):
    if valor is None or str(valor).strip() == '':
        return False, None, 'Debe ingresar un porcentaje de IPC.'

    valor_normalizado = str(valor).strip().replace(',', '.')

    try:
        porcentaje = Decimal(valor_normalizado)
    except (InvalidOperation, ValueError):
        return False, None, 'El porcentaje de IPC debe ser un número válido.'

    if porcentaje <= 0:
        return False, None, 'El porcentaje de IPC debe ser mayor que cero.'

    if porcentaje > 100:
        return False, None, 'El porcentaje ingresado es demasiado alto. Verifique el valor antes de continuar.'

    return True, porcentaje, ''


def obtener_productos_activos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.stock_actual,
            p.stock_minimo,
            COALESCE(c.nombre, 'Sin categoría') AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.activo = 1
        ORDER BY p.nombre
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return productos


def separar_productos_por_precio(productos):
    productos_con_precio = []
    productos_sin_precio = []

    for producto in productos:
        precio = convertir_decimal(producto.get('precio'))

        if precio > 0:
            productos_con_precio.append(producto)
        else:
            productos_sin_precio.append(producto)

    return productos_con_precio, productos_sin_precio


def obtener_historial_ipc():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.*,
            u.nombre AS usuario_nombre
        FROM actualizaciones_precios_ipc a
        JOIN usuarios u ON a.id_usuario = u.id
        ORDER BY a.fecha_actualizacion DESC
        LIMIT 10
    """)

    historial = cursor.fetchall()

    cursor.close()
    conn.close()

    return historial


def construir_vista_previa(productos_con_precio, porcentaje):
    vista_previa = []
    precio_total_anterior = Decimal('0.00')
    precio_total_nuevo = Decimal('0.00')

    for producto in productos_con_precio:
        precio_anterior = convertir_decimal(producto['precio'])
        precio_nuevo = calcular_precio_ipc(precio_anterior, porcentaje)
        diferencia = precio_nuevo - precio_anterior

        precio_total_anterior += precio_anterior
        precio_total_nuevo += precio_nuevo

        vista_previa.append({
            'id': producto['id'],
            'nombre': producto['nombre'],
            'categoria_nombre': producto['categoria_nombre'],
            'precio_anterior': precio_anterior,
            'precio_nuevo': precio_nuevo,
            'diferencia': diferencia
        })

    return vista_previa, precio_total_anterior, precio_total_nuevo


@ipc_bp.route('/precios/ipc', methods=['GET', 'POST'])
def actualizar_precios_ipc():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if not usuario_puede_actualizar_precios():
        flash('No tenés permisos para actualizar precios por IPC.', 'error')
        return redirect(url_for('productos'))

    productos = obtener_productos_activos()
    productos_con_precio, productos_sin_precio = separar_productos_por_precio(productos)
    historial = obtener_historial_ipc()

    porcentaje_ipc = ''
    vista_previa = []
    resumen = {
        'productos_activos': len(productos),
        'productos_con_precio': len(productos_con_precio),
        'productos_sin_precio': len(productos_sin_precio),
        'productos_actualizados': 0,
        'porcentaje_ipc': None,
        'precio_total_anterior': Decimal('0.00'),
        'precio_total_nuevo': Decimal('0.00'),
        'diferencia_total': Decimal('0.00')
    }

    if request.method == 'POST':
        porcentaje_ipc = request.form.get('porcentaje_ipc')

        es_valido, porcentaje, mensaje_error = validar_porcentaje_ipc(porcentaje_ipc)

        if not es_valido:
            flash(mensaje_error, 'error')
            return render_template(
                'actualizar_precios_ipc.html',
                nombre=session['usuario_nombre'],
                rol=session['usuario_rol'],
                productos=productos,
                productos_con_precio=productos_con_precio,
                productos_sin_precio=productos_sin_precio,
                historial=historial,
                porcentaje_ipc=porcentaje_ipc,
                vista_previa=vista_previa,
                resumen=resumen
            )

        vista_previa, precio_total_anterior, precio_total_nuevo = construir_vista_previa(
            productos_con_precio=productos_con_precio,
            porcentaje=porcentaje
        )

        resumen = {
            'productos_activos': len(productos),
            'productos_con_precio': len(productos_con_precio),
            'productos_sin_precio': len(productos_sin_precio),
            'productos_actualizados': len(vista_previa),
            'porcentaje_ipc': porcentaje,
            'precio_total_anterior': precio_total_anterior,
            'precio_total_nuevo': precio_total_nuevo,
            'diferencia_total': precio_total_nuevo - precio_total_anterior
        }

        if 'confirmar_actualizacion' in request.form:
            if not vista_previa:
                flash('No existen productos con precio válido para actualizar. Primero cargá precios base mayores a cero.', 'error')
                return redirect(url_for('ipc.actualizar_precios_ipc'))

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO actualizaciones_precios_ipc
                    (
                        id_usuario,
                        porcentaje_ipc,
                        productos_actualizados,
                        precio_total_anterior,
                        precio_total_nuevo
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    session['usuario_id'],
                    str(porcentaje),
                    len(vista_previa),
                    str(precio_total_anterior),
                    str(precio_total_nuevo)
                ))

                id_actualizacion = cursor.lastrowid

                for fila in vista_previa:
                    cursor.execute("""
                        UPDATE productos
                        SET precio = %s
                        WHERE id = %s
                    """, (
                        str(fila['precio_nuevo']),
                        fila['id']
                    ))

                    cursor.execute("""
                        INSERT INTO actualizaciones_precios_ipc_detalle
                        (
                            id_actualizacion,
                            id_producto,
                            nombre_producto,
                            precio_anterior,
                            precio_nuevo,
                            diferencia
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        id_actualizacion,
                        fila['id'],
                        fila['nombre'],
                        str(fila['precio_anterior']),
                        str(fila['precio_nuevo']),
                        str(fila['diferencia'])
                    ))

                conn.commit()

                flash(
                    f'Actualización aplicada correctamente. Se modificaron {len(vista_previa)} productos con IPC de {porcentaje}%.',
                    'success'
                )

                cursor.close()
                conn.close()

                return redirect(url_for('ipc.actualizar_precios_ipc'))

            except Exception as error:
                conn.rollback()
                cursor.close()
                conn.close()

                flash(f'No se pudo aplicar la actualización por IPC: {str(error)}', 'error')
                return redirect(url_for('ipc.actualizar_precios_ipc'))

    return render_template(
        'actualizar_precios_ipc.html',
        nombre=session['usuario_nombre'],
        rol=session['usuario_rol'],
        productos=productos,
        productos_con_precio=productos_con_precio,
        productos_sin_precio=productos_sin_precio,
        historial=historial,
        porcentaje_ipc=porcentaje_ipc,
        vista_previa=vista_previa,
        resumen=resumen
    )
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import DB_CONFIG
import openpyxl
import os
from decimal import Decimal, InvalidOperation
from werkzeug.utils import secure_filename
from datetime import datetime, date
import unicodedata

app = Flask(__name__)
app.secret_key = "ferreteria_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# CONEXIÓN A BASE DE DATOS
# ============================================================

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# HELPERS GENERALES
# ============================================================

def normalizar_texto(texto):
    if texto is None:
        return ""

    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto


def to_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default


def to_decimal(value, default="0.00"):
    try:
        if value is None or value == "":
            return Decimal(default)
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


def format_excel_date(value):
    if value is None:
        return "Sin fecha"

    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")

    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")

    return str(value)


def get_active_categories(cursor):
    cursor.execute("""
        SELECT *
        FROM categorias
        WHERE activo = 1
        ORDER BY nombre
    """)
    return cursor.fetchall()


def get_default_category_id(cursor):
    cursor.execute("""
        SELECT id
        FROM categorias
        WHERE activo = 1
        ORDER BY id
        LIMIT 1
    """)
    categoria = cursor.fetchone()

    if categoria:
        return categoria["id"]

    cursor.execute("""
        INSERT INTO categorias (nombre, descripcion, activo)
        VALUES (%s, %s, 1)
    """, ("Sin categoría", "Categoría generada automáticamente"))

    return cursor.lastrowid


def buscar_producto_por_nombre(cursor, nombre_producto):
    nombre_producto = str(nombre_producto).strip()

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE LOWER(nombre) = LOWER(%s)
        AND activo = 1
        LIMIT 1
    """, (nombre_producto,))
    producto = cursor.fetchone()

    if producto:
        return producto

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE nombre LIKE %s
        AND activo = 1
        ORDER BY nombre
        LIMIT 1
    """, (f"%{nombre_producto}%",))

    return cursor.fetchone()


def verificar_alerta_stock(cursor, id_producto, nombre_producto, stock_actual, stock_minimo):
    """
    Función relacionada al patrón Observer:
    cuando cambia el stock de un producto, el sistema observa ese cambio
    y genera o resuelve alertas automáticamente.
    """

    if stock_actual < stock_minimo:
        mensaje = f"Stock de '{nombre_producto}' ({stock_actual}) está por debajo del mínimo ({stock_minimo})."

        cursor.execute("""
            INSERT INTO alertas (tipo, mensaje, id_producto)
            SELECT %s, %s, %s FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1
                FROM alertas
                WHERE id_producto = %s
                AND resuelta = 0
            )
        """, ("stock_bajo", mensaje, id_producto, id_producto))

    else:
        cursor.execute("""
            UPDATE alertas
            SET resuelta = 1
            WHERE id_producto = %s
            AND resuelta = 0
        """, (id_producto,))


# ============================================================
# LOGIN
# ============================================================

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE email = %s
            AND password = %s
            AND activo = 1
        """, (email, password))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            session["usuario_rol"] = usuario["rol"]

            # Se mantiene también session["rol"] por compatibilidad con templates viejos.
            session["rol"] = usuario["rol"]

            if usuario["rol"] == "empleado":
                return redirect(url_for("productos"))

            return redirect(url_for("dashboard"))

        error = "Email o contraseña incorrectos."

    return render_template("login.html", error=error)


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") == "empleado":
        return redirect(url_for("productos"))

    busqueda = request.args.get("busqueda", "").strip()
    categoria_filtro = request.args.get("categoria", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM productos
        WHERE activo = 1
    """)
    total_productos = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM alertas
        WHERE resuelta = 0
    """)
    total_alertas = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM productos
        WHERE stock_actual < stock_minimo
        AND activo = 1
    """)
    total_reponer = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM movimientos_stock
        WHERE DATE(fecha) = CURDATE()
    """)
    movimientos_hoy = cursor.fetchone()["total"]

    categorias = get_active_categories(cursor)

    productos_busqueda = None

    if busqueda or categoria_filtro:
        query = """
            SELECT p.*, c.nombre AS categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id
            WHERE p.activo = 1
        """
        params = []

        if busqueda:
            query += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])

        if categoria_filtro:
            query += " AND p.id_categoria = %s"
            params.append(categoria_filtro)

        query += " ORDER BY p.nombre LIMIT 15"

        cursor.execute(query, params)
        productos_busqueda = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"],
        total_productos=total_productos,
        total_alertas=total_alertas,
        total_reponer=total_reponer,
        movimientos_hoy=movimientos_hoy,
        categorias=categorias,
        busqueda=busqueda,
        categoria_filtro=categoria_filtro,
        productos_busqueda=productos_busqueda
    )


# ============================================================
# PRODUCTOS
# ============================================================

@app.route("/productos", methods=["GET", "POST"])
def productos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # Compatibilidad: si algún formulario viejo manda POST a /productos,
    # lo redirigimos al alta de producto.
    if request.method == "POST":
        return registrar_producto()

    busqueda = request.args.get("busqueda", "").strip()
    categoria_filtro = request.args.get("categoria", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.activo = 1
    """
    params = []

    if busqueda:
        query += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
        params.extend([f"%{busqueda}%", f"%{busqueda}%"])

    if categoria_filtro:
        query += " AND p.id_categoria = %s"
        params.append(categoria_filtro)

    query += " ORDER BY p.nombre"

    cursor.execute(query, params)
    lista_productos = cursor.fetchall()

    categorias = get_active_categories(cursor)

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=lista_productos,
        categorias=categorias,
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"],
        busqueda=busqueda,
        categoria_filtro=categoria_filtro
    )


@app.route("/productos/registrar", methods=["POST"])
def registrar_producto():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") not in ["admin", "encargado"]:
        flash("No tenés permisos para registrar productos nuevos.", "error")
        return redirect(url_for("productos"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    precio = to_decimal(request.form.get("precio"))
    stock_actual = to_int(request.form.get("stock_actual"))
    stock_minimo = to_int(request.form.get("stock_minimo"))
    id_categoria = request.form.get("id_categoria") or None

    if not nombre:
        flash("El nombre del producto es obligatorio.", "error")
        return redirect(url_for("productos"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO productos (
            nombre,
            descripcion,
            precio,
            stock_actual,
            stock_minimo,
            id_categoria
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        nombre,
        descripcion,
        str(precio),
        stock_actual,
        stock_minimo,
        id_categoria
    ))

    id_producto = cursor.lastrowid

    verificar_alerta_stock(
        cursor,
        id_producto,
        nombre,
        stock_actual,
        stock_minimo
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Producto registrado correctamente.", "success")
    return redirect(url_for("productos"))


# ============================================================
# MOVIMIENTOS
# ============================================================

@app.route("/movimientos", methods=["GET", "POST"])
def movimientos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # Compatibilidad: si algún formulario viejo manda POST a /movimientos,
    # ejecutamos la misma lógica que /movimientos/registrar.
    if request.method == "POST":
        return registrar_movimiento()

    selected_producto_id = request.args.get("producto_id", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE activo = 1
        ORDER BY nombre
    """)
    lista_productos = cursor.fetchall()

    cursor.execute("""
        SELECT 
            m.*,
            p.nombre AS producto_nombre,
            u.nombre AS usuario_nombre,
            p.stock_actual,
            p.stock_minimo
        FROM movimientos_stock m
        JOIN productos p ON m.id_producto = p.id
        JOIN usuarios u ON m.id_usuario = u.id
        ORDER BY m.fecha DESC
        LIMIT 50
    """)
    lista_movimientos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "movimientos.html",
        productos=lista_productos,
        movimientos=lista_movimientos,
        selected_producto_id=selected_producto_id,
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"]
    )


@app.route("/movimientos/registrar", methods=["POST"])
def registrar_movimiento():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    id_producto = to_int(request.form.get("id_producto"))
    tipo = request.form.get("tipo", "").strip()
    cantidad = to_int(request.form.get("cantidad"))
    motivo = request.form.get("motivo", "").strip()

    if not id_producto or tipo not in ["entrada", "salida", "ajuste"] or cantidad <= 0:
        flash("Datos de movimiento inválidos.", "error")
        return redirect(url_for("movimientos"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id = %s
        AND activo = 1
    """, (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        flash("El producto seleccionado no existe.", "error")
        return redirect(url_for("movimientos"))

    # Patrón Strategy: cada tipo de movimiento tiene una lógica distinta.
    if tipo == "entrada":
        nuevo_stock = producto["stock_actual"] + cantidad

    elif tipo == "salida":
        if cantidad > producto["stock_actual"]:
            cursor.close()
            conn.close()
            flash("No se puede registrar una salida mayor al stock disponible.", "error")
            return redirect(url_for("movimientos"))

        nuevo_stock = producto["stock_actual"] - cantidad

    else:
        nuevo_stock = cantidad

    cursor.execute("""
        UPDATE productos
        SET stock_actual = %s
        WHERE id = %s
    """, (nuevo_stock, id_producto))

    cursor.execute("""
        INSERT INTO movimientos_stock (
            tipo,
            cantidad,
            motivo,
            id_producto,
            id_usuario
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        tipo,
        cantidad,
        motivo,
        id_producto,
        session["usuario_id"]
    ))

    verificar_alerta_stock(
        cursor,
        producto["id"],
        producto["nombre"],
        nuevo_stock,
        producto["stock_minimo"]
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Movimiento registrado correctamente.", "success")
    return redirect(url_for("movimientos"))


# ============================================================
# IMPORTAR EXCEL
# ============================================================

@app.route("/importar", methods=["GET", "POST"])
def importar():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") not in ["admin", "encargado"]:
        flash("No tenés permisos para importar archivos.", "error")
        return redirect(url_for("dashboard"))

    resultados = []
    errores = []

    if request.method == "POST":
        archivo = (
            request.files.get("archivo")
            or request.files.get("archivo_excel")
            or request.files.get("excel")
            or request.files.get("file")
        )

        if not archivo or archivo.filename == "":
            flash("Debés seleccionar un archivo Excel.", "error")
            return render_template(
                "importar.html",
                nombre=session["usuario_nombre"],
                rol=session["usuario_rol"],
                resultados=resultados,
                errores=errores
            )

        filename = secure_filename(archivo.filename)

        if not filename.lower().endswith(".xlsx"):
            flash("El archivo debe ser un Excel en formato .xlsx.", "error")
            return render_template(
                "importar.html",
                nombre=session["usuario_nombre"],
                rol=session["usuario_rol"],
                resultados=resultados,
                errores=errores
            )

        ruta = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(ruta)

        try:
            wb = openpyxl.load_workbook(ruta)
            ws = wb.active
            filas = list(ws.iter_rows(values_only=True))

            if len(filas) < 2:
                errores.append("El archivo no contiene filas para importar.")
            else:
                headers = [
                    normalizar_texto(celda)
                    for celda in filas[0]
                ]

                conn = get_db_connection()
                cursor = conn.cursor(dictionary=True)

                es_formato_proveedor = (
                    "proveedor" in headers
                    and "producto" in headers
                    and "cantidad" in headers
                )

                if es_formato_proveedor:
                    idx_proveedor = headers.index("proveedor")
                    idx_producto = headers.index("producto")
                    idx_cantidad = headers.index("cantidad")

                    idx_fecha = headers.index("fecha") if "fecha" in headers else None

                    idx_precio = None
                    for posible_nombre in ["precio unitario", "precio", "precio_unitario"]:
                        if posible_nombre in headers:
                            idx_precio = headers.index(posible_nombre)
                            break

                    for numero_fila, fila in enumerate(filas[1:], start=2):
                        if not fila or not any(fila):
                            continue

                        proveedor = (
                            str(fila[idx_proveedor]).strip()
                            if idx_proveedor < len(fila) and fila[idx_proveedor]
                            else "Proveedor no informado"
                        )

                        fecha_excel = (
                            format_excel_date(fila[idx_fecha])
                            if idx_fecha is not None and idx_fecha < len(fila)
                            else "Sin fecha"
                        )

                        nombre_producto = (
                            str(fila[idx_producto]).strip()
                            if idx_producto < len(fila) and fila[idx_producto]
                            else ""
                        )

                        cantidad = (
                            to_int(fila[idx_cantidad])
                            if idx_cantidad < len(fila)
                            else 0
                        )

                        precio_unitario = (
                            to_decimal(fila[idx_precio])
                            if idx_precio is not None and idx_precio < len(fila)
                            else Decimal("0.00")
                        )

                        if not nombre_producto or cantidad <= 0:
                            errores.append(
                                f"Fila {numero_fila} omitida: producto o cantidad inválida."
                            )
                            continue

                        producto = buscar_producto_por_nombre(cursor, nombre_producto)

                        if producto:
                            nuevo_stock = producto["stock_actual"] + cantidad

                            cursor.execute("""
                                UPDATE productos
                                SET 
                                    stock_actual = %s,
                                    precio = CASE
                                        WHEN %s > 0 THEN %s
                                        ELSE precio
                                    END
                                WHERE id = %s
                            """, (
                                nuevo_stock,
                                float(precio_unitario),
                                str(precio_unitario),
                                producto["id"]
                            ))

                            id_producto = producto["id"]
                            nombre_final = producto["nombre"]
                            stock_minimo = producto["stock_minimo"]
                            creado = False

                        else:
                            id_categoria = get_default_category_id(cursor)

                            cursor.execute("""
                                INSERT INTO productos (
                                    nombre,
                                    descripcion,
                                    precio,
                                    stock_actual,
                                    stock_minimo,
                                    id_categoria,
                                    activo
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, 1)
                            """, (
                                nombre_producto,
                                f"Producto creado automáticamente desde Excel del proveedor {proveedor}",
                                str(precio_unitario),
                                cantidad,
                                0,
                                id_categoria
                            ))

                            id_producto = cursor.lastrowid
                            nombre_final = nombre_producto
                            nuevo_stock = cantidad
                            stock_minimo = 0
                            creado = True

                        motivo = f"Ingreso por proveedor: {proveedor} — fecha factura: {fecha_excel}"

                        cursor.execute("""
                            INSERT INTO movimientos_stock (
                                tipo,
                                cantidad,
                                motivo,
                                id_producto,
                                id_usuario
                            )
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            "entrada",
                            cantidad,
                            motivo,
                            id_producto,
                            session["usuario_id"]
                        ))

                        verificar_alerta_stock(
                            cursor,
                            id_producto,
                            nombre_final,
                            nuevo_stock,
                            stock_minimo
                        )

                        resultados.append({
                            "producto": nombre_final,
                            "proveedor": proveedor,
                            "cantidad": cantidad,
                            "stock_nuevo": nuevo_stock,
                            "creado": creado
                        })

                else:
                    errores.append(
                        "El Excel no tiene el formato esperado. Debe incluir columnas: Proveedor, Fecha, Producto, Cantidad, Precio Unitario, Total."
                    )

                conn.commit()
                cursor.close()
                conn.close()

                if resultados:
                    flash(f"Importación completada: {len(resultados)} productos procesados.", "success")

                if errores:
                    flash(f"Importación finalizada con {len(errores)} advertencias.", "error")

        except Exception as e:
            errores.append(f"Error al procesar el archivo: {str(e)}")
            flash(f"Error al procesar el archivo: {str(e)}", "error")

        finally:
            if os.path.exists(ruta):
                os.remove(ruta)

    return render_template(
        "importar.html",
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"],
        resultados=resultados,
        errores=errores
    )


# ============================================================
# ALERTAS
# ============================================================

@app.route("/alertas")
def alertas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.id,
            a.tipo,
            a.mensaje,
            a.resuelta,
            a.fecha,
            p.id AS id_producto,
            p.nombre AS producto_nombre,
            p.stock_actual,
            p.stock_minimo,
            c.nombre AS categoria_nombre
        FROM alertas a
        JOIN productos p ON a.id_producto = p.id
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE a.resuelta = 0
        ORDER BY a.fecha DESC
    """)
    lista_alertas = cursor.fetchall()

    cursor.execute("""
        SELECT 
            p.*,
            c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.stock_actual < p.stock_minimo
        AND p.activo = 1
        ORDER BY (p.stock_minimo - p.stock_actual) DESC
    """)
    productos_reponer = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "alertas.html",
        alertas=lista_alertas,
        productos_reponer=productos_reponer,
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"]
    )


@app.route("/alertas/resolver/<int:id>")
def resolver_alerta(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") not in ["admin", "encargado"]:
        flash("No tenés permisos para resolver alertas.", "error")
        return redirect(url_for("alertas"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alertas
        SET resuelta = 1
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Alerta marcada como resuelta.", "success")
    return redirect(url_for("alertas"))


# ============================================================
# USUARIOS
# ============================================================

@app.route("/usuarios", methods=["GET", "POST"])
def gestion_usuarios():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") not in ["admin", "encargado"]:
        flash("No tenés permisos para gestionar usuarios.", "error")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        if "registrar" in request.form:
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            rol = request.form.get("rol", "empleado")

            if rol not in ["empleado", "encargado"]:
                rol = "empleado"

            cursor.execute("""
                SELECT id
                FROM usuarios
                WHERE email = %s
            """, (email,))

            if cursor.fetchone():
                flash("El correo ya está asignado a otro usuario.", "error")
            else:
                cursor.execute("""
                    INSERT INTO usuarios (
                        nombre,
                        email,
                        password,
                        rol,
                        activo
                    )
                    VALUES (%s, %s, %s, %s, 1)
                """, (
                    nombre,
                    email,
                    password,
                    rol
                ))

                conn.commit()
                flash("Usuario registrado correctamente.", "success")

        elif "eliminar" in request.form:
            usuario_id = to_int(request.form.get("usuario_id"))

            if usuario_id == session.get("usuario_id"):
                flash("No podés eliminar tu propio usuario.", "error")
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET activo = 0
                    WHERE id = %s
                """, (usuario_id,))

                conn.commit()
                flash("Usuario desactivado correctamente.", "success")

    cursor.execute("""
        SELECT id, nombre, email, rol, activo
        FROM usuarios
        WHERE activo = 1
        ORDER BY rol, nombre
    """)
    lista_usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios,
        nombre=session["usuario_nombre"],
        rol=session["usuario_rol"]
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
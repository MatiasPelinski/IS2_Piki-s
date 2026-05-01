from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import DB_CONFIG
from datetime import datetime
import openpyxl
import os

app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('login'))
app.secret_key = 'ferreteria_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # 1. Usamos TU método de conexión exacto
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 2. Pedimos la columna 'rol'
        cursor.execute('SELECT id, nombre, email, rol FROM usuarios WHERE email = %s AND password = %s', (email, password))
        usuario = cursor.fetchone()
        
        
        # 3. Cerramos la conexión para liberar memoria (
        cursor.close()
        conn.close()
        
        if usuario:
            # 4. Guardamos las credenciales usando TUS nombres de variables
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            session['usuario_email'] = usuario['email']
            
            # Guardamos el rol en ambas variables para que funcione tanto tu Dashboard 
            # como el nuevo módulo de Gestión de Personal que armamos
            session['usuario_rol'] = usuario['rol']
            session['rol'] = usuario['rol']
             
            # esto era lo q tirabba el cartelito , miren si les gusta sin o con 
            #flash(f"Acceso concedido. Rango operativo: {usuario['rol'].upper()}", "success")
            
            # Si es empleado, mandalo directo al inventario
            if usuario['rol'] == 'empleado':
                return redirect(url_for('productos'))
            
            # Otros roles (como administrador) van al dashboard
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas. Acceso denegado.", "error")
            
    return render_template('login.html')

# ─── LOGIN ───────────────────────────────────────────────

# ─── DASHBOARD ───────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
        
    # 1. Atrapamos los datos del buscador si el usuario escribió algo
    busqueda = request.args.get('busqueda', '')
    categoria_filtro = request.args.get('categoria', '')
    
    
    if session.get('usuario_rol') == 'empleado':
        return redirect(url_for('productos'))
    
    
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 2. Consultas originales de estadísticas
    cursor.execute('SELECT COUNT(*) AS total FROM productos WHERE activo = 1')
    total_productos = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) AS total FROM alertas WHERE resuelta = 0')
    total_alertas = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) AS total FROM productos WHERE stock_actual < stock_minimo AND activo = 1')
    total_reponer = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) AS total FROM movimientos_stock WHERE DATE(fecha) = CURDATE()')
    movimientos_hoy = cursor.fetchone()['total']
    
    # Obtenemos las categorías para que el selector funcione
    cursor.execute('SELECT * FROM categorias WHERE activo = 1')
    categorias = cursor.fetchall()
    
    # 3. LÓGICA NUEVA: Si hay una búsqueda, buscamos los productos
    productos_busqueda = None
    if busqueda or categoria_filtro:
        query = '''
            SELECT p.*, c.nombre AS categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id
            WHERE p.activo = 1
        '''
        params = []
        if busqueda:
            query += ' AND p.nombre LIKE %s'
            params.append(f'%{busqueda}%')
        if categoria_filtro:
            query += ' AND p.id_categoria = %s'
            params.append(categoria_filtro)
            
        query += ' ORDER BY p.nombre LIMIT 10' # Limitamos a 10 resultados para no romper el diseño del panel
        
        cursor.execute(query, params)
        productos_busqueda = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('dashboard.html',
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'],
                           total_productos=total_productos,
                           total_alertas=total_alertas,
                           total_reponer=total_reponer,
                           movimientos_hoy=movimientos_hoy,
                           categorias=categorias,
                           busqueda=busqueda,
                           categoria_filtro=categoria_filtro,
                           productos_busqueda=productos_busqueda)
# ─── PRODUCTOS ───────────────────────────────────────────
@app.route('/productos')
def productos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    busqueda = request.args.get('busqueda', '')
    categoria_filtro = request.args.get('categoria', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.activo = 1
    '''
    params = []
    if busqueda:
        query += ' AND p.nombre LIKE %s'
        params.append(f'%{busqueda}%')
    if categoria_filtro:
        query += ' AND p.id_categoria = %s'
        params.append(categoria_filtro)
    query += ' ORDER BY p.nombre'
    cursor.execute(query, params)
    lista_productos = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias WHERE activo = 1')
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html',
                           productos=lista_productos,
                           categorias=categorias,
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'],
                           busqueda=busqueda,
                           categoria_filtro=categoria_filtro)

@app.route('/productos/registrar', methods=['POST'])
def registrar_producto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_rol'] != 'encargado':
        return redirect(url_for('productos'))
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock_actual = int(request.form['stock_actual'])
    stock_minimo = int(request.form['stock_minimo'])
    id_categoria = request.form['id_categoria']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nombre, descripcion, precio, stock_actual, stock_minimo, id_categoria))
    id_producto = cursor.lastrowid
    if stock_actual < stock_minimo:
        mensaje = f"Stock inicial de '{nombre}' ({stock_actual}) está por debajo del mínimo ({stock_minimo})."
        cursor.execute('''
            INSERT INTO alertas (tipo, mensaje, id_producto)
            VALUES (%s, %s, %s)
        ''', ('stock_bajo', mensaje, id_producto))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('productos'))

# ─── MOVIMIENTOS ─────────────────────────────────────────
@app.route('/movimientos')
def movimientos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE activo = 1 ORDER BY nombre')
    lista_productos = cursor.fetchall()
    cursor.execute('''
        SELECT m.*, p.nombre AS producto_nombre, u.nombre AS usuario_nombre
        FROM movimientos_stock m
        JOIN productos p ON m.id_producto = p.id
        JOIN usuarios u ON m.id_usuario = u.id
        ORDER BY m.fecha DESC
        LIMIT 50
    ''')
    lista_movimientos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movimientos.html',
                           productos=lista_productos,
                           movimientos=lista_movimientos,
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'])

@app.route('/movimientos/registrar', methods=['POST'])
def registrar_movimiento():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    id_producto = int(request.form['id_producto'])
    tipo = request.form['tipo']
    cantidad = int(request.form['cantidad'])
    motivo = request.form['motivo']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id = %s', (id_producto,))
    producto = cursor.fetchone()
    if tipo == 'entrada':
        nuevo_stock = producto['stock_actual'] + cantidad
    elif tipo == 'salida':
        if cantidad > producto['stock_actual']:
            cursor.close()
            conn.close()
            return redirect(url_for('movimientos'))
        nuevo_stock = producto['stock_actual'] - cantidad
    elif tipo == 'ajuste':
        nuevo_stock = cantidad
    cursor2 = conn.cursor()
    cursor2.execute('UPDATE productos SET stock_actual = %s WHERE id = %s', (nuevo_stock, id_producto))
    cursor2.execute('''
        INSERT INTO movimientos_stock (tipo, cantidad, motivo, id_producto, id_usuario)
        VALUES (%s, %s, %s, %s, %s)
    ''', (tipo, cantidad, motivo, id_producto, session['usuario_id']))
    if nuevo_stock < producto['stock_minimo']:
        mensaje = f"Stock de '{producto['nombre']}' ({nuevo_stock}) cayó por debajo del mínimo ({producto['stock_minimo']})."
        cursor2.execute('''
            INSERT INTO alertas (tipo, mensaje, id_producto)
            SELECT %s, %s, %s FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1 FROM alertas WHERE id_producto = %s AND resuelta = 0
            )
        ''', ('stock_bajo', mensaje, id_producto, id_producto))
    conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()
    return redirect(url_for('movimientos'))

# ─── CARGA DE EXCEL DE PROVEEDOR (REDISEÑADA) ────────────
@app.route('/importar', methods=['GET', 'POST'])
def importar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_rol'] != 'encargado':
        return redirect(url_for('dashboard'))

    # Datos que se muestran en la pantalla
    resultados = []
    errores = []
    productos_con_similares = []
    productos_a_importar = []  # Productos que ya existen y se procesarán
    archivo_procesado = False
    
    # Si viene de procesar decisiones (vincular o crear múltiples)
    if request.method == 'POST' and 'procesar_todos' in request.form:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor2 = conn.cursor()
        
        # Procesar cada producto del formulario
        for key, value in request.form.items():
            if key.startswith('accion_'):
                producto_nombre = key.replace('accion_', '')
                accion = value
                cantidad = int(request.form.get(f'cantidad_{producto_nombre}', 0))
                proveedor = request.form.get(f'proveedor_{producto_nombre}', '')
                fecha_excel = request.form.get(f'fecha_{producto_nombre}', '')
                
                if accion == 'crear':
                    # Crear nuevo producto
                    cursor_cat = conn.cursor(dictionary=True)
                    cursor_cat.execute('SELECT id FROM categorias LIMIT 1')
                    cat_default = cursor_cat.fetchone()
                    cursor_cat.close()
                    
                    cursor2.execute('''
                        INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, id_categoria, activo)
                        VALUES (%s, %s, %s, %s, %s, %s, 1)
                    ''', (producto_nombre, f"Producto importado desde Excel del proveedor {proveedor}", 0.00, 0, 0, cat_default['id'] if cat_default else None))
                    
                    id_producto = cursor2.lastrowid
                    
                    # Ahora actualizar stock con la cantidad del Excel
                    cursor2.execute(
                        'UPDATE productos SET stock_actual = %s WHERE id = %s',
                        (cantidad, id_producto)
                    )
                    
                    # Registrar movimiento
                    motivo = f"Ingreso por proveedor: {proveedor} — fecha factura: {fecha_excel}"
                    cursor2.execute('''
                        INSERT INTO movimientos_stock (tipo, cantidad, motivo, id_producto, id_usuario)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', ('entrada', cantidad, motivo, id_producto, session['usuario_id']))
                    
                    resultados.append({
                        'producto': producto_nombre,
                        'proveedor': proveedor,
                        'cantidad': cantidad,
                        'stock_nuevo': cantidad,
                        'creado': True
                    })
                    
                elif accion.startswith('vincular_'):
                    producto_id = accion.replace('vincular_', '')
                    cursor.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
                    producto = cursor.fetchone()
                    
                    if producto:
                        nuevo_stock = producto['stock_actual'] + cantidad
                        cursor2.execute(
                            'UPDATE productos SET stock_actual = %s WHERE id = %s',
                            (nuevo_stock, producto['id'])
                        )
                        motivo = f"Ingreso por proveedor: {proveedor} — fecha factura: {fecha_excel}"
                        cursor2.execute('''
                            INSERT INTO movimientos_stock (tipo, cantidad, motivo, id_producto, id_usuario)
                            VALUES (%s, %s, %s, %s, %s)
                        ''', ('entrada', cantidad, motivo, producto['id'], session['usuario_id']))
                        
                        if nuevo_stock >= producto['stock_minimo']:
                            cursor2.execute('''
                                UPDATE alertas SET resuelta = 1
                                WHERE id_producto = %s AND resuelta = 0
                            ''', (producto['id'],))
                        
                        resultados.append({
                            'producto': producto['nombre'],
                            'proveedor': proveedor,
                            'cantidad': cantidad,
                            'stock_nuevo': nuevo_stock,
                            'creado': False
                        })
        
        conn.commit()
        cursor.close()
        cursor2.close()
        conn.close()
        
        if resultados:
            archivo_procesado = True
            productos_con_similares = []
        
        return render_template('importar.html',
                               nombre=session['usuario_nombre'],
                               rol=session['usuario_rol'],
                               resultados=resultados,
                               errores=errores,
                               productos_con_similares=productos_con_similares,
                               archivo_procesado=archivo_procesado)
    
    # Procesar archivo Excel (primera carga)
    if request.method == 'POST' and 'archivo' in request.files:
        archivo = request.files.get('archivo')
        if not archivo or not archivo.filename.endswith('.xlsx'):
            errores.append('El archivo debe ser un Excel (.xlsx).')
            return render_template('importar.html',
                                   nombre=session['usuario_nombre'],
                                   rol=session['usuario_rol'],
                                   resultados=resultados,
                                   errores=errores,
                                   productos_con_similares=[],
                                   archivo_procesado=False)

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        try:
            wb = openpyxl.load_workbook(ruta)
            ws = wb.active
            filas = list(ws.iter_rows(min_row=2, values_only=True))

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            for fila in filas:
                if not any(fila):
                    continue
                nombre_proveedor = str(fila[0]) if fila[0] else 'Desconocido'
                fecha_excel = str(fila[1]) if fila[1] else ''
                nombre_producto = str(fila[2]) if fila[2] else ''
                cantidad = int(fila[3]) if fila[3] else 0

                if not nombre_producto or cantidad <= 0:
                    continue

                # Buscar coincidencia exacta
                cursor.execute(
                    'SELECT * FROM productos WHERE LOWER(nombre) = LOWER(%s) AND activo = 1',
                    (nombre_producto,)
                )
                producto = cursor.fetchone()
                
                # Buscar coincidencia parcial
                if not producto:
                    cursor.execute(
                        'SELECT * FROM productos WHERE nombre LIKE %s AND activo = 1',
                        (f'%{nombre_producto}%',)
                    )
                    producto = cursor.fetchone()

                if producto:
                    # Producto encontrado - se procesa automáticamente
                    productos_a_importar.append({
                        'nombre': producto['nombre'],
                        'proveedor': nombre_proveedor,
                        'fecha': fecha_excel,
                        'cantidad': cantidad,
                        'producto_id': producto['id'],
                        'stock_actual': producto['stock_actual'],
                        'stock_minimo': producto['stock_minimo'],
                        'existe': True
                    })
                else:
                    # Productos no encontrados - buscar similares
                    cursor.execute('''
                        SELECT id, nombre, 
                               (SELECT nombre FROM categorias WHERE id = p.id_categoria) AS categoria_nombre
                        FROM productos p
                        WHERE p.nombre LIKE %s AND p.activo = 1
                        ORDER BY 
                            CASE WHEN p.nombre LIKE %s THEN 1 ELSE 0 END DESC,
                            p.nombre
                        LIMIT 5
                    ''', (f'%{nombre_producto}%', f'{nombre_producto}%'))
                    
                    similares = cursor.fetchall()
                    
                    ya_en_lista = False
                    for pnc in productos_con_similares:
                        if pnc['nombre'] == nombre_producto:
                            ya_en_lista = True
                            break
                    
                    if not ya_en_lista:
                        productos_con_similares.append({
                            'nombre': nombre_producto,
                            'proveedor': nombre_proveedor,
                            'fecha': fecha_excel,
                            'cantidad': cantidad,
                            'similares': similares
                        })

            # Procesar automáticamente los productos que ya existen
            if productos_a_importar:
                cursor2 = conn.cursor()
                for item in productos_a_importar:
                    nuevo_stock = item['stock_actual'] + item['cantidad']
                    cursor2.execute(
                        'UPDATE productos SET stock_actual = %s WHERE id = %s',
                        (nuevo_stock, item['producto_id'])
                    )
                    motivo = f"Ingreso por proveedor: {item['proveedor']} — fecha factura: {item['fecha']}"
                    cursor2.execute('''
                        INSERT INTO movimientos_stock (tipo, cantidad, motivo, id_producto, id_usuario)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', ('entrada', item['cantidad'], motivo, item['producto_id'], session['usuario_id']))
                    
                    if nuevo_stock >= item['stock_minimo']:
                        cursor2.execute('''
                            UPDATE alertas SET resuelta = 1
                            WHERE id_producto = %s AND resuelta = 0
                        ''', (item['producto_id'],))
                    
                    resultados.append({
                        'producto': item['nombre'],
                        'proveedor': item['proveedor'],
                        'cantidad': item['cantidad'],
                        'stock_nuevo': nuevo_stock,
                        'ok': True
                    })
                conn.commit()
                cursor2.close()
            
            cursor.close()
            conn.close()

        except Exception as e:
            errores.append(f"Error al procesar el archivo: {str(e)}")
        finally:
            if os.path.exists(ruta):
                os.remove(ruta)

    return render_template('importar.html',
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'],
                           resultados=resultados,
                           errores=errores,
                           productos_con_similares=productos_con_similares,
                           archivo_procesado=bool(resultados) or bool(productos_con_similares))

# ─── ALERTAS Y REPOSICIÓN ────────────────────────────────
@app.route('/alertas')
def alertas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.*, p.nombre AS producto_nombre, p.stock_actual, p.stock_minimo
        FROM alertas a
        JOIN productos p ON a.id_producto = p.id
        WHERE a.resuelta = 0
        ORDER BY a.fecha DESC
    ''')
    lista_alertas = cursor.fetchall()
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.stock_actual < p.stock_minimo AND p.activo = 1
        ORDER BY (p.stock_minimo - p.stock_actual) DESC
    ''')
    productos_reponer = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('alertas.html',
                           alertas=lista_alertas,
                           productos_reponer=productos_reponer,
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'])

@app.route('/alertas/resolver/<int:id>')
def resolver_alerta(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_rol'] != 'encargado':
        return redirect(url_for('alertas'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE alertas SET resuelta = 1 WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('alertas'))

# ─── LOGOUT ──────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/usuarios', methods=['GET', 'POST'])
def gestion_usuarios():
    # 1. CERRADURA LÓGICA: Solo el ADMIN puede pisar esta zona
    if session.get('rol') != 'admin':
        flash("ACCESO DENEGADO: Requiere credenciales de Administrador.", "error")
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 2. PROCESAMIENTO DE DATOS (Crear o Eliminar)
    if request.method == 'POST':
        if 'registrar' in request.form:
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password'] # Nota: En un sistema final, esto debería ir encriptado
            rol = request.form['rol']
            
            # Verificamos que el correo no exista ya
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("ERROR: El correo ya está asignado a otro operario.", "error")
            else:
                cursor.execute('INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)', 
                               (nombre, email, password, rol))
                mysql.connection.commit()
                flash("Operario registrado exitosamente en el sistema.", "success")
                
        elif 'eliminar' in request.form:
            id_eliminar = request.form['usuario_id']
            # Evitamos que el admin se borre a sí mismo por accidente
            if int(id_eliminar) == session.get('usuario_id'):
                flash("PROTOCOLO DE SEGURIDAD: No puedes eliminar tu propio usuario.", "error")
            else:
                cursor.execute('DELETE FROM usuarios WHERE id = %s', (id_eliminar,))
                mysql.connection.commit()
                flash("Credenciales revocadas. Operario eliminado.", "error") # Usamos error para que salga en rojo

    # 3. LECTURA DE DATOS
    cursor.execute('SELECT id, nombre, email, rol FROM usuarios ORDER BY rol, nombre')
    lista_usuarios = cursor.fetchall()
    
    return render_template('usuarios.html', usuarios=lista_usuarios)
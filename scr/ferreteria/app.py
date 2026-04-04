from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'ferreteria_secret_key'

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ─── LOGIN ───────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM usuarios WHERE email = %s AND password = %s AND activo = 1',
            (email, password)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            session['usuario_rol'] = usuario['rol']
            return redirect(url_for('dashboard'))
        else:
            error = 'Email o contraseña incorrectos.'

    return render_template('login.html', error=error)

# ─── DASHBOARD ───────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'])

# ─── PRODUCTOS ───────────────────────────────────────────
@app.route('/productos')
def productos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.activo = 1
        ORDER BY p.nombre
    ''')
    lista_productos = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias WHERE activo = 1')
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('productos.html',
                           productos=lista_productos,
                           categorias=categorias,
                           nombre=session['usuario_nombre'],
                           rol=session['usuario_rol'])

@app.route('/productos/registrar', methods=['POST'])
def registrar_producto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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

    # ── PATRÓN OBSERVER ──────────────────────────────────
    # Cuando se registra un producto, se verifica si el
    # stock inicial ya está por debajo del mínimo.
    # Si es así, se genera una alerta automáticamente.
    if stock_actual < stock_minimo:
        mensaje = f"Stock inicial de '{nombre}' ({stock_actual}) está por debajo del mínimo ({stock_minimo})."
        cursor.execute('''
            INSERT INTO alertas (tipo, mensaje, id_producto)
            VALUES (%s, %s, %s)
        ''', ('stock_bajo', mensaje, id_producto))
    # ── FIN OBSERVER ─────────────────────────────────────

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('productos'))

# ─── LOGOUT ──────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, url_for, request, redirect, flash, session
from database import conectar

app = Flask(__name__)
app.secret_key = "9877866554"

#FUNCIONES
def obtener_salario_base(cargo):
    cargo = cargo.lower()
    if cargo == "Gerente":
        return 5000000
    elif cargo == "Administrativo":
        return 3500000
    elif cargo == "Contador":
        return 2800000
    else:
        return 1800000

#LOGIN 
@app.route("/")
def login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_form():
    usuario = request.form['txtusuario']
    password = request.form['txtcontraseña']

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
    resultado = cursor.fetchone()
    cursor.close()
    con.close()

    if resultado:
        session['usuario'] = resultado[1]
        session['rol'] = resultado[3].lower()
        session['documento'] = resultado[4]   
        
        # Redirección según el rol
        if session['rol'] == 'administrador':
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('panel_empleado'))
    else:
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for('login'))

#INICIO
@app.route('/inicio')
def inicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("""
        SELECT e.id_empleado, e.docuempleado, e.nombreemple, e.apellidoemple,
               e.cargoemple, d.Nombrearea, e.salarioB, e.Horasextras,
               e.bonificacion, e.salarioneto
        FROM empleados e
        JOIN departamentos d ON e.id_area = d.id_area
    """)
    empleados = cursor.fetchall()

    cursor.close()
    con.close()
    return render_template('index.html', user=usuarios, emple=empleados)

# REGISTRAR USUARIO COMO ADMI
@app.route('/registrar_usuario', methods=['POST'])
def registrarusario():
    if 'usuario' not in session: return redirect(url_for('login'))
      
    usuario = request.form["txtusuario"]
    password = request.form["txtcontraseña"]
    rolusu = request.form["txtrol"]
    documento = request.form["txtdocumento"]

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT docuempleado FROM empleados WHERE docuempleado=%s", (documento,))
    if not cursor.fetchone():
        flash("El empleado no existe, primero debes registrarlo", "danger")
        con.close()
        return redirect(url_for('inicio'))

    cursor.execute(
        "INSERT INTO usuarios (usuario, password, rol, docuempleado) VALUES (%s, %s, %s, %s)",
        (usuario, password, rolusu, documento)
    )
    con.commit()
    con.close()
    flash("Usuario registrado correctamente", "success")
    return redirect(url_for('inicio'))

# EDITAR USUARIO COMO ADMI

@app.route('/editarusu/<int:id>')
def editarusu(id):
    if 'usuario' not in session: return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (id,))
    usuario = cursor.fetchone()
    con.close()
    return render_template("editarusuario.html", usu=usuario)

# ACTUALIZAR USUARIO COMO ADMI

@app.route('/actualizar', methods=['POST'])
def actualizar_usuarios():
    id_usu = request.form['id']
    usuario = request.form['txtusuario']
    password = request.form['txtpassword']

    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE usuarios SET usuario=%s, password=%s WHERE id_usuario=%s", (usuario, password, id_usu))
    con.commit()
    con.close()
    flash("Usuario actualizado", "success")
    return redirect(url_for('inicio'))

#ELIMINAR USUARIO COMO ADMI

@app.route('/eliminar/<int:id>')
def eliminarusu(id):
    if 'usuario' not in session: return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE id_usuario=%s", (id,))
    res = cursor.fetchone()

    if res and res[0].lower() == "administrador":
        flash("No se puede eliminar al administrador", "warning")
    else:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id,))
        con.commit()
        flash("Usuario eliminado", "success")
    
    con.close()
    return redirect(url_for("inicio"))

# REGISTRAR EMPLEADO COMO ADMI
@app.route('/registrar_empleado', methods=['POST'])
def agregar_empleado():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    nombre = request.form["txtnombre"]
    apellido = request.form["txtapellido"]
    docu = request.form["txtdocumento"]
    cargo = request.form["txtcargo"]
    dpto_nombre = request.form["txtdepartamento"]
    h_extras = int(request.form["txthorasextra"])
    bono = float(request.form["txtbonificacion"])

    base = obtener_salario_base(cargo)
    total_neto = base + (h_extras * 3000) + bono
    salud_pension = total_neto * 0.08
    salario_final = total_neto - salud_pension

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT id_area FROM departamentos WHERE Nombrearea=%s", (dpto_nombre,))
    res_area = cursor.fetchone()
    id_area = res_area[0] if res_area else None

    if not id_area:
        cursor.execute("INSERT INTO departamentos (Nombrearea) VALUES (%s)", (dpto_nombre,))
        con.commit()
        id_area = cursor.lastrowid

    sql = """INSERT INTO empleados 
             (docuempleado, nombreemple, apellidoemple, cargoemple, salarioB, Horasextras, bonificacion, salud, pension, salarioneto, id_area) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
  
    cursor.execute(sql, (docu, nombre, apellido, cargo, salario_final, h_extras, bono, total_neto*0.04, total_neto*0.04, total_neto, id_area))
    con.commit()
    con.close()
    flash("Empleado registrado", "success")
    return redirect(url_for('inicio'))

#EDITAR EMPLEADO COMO ADMI
@app.route('/editar_empleado/<int:id>')
def editar_empleado(id):
    if 'usuario' not in session: return redirect(url_for('login'))
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id_empleado=%s", (id,))
    empleado = cursor.fetchone()
    con.close()
    return render_template("editarempleado.html", emple=empleado)

#ACTUALIZAR EMPLEADO COMO ADMI
@app.route('/actualizaremple/<int:id>', methods=['POST'])
def actualizaremple(id):
    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    cargo = request.form['txtcargo']
    h_extras = int(request.form['txthorasextra'])
    bono = float(request.form['txtbonificacion'])

    base = obtener_salario_base(cargo)
    neto = base + (h_extras * 3000) + bono
    salud = neto * 0.04
    pension = neto * 0.04
    salario_final = neto - salud - pension

    con = conectar()
    cursor = con.cursor()
    sqla = """UPDATE empleados SET nombreemple=%s, apellidoemple=%s, cargoemple=%s, 
              Horasextras=%s, bonificacion=%s, salarioB=%s, salud=%s, pension=%s, 
              salarioneto=%s WHERE id_empleado=%s"""
    cursor.execute(sqla, (nombre, apellido, cargo, h_extras, bono, salario_final, salud, pension, neto, id))
    con.commit()
    con.close()
    flash("Empleado actualizado", "info")
    return redirect(url_for('inicio'))

#ELIMINAR EMPLEADO COMO ADMI

@app.route('/eliminar_empleado/<int:id>')
def eliminar_empleado(id):
    if 'usuario' not in session: return redirect(url_for('login'))
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM empleados WHERE id_empleado=%s", (id,))
    con.commit()
    con.close()
    flash("Empleado eliminado", "danger")
    return redirect(url_for("inicio"))

@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

#PANEL EMPLEADO

@app.route('/panel_empleado')
def panel_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    documento = session.get('documento')
    
    con = conectar()
    cursor = con.cursor()
    
    cursor.execute("""
        SELECT e.docuempleado, e.nombreemple, e.apellidoemple, e.cargoemple, 
               d.Nombrearea, e.salarioB, e.Horasextras, e.bonificacion, 
               e.salud, e.pension, e.salarioneto
        FROM empleados e
        JOIN departamentos d ON e.id_area = d.id_area
        WHERE e.docuempleado = %s
    """, (documento,))
    
    datos_empleado = cursor.fetchone()
    cursor.close()
    con.close()

    return render_template('paneldeempleado.html', empleado=datos_empleado)

# EDITAR PERFIL EMPLEADO lOGUEADO

@app.route('/empleado/editar_perfil', methods=['POST'])
def editar_perfil_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    documento = session.get('documento')
    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    cargo = request.form['txtcargo']
    nombre_area = request.form['txtdepartamento'] # El nombre que escribe el empleado
          
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT id_area FROM departamentos WHERE Nombrearea=%s", (nombre_area,))
    res_area = cursor.fetchone()

    if res_area:
        id_area = res_area[0]
    else:
        cursor.execute("INSERT INTO departamentos (Nombrearea) VALUES (%s)", (nombre_area,))
        con.commit()
        id_area = cursor.lastrowid

    cursor.execute("""
        UPDATE empleados 
        SET nombreemple=%s, apellidoemple=%s, cargoemple=%s, id_area=%s
        WHERE docuempleado=%s
    """, (nombre, apellido, cargo, id_area, documento))
    
    con.commit()
    cursor.close()
    con.close()
    
    flash("Perfil y área actualizados con éxito", "success")
    return redirect(url_for('panel_empleado'))

if __name__ == '__main__':
    app.run(debug=True)
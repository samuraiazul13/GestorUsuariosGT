from flask import Flask, render_template, url_for, request, redirect, flash, session
from database import conectar

app = Flask(__name__)
app.secret_key = "9877866554"

<<<<<<< HEAD
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
=======
# LOGIN
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
@app.route("/")
def login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_form():
<<<<<<< HEAD
=======

>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    usuario = request.form['txtusuario']
    password = request.form['txtcontraseña']

    con = conectar()
    cursor = con.cursor()
<<<<<<< HEAD
    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
    resultado = cursor.fetchone()
=======

    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
    resultado = cursor.fetchone()

>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    cursor.close()
    con.close()

    if resultado:
        session['usuario'] = resultado[1]
<<<<<<< HEAD
        session['rol'] = resultado[3].lower()
        session['documento'] = resultado[4]   
        
        # Redirección según el rol
        if session['rol'] == 'administrador':
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('panel_empleado'))
=======
        session['rol'] = resultado[3]
        return redirect(url_for('inicio'))
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    else:
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for('login'))

<<<<<<< HEAD
#INICIO
@app.route('/inicio')
def inicio():
=======

# INICIO
@app.route('/inicio')
def inicio():
    
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

<<<<<<< HEAD
    cursor.execute("""
        SELECT e.id_empleado, e.docuempleado, e.nombreemple, e.apellidoemple,
               e.cargoemple, d.Nombrearea, e.salarioB, e.Horasextras,
               e.bonificacion, e.salarioneto
        FROM empleados e
        JOIN departamentos d ON e.id_area = d.id_area
    """)
=======
    cursor.execute("""SELECT e.id_empleado, e.docuempleado, e.nombreemple, e.apellidoemple,
       e.cargoemple, d.Nombrearea, e.salarioB, e.Horasextras,
       e.bonificacion, e.salarioneto
    FROM empleados e
    JOIN departamentos d ON e.id_area = d.id_area""")

>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    empleados = cursor.fetchall()

    cursor.close()
    con.close()
<<<<<<< HEAD
    return render_template('index.html', user=usuarios, emple=empleados)

# REGISTRAR USUARIO COMO ADMI
@app.route('/registrar_usuario', methods=['POST'])
def registrarusario():
    if 'usuario' not in session: return redirect(url_for('login'))
=======

    return render_template('index.html', user=usuarios, emple=empleados)


# CERRAR SESIÓN
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))


# ELIMINAR USUARIO
@app.route('/eliminar/<int:id>')
def eliminarusu(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT rol FROM usuarios WHERE id_usuario=%s", (id,))
    usuario = cursor.fetchone()

    if usuario:
        if usuario[0] == "administrador":
            flash("No se puede eliminar el administrador", "warning")
        else:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id,))
            con.commit()
            flash("Usuario eliminado", "success")
    else:
        flash("Usuario no encontrado", "danger")

    cursor.close()
    con.close()

    return redirect(url_for("inicio"))


# REGISTRAR USUARIO
@app.route('/registrar_usuario', methods=['POST'])
def registrarusario():

    if 'usuario' not in session:
        return redirect(url_for('login'))
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
      
    usuario = request.form["txtusuario"]
    password = request.form["txtcontraseña"]
    rolusu = request.form["txtrol"]
    documento = request.form["txtdocumento"]

    con = conectar()
    cursor = con.cursor()

<<<<<<< HEAD
    cursor.execute("SELECT docuempleado FROM empleados WHERE docuempleado=%s", (documento,))
    if not cursor.fetchone():
        flash("El empleado no existe, primero debes registrarlo", "danger")
=======
    # VALIDAR USUARIO
    cursor.execute("SELECT docuempleado FROM empleados WHERE docuempleado=%s", (documento,))
    existe = cursor.fetchone()

    if not existe:
        flash("El empleado no existe, primero debes registrarlo", "danger")
        cursor.close()
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
        con.close()
        return redirect(url_for('inicio'))

    cursor.execute(
        "INSERT INTO usuarios (usuario, password, rol, docuempleado) VALUES (%s, %s, %s, %s)",
        (usuario, password, rolusu, documento)
    )
<<<<<<< HEAD
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
=======

    con.commit()
    cursor.close()
    con.close()

    flash("Usuario registrado correctamente", "success")
    return redirect(url_for('inicio'))


# REGISTRO DE EMPLEADO
@app.route('/registrar_empleado', methods=['POST'])
def agregar_empleado():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    nombreemple = request.form["txtnombre"]
    apellidoemple = request.form["txtapellido"]
    docuempleado = request.form["txtdocumento"]
    cargoemple = request.form["txtcargo"]
    Nombredearea = request.form["txtdepartamento"]
    Horasextras = int(request.form["txthorasextra"])
    bonificacion = float(request.form["txtbonificacion"])

    # CALCUALR SALARIO
    def obtener_salario_base(cargo):
        cargo = cargo.lower()
        if cargo == "gerente":
            return 5000000
        elif cargo == "administrador":
            return 3500000
        elif cargo == "contador":
            return 2800000
        else:
            return 1800000
        
    salarioB = obtener_salario_base(cargoemple)
    totalextras = Horasextras * 3000
    salarioneto = salarioB + totalextras + bonificacion

    salud = salarioneto * 0.04
    pension = salarioneto * 0.04
    salarioB = salarioneto - salud - pension

    con = conectar()
    cursor = con.cursor()

    # DEPARTAMENTO
    cursor.execute("SELECT id_area FROM departamentos WHERE Nombrearea=%s", (Nombredearea,))
    resultado = cursor.fetchone()

    if resultado:
        id_area = resultado[0]
    else:
        cursor.execute("INSERT INTO departamentos (Nombrearea) VALUES (%s)", (Nombredearea,))
        con.commit()
        id_area = cursor.lastrowid

    # INGRESAR EMPLEADO
    sql = """INSERT INTO empleados 
    (docuempleado, nombreemple, apellidoemple, cargoemple, salarioB, Horasextras, bonificacion, salud, pension, salarioneto, id_area) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(sql, (docuempleado,nombreemple,apellidoemple,cargoemple,salarioB,Horasextras,bonificacion,salud,pension,id_area))

    con.commit()
    cursor.close()
    con.close()

    flash("Empleado registrado correctamente", "success")
    return redirect(url_for('inicio'))

#ELIMINAR EMPLEADO

@app.route('/eliminar_empleado/<int:id>')
def eliminar_empleado(id):
    
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM empleados WHERE id_empleado=%s", (id,))
    usuario = cursor.fetchone()

    if usuario:
        if usuario[0] == "administrador":
            flash("No se puede eliminar el administrador", "warning")
        else:
            cursor.execute("SELECT * FROM empleados WHERE id_empleado=%s", (id,))
            empleado = cursor.fetchone()
            cursor.execute("DELETE FROM empleados WHERE id_empleado=%s", (id,))
            con.commit()
            flash("Empleado eliminado", "success")
    else:
        flash("Empleado no encontrado", "danger")

    cursor.close()
    con.close()

    return redirect(url_for("inicio"))

#Editar usuarios

@app.route('/editarusu/<int:id>')
def editarusu(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    con = conectar()
    cursor = con.cursor()

    sql1= "SELECT * FROM usuarios WHERE id_usuario=%s"
    cursor.execute(sql1,(id,))
    usuario = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editarusuario.html",usu= usuario)

#actualizar la informacion del formulario 

@app.route('/actualizar',methods=['POST'])
def actualizar_usuarios():
    
    id = request.form['id']
>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a
    usuario = request.form['txtusuario']
    password = request.form['txtpassword']

    con = conectar()
    cursor = con.cursor()
<<<<<<< HEAD
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
=======

    sqla= "UPDATE usuarios SET usuario=%s,PASSWORD=%s WHERE id_usuario=%s"

    cursor.execute(sqla,(usuario,password,id))
    con.commit()

    cursor.close()
    con.close()

    print("USUARIO ACTUALIZADO")

    return redirect(url_for('inicio'))

#editar empleado

@app.route('/editar_empleado/<int:id>')
def editar_empleado(id):

    if 'usuario' not in session:    
        return redirect(url_for('login'))   
    
    con = conectar()
    cursor = con.cursor()   
    sql2= "SELECT * FROM empleados WHERE id_empleado=%s"
    cursor.execute(sql2,(id,))
    empleado = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editarempleado.html",emple= empleado)

#actualizar empleado 

@app.route('/actualizaremple/<int:id>',methods=['POST'])
def actualizaremple(id):
    
    nombreemple = request.form['txtnombre']
    apellidoemple = request.form['txtapellido']
    cargoemple = request.form['txtcargo']
    Horasextras = int(request.form['txthorasextra'])
    bonificacion = float(request.form['txtbonificacion'])

    con = conectar()
    cursor = con.cursor()

    cursor.close()
    con.close()

#actualizar nuevo sueldo y bonificacion 

    def obtener_salario_base(cargo):
        cargo = cargo.lower()
        if cargo == "gerente":
            return 5000000
        elif cargo == "administrador":
            return 3500000
        elif cargo == "contador":
            return 2800000
        else:
            return 1800000
        
    salarioB = obtener_salario_base(cargoemple)
    totalextras = Horasextras * 3000
    salarioneto = salarioB + totalextras + bonificacion

    salud = salarioneto * 0.04
    pension = salarioneto * 0.04
    salarioB = salarioneto - salud - pension

    con = conectar()
    cursor = con.cursor()

    sqla= "UPDATE empleados SET nombreemple=%s, apellidoemple=%s, cargoemple=%s, Horasextras=%s, bonificacion=%s, salarioB=%s, salud=%s, pension=%s, salarioneto=%s WHERE id_empleado=%s"           
    cursor.execute(sqla,(nombreemple,apellidoemple,cargoemple,Horasextras,bonificacion,salarioB,salud,pension,salarioneto,id))
    con.commit()
    cursor.close()
    con.close()
    
    print("EMPLEADO ACTUALIZADO")
    return redirect(url_for('inicio'))

>>>>>>> 4a869441e58c78fa433a46e0841fba62f40f757a

if __name__ == '__main__':
    app.run(debug=True)
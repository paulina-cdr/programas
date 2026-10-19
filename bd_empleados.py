import sqlite3
import os

# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

DB = "database/empleados.db"


def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB)


# ==========================================
# CREACIÓN DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            curp TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            tel_empleado TEXT,
            edad INTEGER,
            sueldo REAL
        )
    """)

    conexion.commit()
    conexion.close()


# ==========================================
# 1. ALTAS DE EMPLEADOS
# ==========================================

def alta_empleado():
    print("\n===== ALTA DE EMPLEADO =====")

    curp = input("Curp: ").strip().upper()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    tel_empleado = input("Teléfono del empleado: ").strip()
    edad = input("Edad del empleado: ").strip()
    sueldo = input("Sueldo mensual del empleado: ").strip()

    if not curp or not nombre or not apellido:
        print("La curp, el nombre y el apellido son obligatorios.")
        return

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO empleado (
                curp, nombre, apellido, calle,
                colonia, tel_empleado, edad, sueldo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curp, nombre, apellido, calle,
            colonia, tel_empleado, edad, sueldo
        ))

        conexion.commit()
        print("\nEmpleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("\nError: la curp ya existe.")

    except sqlite3.Error as error:
        print("Error al registrar al empleado:", error)

    finally:
        conexion.close()


# ==========================================
# 2. BAJAS DE EMPLEADOS
# ==========================================

def baja_empleado():
    print("\n===== BAJA DE EMPLEADO =====")

    curp = input("Curp del empleado: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado is None:
            print("No se encontró un empleado con esa curp.")
            return

        print("\nDatos del empleado:")
        print("Curp:", empleado[0])
        print("Nombre:", empleado[1])
        print("Apellido:", empleado[2])
        print("Calle:", empleado[3])
        print("Colonia:", empleado[4])
        print("Teléfono del empleado:", empleado[5])
        print("Edad del empleado:", empleado[6])
        print("Sueldo mensual del empleado:", empleado[7])

        confirmacion = input(
            "\n¿Desea eliminar este empleado? (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            cursor.execute("""
                DELETE FROM empleado
                WHERE curp = ?
            """, (curp,))

            conexion.commit()
            print("Empleado eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except sqlite3.Error as error:
        print("Error al eliminar al empleado:", error)

    finally:
        conexion.close()


# ==========================================
# 3. MODIFICACIONES DE EMPLEADOS
# ==========================================

def modificar_empleado():
    print("\n===== MODIFICACIÓN DEL EMPLEADO =====")

    curp = input("Curp del empleado: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, apellido, calle, colonia,
                   tel_empleado, edad, sueldo 
            FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado is None:
            print("No se encontró un empleado con esa curp.")
            return

        print("\nIngrese los nuevos datos.")
        print("Presione ENTER para conservar el dato actual.")

        nombre = input(f"Nombre [{empleado[0]}]: ").strip()
        apellido = input(f"Apellido [{empleado[1]}]: ").strip()
        calle = input(f"Calle [{empleado[2] or ''}]: ").strip()
        colonia = input(f"Colonia [{empleado[3] or ''}]: ").strip()
        tel_empleado = input(
            f"Teléfono del empleado [{empleado[4] or ''}]: "
        ).strip()
        edad = input(
            f"Edad [{empleado[5] or ''}]: "
        ).strip()
        sueldo = input(f"Sueldo mensual [{empleado[6] or ''}]: ").strip()

        # Conservar los valores anteriores cuando se pulsa ENTER
        nombre = nombre or empleado[0]
        apellido = apellido or empleado[1]
        calle = calle or empleado[2] or ""
        colonia = colonia or empleado[3] or ""
        tel_empleado = tel_empleado or empleado[4] or ""
        edad = edad or empleado[5] or ""
        sueldo = sueldo or empleado[6] or ""

        cursor.execute("""
            UPDATE empleado
            SET nombre = ?,
                apellido = ?,
                calle = ?,
                colonia = ?,
                tel_empleado = ?,
                edad = ?,
                sueldo = ?
            WHERE curp = ?
        """, (
            nombre, apellido, calle, colonia,
            tel_empleado, edad, sueldo, curp
        ))

        conexion.commit()
        print("\nEmpleado modificado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al modificar al empleado:", error)

    finally:
        conexion.close()


# ==========================================
# 4. CONSULTA DE TODA LA TABLA
# ==========================================

def consultar_todos():
    print("\n===== LISTADO DE EMPLEADOS =====")

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT curp, nombre, apellido, calle,
                   colonia, tel_empleado, edad, sueldo
            FROM empleado
            ORDER BY apellido, nombre
        """)

        empleados = cursor.fetchall()

        if not empleados:
            print("No hay empleados registrados.")
            return

        for empleado in empleados:
            print("-" * 50)
            print("Curp:", empleado[0])
            print("Nombre:", empleado[1])
            print("Apellido:", empleado[2])
            print("Calle:", empleado[3] or "")
            print("Colonia:", empleado[4] or "")
            print("Teléfono del empleado:", empleado[5] or "")
            print("Edad:", empleado[6] or "")
            print("Sueldo:", empleado[7] or "")

        print("-" * 50)
        print("Total de empleados:", len(empleados))

    except sqlite3.Error as error:
        print("Error al consultar los empleados:", error)

    finally:
        conexion.close()


# ==========================================
# 5. CONSULTA POR CURP
# ==========================================

def consultar_curp():
    print("\n===== CONSULTA POR CURP =====")

    curp = input("Ingrese la curp: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT curp, nombre, apellido, calle,
                   colonia, tel_empleado, edad, sueldo
            FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado:
            print("\n===== DATOS DEL EMPLEADO =====")
            print("Curp:", empleado[0])
            print("Nombre:", empleado[1])
            print("Apellido:", empleado[2])
            print("Calle:", empleado[3] or "")
            print("Colonia:", empleado[4] or "")
            print("Teléfono del empleado:", empleado[5] or "")
            print("Edad:", empleado[6] or "")
            print("Sueldo:", empleado[7] or "")
        else:
            print("No se encontró un empleado con esa curp.")

    except sqlite3.Error as error:
        print("Error al consultar al empleado:", error)

    finally:
        conexion.close()


# ==========================================
# 6. MENÚ PRINCIPAL
# ==========================================

def menu():
    while True:
        print("\n" + "=" * 45)
        print("         SISTEMA DE CONTROL DE EMPLEADOS")
        print("=" * 45)
        print("1. Alta de empleados")
        print("2. Baja de empleados")
        print("3. Modificación de empleados")
        print("4. Consulta de toda la tabla")
        print("5. Consulta por curp")
        print("6. Salir del sistema")
        print("=" * 45)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            alta_empleado()

        elif opcion == "2":
            baja_empleado()

        elif opcion == "3":
            modificar_empleado()

        elif opcion == "4":
            consultar_todos()

        elif opcion == "5":
            consultar_curp()

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            print("Gracias por utilizar el sistema.")
            break

        else:
            print("\nOpción inválida. Seleccione del 1 al 6.")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    crear_bd()
    menu()
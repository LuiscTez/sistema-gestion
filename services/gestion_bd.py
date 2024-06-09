from flask import current_app
import sqlite3
import os

class GestionBD:

    def __init__(self):
        self.direccion_bd = current_app.config["DIRECCION_BD"]

    def crear_bd(self):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        # Crear tabla Producto
        cursor.execute('''CREATE TABLE IF NOT EXISTS Producto (
                        id_producto INTEGER PRIMARY KEY,
                        nombre TEXT,
                        descripcion TEXT,
                        precio REAL,
                        stock INTEGER,
                        id_categoria INTEGER,
                        FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
                    )''')

        # Crear tabla Categoria
        cursor.execute('''CREATE TABLE IF NOT EXISTS Categoria (
                            id_categoria INTEGER PRIMARY KEY,
                            nombre TEXT,
                            descripcion TEXT
                        )''')

        # Crear tabla Proveedor
        cursor.execute('''CREATE TABLE IF NOT EXISTS Proveedor (
                            id_proveedor INTEGER PRIMARY KEY,
                            nombre TEXT,
                            direccion TEXT,
                            telefono TEXT
                        )''')

        # Crear tabla Bodega
        cursor.execute('''CREATE TABLE IF NOT EXISTS Bodega (
                            id_bodega INTEGER PRIMARY KEY,
                            nombre TEXT,
                            ubicacion TEXT,
                            capacidad INTEGER
                        )''')

        # Crear tabla ProductoProveedor (relación muchos a muchos entre Producto y Proveedor)
        cursor.execute('''CREATE TABLE IF NOT EXISTS ProductoProveedor (
                            id_proveedor INTEGER,
                            id_producto INTEGER,
                            FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
                            FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
                            PRIMARY KEY (id_proveedor, id_producto)
                        )''')

        # Crear tabla ProductoBodega (relación muchos a muchos entre Producto y Bodega)
        cursor.execute('''CREATE TABLE IF NOT EXISTS ProductoBodega (
                            id_bodega INTEGER,
                            id_producto INTEGER,
                            cantidad INTEGER,
                            FOREIGN KEY (id_bodega) REFERENCES Bodega(id_bodega),
                            FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
                            PRIMARY KEY (id_bodega, id_producto)
                        )''')

        # Crear tabla InformeStock
        cursor.execute('''CREATE TABLE IF NOT EXISTS InformeStock (
                            id_informe INTEGER PRIMARY KEY,
                            fecha_informe DATE,
                            stock_total INTEGER,
                            stock_categoria TEXT,
                            stock_proveedor TEXT,
                            stock_bodega TEXT
                        )''')

        conn.commit()
        conn.close()

    # Función para registrar un producto en la base de datos
    def registrar_producto(self, nombre, descripcion, precio, stock, id_categoria):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria)
                          VALUES (?, ?, ?, ?, ?)''', (nombre, descripcion, precio, stock, id_categoria))

        conn.commit()
        conn.close()

    # Función para registrar una categoría en la base de datos
    def registrar_categoria(self, nombre, descripcion):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO Categoria (nombre, descripcion)
                          VALUES (?, ?)''', (nombre, descripcion))

        conn.commit()
        conn.close()

    # Función para registrar un proveedor en la base de datos
    def registrar_proveedor(self, nombre, direccion, telefono):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO Proveedor (nombre, direccion, telefono)
                          VALUES (?, ?, ?)''', (nombre, direccion, telefono))

        conn.commit()
        conn.close()

    # Función para registrar una bodega en la base de datos
    def registrar_bodega(self, nombre, ubicacion, capacidad):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO Bodega (nombre, ubicacion, capacidad)
                          VALUES (?, ?, ?)''', (nombre, ubicacion, capacidad))

        conn.commit()
        conn.close()

    # Función para agregar stock a un producto existente
    def agregar_stock(self, id_producto, cantidad):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''UPDATE Producto
                          SET stock = stock + ?
                          WHERE id_producto = ?''', (cantidad, id_producto))

        conn.commit()
        conn.close()

    # Función para retirar stock de un producto existente
    def retirar_stock(self, id_producto, cantidad):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''UPDATE Producto
                          SET stock = stock - ?
                          WHERE id_producto = ?''', (cantidad, id_producto))

        conn.commit()
        conn.close()

    # Funcion para obtener los productos
    def obtener_productos(self):
        conn = sqlite3.connect(self.direccion_bd)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM Producto;
        """)

        productos =[dict(producto) for producto in cursor.fetchall()]
        cursor.close()
        conn.close()

        return productos

    # Funcion para obtener las categorias
    def obtener_categorias(self):
        conn = sqlite3.connect(self.direccion_bd)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM Categoria;
        """)

        categorias =[dict(categoria) for categoria in cursor.fetchall()]
        cursor.close()
        conn.close()

        return categorias

    # Funcion para obtener los proveedores
    def obtener_proveedores(self):
        conn = sqlite3.connect(self.direccion_bd)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM Proveedor;
        """)

        proveedores =[dict(proveedor) for proveedor in cursor.fetchall()]
        cursor.close()
        conn.close()

        return proveedores

    # Funcion para obtener las bodegas
    def obtener_bodegas(self):
        conn = sqlite3.connect(self.direccion_bd)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM Bodega;
        """)

        bodegas =[dict(bodega) for bodega in cursor.fetchall()]
        cursor.close()
        conn.close()

        return bodegas

    # Función para calcular el valor total del stock
    def calcular_valor_total_stock(self):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''SELECT SUM(precio * stock)
                          FROM Producto''')
        total_valor_stock = cursor.fetchone()[0]

        conn.close()

        return total_valor_stock

    # Función para imprimir los datos de una tabla
    def imprimir_tabla(self, tabla):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {tabla};")
        rows = cursor.fetchall()

        print(f"\nDatos de la tabla {tabla}:")
        for row in rows:
            print(row)

        conn.close()

    #FUNCIONES CORRESPONDIENTES A RELACIONES ENTRE ENTIDADES

    def agregar_producto_a_categoria(self, id_producto, id_categoria):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE Producto
                              SET id_categoria = ?
                              WHERE id_producto = ?''', (id_categoria, id_producto))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def eliminar_producto_de_categoria(self, id_producto):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE Producto
                              SET id_categoria = NULL
                              WHERE id_producto = ?''', (id_producto,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def agregar_producto_a_proveedor(self, id_producto, id_proveedor):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO ProductoProveedor (id_producto, id_proveedor)
                              VALUES (?, ?)''', (id_producto, id_proveedor))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def eliminar_producto_de_proveedor(self, id_producto, id_proveedor):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''DELETE FROM ProductoProveedor
                              WHERE id_producto = ? AND id_proveedor = ?''', (id_producto, id_proveedor))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def agregar_producto_a_bodega(self, id_producto, id_bodega, cantidad):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT SUM(cantidad) FROM ProductoBodega WHERE id_bodega = ?''', (id_bodega,))
            total_cantidad_bodega = cursor.fetchone()[0]
            if total_cantidad_bodega is None:
                total_cantidad_bodega = 0
            cursor.execute('''SELECT capacidad FROM Bodega WHERE id_bodega = ?''', (id_bodega,))
            capacidad_bodega = cursor.fetchone()[0]
            if total_cantidad_bodega + cantidad > capacidad_bodega:
                print("No hay suficiente espacio en la bodega para agregar el producto.")
                return False
            cursor.execute('''INSERT INTO ProductoBodega (id_bodega, id_producto, cantidad)
                              VALUES (?, ?, ?)''', (id_bodega, id_producto, cantidad))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def retirar_producto_de_bodega(self, id_producto, id_bodega, cantidad):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT cantidad FROM ProductoBodega
                              WHERE id_producto = ? AND id_bodega = ?''', (id_producto, id_bodega))
            cantidad_en_bodega = cursor.fetchone()[0]
            if cantidad_en_bodega >= cantidad:
                cursor.execute('''UPDATE ProductoBodega
                                  SET cantidad = cantidad - ?
                                  WHERE id_producto = ? AND id_bodega = ?''', (cantidad, id_producto, id_bodega))
                conn.commit()
                conn.close()
                return True
            else:
                print("No hay suficiente cantidad del producto en la bodega.")
                conn.close()
                return False
        except Exception as e:
            print("Error:", e)
            conn.close()
            return False

    def consultar_disponibilidad_en_bodega(self, id_producto, id_bodega):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT cantidad FROM ProductoBodega
                              WHERE id_producto = ? AND id_bodega = ?''', (id_producto, id_bodega))
            cantidad_en_bodega = cursor.fetchone()
            conn.close()
            if cantidad_en_bodega is None:
                return 0
            else:
                return cantidad_en_bodega[0]
        except Exception as e:
            print("Error:", e)
            conn.close()
            return 0

    #CONSULTAS Y REPORTES:

    def consultar_info_producto(self, id_producto):
        conexion = sqlite3.connect(self.direccion_bd)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Producto WHERE id_producto = ?", (id_producto,))
        producto = cursor.fetchone()
        conexion.close()
        if producto:
            return dict(producto)
        return None

    def consultar_info_categoria(self, id_categoria):
        conexion = sqlite3.connect(self.direccion_bd)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Categoria WHERE id_categoria = ?", (id_categoria,))
        categoria = cursor.fetchone()
        cursor.execute("SELECT * FROM Producto WHERE id_categoria = ?", (id_categoria,))
        productos = [dict(producto) for producto in cursor.fetchall()]
        conexion.close()
        if categoria:
            return {"nombre": categoria["nombre"], "descripcion": categoria["descripcion"], "productos": productos}
        return None

    def consultar_info_proveedor(self, id_proveedor):
        conexion = sqlite3.connect(self.direccion_bd)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Proveedor WHERE id_proveedor = ?", (id_proveedor,))
        proveedor = cursor.fetchone()
        #cursor.execute("SELECT * FROM ProductoProveedor WHERE id_proveedor = ?", (id_proveedor,))
        cursor.execute("SELECT Producto.* FROM Producto JOIN ProductoProveedor ON Producto.id_producto = ProductoProveedor.id_producto WHERE id_proveedor = ?", (id_proveedor,))
        productos = [dict(producto) for producto in cursor.fetchall()]
        conexion.close()
        if proveedor:
            return {"id": proveedor["id_proveedor"], "nombre": proveedor["nombre"], "direccion": proveedor["direccion"], "telefono": proveedor["telefono"], "productos": productos}
        return None

    # Funcion para obtener los productos suministrados por un proveedor
    def obtener_producto_provedor(self, id_proveedor):
        conexion = sqlite3.connect(self.direccion_bd)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        cursor.execute("SELECT Producto.* FROM Producto JOIN ProductoProveedor ON Producto.id_producto = ProductoProveedor.id_producto WHERE id_proveedor = ?", (id_proveedor,))
        productos = [dict(producto) for producto in cursor.fetchall()]

        return productos

    def consultar_info_bodega(self, id_bodega):
        conexion = sqlite3.connect(self.direccion_bd)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Bodega WHERE id_bodega = ?", (id_bodega,))
        bodega = cursor.fetchone()
        cursor.execute("""
            SELECT p.id_producto, p.nombre, pb.cantidad 
            FROM ProductoBodega pb 
            JOIN Producto p ON pb.id_producto = p.id_producto 
            WHERE pb.id_bodega = ?
        """, (id_bodega,))
        productos_bodega = [dict(producto) for producto in cursor.fetchall()]
        conexion.close()
        if bodega:
            return {"nombre": bodega["nombre"], "ubicacion": bodega["ubicacion"], "capacidad": bodega["capacidad"], "productos": productos_bodega}
        return None

    def generar_informe_stock(self):
        conn = sqlite3.connect(self.direccion_bd)
        cursor = conn.cursor()

        cursor.execute('''SELECT SUM(stock) FROM Producto''')
        stock_total = cursor.fetchone()[0]
        
        cursor.execute('''SELECT c.nombre, SUM(p.stock)
                          FROM Producto p
                          LEFT JOIN Categoria c ON p.id_categoria = c.id_categoria
                          GROUP BY c.nombre''')
        stock_por_categoria_data = cursor.fetchall()
        stock_por_categoria = {nombre: stock for nombre, stock in stock_por_categoria_data}

        cursor.execute('''SELECT pr.nombre, SUM(p.stock)
                          FROM Producto p
                          LEFT JOIN ProductoProveedor pp ON p.id_producto = pp.id_producto
                          LEFT JOIN Proveedor pr ON pp.id_proveedor = pr.id_proveedor
                          GROUP BY pr.nombre''')
        stock_por_proveedor_data = cursor.fetchall()
        stock_por_proveedor = {nombre: stock for nombre, stock in stock_por_proveedor_data}

        cursor.execute('''SELECT b.nombre, SUM(pb.cantidad)
                          FROM Bodega b
                          LEFT JOIN ProductoBodega pb ON b.id_bodega = pb.id_bodega
                          GROUP BY b.nombre''')
        stock_por_bodega_data = cursor.fetchall()
        stock_por_bodega = {nombre: cantidad for nombre, cantidad in stock_por_bodega_data}

        conn.close()
        return stock_total, stock_por_categoria, stock_por_proveedor, stock_por_bodega



    #ESTA FUNCIÓN ELIMINA LA BASE DE DATOS, EL OBJETIVO DE ELLA ES PARA PODER REALIZAR PRUEBAS
    def eliminar_bd():
        if os.path.exists('gestion_inventario.db'):
            os.remove('gestion_inventario.db')
            print("Base de datos eliminada con éxito.")
        else:
            print("La base de datos no existe.")
from flask import Blueprint, render_template, request, redirect, g
from services.gestion_bd import GestionBD
from models.producto import Producto
from models.categoria import Categoria
from models.proveedor import Proveedor
from models.bodega import Bodega
from models.producto_proveedor import ProductoProveedor
from models.producto_bodega import ProductoBodega

main = Blueprint("main", __name__)

# Funcion para inicializar la base de datos antes de cualquier peticion
@main.before_request
def inicializar_bd():
    bd = GestionBD()
    g.bd = bd # Definir una variable global para gestion de bd
    bd.crear_bd()

@main.route("/")
def ruta_raiz():
    return render_template("index.html")

@main.route("/consultar_producto")
def consultar_producto():
    bd = g.get("bd")
    productos = bd.obtener_productos()

    return render_template("consultar_productos.html", productos = productos)

@main.route("/consultar_categoria")
def consultar_categoria():
    bd = g.get("bd")
    categorias = bd.obtener_categorias()

    return render_template("consultar_categorias.html", categorias = categorias)

@main.route("/categoria/<int:id>")
def categoria(id):
    bd = g.get("bd")
    info_categoria = bd.consultar_info_categoria(id)

    return render_template("categoria.html", categoria = info_categoria)

@main.route("/consultar_proveedor")
def consultar_proveedor():
    bd = g.get("bd")
    proveedores = bd.obtener_proveedores()

    return render_template("consultar_proveedores.html", proveedores = proveedores)

@main.route("/consultar_bodega")
def consultar_bodega():
    bd = g.get("bd")
    bodegas = bd.obtener_bodegas()

    return render_template("consultar_bodegas.html", bodegas = bodegas)

@main.route("/proveedor/<int:id>")
def proveedor(id):
    bd = g.get("bd")
    proveedor = bd.consultar_info_proveedor(id)

    print(proveedor)

    return render_template("proveedor.html", proveedor = proveedor)

@main.route("/bodega/<int:id>")
def bodega(id):
    bd = g.get("bd")
    bodega = bd.consultar_info_bodega(id)

    print(bodega)

    return render_template("bodega.html", bodega = bodega)

#Rutas para registrar entidades
@main.route('/registrar_producto', methods=['GET', 'POST'])
def registrar_producto():
    bd = g.get("bd")
    categorias = bd.obtener_ids_categorias()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        id_categoria = int(request.form.get("opciones"))

        prod = Producto(nombre, descripcion, precio, stock, id_categoria)
        bd.registrar_producto(prod.nombre, prod.descripcion, prod.precio, prod.stock, prod.id_categoria)
        return redirect('/')
    return render_template('registrar_producto.html', opciones=categorias)

@main.route('/registrar_categoria', methods=['GET', 'POST'])
def registrar_categoria():
    bd = g.get("bd")

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        cat = Categoria(nombre, descripcion)
        bd.registrar_categoria(cat.nombre, cat.descripcion)
        return redirect('/')
    return render_template('registrar_categoria.html')

@main.route('/registrar_proveedor', methods=['GET', 'POST'])
def registrar_proveedor():
    bd = g.get("bd")

    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        prov = Proveedor(nombre, direccion, telefono)
        bd.registrar_proveedor(prov.nombre, prov.direccion, prov.telefono)
        return redirect('/')
    return render_template('registrar_proveedor.html')

@main.route('/registrar_bodega', methods=['GET', 'POST'])
def registrar_bodega():
    bd = g.get("bd")

    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad = int(request.form['capacidad'])

        bod = Bodega(nombre, ubicacion, capacidad)
        bd.registrar_bodega(bod.nombre, bod.ubicacion, bod.capacidad)
        return redirect('/')
    return render_template('registrar_bodega.html')

# Rutas para gestionar stock
@main.route('/gestionar_stock', methods=['GET', 'POST'])
def gestionar_stock():
    bd = g.get("bd")
    if request.method == 'POST':
        operacion = request.form['operacion']
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        if operacion == 'agregar':
            bd.agregar_stock(id_producto, cantidad)
        elif operacion == 'retirar':
            bd.retirar_stock(id_producto, cantidad)
        return redirect('/')
    return render_template('gestionar_stock.html')

# Rutas para consultas y reportes
@main.route('/consultar_info', methods=['GET', 'POST'])
def consultar_info():
    bd = g.get("bd")
    if request.method == 'POST':
        tipo_consulta = request.form['tipo_consulta']
        id_entidad = int(request.form['id_entidad'])
        if tipo_consulta == 'producto':
            info = bd.consultar_info_producto(id_entidad)
        elif tipo_consulta == 'categoria':
            info = bd.consultar_info_categoria(id_entidad)
        elif tipo_consulta == 'proveedor':
            info = bd.consultar_info_proveedor(id_entidad)
        elif tipo_consulta == 'bodega':
            info = bd.consultar_info_bodega(id_entidad)
        return render_template('consultar_info.html', info=info)
    return render_template('consultar_info.html')

@main.route('/informe_stock')
def informe_stock():
    bd = g.get("bd")
    stock_total, stock_por_categoria, stock_por_proveedor, stock_por_bodega = bd.generar_informe_stock()
    return render_template('informe_stock.html', stock_total=stock_total, stock_por_categoria=stock_por_categoria, stock_por_proveedor=stock_por_proveedor, stock_por_bodega=stock_por_bodega)


@main.route('/producto/<int:id>')
def mostrar_producto(id):
    bd = g.get("bd")
    producto = bd.consultar_info_producto(id)
    if producto:
        return render_template('producto.html', producto=producto)
    return "Producto no encontrado", 404

@main.route('/categoria/<int:id>')
def mostrar_categoria(id):
    bd = g.get("bd")
    categoria = bd.consultar_info_categoria(id)
    if categoria:
        return render_template('categoria.html', categoria=categoria)
    return "Categoría no encontrada", 404

@main.route('/proveedor/<int:id>')
def mostrar_proveedor(id):
    bd = g.get("bd")
    proveedor = bd.consultar_info_proveedor(id)
    if proveedor:
        return render_template('proveedor.html', proveedor=proveedor)
    return "Proveedor no encontrado", 404

@main.route('/bodega/<int:id>')
def mostrar_bodega(id):
    bd = g.get("bd")
    bodega = bd.consultar_info_bodega(id)
    if bodega:
        return render_template('bodega.html', bodega=bodega)
    return "Bodega no encontrada", 404

@main.route("/agregar_producto_categoria", methods=['GET', 'POST'])
def agregar_producto_categoria():
    db = g.get("bd")
    categorias = db.obtener_ids_categorias()

    if request.method == "POST":
        id_producto = int(request.form["id_producto"])
        id_categoria = int(request.form.get("opciones"))

        db.agregar_producto_a_categoria(id_producto, id_categoria)

    return render_template("registrar_producto_categoria.html", opciones=categorias)

@main.route("/agregar_producto_proveedor", methods=['GET', 'POST'])
def agregar_producto_proveedor():
    db = g.get("bd")
    proveedores = db.obtener_ids_proveedor()

    if request.method == "POST":
        id_producto = int(request.form["id_producto"])
        id_proveedor = int(request.form.get("opciones"))

        prod_proveedor = ProductoProveedor(id_producto, id_proveedor)

        db.agregar_producto_a_proveedor(prod_proveedor.id_producto, prod_proveedor.id_proveedor)

    return render_template("registrar_producto_proveedor.html", opciones = proveedores)

@main.route("/agregar_producto_bodega", methods=['GET', 'POST'])
def agregar_producto_bodega():
    db = g.get("bd")
    bodegas = db.obtener_ids_bodegas()

    if request.method == "POST":
        id_producto = int(request.form["id_producto"])
        id_bodega = int(request.form.get("opciones"))
        cantidad = int(request.form["cantidad"])

        prod_bodega = ProductoBodega(id_bodega, id_producto, cantidad)

        print(id_bodega, "id")

        #db.agregar_producto_a_bodega(prod_bodega.id_producto, prod_bodega.id_bodega, prod_bodega.cantidad)

    return render_template("registrar_producto_bodega.html", opciones = bodegas)

@main.route("/eliminar_producto_categoria/<int:id>")
def eliminar_producto_categoria(id):
    db = g.get("bd")

    db.eliminar_producto_de_categoria(id)

    return redirect("/consultar_categoria")

@main.route("/eliminar_producto_proveedor/<int:id_proveedor>/<int:id_producto>")
def eliminar_producto_proveedor(id_proveedor, id_producto):
    db = g.get("bd")

    db.eliminar_producto_de_proveedor(id_producto, id_proveedor)

    return redirect("/consultar_proveedor")

@main.route("/test")
def test():
    bd = g.get("bd")
    categorias = bd.obtener_ids_categorias()

    return categorias




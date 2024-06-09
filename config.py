import os

class Config:
    TEMPLATE_FOLDER = "templates/"
    STATIC_FOLDER = "static/"
    DIRECCION_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "gestion_inventario.sqlite3")
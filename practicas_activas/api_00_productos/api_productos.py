from typing import Optional
from uuid import uuid4 as uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Base para la appi
class Producto(BaseModel):
    id: Optional[str]
    nombre: str
    precio_compra: float
    precio_venta: float
    proveedor: str


app = FastAPI()

productos = []


@app.get('/')
def index():
    return {'mensaje': 'Bienvenidos a la API de Productos'}


@app.get('/producto')
def obtener_productos():
    return productos


@app.post('/producto')
def crear_producto(producto: Producto):
####################################################################################################
# Un UUID es un identificador único. Corresponde a las siglas de Identificador Único Universal. 
# Es un código de 16 bytes compuesto por 32 caracteres. Estos códigos o identificadores se usan para
# identificar información que debe ser única y que no debe repetirse.    
    producto.id = str(uuid())

    productos.append(producto)
    return {'mensaje': 'Producto creado satisfactoriamente.'}


#############################################################################################################
#Ruta GET que Permite Buscar un Producto a partir de su ID
#Búsqueda sobre una Lista con la Función Filter
@app.get('/producto/{producto_id}')
def obtener_producto_por_id(producto_id: str):
    resultado = list(filter(lambda p: p.id == producto_id, productos))

    if len(resultado):
        return resultado[0]   
 
# La función raise se usa para indicar que se ha producido un error o una condición excepcional. 
# La información sobre el error se captura en un objeto de excepción.    
    raise HTTPException(status_code=404, detail=f'El producto con el ID {producto_id} no fue encontrado.')
# Los códigos de estado de respuesta HTTP indican si se ha completado satisfactoriamente una solicitud HTTP específica. Las respuestas se agrupan en cinco clases:
#    Respuestas informativas (100–199),
#    Respuestas satisfactorias (200–299),
#    Redirecciones (300–399),
#    Errores de los clientes (400–499),
#    y errores de los servidores (500–599).

#############################################################################################################
# Ruta DELETE para Eliminar un Producto de la Lista Usando Su ID
@app.delete('/producto/{producto_id}')
def eliminar_producto_por_id(producto_id: str):
    resultado = list(filter(lambda p: p.id == producto_id, productos))

    if len(resultado):
        producto = resultado[0]
        productos.remove(producto)

        return {'mensaje': f'El producto con ID {producto_id} fue eliminado.'}
# 404 Not Found
# El servidor no pudo encontrar el contenido solicitado. Este código de respuesta es uno de los más famosos dada su alta
# ocurrencia en la web.

    raise HTTPException(status_code=404, detail=f'El producto con el ID {producto_id} no fue encontrado.')
##############################################################################################################
#Actualizar un Producto Por Medio del Método PUT de HTTP
@app.put('/producto/{producto_id}')
def actualizar_producto(producto_id: str, producto: Producto):
    resultado = list(filter(lambda p: p.id == producto_id, productos))

    if len(resultado):
        producto_encontrado = resultado[0]
        producto_encontrado.nombre = producto.nombre
        producto_encontrado.precio_compra = producto.precio_compra
        producto_encontrado.precio_venta = producto.precio_venta
        producto_encontrado.proveedor = producto.proveedor

        return producto_encontrado

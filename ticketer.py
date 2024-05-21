from dbconfig import *
def generar_ticket(id_orden):

    ordenes = pedidos_collection

    orden = ordenes.find_one({'_id': id_orden})
    if not orden:
        return 'Orden no encontrada'

    nombre_cliente = orden.get('nombre', 'Nombre no disponible')
    ticket = f"Orden: {orden['numero_pedido']}\n"
    ticket += f"Cliente: {nombre_cliente}\n"
    
    total_con_impuestos = 0
    for producto in orden['productos']:
        subtotal = producto['precio'] * producto['cantidad']
        total_con_impuestos += subtotal
        ticket += f"Producto: {producto['producto_nombre']}\n"
        ticket += f"Cantidad: {producto['cantidad']}\n"
        ticket += f"Precio: ${producto['precio']}\n"
        ticket += f"Subtotal: ${subtotal}\n"
        ticket += "------------------------\n"
    
    total_con_impuestos *= 1.15
    ticket += f"Total: ${total_con_impuestos}\n"

    return ticket

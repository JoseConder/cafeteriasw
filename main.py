import tkinter as tk
from tkinter import messagebox
from ticketer import generar_ticket
from dbconfig import *

productos_collection = db['productos']
pedidos_collection = db['pedidos']

productos_seleccionados = []
cantidades_seleccionadas = []
contador_pedidos = 1

def agregar_producto():
    producto_index = listbox_productos.curselection()
    if not producto_index:
        messagebox.showerror("Error", "Por favor seleccione un producto")
        return

    cantidad = cantidad_var.get()
    if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
        return

    producto = productos[int(producto_index[0])]
    productos_seleccionados.append(producto)
    cantidades_seleccionadas.append(int(cantidad))

    actualizar_lista_pedido()

def eliminar_producto():
    producto_index = listbox_pedido.curselection()
    if not producto_index:
        messagebox.showerror("Error", "Por favor seleccione un producto de la orden")
        return

    del productos_seleccionados[producto_index[0]]
    del cantidades_seleccionadas[producto_index[0]]

    actualizar_lista_pedido()

def actualizar_lista_pedido():
    listbox_pedido.delete(0, tk.END)
    for i, producto in enumerate(productos_seleccionados):
        cantidad = cantidades_seleccionadas[i]
        listbox_pedido.insert(tk.END, f"{producto['nombre']} - {cantidad}")

def agregar_pedido():
    global contador_pedidos  

    if not productos_seleccionados:
        messagebox.showerror("Error", "Por favor seleccione al menos un producto")
        return

    nombre = entry_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "Por favor ingrese su nombre")
        return

    total = sum([producto['precio'] * cantidad for producto, cantidad in zip(productos_seleccionados, cantidades_seleccionadas)])
    total_con_impuestos = total * 1.15

    global contador_pedidos  
    ticket = {
        "numero_pedido": contador_pedidos,  
        "nombre": nombre,
        "productos": [{"producto_id": producto['_id'], "producto_nombre": producto['nombre'], "precio": producto['precio'], "cantidad": cantidad} for producto, cantidad in zip(productos_seleccionados, cantidades_seleccionadas)],
        "total": total_con_impuestos,
        "estado": "En espera"
    }
    resultado_insert = pedidos_collection.insert_one(ticket)

    orden_id = resultado_insert.inserted_id

    ticket_generado = generar_ticket(orden_id)
    print(ticket_generado)

    messagebox.showinfo("Pedido Generado", "Su pedido ha sido generado")
    actualizar_cola_espera()

    contador_pedidos += 1  

    if contador_pedidos > 500:  
        contador_pedidos = 1

def actualizar_cola_espera():
    pedidos = pedidos_collection.find()
    listbox_espera.delete(0, tk.END)
    for pedido in pedidos:
        nombre_cliente = pedido.get('nombre', 'Nombre no disponible')
        total_pedido = pedido.get('total', 'Total no disponible')
        estado_pedido = pedido.get('estado', 'Estado no disponible')
        listbox_espera.insert(tk.END, f"{nombre_cliente} - ${total_pedido} - {estado_pedido}")

root = tk.Tk()
root.title("Sistema de Pedidos")

tk.Label(root, text="Nombre:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

tk.Label(root, text="Productos Disponibles:").pack(pady=10)
listbox_productos = tk.Listbox(root, width=50, height=10)
listbox_productos.pack()
productos = list(productos_collection.find())
for producto in productos:
    listbox_productos.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")
cantidad_var = tk.StringVar()
tk.Label(root, text="Cantidad:").pack()
entry_cantidad = tk.Entry(root, textvariable=cantidad_var)
entry_cantidad.pack()

tk.Button(root, text="Agregar Producto", command=agregar_producto).pack(pady=5)

tk.Label(root, text="Productos en la Orden:").pack()
listbox_pedido = tk.Listbox(root, width=50, height=10)
listbox_pedido.pack()

tk.Button(root, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)

tk.Button(root, text="Agregar Pedido", command=agregar_pedido).pack(pady=10)

tk.Label(root, text="Pedidos en Espera:").pack()
listbox_espera = tk.Listbox(root, width=50, height=10)
listbox_espera.pack()

actualizar_cola_espera()

root.mainloop()


import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
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


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


root = ctk.CTk()
root.title("Sistema de Pedidos")


frame_top = ctk.CTkFrame(root)
frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


ctk.CTkLabel(frame_top, text="Nombre:").pack(side=tk.LEFT)
entry_nombre = ctk.CTkEntry(frame_top)
entry_nombre.pack(side=tk.LEFT, padx=5)


frame_productos = ctk.CTkFrame(root)
frame_productos.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


ctk.CTkLabel(frame_productos, text="Productos Disponibles:").pack(side=tk.TOP, anchor=tk.W)
listbox_productos = tk.Listbox(frame_productos, width=50, height=10)
listbox_productos.pack(side=tk.LEFT)
productos = list(productos_collection.find())
for producto in productos:
   listbox_productos.insert(tk.END, f"{producto['nombre']} - ${producto['precio']}")


frame_cantidad = ctk.CTkFrame(frame_productos)
frame_cantidad.pack(side=tk.LEFT, padx=10)


ctk.CTkLabel(frame_cantidad, text="Cantidad:").pack()
cantidad_var = ctk.StringVar()
entry_cantidad = ctk.CTkEntry(frame_cantidad, textvariable=cantidad_var)
entry_cantidad.pack()


ctk.CTkButton(frame_cantidad, text="Agregar Producto", command=agregar_producto).pack(pady=5)


frame_pedido = ctk.CTkFrame(root)
frame_pedido.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


ctk.CTkLabel(frame_pedido, text="Productos en la Orden:").pack(side=tk.TOP, anchor=tk.W)
listbox_pedido = tk.Listbox(frame_pedido, width=50, height=10)
listbox_pedido.pack(side=tk.LEFT)


ctk.CTkButton(frame_pedido, text="Eliminar Producto", command=eliminar_producto).pack(side=tk.LEFT, padx=10)


ctk.CTkButton(root, text="Agregar Pedido", command=agregar_pedido).pack(pady=10)


frame_espera = ctk.CTkFrame(root)
frame_espera.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


ctk.CTkLabel(frame_espera, text="Pedidos en Espera:").pack(side=tk.TOP, anchor=tk.W)
listbox_espera = tk.Listbox(frame_espera, width=50, height=10)
listbox_espera.pack()


actualizar_cola_espera()


root.mainloop()

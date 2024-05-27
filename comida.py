import tkinter as tk
from tkinter import messagebox
from dbconfig import *

def agregar_producto():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    tiempo_preparacion = entry_tiempo_preparacion.get()

    if not nombre or not descripcion or not precio or not tiempo_preparacion:
        messagebox.showerror("Error", "Por favor complete todos los campos")
        return

    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": float(precio),
        "tiempo_preparacion": int(tiempo_preparacion)
    }
    productos_collection.insert_one(producto)
    messagebox.showinfo("Producto Agregado", "El producto ha sido agregado exitosamente")
    limpiar_campos()
    actualizar_lista_productos()

def actualizar_lista_productos():
    productos = productos_collection.find()
    listbox_productos.delete(0, tk.END)
    for producto in productos:
        listbox_productos.insert(tk.END, f"{producto['nombre']} - {producto['descripcion']} - ${producto['precio']} - {producto['tiempo_preparacion']} mins")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_tiempo_preparacion.delete(0, tk.END)

root = tk.Tk()
root.title("Gestión de Productos")

frame_campos = tk.Frame(root)
frame_campos.pack(pady=10)

tk.Label(frame_campos, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_campos, width=50)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
entry_descripcion = tk.Entry(frame_campos, width=50)
entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Precio ($):").grid(row=2, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_campos, width=50)
entry_precio.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Tiempo de Preparación (minutos):").grid(row=3, column=0, padx=5, pady=5)
entry_tiempo_preparacion = tk.Entry(frame_campos, width=50)
entry_tiempo_preparacion.grid(row=3, column=1, padx=5, pady=5)

tk.Button(root, text="Agregar Producto", command=agregar_producto).pack()

frame_productos = tk.Frame(root)
frame_productos.pack(pady=10)

tk.Label(frame_productos, text="Lista de Productos:").pack()
listbox_productos = tk.Listbox(frame_productos, width=80, height=15)
listbox_productos.pack()

actualizar_lista_productos()

root.mainloop()

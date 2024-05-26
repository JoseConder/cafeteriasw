import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dbconfig import *
import customtkinter as ctk

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
    treeview_productos.delete(*treeview_productos.get_children())
    productos = productos_collection.find()
    for producto in productos:
        nombre = producto['nombre']
        descripcion = producto['descripcion']
        precio = producto['precio']
        tiempo_preparacion = producto['tiempo_preparacion']
        treeview_productos.insert("", "end", values=(nombre, descripcion, f"${precio}", f"{tiempo_preparacion} mins"))

def limpiar_campos():
    entry_nombre.delete(0, ctk.END)
    entry_descripcion.delete(0, ctk.END)
    entry_precio.delete(0, ctk.END)
    entry_tiempo_preparacion.delete(0, ctk.END)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sistema de Pedidos")

frame_campos = ctk.CTkFrame(root)
frame_campos.pack(pady=10)

ctk.CTkLabel(frame_campos, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = ctk.CTkEntry(frame_campos, width=300)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_campos, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
entry_descripcion = ctk.CTkEntry(frame_campos, width=300)
entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Precio ($):").grid(row=2, column=0, padx=5, pady=5)
entry_precio = ctk.CTkEntry(frame_campos, width=300)
entry_precio.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_campos, text="Tiempo de Preparación (minutos):").grid(row=3, column=0, padx=5, pady=5)
entry_tiempo_preparacion = ctk.CTkEntry(frame_campos, width=300)
entry_tiempo_preparacion.grid(row=3, column=1, padx=5, pady=5)

ctk.CTkButton(root, text="Agregar Producto", command=agregar_producto).pack()

frame_productos = ctk.CTkFrame(root)
frame_productos.pack(pady=10)

ctk.CTkLabel(frame_productos, text="Lista de Productos:").pack()

columns = ("Nombre", "Descripción", "Precio", "Tiempo de Preparación")
treeview_productos = ttk.Treeview(frame_productos, columns=columns, show="headings")
for col in columns:
    treeview_productos.heading(col, text=col)
treeview_productos.pack()

actualizar_lista_productos()

root.mainloop()

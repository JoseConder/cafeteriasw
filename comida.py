import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from dbconfig import *
import threading

def mostrar_alerta(tipo, mensaje):
    alerta_frame = ctk.CTkFrame(root, corner_radius=10)
    alerta_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    mensaje_label = ctk.CTkLabel(alerta_frame, text=mensaje, wraplength=300, font=('Arial', 14))
    mensaje_label.pack(padx=20, pady=10)

    if tipo == "error":
        alerta_frame.configure(fg_color=("red", "darkred"))
    elif tipo == "info":
        alerta_frame.configure(fg_color=("green", "darkgreen"))

    def cerrar_alerta():
        alerta_frame.after(3000, alerta_frame.destroy)  # Espera 3 segundos y cierra la alerta

    threading.Thread(target=cerrar_alerta).start()

def agregar_producto():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    tiempo_preparacion = entry_tiempo_preparacion.get()

    if not nombre or not descripcion or not precio:
        mostrar_alerta("error", "Por favor complete todos los campos")
        return

    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": float(precio),
        "tiempo_preparacion": int(tiempo_preparacion)
    }
    productos_collection.insert_one(producto)
    mostrar_alerta("info", "El producto ha sido agregado exitosamente")
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
ctk.set_default_color_theme("green")

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

ctk.CTkButton(root, text="Agregar Producto", command=agregar_producto).pack(pady=10)

frame_productos = ctk.CTkFrame(root)
frame_productos.pack(pady=10, fill="both", expand=True)

ctk.CTkLabel(frame_productos, text="Lista de Productos:").pack(pady=5)

columns = ("Nombre", "Descripción", "Precio", "Tiempo de Preparación")
treeview_productos = ttk.Treeview(frame_productos, columns=columns, show="headings")
treeview_productos.heading("Nombre", text="Nombre")
treeview_productos.heading("Descripción", text="Descripción")
treeview_productos.heading("Precio", text="Precio")
treeview_productos.heading("Tiempo de Preparación", text="Tiempo de Preparación")

treeview_productos.column("Nombre", width=150, anchor="center")
treeview_productos.column("Descripción", width=200, anchor="center")
treeview_productos.column("Precio", width=100, anchor="center")
treeview_productos.column("Tiempo de Preparación", width=200, anchor="center")

# Configurar colores manualmente para coincidir con el tema
style = ttk.Style()
style.configure("Treeview", background="#2b2b2b", foreground="#ffffff", fieldbackground="#2b2b2b", font=("Arial", 12))
style.configure("Treeview.Heading", background="#2b2b2b", foreground="#ffffff", font=("Arial", 14, "bold"))

# Aplicar el estilo a la Treeview
treeview_productos.configure(style="Treeview")
treeview_productos.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

actualizar_lista_productos()

root.mainloop()

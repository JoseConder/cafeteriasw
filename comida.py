import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dbconfig import *
import customtkinter as ctk
import threading

def mostrar_alerta(tipo, mensaje):
    alerta_frame = ctk.CTkFrame(root, corner_radius=10)
    alerta_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    mensaje_label = ctk.CTkLabel(alerta_frame, text=mensaje, wraplength=300, font=('Arial', 14))
    mensaje_label.pack(padx=20, pady=10)

    if tipo == "Error":
        alerta_frame.configure(fg_color=("red", "darkred"))
    elif tipo == "info":
        alerta_frame.configure(fg_color=("green", "darkgreen"))

    def cerrar_alerta():
        alerta_frame.after(1000, alerta_frame.destroy)  # Espera 3 segundos y cierra la alerta

    threading.Thread(target=cerrar_alerta).start()



def agregar_producto():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    tiempo_preparacion = entry_tiempo_preparacion.get()

    if not nombre or not descripcion or not precio or not tiempo_preparacion:
        mostrar_alerta("Error", "Por favor complete todos los campos")
        return

    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": float(precio),
        "tiempo_preparacion": int(tiempo_preparacion)
    }
    productos_collection.insert_one(producto)
    mostrar_alerta("info","El producto ha sido agregado exitosamente")
    limpiar_campos()
    actualizar_lista_productos()

def eliminar_producto():
    selected_item = treeview_productos.selection()
    if not selected_item:
        mostrar_alerta("Error", "Por favor seleccione un producto para eliminar")
        return

    nombre_producto = treeview_productos.item(selected_item, "values")[0]
    productos_collection.delete_one({"nombre": nombre_producto})
    mostrar_alerta("info", f"El producto '{nombre_producto}' ha sido eliminado exitosamente")
    actualizar_lista_productos()

def actualizar_producto():
    selected_item = treeview_productos.selection()
    if not selected_item:
        mostrar_alerta("Error", "Por favor seleccione un producto para actualizar")
        return

    nombre_viejo = treeview_productos.item(selected_item, "values")[0]

    # Obtener los nuevos detalles del producto
    nuevo_nombre = entry_nombre.get()
    nueva_descripcion = entry_descripcion.get()
    nuevo_precio = entry_precio.get()
    nuevo_tiempo_preparacion = entry_tiempo_preparacion.get()

    # Actualizar los detalles del producto en la base de datos
    productos_collection.update_one(
        {"nombre": nombre_viejo},
        {"$set": {
            "nombre": nuevo_nombre,
            "descripcion": nueva_descripcion,
            "precio": float(nuevo_precio),
            "tiempo_preparacion": int(nuevo_tiempo_preparacion)
        }}
    )

    mostrar_alerta("info", f"El producto '{nombre_viejo}' ha sido actualizado exitosamente")
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

# Configuración de la apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Creación de la interfaz de usuario
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

# ctk.CTkButton(root, text="Agregar Producto", command=agregar_producto).pack()
# ctk.CTkButton(root, text="Actualizar Producto", command=actualizar_producto).pack()

ctk.CTkButton(root, text="Agregar Producto", command=agregar_producto).pack(pady=5)
ctk.CTkButton(root, text="Actualizar Producto", command=actualizar_producto).pack(pady=5)


frame_productos = ctk.CTkFrame(root)
frame_productos.pack(pady=10,fill="both", expand=True)

ctk.CTkLabel(frame_productos, text="Lista de Productos:").pack(pady=5)

columns = ("Nombre", "Descripción", "Precio", "Tiempo de Preparación")
treeview_productos = ttk.Treeview(frame_productos, columns=columns, show="headings")
for col in columns:
    treeview_productos.heading(col, text=col)
treeview_productos.pack()
ctk.CTkButton(root, text="Eliminar Producto", fg_color=("darkred"),command=eliminar_producto).pack()



# Configurar colores manualmente para coincidir con el tema
style = ttk.Style()
style.configure("Treeview", background="#2b2b2b", foreground="#ffffff", fieldbackground="#2b2b2b", font=("Arial", 12))
style.configure("Treeview.Heading", background="#2b2b2b", foreground="#ffffff", font=("Arial", 14, "bold"))

# Aplicar el estilo a la Treeview
treeview_productos.configure(style="Treeview")
treeview_productos.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)


actualizar_lista_productos()

root.mainloop()
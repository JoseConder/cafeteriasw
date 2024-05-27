import tkinter as tk
from dbconfig import *
from bson import ObjectId

def actualizar_cola_espera():
    pedidos = pedidos_collection.find({"estado": "En espera"})
    listbox_espera.delete(0, tk.END)
    for pedido in pedidos:
        ticket_info = f"Ticket {pedido['numero_pedido']} - {pedido['nombre']}\n"
        for producto in pedido['productos']:
            producto_info = productos_collection.find_one({"_id": producto['producto_id']})
            if producto_info:
                descripcion_producto = f"    {producto_info['nombre']} (x{producto['cantidad']}) - ${producto['precio']}\n"
                descripcion_producto += f"    Descripción: {producto_info['descripcion']}\n"
                ticket_info += descripcion_producto
        listbox_espera.insert(tk.END, ticket_info)
    root.after(5000, actualizar_cola_espera)  # Actualizar cada 5 segundos

def marcar_como_listo():
    selected_index = listbox_espera.curselection()
    if not selected_index:
        return
    selected_ticket_info = listbox_espera.get(selected_index)
    selected_ticket_id1 = selected_ticket_info.split()[1]
    selected_ticket_id2 = selected_ticket_info.split()[3]
    pedidos_collection.update_one({"numero_pedido": int(selected_ticket_id1), "nombre": selected_ticket_id2, "estado": "En espera"}, {"$set": {"estado": "Listo"}})
    #pedidos_collection.update_one({"_id": ObjectId(selected_ticket_id)}, {"$set": {"estado": "Listo"}})
    actualizar_cola_espera()

root = tk.Tk()
root.title("Control Cocina")

tk.Label(root, text="Pedidos en Espera:").pack(pady=10)
listbox_espera = tk.Listbox(root, width=500, height=20)
listbox_espera.pack()

tk.Button(root, text="Marcar como Listo", command=marcar_como_listo).pack(pady=5)

actualizar_cola_espera()

root.mainloop()

import tkinter as tk
from dbconfig import *

def actualizar_cola_espera():
    pedidos = pedidos_collection.find({"estado": "En espera"})
    listbox_espera.delete(0, tk.END)
    for pedido in pedidos:
        ticket_info = f"Ticket {pedido['numero_pedido']} - {pedido['nombre']} "
        listbox_espera.insert(tk.END, ticket_info)
    root.after(5000, actualizar_cola_espera)  

def marcar_como_listo():
    selected_index = listbox_espera.curselection()
    if not selected_index:
        return
    selected_ticket_info = listbox_espera.get(selected_index)
    selected_ticket_number = int(selected_ticket_info.split()[1])  
    pedidos_collection.update_one({"numero_pedido": selected_ticket_number}, {"$set": {"estado": "Listo"}})
    actualizar_cola_espera()  

root = tk.Tk()
root.title("Control Cocina")

tk.Label(root, text="Pedidos en Espera:").pack(pady=10)
listbox_espera = tk.Listbox(root, width=50, height=20)
listbox_espera.pack()

tk.Button(root, text="Marcar como Listo", command=marcar_como_listo).pack(pady=5)

actualizar_cola_espera()

root.mainloop()

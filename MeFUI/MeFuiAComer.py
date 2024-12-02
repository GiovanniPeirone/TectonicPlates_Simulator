import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Aviso")
root.geometry("800x400")  # Tamaño de la ventana

# Configurar el recuadro
frame = tk.Frame(root, bg="#ffe0b2", borderwidth=5, relief="solid")
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Texto en el recuadro
label = tk.Label(
    frame,
    text="Me fui a comer",
    font=("Arial", 40, "bold"),
    fg="#ff5722",
    bg="#ffe0b2"
)
label.pack(expand=True)

# Ejecutar la ventana
root.mainloop()

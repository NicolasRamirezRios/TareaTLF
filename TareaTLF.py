import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3
from matplotlib.figure import Figure

# Funciones de operaciones entre conjuntos
def union(conj1, conj2):
    resultado = conj1[:]
    for elem in conj2:
        if elem not in resultado:
            resultado.append(elem)
    return resultado

def interseccion(conj1, conj2):
    return [elem for elem in conj1 if elem in conj2]

def diferencia(conj1, conj2):
    return [elem for elem in conj1 if elem not in conj2]

def diferencia_simetrica(conj1, conj2):
    return union(diferencia(conj1, conj2), diferencia(conj2, conj1))

def es_subconjunto(conj1, conj2):
    return all(elem in conj2 for elem in conj1)

def es_superconjunto(conj1, conj2):
    return es_subconjunto(conj2, conj1)

# Función para graficar el diagrama de Venn para 2 o 3 conjuntos en la interfaz
def graficar_diagrama(conjunto1, conjunto2, conjunto3=None):
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)

    set1 = set(conjunto1)
    set2 = set(conjunto2)

    if conjunto3 is None:  # Diagrama de Venn para 2 conjuntos
        venn2([set1, set2], set_labels=('Conjunto 1', 'Conjunto 2'), ax=ax)
    else:  # Diagrama de Venn para 3 conjuntos
        set3 = set(conjunto3)
        venn3([set1, set2, set3], set_labels=('Conjunto 1', 'Conjunto 2', 'Conjunto 3'), ax=ax)

    # Limpia el canvas anterior antes de agregar uno nuevo
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para manejar los eventos de la interfaz
def realizar_operaciones():
    try:
        conjunto1 = list(map(int, entry_conjunto1.get().split(',')))
        conjunto2 = list(map(int, entry_conjunto2.get().split(',')))

        operacion = var_operacion.get()
        num_conjuntos = var_num_conjuntos.get()

        if num_conjuntos == 3:
            conjunto3 = list(map(int, entry_conjunto3.get().split(',')))
        else:
            conjunto3 = None

        if operacion == 'Unión':
            if conjunto3 is not None:
                resultado = union(union(conjunto1, conjunto2), conjunto3)
            else:
                resultado = union(conjunto1, conjunto2)
        elif operacion == 'Intersección':
            if conjunto3 is not None:
                resultado = interseccion(interseccion(conjunto1, conjunto2), conjunto3)
            else:
                resultado = interseccion(conjunto1, conjunto2)
        elif operacion == 'Diferencia':
            if conjunto3 is not None:
                resultado = diferencia(diferencia(conjunto1, conjunto2), conjunto3)
            else:
                resultado = diferencia(conjunto1, conjunto2)
        elif operacion == 'Diferencia Simétrica':
            if conjunto3 is not None:
                resultado = diferencia_simetrica(diferencia_simetrica(conjunto1, conjunto2), conjunto3)
            else:
                resultado = diferencia_simetrica(conjunto1, conjunto2)
        elif operacion == 'Subconjunto':
            if conjunto3 is not None:
                resultado = es_subconjunto(conjunto1, conjunto2) and es_subconjunto(conjunto1, conjunto3)
            else:
                resultado = es_subconjunto(conjunto1, conjunto2)
        elif operacion == 'Superconjunto':
            if conjunto3 is not None:
                resultado = es_superconjunto(conjunto1, conjunto2) and es_superconjunto(conjunto1, conjunto3)
            else:
                resultado = es_superconjunto(conjunto1, conjunto2)
        else:
            messagebox.showerror("Error", "Operación no válida")
            return

        resultado_label.config(text=f"Resultado: {resultado}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números separados por comas.")

def mostrar_diagrama():
    try:
        conjunto1 = list(map(int, entry_conjunto1.get().split(',')))
        conjunto2 = list(map(int, entry_conjunto2.get().split(',')))

        num_conjuntos = var_num_conjuntos.get()
        if num_conjuntos == 3:
            conjunto3 = list(map(int, entry_conjunto3.get().split(',')))
            graficar_diagrama(conjunto1, conjunto2, conjunto3)
        else:
            graficar_diagrama(conjunto1, conjunto2)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Operaciones de Teoría de Conjuntos")

# Mejora en el estilo de la interfaz
root.geometry("600x600")
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# Labels y Entry para los conjuntos
label_conjunto1 = tk.Label(frame, text="Conjunto 1 (separado por comas):")
label_conjunto1.grid(row=0, column=0, pady=5, sticky="w")
entry_conjunto1 = tk.Entry(frame, width=30)
entry_conjunto1.grid(row=0, column=1, pady=5)

label_conjunto2 = tk.Label(frame, text="Conjunto 2 (separado por comas):")
label_conjunto2.grid(row=1, column=0, pady=5, sticky="w")
entry_conjunto2 = tk.Entry(frame, width=30)
entry_conjunto2.grid(row=1, column=1, pady=5)

label_conjunto3 = tk.Label(frame, text="Conjunto 3 (separado por comas):")
label_conjunto3.grid(row=2, column=0, pady=5, sticky="w")
entry_conjunto3 = tk.Entry(frame, width=30)
entry_conjunto3.grid(row=2, column=1, pady=5)
entry_conjunto3.config(state='disabled')

# Opción para seleccionar el número de conjuntos
var_num_conjuntos = tk.IntVar(value=2)

def actualizar_conjuntos():
    if var_num_conjuntos.get() == 3:
        entry_conjunto3.config(state='normal')
    else:
        entry_conjunto3.config(state='disabled')

label_num_conjuntos = tk.Label(frame, text="Número de conjuntos:")
label_num_conjuntos.grid(row=3, column=0, pady=5, sticky="w")
radio_2conjuntos = tk.Radiobutton(frame, text="2", variable=var_num_conjuntos, value=2, command=actualizar_conjuntos)
radio_2conjuntos.grid(row=3, column=1, sticky='w')
radio_3conjuntos = tk.Radiobutton(frame, text="3", variable=var_num_conjuntos, value=3, command=actualizar_conjuntos)
radio_3conjuntos.grid(row=3, column=1, sticky='e')

# Operaciones disponibles
var_operacion = tk.StringVar(root)
var_operacion.set("Unión")  # Valor predeterminado

operaciones = ["Unión", "Intersección", "Diferencia", "Diferencia Simétrica", "Subconjunto", "Superconjunto"]
operacion_menu = tk.OptionMenu(frame, var_operacion, *operaciones)
operacion_menu.grid(row=4, column=1, pady=5)

# Botón para realizar la operación
boton_operar = tk.Button(frame, text="Realizar operación", command=realizar_operaciones)
boton_operar.grid(row=5, column=1, pady=5)

# Botón para mostrar el diagrama de Venn
boton_diagrama = tk.Button(frame, text="Mostrar Diagrama de Venn", command=mostrar_diagrama)
boton_diagrama.grid(row=6, column=1, pady=5)

# Etiqueta para mostrar resultados
resultado_label = tk.Label(frame, text="Resultado:")
resultado_label.grid(row=7, column=0, columnspan=2, pady=5)

# Frame para la gráfica
plot_frame = tk.Frame(root)
plot_frame.pack(padx=10, pady=10)

# Iniciar la interfaz gráfica
root.mainloop()

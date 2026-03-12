# This code is generated using PyUIbuilder: https://pyuibuilder.com

import os
import tkinter as tk
from tkinter import ttk
from gui.pyuiWidgets.imageLabel import ImageLabel
from utils.utils import obtener_opciones

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GUI:
    main = tk.Tk()
    main.title("Piedra Papel Tijeras Nivel 2")
    main.config(bg="#E4E2E2")
    main.geometry("700x345")
    main.update_idletasks()

    geometryX = 0
    geometryY = 0

    main.geometry("+%d+%d"%(geometryX, geometryY))


    style = ttk.Style(main)
    style.theme_use("vista")


    style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label = ttk.Label(master=main, text="La elección del CPU", style="label.TLabel")
    label.configure(anchor="center")
    label.place(x=39, y=200, width=160, height=40)

    style.configure("button_play.TButton", background="#E4E2E2", foreground="#000")
    style.map("button_play.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    style.configure("label_victorias_variable.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_victorias_variable = ttk.Label(master=main, text="0", style="label_victorias_variable.TLabel")
    label_victorias_variable.configure(anchor="center")
    label_victorias_variable.place(x=570, y=80, width=120, height=40)

    style.configure("label_derrotas_variable.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_derrotas_variable = ttk.Label(master=main, text="0", style="label_derrotas_variable.TLabel")
    label_derrotas_variable.configure(anchor="center")
    label_derrotas_variable.place(x=570, y=140, width=120, height=40)

    style.configure("label_empates_variable.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_empates_variable = ttk.Label(master=main, text="0", style="label_empates_variable.TLabel")
    label_empates_variable.configure(anchor="center")
    label_empates_variable.place(x=570, y=200, width=120, height=40)

    style.configure("label_porcentajes_variable.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_porcentajes_variable = ttk.Label(master=main, text="", style="label_porcentajes_variable.TLabel")
    label_porcentajes_variable.configure(anchor="center")
    label_porcentajes_variable.place(x=570, y=260, width=120, height=40)

    style.configure("label_porcentajes.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_porcentajes = ttk.Label(master=main, text="Porcentajes", style="label_porcentajes.TLabel")
    label_porcentajes.configure(anchor="center")
    label_porcentajes.place(x=470, y=260, width=120, height=40)

    style.configure("label_empates.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_empates = ttk.Label(master=main, text="Empates", style="label_empates.TLabel")
    label_empates.configure(anchor="center")
    label_empates.place(x=470, y=200, width=120, height=40)

    style.configure("label_derrotas.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_derrotas = ttk.Label(master=main, text="Derrotas", style="label_derrotas.TLabel")
    label_derrotas.configure(anchor="center")
    label_derrotas.place(x=470, y=140, width=120, height=40)

    style.configure("label_victorias.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_victorias = ttk.Label(master=main, text="Victorias", style="label_victorias.TLabel")
    label_victorias.configure(anchor="center")
    label_victorias.place(x=470, y=80, width=120, height=40)

    style.configure("label_estadisticas.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_estadisticas = ttk.Label(master=main, text="Estadisticas", style="label_estadisticas.TLabel")
    label_estadisticas.configure(anchor="center")
    label_estadisticas.place(x=520, y=50, width=120, height=40)

    style.configure("option_menu.TCombobox", fieldbackground="#E4E2E2", foreground="#000")
    option_menu_options = obtener_opciones()
    option_menu_var = tk.StringVar(value="Tipos")
    option_menu = ttk.Combobox(main, textvariable=option_menu_var, values=option_menu_options, style="option_menu.TCombobox")
    option_menu.place(x=39, y=99, width=160, height=40)

    style.configure("label1.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label1 = ttk.Label(master=main, text="Tu elección", style="label1.TLabel")
    label1.configure(anchor="center")
    label1.place(x=39, y=49, width=160, height=40)

    style.configure("label_seleccion_cpu_variable.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_seleccion_cpu_variable = ttk.Label(master=main, text="", style="label_seleccion_cpu_variable.TLabel")
    label_seleccion_cpu_variable.configure(anchor="center")
    label_seleccion_cpu_variable.place(x=39, y=250, width=160, height=40)

    style.configure("label_resultado.TLabel", background="#E4E2E2", foreground="#000", font=("", 20), anchor="center")
    label_resultado = ttk.Label(master=main, text="VICTORIA", style="label_resultado.TLabel")
    label_resultado.configure(anchor="center")
    label_resultado.place(x=250, y=180, width=199, height=71)

    style.configure("button_reglas.TButton", background="#E4E2E2", foreground="#000")
    style.map("button_reglas.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    button_reglas = ttk.Button(master=main, text="Reglas", style="button_reglas.TButton")
    button_reglas.place(x=520, y=0, width=122, height=40)
    
    button_play = ttk.Button(master=main, text="Play", style="button_play.TButton")
    button_play.place(x=309, y=129, width=80, height=40)







def top_level_reglas():

    top_level = tk.Toplevel(master=GUI.main)
    top_level.config(bg="#E4E2E2")
    top_level.title("Reglas (si se ve mal mueve la ventana)")
    top_level.geometry("400x403")
    top_level.update_idletasks()

    geometryX = 50
    geometryY = 50

    top_level.geometry("+%d+%d"%(geometryX, geometryY))


    GUI.style.configure("label_img.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    label_img = ImageLabel(master=top_level, image_path=os.path.join(BASE_DIR, "assets", "images", "rock-paper-scissors-lizard-spock-level-2-v0-2rkr58a1awqb1.png"), text="", compound=tk.TOP, mode="cover")
    label_img.configure(anchor="center")
    label_img.place(x=50, y=50, width=300, height=300)
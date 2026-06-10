import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, simpledialog

# =====================================================================
# MÓDULO 1: CONTROL DIARIO (LOGICA ORIGINAL)
# =====================================================================
def abrir_control_diario():
    ventana_diaria = tk.Toplevel(root)
    ventana_diaria.title("Control Diario de Horas")
    ventana_diaria.geometry("360x400")
    ventana_diaria.resizable(False, False)

    fuente_titulo = ("Segoe UI", 14, "bold")
    fuente = ("Segoe UI", 10)
    fuente_boton = ("Segoe UI", 11, "bold")

    tk.Label(
        ventana_diaria, text="Control Diario de Horas", font=fuente_titulo
    ).pack(pady=10)

    frame_obj = tk.Frame(ventana_diaria)
    frame_obj.pack(pady=5)

    tk.Label(frame_obj, text="Horas objetivo:", font=fuente).grid(
        row=0, column=0, padx=5
    )
    entry_objetivo = tk.Entry(frame_obj, width=6, justify="center", font=fuente)
    entry_objetivo.grid(row=0, column=1)
    entry_objetivo.insert(0, "4")

    frame_tabla = tk.Frame(ventana_diaria)
    frame_tabla.pack(pady=10)

    tk.Label(frame_tabla, text="Entrada", font=fuente).grid(
        row=0, column=0, padx=15
    )
    tk.Label(frame_tabla, text="Salida", font=fuente).grid(
        row=0, column=1, padx=15
    )

    registros = []
    for i in range(3):
        ent = tk.Entry(frame_tabla, width=7, justify="center", font=fuente)
        sal = tk.Entry(frame_tabla, width=7, justify="center", font=fuente)
        ent.grid(row=i + 1, column=0, pady=3)
        sal.grid(row=i + 1, column=1, pady=3)
        registros.append((ent, sal))

    lbl_resultado = tk.Label(
        ventana_diaria, text="", font=("Segoe UI", 12, "bold")
    )

    def calcular_salida():
        try:
            objetivo = float(entry_objetivo.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Ingresá horas objetivo válidas (ej: 4)", parent=ventana_diaria
            )
            return

        objetivo_td = timedelta(hours=objetivo)
        total = timedelta()
        ultima_entrada = None

        for ent, sal in registros:
            e = ent.get().strip()
            s = sal.get().strip()

            if e:
                try:
                    ent_dt = datetime.strptime(e, "%H:%M")
                except ValueError:
                    messagebox.showerror(
                        "Error", f"Hora inválida: {e}", parent=ventana_diaria
                    )
                    return

                if s:
                    try:
                        sal_dt = datetime.strptime(s, "%H:%M")
                    except ValueError:
                        messagebox.showerror(
                            "Error", f"Hora inválida: {s}", parent=ventana_diaria
                        )
                        return
                    total += sal_dt - ent_dt
                else:
                    ultima_entrada = ent_dt

        faltante = objetivo_td - total

        if faltante.total_seconds() <= 0:
            lbl_resultado.config(text="✔ Objetivo cumplido", fg="green")
        elif ultima_entrada:
            salida = ultima_entrada + faltante
            lbl_resultado.config(
                text=f"👉 Podés salir a las {salida.strftime('%H:%M')}",
                fg="#0b5394",
            )
        else:
            lbl_resultado.config(text="⚠ No hay entrada activa", fg="orange")

    btn = tk.Button(
        ventana_diaria,
        text="CALCULAR SALIDA",
        font=fuente_boton,
        bg="#0b5394",
        fg="white",
        activebackground="#073763",
        padx=10,
        pady=5,
        command=calcular_salida,
    )
    btn.pack(pady=15)
    lbl_resultado.pack(pady=10)


# =====================================================================
# MÓDULO 2: DISTRIBUCIÓN MENSUAL CON INTERFAZ DINÁMICA INTEGRADA
# =====================================================================
def abrir_distribucion_mensual():
    ventana_mensual = tk.Toplevel(root)
    ventana_mensual.title("Proyección y Escenarios Personalizados")
    ventana_mensual.geometry("760x520")
    ventana_mensual.resizable(False, False)
    ventana_mensual.configure(bg="#e5eef7")

    fuente_titulo = ("Segoe UI", 13, "bold")
    fuente_sub = ("Segoe UI", 11, "bold")
    fuente = ("Segoe UI", 10)

    # Variables globales de control interno del cálculo temporal
    valores_calculados = {}

    tk.Label(
        ventana_mensual,
        text="Planificación Mensual de Horas",
        font=fuente_titulo,
        fg="#274e13",
        bg="#e5eef7",
    ).pack(pady=12)

    # --- CONTENEDORES PRINCIPALES HORIZONTALES ---
    frame_content = tk.Frame(ventana_mensual, bg="#e5eef7")
    frame_content.pack(fill="both", expand=True, padx=12, pady=8)

    frame_left = tk.Frame(frame_content, bg="#ffffff", bd=1, relief="solid")
    frame_right = tk.Frame(frame_content, bg="#ffffff", bd=1, relief="solid")

    frame_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
    frame_right.grid(row=0, column=1, sticky="nsew", pady=5)

    frame_content.grid_columnconfigure(0, weight=1)
    frame_content.grid_columnconfigure(1, weight=1)
    frame_content.grid_rowconfigure(0, weight=1)

    # --- FORMULARIO PRINCIPAL BASE ---
    frame_form = tk.Frame(frame_left, bg="#ffffff")
    frame_form.pack(fill="x", pady=(10, 8), padx=10)

    campos = [
        ("Cantidad de días trabajados:", "dias_trabajados", "10"),
        ("Horario oficial (HH:MM[:SS]):", "horario_oficial", "08:00"),
        ("Cantidad de días hábiles del mes:", "dias_habiles", "22"),
        ("Promedio de horas trabajadas (HH:MM[:SS]):", "promedio_trabajado", "07:30"),
    ]

    entries = {}
    for idx, (label_text, key, defecto) in enumerate(campos):
        tk.Label(frame_form, text=label_text, font=fuente, anchor="w", bg="#ffffff").grid(
            row=idx, column=0, sticky="w", pady=3, padx=10
        )
        entry = tk.Entry(frame_form, width=11, justify="center", font=fuente)
        entry.grid(row=idx, column=1, pady=3, padx=10)
        entry.insert(0, defecto)
        entries[key] = entry

    # Selector de asistencia total
    frame_check = tk.Frame(frame_left, bg="#ffffff")
    frame_check.pack(fill="x", pady=5, padx=10)

    tk.Label(frame_check, text="¿Vas a cumplir todos los días hábiles?", font=fuente, bg="#ffffff").pack(anchor="w")
    var_cumplir = tk.StringVar(value="SÍ")

    def toggle_dias_restar():
        if var_cumplir.get() == "NO":
            frame_restar.pack(pady=2)
        else:
            frame_restar.pack_forget()
            entry_restar.delete(0, tk.END)
            entry_restar.insert(0, "0")

    rb_si = tk.Radiobutton(frame_check, text="Sí", variable=var_cumplir, value="SÍ", command=toggle_dias_restar, font=fuente)
    rb_no = tk.Radiobutton(frame_check, text="No", variable=var_cumplir, value="NO", command=toggle_dias_restar, font=fuente)
    rb_si.pack(side="left", padx=35)
    rb_no.pack(side="left", padx=35)

    frame_restar = tk.Frame(frame_left, bg="#ffffff")
    tk.Label(frame_restar, text="¿Cuántos días le restamos a los hábiles?:", font=fuente, bg="#ffffff").grid(row=0, column=0, padx=5)
    entry_restar = tk.Entry(frame_restar, width=6, justify="center", font=fuente)
    entry_restar.grid(row=0, column=1)
    entry_restar.insert(0, "0")

    # --- TEXT BOX REUTILIZABLE PARA MOSTRAR LOS RESULTADOS ---
    txt_resultados = tk.Text(
        frame_right, width=40, height=20, font=("Consolas", 10),
        bg="#f9fbf9", bd=0, relief="flat", state="disabled", wrap="word"
    )

    # --- ELEMENTOS DEL SUBMENÚ DE ESCENARIO OPCIONAL (OCULTOS AL INICIO) ---
    frame_opcional = tk.LabelFrame(frame_left, text=" Escenario Personalizado Opcional ", font=fuente_sub, fg="#0b5394", bg="#ffffff", bd=0)
    frame_opcional.pack(fill="x", pady=10, padx=10)
    frame_opcional.configure(labelanchor="nw")

    tk.Label(frame_opcional, text="Horario a cumplir estándar (HH:MM[:SS]):", font=fuente, bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_h_custom = tk.Entry(frame_opcional, width=11, justify="center", font=fuente)
    entry_h_custom.grid(row=0, column=1, padx=10, pady=5)
    
    lbl_dias_ajuste_texto = tk.Label(frame_opcional, text="Cantidad de días de ajuste:", font=fuente, bg="#ffffff")
    lbl_dias_ajuste_texto.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_dias_ajuste = tk.Entry(frame_opcional, width=11, justify="center", font=fuente)
    entry_dias_ajuste.grid(row=1, column=1, padx=10, pady=5)
    entry_dias_ajuste.insert(0, "1")

    def format_tiempo(segundos):
        es_negativo = segundos < 0
        segundos = abs(int(segundos))
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        seg = segundos % 60
        return f"{'-' if es_negativo else ''}{horas:02d}:{minutos:02d}:{seg:02d}"

    def parse_tiempo_input(cadena, nombre, parent):
        cadena = cadena.strip()
        if not cadena:
            raise ValueError(f"{nombre} no puede quedar vacío.")

        if ":" not in cadena:
            try:
                return timedelta(hours=float(cadena))
            except ValueError:
                raise ValueError(f"{nombre} debe ser un número o un tiempo en formato HH:MM[:SS].")

        partes = cadena.count(":")
        if partes == 1:
            formato = "%H:%M"
        elif partes == 2:
            formato = "%H:%M:%S"
        else:
            raise ValueError(f"{nombre} debe usar HH:MM o HH:MM:SS.")

        try:
            partes_hora = datetime.strptime(cadena, formato)
            return timedelta(
                hours=partes_hora.hour,
                minutes=partes_hora.minute,
                seconds=partes_hora.second,
            )
        except ValueError:
            raise ValueError(f"{nombre} debe usar el formato HH:MM o HH:MM:SS.")

    # --- ACCIÓN 1: CALCULA EL ESCENARIO BASE (UNIFORME) ---
    def calcular_escenario_base():
        try:
            d_trabajados = int(entries["dias_trabajados"].get())
            h_oficial_td = parse_tiempo_input(entries["horario_oficial"].get(), "Horario oficial", ventana_mensual)
            d_habiles = int(entries["dias_habiles"].get())
            str_promedio = entries["promedio_trabajado"].get().strip()
            d_restar = int(entry_restar.get()) if var_cumplir.get() == "NO" else 0
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresá valores numéricos válidos o tiempos en formato HH:MM[:SS].", parent=ventana_mensual)
            return

        try:
            promedio_td = parse_tiempo_input(str_promedio, "Promedio de horas trabajadas", ventana_mensual)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=ventana_mensual)
            return

        dias_habiles_reales = d_habiles - d_restar
        dias_restantes = dias_habiles_reales - d_trabajados

        if dias_restantes <= 0:
            messagebox.showerror("Error", "Los días gestionados superan los días hábiles del mes.", parent=ventana_mensual)
            return

        horas_totales_objetivo_td = h_oficial_td * dias_habiles_reales
        horas_ya_hechas_td = promedio_td * d_trabajados
        horas_faltantes_td = horas_totales_objetivo_td - horas_ya_hechas_td

        # Guardar en memoria interna para cruzar los datos con la acción secundaria
        valores_calculados.update({
            "dias_restantes": dias_restantes,
            "h_oficial": h_oficial_td,
            "segundos_faltantes": horas_faltantes_td.total_seconds()
        })

        txt_resultados.config(state="normal")
        txt_resultados.delete("1.0", tk.END)

        if horas_faltantes_td.total_seconds() <= 0:
            txt_resultados.insert(tk.END, "✔ ¡Objetivo mensual cumplido! Tu promedio actual ya cubre el horario oficial.\n")
            txt_resultados.config(state="disabled")
            frame_opcional.pack_forget()
            return

        # Renderizar Escenario 1
        seg_por_dia_e1 = horas_faltantes_td.total_seconds() / dias_restantes
        res_general = (
            f" RESUMEN GENERAL Y ESCENARIO BASE\n"
            f" --------------------------------------------------\n"
            f" Días restantes a trabajar: {dias_restantes} días\n"
            f" Tiempo total a cumplir:    {format_tiempo(horas_faltantes_td.total_seconds())}\n"
            f" ==================================================\n\n"
            f" 💡 ESCENARIO 1: Distribución Uniforme\n"
            f" -> Hacer exactamente {format_tiempo(seg_por_dia_e1)} todos los días restantes.\n"
        )
        txt_resultados.insert(tk.END, res_general)
        txt_resultados.config(state="disabled")

        # --- VALIDACIÓN LOGICA DE DÍAS DE AJUSTE ---
        # Si quedan 3 días o menos, se deshabilita/fija el campo para forzar la regla de 1 solo día
        if dias_restantes <= 3:
            entry_dias_ajuste.delete(0, tk.END)
            entry_dias_ajuste.insert(0, "1")
            entry_dias_ajuste.config(state="disabled")
            lbl_dias_ajuste_texto.config(text="Cantidad de días de ajuste (Fijo <=3 días):")
        else:
            entry_dias_ajuste.config(state="normal")
            lbl_dias_ajuste_texto.config(text="Cantidad de días de ajuste:")

        # Desplegar el menú inferior de opciones avanzadas
        frame_opcional.pack(pady=10, fill="x", padx=15)

    # --- ACCIÓN 2: CALCULA EL ESCENARIO COMBINADO (PERSONALIZADO) ---
    def calcular_escenario_personalizado():
        if not valores_calculados:
            return

        dias_restantes = valores_calculados["dias_restantes"]
        h_oficial = valores_calculados["h_oficial"]
        segundos_faltantes = valores_calculados["segundos_faltantes"]

        try:
            dias_ajuste = int(entry_dias_ajuste.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresá una cantidad de días de ajuste válida.", parent=ventana_mensual)
            return

        # Forzar validación estricta de días si quedan <= 3
        if dias_restantes <= 3:
            dias_ajuste = 1

        if dias_ajuste < 1 or dias_ajuste >= dias_restantes:
            messagebox.showerror("Error", f"Los días de ajuste deben estar entre 1 y {dias_restantes - 1}.", parent=ventana_mensual)
            return

        # Determinar horario base estándar elegido
        str_h_custom = entry_h_custom.get().strip()
        if str_h_custom == "":
            # Si se deja vacío, toma el Horario Oficial de forma predeterminada
            seg_dia_estandar = h_oficial.total_seconds()
            texto_regimen = "Horario Oficial"
        else:
            try:
                horario_custom_td = parse_tiempo_input(str_h_custom, "Horario personalizado", ventana_mensual)
                seg_dia_estandar = horario_custom_td.total_seconds()
                texto_regimen = f"Fijo personalizado ({str_h_custom})"
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=ventana_mensual)
                return

        # Cálculo matemático del reparto
        dias_estandar = dias_restantes - dias_ajuste
        seg_acumulados_estandar = seg_dia_estandar * dias_estandar
        seg_totales_ajuste = segundos_faltantes - seg_acumulados_estandar
        seg_por_dia_ajuste = seg_totales_ajuste / dias_ajuste

        # Imprimir la actualización en el mismo Text Box sin borrar el Escenario 1
        txt_resultados.config(state="normal")
        
        # Si ya existía un cálculo previo impreso de un escenario 2/3, lo limpiamos manteniendo la cabecera
        contenido_actual = txt_resultados.get("1.0", tk.END)
        if "💡 ESCENARIO COMBINADO" in contenido_actual:
            # Cortamos el texto justo donde termina el Escenario 1
            indice_corte = contenido_actual.find("💡 ESCENARIO COMBINADO")
            txt_resultados.delete(f"1.0 + {indice_corte} chars", tk.END)

        res_personalizado = (
            f"\n 💡 ESCENARIO COMBINADO: Personalizado\n"
            f" -> {dias_estandar} día(s) en régimen {texto_regimen}: {format_tiempo(seg_dia_estandar)}\n"
            f" -> {dias_ajuste} día(s) restante(s) de AJUSTE haciendo: {format_tiempo(seg_por_dia_ajuste)} c/u\n"
        )
        txt_resultados.insert(tk.END, res_personalizado)
        txt_resultados.config(state="disabled")

    # Botón de Procesamiento Inicial
    btn_calc_base = tk.Button(
        frame_right, text="CALCULAR DISTRIBUCIÓN BASE", font=("Segoe UI", 11, "bold"),
        bg="#274e13", fg="white", activebackground="#1e3b0f", padx=12, pady=8,
        command=calcular_escenario_base,
        relief="flat"
    )
    btn_calc_base.pack(fill="x", pady=(10, 0), padx=10)

    tk.Label(frame_right, text="Resultados", font=fuente_sub, bg="#ffffff", fg="#274e13").pack(anchor="w", padx=10, pady=(12, 0))
    txt_resultados.pack(fill="both", expand=True, pady=10, padx=10)

    # Botón secundario ubicado adentro del panel dinámico desplegable
    btn_calc_custom = tk.Button(
        frame_opcional, text="Aplicar Escenario Combinado", font=("Segoe UI", 10, "bold"),
        bg="#0b5394", fg="white", activebackground="#073763", padx=8, pady=6,
        command=calcular_escenario_personalizado,
        relief="flat"
    )
    btn_calc_custom.grid(row=2, column=0, columnspan=2, pady=8)


    
# =====================================================================
# VENTANA PRINCIPAL (MENÚ)
# =====================================================================
root = tk.Tk()
root.title("Gestor de Asistencia y Tiempos")
root.geometry("400x250")
root.resizable(False, False)

fuente_menu_titulo = ("Segoe UI", 14, "bold")
fuente_botones_menu = ("Segoe UI", 11, "bold")

tk.Label(
    root, text="Seleccione el Módulo de Control", font=fuente_menu_titulo
).pack(pady=20)

# Botón Módulo Horas Diario
btn_diario = tk.Button(
    root,
    text="⏱ CONTROL DIARIO (HORA)",
    font=fuente_botones_menu,
    bg="#0b5394",
    fg="white",
    activebackground="#073763",
    width=25,
    pady=8,
    command=abrir_control_diario,
)
btn_diario.pack(pady=10)

# Botón Módulo Planificación Mensual
btn_mensual = tk.Button(
    root,
    text="📅 PROYECCIÓN MENSUAL",
    font=fuente_botones_menu,
    bg="#274e13",
    fg="white",
    activebackground="#1e3b0f",
    width=25,
    pady=8,
    command=abrir_distribucion_mensual,
)
btn_mensual.pack(pady=10)

root.mainloop()
import os
import sys
import subprocess
import tempfile
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

try:
    import edge_tts
    import pygame
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Faltan dependencias.\nInstálalas en tu terminal con:\npip install edge-tts pygame")
    sys.exit(1)

class GeneradorVozIA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estudio de Locución IA - Nación Cristiana")
        self.geometry("750x650")
        self.minsize(700, 550)

        # Inicializar el motor de audio para el preview
        pygame.mixer.init()

        # Catálogo de las mejores voces masculinas/serias en español
        self.voces = {
            "🇲🇽 Jorge (México - Masculino, Serio y Profundo)": "es-MX-JorgeNeural",
            "🇪🇸 Álvaro (España - Masculino, Documental)": "es-ES-AlvaroNeural",
            "🇨🇴 Gonzalo (Colombia - Masculino)": "es-CO-GonzaloNeural",
            "🇺🇸 Alonso (EEUU - Masculino, Neutro)": "es-US-AlonsoNeural",
            "🇪🇸 Elvira (España - Femenino, Cálida)": "es-ES-ElviraNeural"
        }

        self.preview_path = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Área de texto
        ttk.Label(self, text="✍️ Pega aquí tu guion final para narrar:", font=("Arial", 10, "bold")).pack(pady=(15, 5), padx=15, anchor=tk.W)
        self.txt_guion = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=12, font=("Arial", 12))
        self.txt_guion.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Marco de Configuración
        frame_config = ttk.LabelFrame(self, text="🎛️ Consola de Audio")
        frame_config.pack(fill=tk.X, padx=15, pady=15)

        # Selección de Voz
        ttk.Label(frame_config, text="Locutor:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.var_voz = tk.StringVar(value=list(self.voces.keys())[0])
        cb_voces = ttk.Combobox(frame_config, textvariable=self.var_voz, values=list(self.voces.keys()), state="readonly", width=45)
        cb_voces.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Velocidad
        ttk.Label(frame_config, text="Velocidad (%):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.var_velocidad = tk.IntVar(value=-10)
        ttk.Spinbox(frame_config, from_=-50, to=50, textvariable=self.var_velocidad, width=10).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(frame_config, text="<- Valores negativos (-10, -15) dan un tono reflexivo", font=("Arial", 8, "italic"), foreground="gray").grid(row=1, column=2, sticky=tk.W)

        # Tono (Pitch)
        ttk.Label(frame_config, text="Tono (Hz):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.var_tono = tk.IntVar(value=-5)
        ttk.Spinbox(frame_config, from_=-50, to=50, textvariable=self.var_tono, width=10).grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(frame_config, text="<- Valores negativos hacen la voz más grave", font=("Arial", 8, "italic"), foreground="gray").grid(row=2, column=2, sticky=tk.W)

        # Controles y Descarga
        frame_controles = ttk.Frame(self)
        frame_controles.pack(fill=tk.X, padx=15, pady=5)
        
        # Botones de Preview (Izquierda)
        self.btn_preview = ttk.Button(frame_controles, text="▶️ Escuchar Preview", command=self.iniciar_preview)
        self.btn_preview.pack(side=tk.LEFT, padx=5)

        self.btn_detener = ttk.Button(frame_controles, text="⏹ Detener", command=self.detener_preview, state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=5)

        # Botón de Descarga (Derecha)
        btn_generar = ttk.Button(frame_controles, text="💾 Descargar MP3 Final", command=self.generar_audio)
        btn_generar.pack(side=tk.RIGHT, padx=5)

        self.status_var = tk.StringVar(value="Listo para grabar.")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def _obtener_parametros(self):
        texto = self.txt_guion.get("1.0", tk.END).strip()
        nombre_voz_seleccionada = self.var_voz.get()
        id_voz = self.voces[nombre_voz_seleccionada]
        
        vel = self.var_velocidad.get()
        str_vel = f"+{vel}%" if vel >= 0 else f"{vel}%"
        
        tono = self.var_tono.get()
        str_tono = f"+{tono}Hz" if tono >= 0 else f"{tono}Hz"
        
        return texto, id_voz, str_vel, str_tono

    def iniciar_preview(self):
        texto, id_voz, str_vel, str_tono = self._obtener_parametros()
        if not texto:
            messagebox.showwarning("Texto vacío", "Por favor pega el guion antes de escuchar.")
            return

        self.btn_preview.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.status_var.set("Cargando preview...")
        
        threading.Thread(target=self._hilo_preview, args=(texto, id_voz, str_vel, str_tono), daemon=True).start()

    def _hilo_preview(self, texto, id_voz, str_vel, str_tono):
        try:
            pygame.mixer.music.unload()
            
            fd, temp_audio = tempfile.mkstemp(suffix=".mp3", prefix="preview_")
            os.close(fd)
            self.preview_path = temp_audio

            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
                f.write(texto)
                temp_txt_path = f.name

            # Aquí está el comando corregido con el "="
            comando = [
                sys.executable, "-m", "edge_tts",
                "--voice", id_voz, 
                f"--rate={str_vel}", 
                f"--pitch={str_tono}",
                "-f", temp_txt_path, 
                "--write-media", temp_audio
            ]

            subprocess.run(comando, check=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            os.remove(temp_txt_path)

            self.status_var.set("▶️ Reproduciendo...")
            
            pygame.mixer.music.load(temp_audio)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            self.status_var.set("Preview finalizado.")

        except Exception as e:
            self.status_var.set("Error en el preview.")
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
        finally:
            self.btn_preview.after(0, lambda: self.btn_preview.config(state=tk.NORMAL))
            self.btn_detener.after(0, lambda: self.btn_detener.config(state=tk.DISABLED))

    def detener_preview(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.status_var.set("Preview detenido.")
        self.btn_preview.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)

    def generar_audio(self):
        texto, id_voz, str_vel, str_tono = self._obtener_parametros()
        if not texto:
            messagebox.showwarning("Texto vacío", "Por favor pega el guion antes de generar el audio.")
            return

        ruta_salida = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            initialfile="voz_reflexion.mp3",
            title="Guardar Narración Como",
            filetypes=[("Archivos MP3", "*.mp3")]
        )

        if not ruta_salida:
            return

        self.status_var.set("Generando MP3 de alta calidad...")
        self.update()

        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
                f.write(texto)
                temp_txt_path = f.name

            # Aquí también está el comando corregido con el "="
            comando = [
                sys.executable, "-m", "edge_tts",
                "--voice", id_voz, 
                f"--rate={str_vel}", 
                f"--pitch={str_tono}",
                "-f", temp_txt_path, 
                "--write-media", ruta_salida
            ]

            subprocess.run(comando, check=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            os.remove(temp_txt_path)

            self.status_var.set("¡Audio descargado con éxito!")
            messagebox.showinfo("¡Listo!", f"Tu narración se guardó correctamente en:\n{ruta_salida}\n\n¡Lista para usar en tu editor!")
            
        except Exception as e:
            self.status_var.set("Error al generar el audio.")
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")

if __name__ == "__main__":
    app = GeneradorVozIA()
    app.mainloop()
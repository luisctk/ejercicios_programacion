#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación para crear videos de frases cristianas automáticamente.
Incluye interfaz gráfica (Tkinter), búsqueda de videos en Pexels,
generación de frases con OpenAI y renderizado con MoviePy.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import requests
from PIL import Image, ImageTk
import io
from moviepy import *

# Dependencias que deben estar instaladas:
# pip install openai pexels-api-py moviepy requests pillow

# Intentar importar las librerías (con manejo de error amigable)
try:
    from pexels_api import API
except ImportError:
    API = None
try:
    import openai
except ImportError:
    openai = None
try:
    from moviepy import *
except ImportError:
    from moviepy import *  # Si falla, mostrará error después
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

# ----------------------------------------------------------------------
# CONFIGURACIÓN (completa con tus API keys)
# ----------------------------------------------------------------------
PEXELS_API_KEY = "TU_API_KEY_DE_PEXELS"          # Obligatoria
OPENAI_API_KEY = "TU_API_KEY_DE_OPENAI"          # Opcional (para generar frases)
OPENAI_MODEL = "gpt-4"                           # o "gpt-3.5-turbo"
# ----------------------------------------------------------------------

class VideoCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador Automático de Videos Cristianos")
        self.root.geometry("950x700")
        self.root.resizable(True, True)
        
        # Variables de control
        self.frases = []                      # Lista de frases a procesar
        self.videos_pexels_cache = {}         # Caché de resultados de búsqueda
        self.output_dir = os.getcwd()
        
        self._init_apis()
        self._create_widgets()
        self._load_icon()
    
    def _init_apis(self):
        """Inicializa las APIs si las llaves están disponibles."""
        if PEXELS_API_KEY != "TU_API_KEY_DE_PEXELS" and API is not None:
            self.pexels = API(PEXELS_API_KEY)
            self.pexels_ok = True
        else:
            self.pexels_ok = False
            print("Advertencia: Pexels API no configurada.")
        
        if OPENAI_API_KEY != "TU_API_KEY_DE_OPENAI" and openai is not None:
            openai.api_key = OPENAI_API_KEY
            self.openai_ok = True
        else:
            self.openai_ok = False
            print("Advertencia: OpenAI API no configurada.")
    
    def _load_icon(self):
        """Carga un ícono para la ventana (opcional)."""
        try:
            self.root.iconbitmap(default="icon.ico")  # Si tienes un icono
        except:
            pass
    
    def _create_widgets(self):
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Entrada de frases
        self.tab_input = ttk.Frame(notebook)
        notebook.add(self.tab_input, text="1. Frases")
        self._build_tab_input()
        
        # Pestaña 2: Configuración de video
        self.tab_config = ttk.Frame(notebook)
        notebook.add(self.tab_config, text="2. Estilo")
        self._build_tab_config()
        
        # Pestaña 3: Procesamiento
        self.tab_process = ttk.Frame(notebook)
        notebook.add(self.tab_process, text="3. Procesar")
        self._build_tab_process()
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _build_tab_input(self):
        frame = self.tab_input
        
        # Área de texto para frases
        lbl = ttk.Label(frame, text="Ingresa las frases (una por línea). Formato sugerido:")
        lbl.pack(anchor=tk.W, padx=5, pady=2)
        lbl2 = ttk.Label(frame, text="Frase principal | Versículo (opcional) | Palabras clave (opcional, separadas por comas)")
        lbl2.pack(anchor=tk.W, padx=5, pady=2)
        
        self.text_frases = scrolledtext.ScrolledText(frame, height=12, width=80, font=("Arial", 10))
        self.text_frases.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de acciones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Cargar desde archivo", command=self.cargar_archivo).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Guardar frases", command=self.guardar_frases).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Generar frases con IA", command=self.generar_frases_ia_thread).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.text_frases.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=2)
    
    def _build_tab_config(self):
        frame = self.tab_config
        
        # Carpeta de salida
        ttk.Label(frame, text="Carpeta de salida:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_var = tk.StringVar(value=os.getcwd())
        ttk.Entry(frame, textvariable=self.output_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Examinar", command=self.seleccionar_carpeta).grid(row=0, column=2, padx=5, pady=5)
        
        # Estilo de texto
        ttk.Label(frame, text="Fuente:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.font_family = tk.StringVar(value="Arial")
        fuentes = ["Arial", "Times New Roman", "Verdana", "Courier New", "Comic Sans MS", "Georgia"]
        ttk.Combobox(frame, textvariable=self.font_family, values=fuentes, state="readonly").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Tamaño de fuente:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.font_size = tk.IntVar(value=60)
        ttk.Spinbox(frame, from_=20, to=200, textvariable=self.font_size, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Color del texto:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_color = tk.StringVar(value="white")
        colores = ["white", "yellow", "black", "red", "blue", "gold"]
        ttk.Combobox(frame, textvariable=self.text_color, values=colores, state="readonly").grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Color del borde:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.stroke_color = tk.StringVar(value="black")
        ttk.Combobox(frame, textvariable=self.stroke_color, values=["black", "white", "red", "blue", "none"], state="readonly").grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Grosor del borde:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.stroke_width = tk.IntVar(value=2)
        ttk.Spinbox(frame, from_=0, to=10, textvariable=self.stroke_width, width=10).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Posición del texto
        ttk.Label(frame, text="Posición del texto:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_pos = tk.StringVar(value="center")
        posiciones = ["center", "top", "bottom", "left", "right"]
        ttk.Combobox(frame, textvariable=self.text_pos, values=posiciones, state="readonly").grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Duración del video
        ttk.Label(frame, text="Duración del video (segundos):").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.video_duration = tk.IntVar(value=10)
        ttk.Spinbox(frame, from_=3, to=60, textvariable=self.video_duration, width=10).grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Música de fondo (opcional)
        ttk.Label(frame, text="Archivo de música (opcional):").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.music_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.music_path, width=50).grid(row=8, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Seleccionar", command=self.seleccionar_musica).grid(row=8, column=2, padx=5, pady=5)
        
        # Checkbox para usar palabras clave en la búsqueda de videos
        self.use_keywords = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Usar palabras clave de la frase (si se proporcionan) para buscar videos", variable=self.use_keywords).grid(row=9, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
    
    def _build_tab_process(self):
        frame = self.tab_process
        
        # Área de log
        ttk.Label(frame, text="Registro de procesos:").pack(anchor=tk.W, padx=5, pady=2)
        self.log_text = scrolledtext.ScrolledText(frame, height=15, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.process_btn = ttk.Button(btn_frame, text="Procesar todas las frases", command=self.procesar_lote_thread)
        self.process_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = ttk.Button(btn_frame, text="Detener", command=self.detener_proceso, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(btn_frame, text="Abrir carpeta de salida", command=self.abrir_carpeta).pack(side=tk.LEFT, padx=2)
    
    # ------------------------------------------------------------------
    # Funciones de la interfaz
    # ------------------------------------------------------------------
    def log(self, mensaje, nivel="info"):
        """Añade un mensaje al área de log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, mensaje + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Archivos CSV", "*.csv"), ("Todos", "*.*")])
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.text_frases.delete(1.0, tk.END)
                self.text_frases.insert(1.0, contenido)
                self.log(f"Archivo cargado: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
    
    def guardar_frases(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(self.text_frases.get(1.0, tk.END))
                self.log(f"Frases guardadas en: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")
    
    def generar_frases_ia_thread(self):
        if not self.openai_ok:
            messagebox.showerror("Error", "OpenAI no está configurado correctamente.\nRevisa tu API key en el código.")
            return
        threading.Thread(target=self.generar_frases_ia, daemon=True).start()
    
    def generar_frases_ia(self):
        """Genera frases usando OpenAI y las inserta en el área de texto."""
        try:
            self.status_var.set("Generando frases con IA...")
            prompt = "Genera 10 frases cristianas cortas para TikTok. Para cada frase, incluye el texto principal, el versículo bíblico correspondiente y tres palabras clave en inglés separadas por comas. Formato: Frase principal | Versículo | palabra1, palabra2, palabra3"
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            contenido = response.choices[0].message.content
            # Insertar al final del texto actual
            self.text_frases.insert(tk.END, "\n" + contenido + "\n")
            self.log("Frases generadas por IA añadidas.")
        except Exception as e:
            self.log(f"Error generando frases: {e}")
            messagebox.showerror("Error", f"No se pudieron generar frases: {e}")
        finally:
            self.status_var.set("Listo")
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.output_var.set(carpeta)
    
    def seleccionar_musica(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3 *.wav *.m4a")])
        if archivo:
            self.music_path.set(archivo)
    
    def abrir_carpeta(self):
        import subprocess
        import platform
        carpeta = self.output_var.get()
        if os.path.exists(carpeta):
            if platform.system() == "Windows":
                os.startfile(carpeta)
            elif platform.system() == "Darwin":
                subprocess.run(["open", carpeta])
            else:
                subprocess.run(["xdg-open", carpeta])
        else:
            messagebox.showerror("Error", "La carpeta no existe.")
    
    def detener_proceso(self):
        self.stop_requested = True
        self.log("Deteniendo proceso... (puede tardar unos segundos)")
    
    def procesar_lote_thread(self):
        self.stop_requested = False
        self.process_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        threading.Thread(target=self.procesar_lote, daemon=True).start()
    
    def procesar_lote(self):
        # Leer frases del área de texto
        texto = self.text_frases.get(1.0, tk.END).strip()
        if not texto:
            self.log("No hay frases para procesar.")
            self._finalizar_proceso()
            return
        
        lineas = texto.splitlines()
        frases_procesadas = []
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            # Formato esperado: "Texto | Versículo | palabras clave"
            partes = [p.strip() for p in linea.split('|')]
            frase = {
                'texto': partes[0],
                'versiculo': partes[1] if len(partes) > 1 else '',
                'keywords': partes[2] if len(partes) > 2 else ''
            }
            frases_procesadas.append(frase)
        
        self.log(f"Se procesarán {len(frases_procesadas)} frases.")
        
        # Configuración de estilo
        font = self.font_family.get()
        fontsize = self.font_size.get()
        color = self.text_color.get()
        stroke_color = self.stroke_color.get()
        stroke_width = self.stroke_width.get()
        pos = self.text_pos.get()
        duracion = self.video_duration.get()
        musica = self.music_path.get() if self.music_path.get() else None
        usar_keywords = self.use_keywords.get()
        
        output_dir = self.output_var.get()
        os.makedirs(output_dir, exist_ok=True)
        
        self.progress['maximum'] = len(frases_procesadas)
        self.progress['value'] = 0
        
        for idx, frase in enumerate(frases_procesadas):
            if self.stop_requested:
                self.log("Proceso detenido por el usuario.")
                break
            
            self.status_var.set(f"Procesando frase {idx+1}/{len(frases_procesadas)}: {frase['texto'][:30]}...")
            self.log(f"Frase {idx+1}: {frase['texto']}")
            
            # Buscar video
            video_url = None
            if usar_keywords and frase['keywords']:
                keywords = [k.strip() for k in frase['keywords'].split(',')]
                for kw in keywords:
                    self.log(f"  Buscando video con palabra clave: {kw}")
                    video_url = self.buscar_video_pexels(kw)
                    if video_url:
                        break
            
            if not video_url:
                # Palabra clave por defecto: "christian nature"
                self.log("  Usando palabra clave por defecto: christian nature")
                video_url = self.buscar_video_pexels("christian nature")
            
            if not video_url:
                self.log("  No se encontró ningún video, se omitirá esta frase.")
                continue
            
            # Crear video
            try:
                output_path = os.path.join(output_dir, f"video_{idx+1}.mp4")
                self.crear_video(frase, video_url, output_path, font, fontsize, color,
                                 stroke_color, stroke_width, pos, duracion, musica)
                self.log(f"  Video guardado: {output_path}")
            except Exception as e:
                self.log(f"  Error al crear video: {e}")
            
            self.progress['value'] = idx + 1
            self.root.update_idletasks()
        
        self._finalizar_proceso()
    
    def _finalizar_proceso(self):
        self.progress['value'] = 0
        self.status_var.set("Proceso finalizado")
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("--- Proceso completado ---")
    
    def buscar_video_pexels(self, keyword):
        """Busca un video en Pexels y retorna la URL del primer resultado en vertical."""
        if not self.pexels_ok:
            self.log("  Pexels no configurado. No se puede buscar video.")
            return None
        
        try:
            # Usar caché para no repetir búsquedas
            if keyword in self.videos_pexels_cache:
                return self.videos_pexels_cache[keyword]
            
            self.pexels.search(keyword, page=1, results_per_page=5)
            videos = self.pexels.get_videos()
            if videos:
                for video in videos:
                    # Buscar un archivo con orientación vertical (1080x1920)
                    for file in video.video_files:
                        if file.width == 1080 and file.height == 1920:
                            self.videos_pexels_cache[keyword] = file.link
                            return file.link
                    # Si no hay vertical, tomar el primero
                    if video.video_files:
                        self.videos_pexels_cache[keyword] = video.video_files[0].link
                        return video.video_files[0].link
            self.videos_pexels_cache[keyword] = None
            return None
        except Exception as e:
            self.log(f"  Error en búsqueda Pexels: {e}")
            return None
    
    def crear_video(self, frase, video_url, output_path, font, fontsize, color,
                    stroke_color, stroke_width, pos, duracion, musica):
        """Crea el video con MoviePy."""
        # Descargar video temporal
        r = requests.get(video_url, stream=True)
        temp_video = "temp_video.mp4"
        with open(temp_video, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Cargar clip
        clip = VideoFileClip(temp_video)
        
        # Recortar o redimensionar para que sea 9:16 (1080x1920)
        clip = self.ajustar_ratio(clip, 9/16)
        clip = clip.resize((1080, 1920))
        
        # Ajustar duración
        if clip.duration > duracion:
            clip = clip.subclip(0, duracion)
        else:
            # Si es más corto, lo repetimos? Por simplicidad, lo dejamos tal cual
            pass
        
        # Preparar texto
        texto_completo = frase['texto']
        if frase['versiculo']:
            texto_completo += f"\n\n{frase['versiculo']}"
        
        txt_clip = TextClip(
            texto_completo,
            fontsize=fontsize,
            color=color,
            font=font,
            stroke_color=stroke_color if stroke_color != 'none' else None,
            stroke_width=stroke_width,
            method='caption',
            size=(900, 0)  # Ancho máximo
        ).set_duration(clip.duration)
        
        # Posición
        if pos == 'center':
            txt_clip = txt_clip.set_position(('center', 'center'))
        elif pos == 'top':
            txt_clip = txt_clip.set_position(('center', 100))
        elif pos == 'bottom':
            txt_clip = txt_clip.set_position(('center', clip.h - txt_clip.h - 100))
        elif pos == 'left':
            txt_clip = txt_clip.set_position((100, 'center'))
        elif pos == 'right':
            txt_clip = txt_clip.set_position((clip.w - txt_clip.w - 100, 'center'))
        
        # Componer video
        final = CompositeVideoClip([clip, txt_clip])
        
        # Añadir música si se especificó
        if musica and os.path.exists(musica):
            audio_fondo = AudioFileClip(musica).subclip(0, final.duration)
            audio_fondo = audio_fondo.volumex(0.3)  # Volumen bajo
            if final.audio:
                audio_final = CompositeAudioClip([final.audio, audio_fondo])
            else:
                audio_final = audio_fondo
            final = final.set_audio(audio_final)
        
        # Guardar
        final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, verbose=False, logger=None)
        
        # Limpiar
        clip.close()
        txt_clip.close()
        final.close()
        os.remove(temp_video)
    
    def ajustar_ratio(self, clip, target_ratio):
        """Ajusta el clip al ratio objetivo (ancho/alto) recortando el centro."""
        w, h = clip.w, clip.h
        current_ratio = w / h
        if current_ratio > target_ratio:
            # Es más ancho, recortar los lados
            new_w = int(h * target_ratio)
            x_center = w // 2
            clip = clip.crop(x_center=x_center, width=new_w)
        else:
            # Es más alto, recortar arriba/abajo
            new_h = int(w / target_ratio)
            y_center = h // 2
            clip = clip.crop(y_center=y_center, height=new_h)
        return clip

def main():
    # Verificar dependencias
    missing = []
    if not API:
        missing.append("pexels-api-py")
    if not openai:
        missing.append("openai")
    try:
        from moviepy.editor import VideoFileClip
    except:
        missing.append("moviepy")
    if not Image:
        missing.append("pillow")
    
    if missing:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Faltan dependencias",
                               f"Las siguientes librerías no están instaladas:\n{', '.join(missing)}\n\n"
                               "Ejecuta en tu terminal:\n"
                               f"pip install {' '.join(missing)}")
        root.destroy()
        return
    
    root = tk.Tk()
    app = VideoCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
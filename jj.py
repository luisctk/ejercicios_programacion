import os
import sys
import threading
import time
import random
import tempfile
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

# ==============================================================================
# CONFIGURACIÓN DE API KEYS (Pon tus llaves aquí)
# ==============================================================================
PEXELS_API_KEY = "SAGEwAzhwp6zaMJavXYgCrk5bVeHut8oyDoqPAPMHgPds8aPLF50F2BN"
GEMINI_API_KEY = "AIzaSyAjtE9bcFCwful7nSE896iP0YgfeuQpRos"

# ==============================================================================
# VERIFICACIÓN DE DEPENDENCIAS
# ==============================================================================
try:
    import requests
    from google import genai
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    from moviepy.video.fx.all import crop, resize
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Faltan dependencias",
        f"Falta una librería requerida.\nError: {e}\n\nInstala con:\npip install google-genai moviepy==1.0.3 requests"
    )
    sys.exit(1)

try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    pass

class GeneradorFondosTikTok(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Producción Nación Cristiana - Fondos Dinámicos")
        self.geometry("900x780")
        self.minsize(800, 680)
        
        self.stop_flag = False
        self.videos_usados_pexels = set()
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Pestaña 1: Guiones
        self.tab_frases = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_frases, text="1. Guiones e IA")
        self._setup_tab_frases()
        
        # Pestaña 2: Video
        self.tab_estilo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estilo, text="2. Configuración Video")
        self._setup_tab_estilo()
        
        # Pestaña 3: Log
        self.tab_procesar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_procesar, text="3. Consola de Producción")
        self._setup_tab_procesar()
        
        self.status_var = tk.StringVar(value="Listo")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_tab_frases(self):
        # --- Selector de Modo ---
        frame_modo = ttk.Frame(self.tab_frases)
        frame_modo.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame_modo, text="Modo de trabajo:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.var_modo = tk.StringVar(value="ia")
        ttk.Radiobutton(frame_modo, text="🤖 IA Automática (Gemini)", variable=self.var_modo, value="ia", command=self._toggle_modo).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_modo, text="✍️ Ingreso Manual", variable=self.var_modo, value="manual", command=self._toggle_modo).pack(side=tk.LEFT, padx=10)

        # --- Panel IA (Modo Automático) ---
        self.frame_ia = ttk.LabelFrame(self.tab_frases, text="Configuración de Producción (Gemini)")
        self.frame_ia.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.frame_ia, text="Videos a crear:").grid(row=0, column=0, padx=10, pady=10)
        self.var_cantidad_videos = tk.IntVar(value=5)
        self.spin_cant = ttk.Spinbox(self.frame_ia, from_=1, to=50, textvariable=self.var_cantidad_videos, width=5)
        self.spin_cant.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(self.frame_ia, text="Mín. palabras:").grid(row=0, column=2, padx=10, pady=10)
        self.var_min_palabras = tk.IntVar(value=60)
        self.spin_palabras = ttk.Spinbox(self.frame_ia, from_=10, to=500, textvariable=self.var_min_palabras, width=5)
        self.spin_palabras.grid(row=0, column=3, padx=5, pady=10)
        
        self.btn_gemini = ttk.Button(self.frame_ia, text="💡 Generar Guiones", command=self.generar_con_ia)
        self.btn_gemini.grid(row=0, column=4, padx=20, pady=10)

        # --- NUEVO: Panel Manual (Oculto al inicio) ---
        self.frame_manual = ttk.LabelFrame(self.tab_frases, text="Inyector de Fondos Pexels")
        
        ttk.Label(self.frame_manual, text="Elige la vibra visual:").pack(side=tk.LEFT, padx=5, pady=5)
        
        self.opciones_fondos = {
            "🌊 Mar y Olas relajantes": "ocean waves, peaceful beach",
            "⛰️ Montañas y Niebla": "mountains, epic landscape, fog",
            "🌅 Atardecer y Cielo": "sunset, sky, clouds",
            "💧 Cascadas y Ríos": "waterfall, flowing river, nature",
            "🌲 Bosque Misterioso": "peaceful forest, trees, sunlight",
            "🌌 Espacio y Estrellas": "night sky, stars, galaxy",
            "🦅 Animales / Aves": "birds flying, majestic eagle"
        }
        
        self.var_fondo_manual = tk.StringVar(value=list(self.opciones_fondos.keys())[0])
        ttk.Combobox(self.frame_manual, textvariable=self.var_fondo_manual, values=list(self.opciones_fondos.keys()), state="readonly", width=25).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(self.frame_manual, text="➕ Insertar Código de Fondo", command=self._insertar_fondo_manual).pack(side=tk.LEFT, padx=10, pady=5)
        
        # --- Caja de Texto y Botones Inferiores ---
        self.txt_frases = scrolledtext.ScrolledText(self.tab_frases, wrap=tk.WORD, font=("Consolas", 10))
        self.txt_frases.pack(expand=True, fill='both', padx=10, pady=5)
        
        f_bot = ttk.Frame(self.tab_frases)
        f_bot.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(f_bot, text="Cargar archivo .txt", command=self.cargar_frases).pack(side=tk.LEFT, padx=5)
        ttk.Button(f_bot, text="Guardar lista", command=self.guardar_frases).pack(side=tk.LEFT, padx=5)
        ttk.Button(f_bot, text="Limpiar Todo", command=lambda: self.txt_frases.delete("1.0", tk.END)).pack(side=tk.RIGHT, padx=5)

    def _toggle_modo(self):
        modo = self.var_modo.get()
        if modo == "manual":
            self.spin_cant.config(state=tk.DISABLED)
            self.spin_palabras.config(state=tk.DISABLED)
            self.btn_gemini.config(state=tk.DISABLED)
            self.frame_manual.pack(fill=tk.X, padx=10, pady=5, before=self.txt_frases)
            
            self.txt_frases.delete("1.0", tk.END)
            self.txt_frases.insert(tk.END, "Escribe tu reflexión completa aquí | Escribe tu Llamado a la acción")
        else:
            self.spin_cant.config(state=tk.NORMAL)
            self.spin_palabras.config(state=tk.NORMAL)
            self.btn_gemini.config(state=tk.NORMAL)
            self.frame_manual.pack_forget()
            self.txt_frases.delete("1.0", tk.END)

    def _insertar_fondo_manual(self):
        seleccion = self.var_fondo_manual.get()
        keywords = self.opciones_fondos[seleccion]
        self.txt_frases.insert(tk.END, f" | {keywords}\n")

    def _setup_tab_estilo(self):
        f = ttk.Frame(self.tab_estilo)
        f.pack(fill='both', expand=True, padx=20, pady=20)
        
        lf_dir = ttk.LabelFrame(f, text="Carpeta de Destino")
        lf_dir.pack(fill=tk.X, pady=10)
        self.var_carpeta_salida = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Videos_Nacion_Cristiana"))
        ttk.Entry(lf_dir, textvariable=self.var_carpeta_salida, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        ttk.Button(lf_dir, text="Cambiar", command=self.seleccionar_carpeta).pack(side=tk.LEFT, padx=5)

        lf_vid = ttk.LabelFrame(f, text="Ajustes de Edición")
        lf_vid.pack(fill=tk.X, pady=10)
        
        ttk.Label(lf_vid, text="Segundos por video:").grid(row=0, column=0, padx=10, pady=10)
        self.var_duracion = tk.IntVar(value=30)
        ttk.Spinbox(lf_vid, from_=5, to=120, textvariable=self.var_duracion, width=10).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(lf_vid, text="Ritmo de cortes:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Label(lf_vid, text="Fijo cada 2.5 segundos (Estilo Viral)", foreground="blue").grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    def _setup_tab_procesar(self):
        self.log_area = scrolledtext.ScrolledText(self.tab_procesar, wrap=tk.WORD, font=("Consolas", 9), bg="#1e1e1e", fg="#4af626")
        self.log_area.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(self.tab_procesar, variable=self.progress_var, maximum=100).pack(fill=tk.X, padx=10, pady=5)
        
        f_btns = ttk.Frame(self.tab_procesar)
        f_btns.pack(fill=tk.X, padx=10, pady=10)
        self.btn_run = ttk.Button(f_btns, text="▶ INICIAR PRODUCCIÓN", command=self.iniciar_procesamiento)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        self.btn_stop = ttk.Button(f_btns, text="⏹ Detener", command=self.detener_procesamiento, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

    def log(self, m):
        self.log_area.after(0, lambda: (self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {m}\n"), self.log_area.see(tk.END)))

    def cargar_frases(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.txt_frases.insert(tk.END, f.read() + "\n")

    def guardar_frases(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(self.txt_frases.get("1.0", tk.END).strip())
            messagebox.showinfo("Éxito", "Lista guardada correctamente.")

    def seleccionar_carpeta(self):
        c = filedialog.askdirectory()
        if c: self.var_carpeta_salida.set(c)

    # ==============================================================================
    # LÓGICA GEMINI
    # ==============================================================================
    def generar_con_ia(self):
        if not GEMINI_API_KEY or "TU_API_KEY" in GEMINI_API_KEY:
            messagebox.showwarning("API Key", "Falta tu API Key de Gemini.")
            return
        threading.Thread(target=self._hilo_gemini, daemon=True).start()

    def _hilo_gemini(self):
        try:
            self.log("Generando guiones con Gemini...")
            client = genai.Client(api_key=GEMINI_API_KEY)
            num = self.var_cantidad_videos.get()
            pals = self.var_min_palabras.get()
            
            prompt = (
                f"Actúa como guionista de una cuenta de TikTok cristiana. Genera exactamente {num} guiones profundos.\n"
                f"REGLA 1: La narrativa debe tener un mínimo estricto de {pals} palabras.\n"
                "REGLA 2: El guion debe estar escrito exactamente como lo leerá un humano, con una transición fluida hacia el versículo, el cual debe estar completo en la misma narrativa.\n"
                "Formato por línea, separado por barras (|):\n"
                "Guion completo a narrar | Llamado a la acción | 3 keywords en inglés para B-Roll de naturaleza\n"
                "Ejemplo: El desierto es solo una etapa... Por eso recordemos Salmos 23:1: Jehová es mi pastor, nada me faltará. | Comenta Amén | desert, oasis, sky\n"
                "Sin introducciones, ni asteriscos, solo el texto."
            )
            
            res = client.models.generate_content(model='gemini-1.5-flash-002', contents=prompt)
            self.txt_frases.after(0, lambda: self.txt_frases.insert(tk.END, res.text.strip() + "\n\n"))
            self.log(f"✅ Se han generado {num} guiones exitosamente.")
        except Exception as e:
            self.log(f"❌ Error IA: {e}")
            messagebox.showerror("Error de Gemini", f"Ocurrió un problema: {e}")

    # ==============================================================================
    # LÓGICA DE VIDEO (CORTES RÁPIDOS Y DESCARGA ANTI-403)
    # ==============================================================================
    def obtener_urls_pexels(self, kw, total):
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={kw}&orientation=portrait&per_page=25"
        try:
            r = requests.get(url, headers=headers)
            vids = r.json().get("videos", [])
            random.shuffle(vids)
            links = []
            for v in vids:
                if v["id"] in self.videos_usados_pexels: continue
                for f in v["video_files"]:
                    if f["width"] >= 720:
                        links.append(f["link"])
                        self.videos_usados_pexels.add(v["id"])
                        break
                if len(links) >= total: break
            return links
        except: return []

    def iniciar_procesamiento(self):
        lineas = [l.strip() for l in self.txt_frases.get("1.0", tk.END).split('\n') if l.strip() and not l.startswith("===")]
        if not lineas: 
            messagebox.showwarning("Texto vacío", "No hay guiones válidos para procesar.")
            return
        
        self.stop_flag = False
        self.btn_run.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.log_area.delete("1.0", tk.END)
        threading.Thread(target=self._hilo_video, args=(lineas,), daemon=True).start()

    def detener_procesamiento(self):
        self.stop_flag = True
        self.log("Deteniendo... (Esperando a terminar el clip actual)")

    def _hilo_video(self, lineas):
        meta = self.var_duracion.get()
        corte = 2.5
        out = self.var_carpeta_salida.get()
        os.makedirs(out, exist_ok=True)
        
        for idx, l in enumerate(lineas):
            if self.stop_flag: break
            self.log(f"\n--- Produciendo fondo {idx+1}/{len(lineas)} ---")
            partes = l.split('|')
            kw = partes[-1].split(',')[0].strip() if len(partes) > 1 else "peaceful nature"
            
            num_clips = int(meta / corte) + 1
            self.log(f"Descargando clips para: '{kw}'")
            urls = self.obtener_urls_pexels(kw, num_clips)
            
            if not urls:
                self.log(f"No se encontraron videos para '{kw}'. Saltando...")
                continue
                
            clips = []
            temps = []
            duracion_acumulada = 0.0
            
            for u in urls:
                if duracion_acumulada >= meta or self.stop_flag: break
                path = os.path.join(tempfile.gettempdir(), f"raw_{random.randint(0,9999)}.mp4")
                
                self.log(f"📥 Descargando clip ({len(temps)+1}/{num_clips})...")
                self.update_idletasks()
                
                try:
                    headers_descarga = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Authorization": PEXELS_API_KEY
                    }
                    respuesta = requests.get(u, headers=headers_descarga, stream=True)
                    
                    if respuesta.status_code == 200:
                        with open(path, 'wb') as f:
                            for chunk in respuesta.iter_content(chunk_size=8192):
                                f.write(chunk)
                    else:
                        raise Exception(f"HTTP Error {respuesta.status_code}")
                        
                    temps.append(path)
                    
                    self.log(f"✂️ Cortando a 2.5s...")
                    self.update_idletasks()
                    c = VideoFileClip(path).without_audio()
                    
                    w, h = c.size
                    if w/h > 9/16:
                        c = crop(c, width=int(h*9/16), height=h, x_center=w/2, y_center=h/2)
                    else:
                        c = crop(c, width=w, height=int(w*16/9), x_center=w/2, y_center=h/2)
                    
                    final_t = min(corte, c.duration)
                    clip_recortado = resize(c, newsize=(1080, 1920)).subclip(0, final_t)
                    clips.append(clip_recortado)
                    duracion_acumulada += final_t
                    self.log(f"✅ Listo. Total: {duracion_acumulada:.1f}s / {meta}s")
                except Exception as e:
                    self.log(f"⚠️ Error en clip: {e}. Saltando...")
            
            if clips and not self.stop_flag:
                try:
                    self.log("Uniendo clips y renderizando final...")
                    final = concatenate_videoclips(clips, method="compose")
                    if final.duration > meta:
                        final = final.subclip(0, meta)
                        
                    nombre_archivo = f"NacionCristiana_{idx+1}_{kw.replace(' ', '')}.mp4"
                    ruta_final = os.path.join(out, nombre_archivo)
                    
                    final.write_videofile(ruta_final, fps=30, codec="libx264", logger=None)
                    
                    final.close()
                    for c in clips: c.close()
                    self.log(f"✅ ¡Video guardado en {ruta_final}!")
                except Exception as e:
                    self.log(f"❌ Error al renderizar: {e}")
            
            for t in temps: 
                try: os.remove(t)
                except: pass
            
            self.progress_var.set(((idx+1)/len(lineas))*100)

        self.log("\n=================================")
        self.log("🎬 ¡PRODUCCIÓN FINALIZADA! 🎬")
        self.btn_run.after(0, lambda: self.btn_run.config(state=tk.NORMAL))
        self.btn_stop.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))

if __name__ == "__main__":
    GeneradorFondosTikTok().mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox,simpledialog,ttk
from pytube import YouTube
from PIL import Image
from moviepy.editor import VideoFileClip
from moviepy.editor import ImageSequenceClip
from pydub import AudioSegment
import numpy as np
import json
import os
import subprocess
import shutil
import platform

def check_ffmpeg_installed():
    # Verifica si ffmpeg está instalado en el sistema
    return shutil.which('ffmpeg') is not None

def install_ffmpeg():
    if not check_ffmpeg_installed():
        system = platform.system()
        if system == 'Windows':
            # Ejecutar comandos de instalación para Windows
            subprocess.run(['ffmpeg.exe', '/S'])  # Ejemplo de un instalador silencioso en Windows
        elif system == 'Linux':
            # Ejecutar comandos de instalación para Linux
            subprocess.run(['sudo', 'apt', 'install', 'ffmpeg'])  # Ejemplo de instalación en sistemas basados en Debian
        elif system == 'Darwin':
            # Ejecutar comandos de instalación para macOS
            subprocess.run(['brew', 'install', 'ffmpeg'])  # Ejemplo de instalación usando Homebrew en macOS

# Llama a la función de instalación de ffmpeg solo si no está instalado
if not check_ffmpeg_installed():
    install_ffmpeg()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")
def menu_ventana(root): 
    # Crear el menú
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Agregar comandos directamente al menú principal
    menubar.add_command(label="Downloader", command=downloader)
    menubar.add_command(label="Convertidor-IMG", command=convertidor)
    menubar.add_command(label="Convertidor-MP3",command=convertidormp3)

#funciones de los menu
def downloader():
    ventana.deiconify()
    convertidor_ventana.withdraw()
    convertidor_mp3.withdraw()
    menu_ventana(ventana)
def convertidor():
    convertidor_ventana.deiconify()
    ventana.withdraw()
    convertidor_mp3.withdraw()
    menu_ventana(convertidor_ventana)

def convertidormp3():
    convertidor_mp3.deiconify()
    ventana.withdraw()
    convertidor_ventana.withdraw()
    menu_ventana(convertidor_mp3)    
def carpeta():
    if 'ultima_ruta' in configuracion:
        carpeta_descargas = configuracion['ultima_ruta']
        os.startfile(carpeta_descargas)
    else:
        messagebox.showerror('error',"NO HAS SELECIONADO LA RUTA DE DESCARGA")    


def cerrar_segunda_ventana():
    convertidor_ventana.withdraw()
    ventana.withdraw()
    ventana.quit()

def cerrar_tercera_ventana():
    convertidor_mp3.withdraw()
    ventana.withdraw()
    ventana.quit()    

#funcion para descargar musica
def descargar_musica():
    url = entrada_url.get()
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        tituloyt = yt.title
        if 'ultima_ruta' in configuracion:
            directorio_destino = configuracion['ultima_ruta']
        else:
            directorio_destino = None
        if directorio_destino:
            audio.download(output_path=directorio_destino, filename=tituloyt + '.mp3')
            messagebox.showinfo("Descarga completada", "La música se ha descargado correctamente.")
            limpiar_entrada()
        else:
            messagebox.showerror("Error", "No se ha seleccionado una ruta de destino.")
            limpiar_entrada()
    except Exception as e:
        messagebox.showerror("Error", "intente con otra url: " + str(e))
        limpiar_entrada()
#funcion para descargar videos
def descargar_video():
    url = entrada_url.get()
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        tituloyt = yt.title
        if 'ultima_ruta' in configuracion:
            directorio_destino = configuracion['ultima_ruta']
        else:
            directorio_destino = None
        if directorio_destino:
            video.download(output_path=directorio_destino, filename=tituloyt + '.mp4')
            messagebox.showinfo("Descarga completada", "El video se ha descargado correctamente.")
            limpiar_entrada()
        else:
            messagebox.showerror("Error", "No se ha seleccionado una ruta de destino.")
            limpiar_entrada()
    except Exception as e:
        messagebox.showerror("Error", "intente con otra url: " + str(e))
        limpiar_entrada()
#funcion para limpiar la entrada del url
def limpiar_entrada():
    entrada_url.delete(0, tk.END)
#funcion para que de la opcion de pegar con clik derecho
def funcion_pegar():
    content = ventana.clipboard_get()
    entrada_url.insert(tk.END, content)
#funcion que hara el evento de pegar
def mostrar_menu(event):
    popup_menu.post(event.x_root, event.y_root)
#funcion para elegir el directorio
def seleccionar_nueva():
    nueva_ruta = filedialog.askdirectory()
    if nueva_ruta:
        configuracion['ultima_ruta'] = nueva_ruta
        with open('configuracion.json','w') as archivo_configuracion:
            json.dump(configuracion, archivo_configuracion)
            messagebox.showinfo("Ruta seleccionada", "La ruta de destino se ha cambiado correctamente a: " + nueva_ruta)
            mensaje.config(text='DIRECTORIO:' + nueva_ruta)
#creacion y configuracion de la ventana
ventana = tk.Tk()
ventana.title('DOWNLOADER RZ')
ventana.geometry('950x500')
ventana.resizable(False,False)
center_window(ventana, 950, 500)
#configuracion donde se guardara la ultima ruta elegida
configuracion = {}
try:
    with open('configuracion.json', 'r') as archivo_configuracion:
        configuracion = json.load(archivo_configuracion)
except FileNotFoundError:
    pass
#icono de la app
ventana.iconbitmap("icon_logo.ico")

#fondo de la aplicacion
fondo = tk.PhotoImage(file="bg.png")
fondo_label = tk.Label(ventana, image=fondo)
logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(ventana, image=logo,borderwidth=0)
logo_label.place(x=50,y=50)
fondo_label.place(relwidth=1, relheight=1)
titulo = tk.Label(ventana, bg="black", fg="white", text="BIENVENIDO A DOWNLOADER RZ", font=("ARIAL", 20))
titulo.place(x=250, y=70)

boton_img = tk.PhotoImage(file="car.png")
entrada_direct = tk.Button(ventana, image=boton_img, command=seleccionar_nueva)  # Aquí asigna la función seleccionar_nueva
entrada_direct.place(x=180, y=180)
entrada_direct.configure(bg="black")
#entrada del url para descargar el video o la musica
label_url = tk.Label(ventana, text="URL DEL VIDEO DE YOUTUBE:", font=("black", 15), bg="black", fg="white")
label_url.place(y=230, x=350)

entrada_url = tk.Entry(ventana, width=80)
entrada_url.place(x=250, y=270)

popup_menu = tk.Menu(ventana, tearoff=0)
popup_menu.add_command(label="PEGAR", command=funcion_pegar)

entrada_url.bind("<Button-3>", mostrar_menu)
menu_ventana(ventana)
#botono para abrir la carpeta del directorio
directorio=tk.Button(ventana,text="...",command=carpeta)
directorio.place(x=700,y=200)
#botones para que seactiven la funciones de descarga tanto para video y musica
boton_descargar_musica = tk.Button(ventana, text="DESCARGA MÚSICA", command=descargar_musica, width=25)
boton_descargar_musica.place(x=300, y=300)
boton_descargar_musica.configure(bg="black", fg="white")

boton_descargar_video = tk.Button(ventana, text="DESCARGA VIDEO", command=descargar_video, width=25)
boton_descargar_video.place(x=500, y=300)
boton_descargar_video.configure(bg="black", fg="white")

mensaje = tk.Label(ventana, text="", bg="black", fg="white", font=("ARIAL", 10))
mensaje.place(x=250, y=200)

if 'ultima_ruta' in configuracion:
    mensaje.config(text='Ruta: ' + configuracion['ultima_ruta'])

#funciones para convertidor
def selecionar_video():
    archivo_mp4 = filedialog.askopenfilename(filetypes=[("Archivos MP4","*.mp4")])
    if archivo_mp4:
        duracion = obtener_duracion(archivo_mp4)
        if duracion <= 15:
            label_ruta.config(text="" + archivo_mp4)
        else:
            messagebox.showerror("ERROR","EL ARCHIVO NO TIENE UNA DURACION DE 15 SEGUNDOS")

def obtener_duracion(archivo):
    clip = VideoFileClip(archivo)
    duracion = int(clip.duration)
    clip.close()
    return duracion 
    
def selecionar_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen","*.jpg;*.jpeg;*.png;*.gif;*.jfif;*.webp")])
    if ruta_imagen:
        label_ruta.config(text=" " + ruta_imagen)
def convertir_imagen():
    selecion= var_opcion.get()
    if selecion == "PNG" or selecion == "JPG" or selecion == "ICO":
    # Debes pasar el nombre del archivo seleccionado a la función jpg_a_png
      if label_ruta.cget("text"):  # Verifica si se ha seleccionado una imagen
            archivo_seleccionado = label_ruta.cget("text").strip()  # Obtener el nombre del archivo seleccionado
            if selecion == "PNG":    
               jpg_a_png(archivo_seleccionado)
            elif selecion == "JPG":
                 png_a_jpg(archivo_seleccionado)
            elif selecion == "ICO":
                imagen_ico(archivo_seleccionado)                       
      else:
            messagebox.showerror("Error", "No se ha seleccionado ninguna imagen.")
    elif selecion == "GIF":
         archivo_seleccionado = label_ruta.cget("text").strip()
         if archivo_seleccionado.lower().endswith('.mp4'):
            if os.path.exists(archivo_seleccionado):
                ruta_salida = archivo_seleccionado.replace('.mp4', '.gif')
                convertir_a_gif(archivo_seleccionado, ruta_salida)
                messagebox.showinfo("CONVERTIDO", f"Archivo convertido a GIF")
           
            else:
                messagebox.showerror("Error", "El archivo seleccionado no existe.")
         
         else:
            carpeta_seleccionada = filedialog.askdirectory()
            if carpeta_seleccionada:
                convertir_a_gif_carpeta(carpeta_seleccionada)
    else:
        messagebox.showerror("Error", "Hubo un error al convertir la imagen.")
            
    
#funciones donde convertira la imagen


def jpg_a_png(boton_seleccionar):
    nombre_archivo, _ = os.path.splitext(boton_seleccionar)
    img = Image.open(boton_seleccionar)
    
    # Solicitar al usuario que elija un nombre y ubicación para guardar el archivo
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("Archivos PNG", "*.png")],
                                                  initialfile=f"{nombre_archivo}.png")
    if not ruta_guardado:
        messagebox.showerror("Error", "No se seleccionó ningún archivo o ubicación.")
        return
    
    img.save(ruta_guardado, "PNG")
    messagebox.showinfo("Éxito", f"Imagen guardada como {ruta_guardado}")

def png_a_jpg(boton_seleccionar):
    nombre_archivo, _ = os.path.splitext(boton_seleccionar)
    img = Image.open(boton_seleccionar)
    
    # Solicitar al usuario que elija un nombre y ubicación para guardar el archivo
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                  filetypes=[("Archivos JPG", "*.jpg")],
                                                  initialfile=f"{nombre_archivo}.jpg")
    if not ruta_guardado:
        messagebox.showerror("Error", "No se seleccionó ningún archivo o ubicación.")
        return
    
    img.save(ruta_guardado, "JPEG")
    messagebox.showinfo("Éxito", f"Imagen guardada como {ruta_guardado}")
def imagen_ico(boton_selecionar):
    nombre_archivo, _ = os.path.splitext(boton_selecionar)
    img = Image.open(boton_selecionar)
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".ico",
                                                 filetypes=[("Archivos ICO","*.ico")],
                                                 initialfile=f"{nombre_archivo}.ico")
    if not ruta_guardado:
        messagebox.showerror("ERROR","No se seleciono ningun archivo o ubicacion")
        return
    img.save(ruta_guardado,"ICO")
    messagebox.showinfo("EXITO",f"Imagen guardada como {ruta_guardado}") 

def convertir_a_gif(archivo_mp4,ruta_guardado):
    clip = VideoFileClip(archivo_mp4)
       
    # Ajustar los parámetros para mejorar la calidad y el rendimiento del GIF
    fps = clip.fps / 2  # Reducir los fotogramas por segundo a la mitad
   
    
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".gif",
                                                 filetypes=[("Archivos GIF", "*.gif")],
                                                 initialfile="video.gif")
    if not ruta_guardado:
        messagebox.showerror("ERROR","No se selecciono ningun archivo o ubicacion")
        return
    clip.write_gif(ruta_guardado, fps=fps, program='ffmpeg', opt='nq', fuzz=1, verbose=False)
    clip.close()
  
def convertir_a_gif_carpeta(carpeta_entrada):
    archivos_imagen = [os.path.join(carpeta_entrada, archivo) for archivo in sorted(os.listdir(carpeta_entrada))]

    imagenes = []
    for archivo_imagen in archivos_imagen:
        if archivo_imagen.lower().endswith(('.png', '.jpg', '.jpeg')):
            imagen = Image.open(archivo_imagen)
            imagenes.append(np.array(imagen))  # Convertir a matriz de imagen

    if imagenes:
        # Solicitar al usuario que elija los FPS
        fps = solicitar_fps()
        if fps:
            # Solicitar al usuario que elija la ubicación y el nombre del archivo GIF de salida
            ruta_salida = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("Archivo GIF", "*.gif")], initialfile="animacion.gif")
            
            if ruta_salida:
                # Crear un clip de secuencia de imágenes solo con los fotogramas seleccionados
                clip = ImageSequenceClip(imagenes, fps=fps)
                clip.write_gif(ruta_salida, fps=fps)
                messagebox.showinfo("CONVERTIDO", f"Imágenes convertidas a GIF en: {ruta_salida} con {fps} FPS")
        else:
            messagebox.showerror("ERROR", "Los FPS ingresados no son válidos")
    else:
        messagebox.showerror("ERROR", "No se encontraron imágenes válidas en la carpeta de entrada")

def solicitar_fps():
    # Solicitar al usuario que ingrese los FPS
    try:
        fps = simpledialog.askfloat("FPS", "Ingrese los FPS (Fotogramas por segundo):", initialvalue=10)
        if fps <= 0:
            return None
        return fps
    except ValueError:
        return None



def seleccionar_carpeta():

    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        label_ruta.config(text=carpeta_seleccionada)
    else:
            messagebox.showerror("ERROR", "No se seleccionó una ubicación de salida para el archivo GIF")




#termino de funciones de converciones
    
opciones = ["JPG","PNG","GIF","ICO"]


#VENTANA CONVERTIDOR
convertidor_ventana = tk.Toplevel(ventana)
convertidor_ventana.title("CONVERTIDOR DE IMAGENES")
convertidor_ventana.iconbitmap("icon_logo.ico")
convertidor_ventana.geometry('950x500')
convertidor_ventana.resizable(False,False)
convertidor_ventana.withdraw()
convertidor_ventana.protocol("WM_DELETE_WINDOW", cerrar_segunda_ventana)
fondo_label1 = tk.Label(convertidor_ventana, image=fondo)
fondo_label1.place(relwidth=1, relheight=1)
center_window(convertidor_ventana, 950, 500)
logo_img = tk.Label(convertidor_ventana,image=logo,borderwidth=0)
logo_img.place(x=50,y=50)
titulo_img = tk.Label(convertidor_ventana, bg="black", fg="white", text="CONVERTIDOR DE IMAGENES", font=("ARIAL", 20))
titulo_img.place(x=250, y=70)
#variable para almacenar selecion
var_opcion = tk.StringVar(convertidor_ventana)
var_opcion.set(opciones[0]) #esto seleciona una de las opciones preterminadas
#funcion para empaquetar botones de radio para cada opcion
x_pos = 220
y_pos = 130
margen_entre_botones_horizontal = 50
for opcion in opciones:
    boton_radio = tk.Radiobutton(convertidor_ventana,text=opcion,variable=var_opcion,value=opcion)
    boton_radio.place(x=x_pos, y=y_pos,width=130)
    x_pos += 100  # Ajuste horizontal
    x_pos += margen_entre_botones_horizontal
icon_img = tk.PhotoImage(file="imagen.png")
boton_selecionar = tk.Button(convertidor_ventana, image=icon_img, command=selecionar_imagen,borderwidth=0)
boton_selecionar.place(x=200,y=200)
icon_video = tk.PhotoImage(file="video.png")
boton_mp4 = tk.Button(convertidor_ventana,image=icon_video,command=selecionar_video,borderwidth=0)
boton_mp4.place(x=200,y=260)
icon_carpeta = tk.PhotoImage(file="carpeta.png")
boton_carpeta = tk.Button(convertidor_ventana,image=icon_carpeta,command=seleccionar_carpeta,borderwidth=0)
boton_carpeta.place(x=200,y=320)
boton_selecion = tk.Button(convertidor_ventana,text="CONVERTIR",command=convertir_imagen)
boton_selecion.place(x=370,y=300,width=400)
label_ruta = tk.Label(convertidor_ventana, text="")
label_ruta.place(x=320,y=250,width=500)

#tercera ventana convertidor mp3
#VENTANA CONVERTIDOR
convertidor_mp3 = tk.Toplevel(convertidor_ventana)
convertidor_mp3.title("CONVERTIDOR DE MP3")
convertidor_mp3.geometry('950x500')
convertidor_mp3.resizable(False,False)
convertidor_mp3.withdraw()
convertidor_mp3.iconbitmap("icon_logo.ico")

convertidor_mp3.protocol("WM_DELETE_WINDOW", cerrar_tercera_ventana)
fondo_label1 = tk.Label(convertidor_mp3, image=fondo)
fondo_label1.place(relwidth=1, relheight=1)
center_window(convertidor_mp3, 950, 500)
logo_mp3 = tk.Label(convertidor_mp3,image=logo,borderwidth=0)
logo_mp3.place(x=50,y=50)

#FUNCIONES PARA LA VENTAN CONVERTIDOR MP3
def selecionar_video():
    ruta_video = filedialog.askopenfilename(filetypes=[("Archivos de video","*.mp4;*.avi;*.mkv")])
    if ruta_video:
        label_audio.config(text=""+ruta_video)
def selecionar_musica():
    ruta_musica = filedialog.askopenfilename(filetypes=[("Archivos de audio","*.mp3;*.wav;*.ogg;*.aac")])
    if ruta_musica:
        label_audio.config(text=""+ruta_musica)
def convercion_mp3():
    selecion = selecion_format.get()
    if selecion == "MP3":
     ruta_audio = label_audio.cget("text").strip()
     if ruta_audio:
        mp3()
    elif selecion == "" "OGG":
         ruta_audio = label_audio.cget("text").strip()
         if ruta_audio:
          ogg()
    elif selecion == "" "WAV":
         ruta_audio = label_audio.cget("text").strip()
         if ruta_audio:
          wav()
    elif selecion == "" "AAC":
         ruta_audio = label_audio.cget("text").strip()
         if ruta_audio:
          aac()     
    elif selecion == "EXTRAER":   
        ruta_audio = label_audio.cget("text").strip()
        if ruta_audio:
            extraer_audio()  

    else:
         messagebox.showerror("ERROR", "NO SE SELECIONO NINGUN ARCHIVO")   

def mp3():
    ruta_audio = label_audio.cget("text")
    if ruta_audio:
        try:
            sound = AudioSegment.from_file(ruta_audio)
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                         filetypes=[("Archivos MP3", "*.mp3")],
                                                         initialfile="audio.mp3")
            if ruta_guardado:
                sound.export(ruta_guardado, format="mp3")
                messagebox.showinfo("Éxito", "El archivo se ha convertido a MP3 y se ha guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")
def wav():
    ruta_audio = label_audio.cget("text")
    if ruta_audio:
        try:
            sound = AudioSegment.from_file(ruta_audio)
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".wav",
                                                         filetypes=[("Archivos WAV", "*.wav")],
                                                         initialfile="audio.wav")
            if ruta_guardado:
                sound.export(ruta_guardado, format="wav")
                messagebox.showinfo("Éxito", "El archivo se ha convertido a WAV y se ha guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")
def ogg():
    ruta_audio = label_audio.cget("text")
    if ruta_audio:
        try:
            sound = AudioSegment.from_file(ruta_audio)
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".ogg",
                                                         filetypes=[("Archivos OGG", "*.ogg")],
                                                         initialfile="audio.ogg")
            if ruta_guardado:
                sound.export(ruta_guardado, format="ogg")
                messagebox.showinfo("Éxito", "El archivo se ha convertido a OGG y se ha guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")     
def aac():
    ruta_audio = label_audio.cget("text")
    if ruta_audio:
        try:
            sound = AudioSegment.from_file(ruta_audio)
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".aac",
                                                         filetypes=[("Archivos AAC", "*.aac")],
                                                         initialfile="audio.aac")
            if ruta_guardado:
                sound.export(ruta_guardado, format="ogg")
                messagebox.showinfo("Éxito", "El archivo se ha convertido a AAC y se ha guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")                         
def extraer_audio():
    ruta_video = label_audio.cget("text")
    if not ruta_video:
        messagebox.showerror("Error", "No se seleccionó ningún archivo de video.")
        return
    
    # Verificar si el archivo es de formato MP4
    if not ruta_video.lower().endswith(".mp4") or ruta_video.lower().endswith(".avi") or ruta_video.lower().endswith(".mkv"):
        messagebox.showerror("Error", "El archivo seleccionado no es de formato MP4.")
        return
    
    # Obtener la ruta para guardar el audio
    ruta_audio_extraido = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                       filetypes=[("Archivos MP3", "*.mp3")],
                                                       initialfile="audio_extraido.mp3")
    if not ruta_audio_extraido:
        messagebox.showerror("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
        return
    
    # Extraer el audio del video
    video_clip = VideoFileClip(ruta_video)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(ruta_audio_extraido)
    audio_clip.close()
    video_clip.close()
    
    messagebox.showinfo("Éxito", "El audio se ha extraído y guardado correctamente.")
#TERMINO DE FUCIONES
#opciones de selector
opciones = ["MP3","OGG","AAC","WAV","EXTRAER"]   
selecion_format = tk.StringVar()#variable para guarda la seleccion
selecion_format.set("SELECIONA UNA OPCION") #formato para que de un texto inicial
combo = ttk.Combobox(convertidor_mp3,values=opciones,textvariable=selecion_format)
combo.place(x=350,y=200,width=280)
ti_mp3 = tk.Label(convertidor_mp3, bg="black", fg="white", text="CONVERTIDOR DE AUDIO", font=("ARIAL", 20))
ti_mp3.place(x=300,y=100)
btn_v = tk.Button(convertidor_mp3, image=icon_video, command=selecionar_video,borderwidth=0)
btn_v.place(x=250,y=200)
icon_music = tk.PhotoImage(file="muc.png")
btn_m = tk.Button(convertidor_mp3,image=icon_music,command=selecionar_musica,borderwidth=0)
btn_m.place(x=250, y=300)
label_audio = tk.Label(convertidor_mp3,text="")    
label_audio.place(x=330,y=225,width=400)    
btn_convertir = tk.Button(convertidor_mp3,text="CONVERTIR",command=convercion_mp3)
btn_convertir.place(x=380,y=300,width=250)
ventana.mainloop()

import speech_recognition as sr  # Librería de reconocimiento de voz
import pyttsx3  # Librería de texto a voz
import time  # Librería de tiempo
from time import ctime  # Función ctime del módulo time
import webbrowser  # Librería para abrir páginas web
import os  # Librería para trabajar con el sistema operativo
import random  # Librería para generar números aleatorios
from gtts import gTTS  # Librería de generación de voz a partir de texto
from tkinter import *  # Librería de interfaz gráfica de usuario
from PIL import ImageTk, Image  # Librería para trabajar con imágenes
import pygame  # Librería para reproducir sonidos
import psutil  # Librería para obtener estadísticas del sistema
import cpuinfo # Librería para obtener información del procesador
import subprocess # Para ejecutar comandos en la línea de comandos


# Imprime un mensaje de inicio
print('Di algo...')

r = sr.Recognizer()
speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)  # Índice 1 para el idioma español

def record_audio(ask=False):
    """
    Graba el audio del usuario utilizando el micrófono.

    Args:
        ask (bool): Indica si se debe leer una pregunta antes de grabar.

    Returns:
        str: El texto reconocido a partir del audio grabado.
    """
    with sr.Microphone() as source:
        if ask:
            lee_voice(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language='es-ES')
            print('Voz reconocida: ' + voice_data)
        except Exception:
            print('Oops, algo salió mal')
            # lee_voice('Oops, algo salió mal')
        return voice_data


def lee_voice(audio_string):
    """
    Reproduce el audio proporcionado como texto.

    Args:
        audio_string (str): El texto a reproducir como audio.
    """
    tts = gTTS(text=audio_string, lang='es')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    print(audio_string)

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove(audio_file)

def adb_command(command):
    """
    Ejecuta un comando de ADB y devuelve la salida y el error resultantes.

    Args:
        command (str): El comando de ADB a ejecutar.

    Returns:
        tuple: Una tupla que contiene la salida y el error resultantes en formato de texto.
    """
    process = subprocess.Popen(['adb'] + command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip(), error.decode().strip()


class Iris:
    """
    Clase que representa el asistente virtual Iris y sus comandos.
    """

    def __init__(self):
        self.widget = Widget(self)

    def respond(self, voice_data):
        """
        Responde al comando de voz dado por el usuario.

        Args:
            voice_data (str): El comando de voz reconocido.
        """
        voice_data = voice_data.lower()


        if 'hola' in voice_data:
            lee_voice('¡Hola soy Iris, tu asistente virtual! ¿En qué puedo ayudarte?')

        if 'abrir' in voice_data:
            # Obtén el nombre de la aplicación a abrir
            if 'abrir' in voice_data:
                app_name = voice_data.split('abrir')[1].strip()
            else:
                lee_voice('No se proporcionó el nombre de la aplicación.')
                return

            # Verifica si el nombre de la aplicación está en el sistema
            if app_name.lower() == 'calculadora':
                app_path = 'calc.exe'  # Ruta de la aplicacion
            
            elif app_name.lower() == 'bloc de notas':
                app_path = 'notepad.exe'  # Ruta de la aplicacion
            
            elif app_name.lower() == 'navegador' or app_name.lower() == 'firefox':
                app_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe' # Ruta de la aplicacion
            
            elif app_name.lower() == 'spotify' or app_name.lower() == 'música':
                app_path = 'C:\\Users\\fabia\\AppData\\Roaming\\Spotify\\Spotify.exe' # Ruta de la aplicacion
            
            elif app_name.lower() == 'terminal':
                app_path = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe' # Ruta de la aplicacion
    
            
            # Intenta abrir la aplicación
            try:
                os.startfile(app_path)
                lee_voice('Aplicación ' + app_name + ' abierta.')
            except Exception as e:
                lee_voice('No se pudo abrir la aplicación ' + app_name + '.')

        if 'buscar' in voice_data:
            search = record_audio('¿Qué deseas buscar?')
            url = 'https://google.com/search?q=' + search
            webbrowser.open(url)
            lee_voice('Esto es lo que encontré para ' + search)

        if 'encontrar ubicación' in voice_data:
            location = record_audio('¿Cuál es tu ubicación?')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.open(url)
            lee_voice('Aquí está la ubicación de ' + location)

        if 'hora' in voice_data:
            lee_voice("La hora actual es: " + ctime())
            
        if 'características' in voice_data or 'componentes' in voice_data:
            lee_voice('¡Con mucho gusto! Dime ¿qué quieres que monitoree? o dime la palabra todo y te doy un recuento de tus componentes')
            respuesta = record_audio()
            respuesta = respuesta.lower()
            
            if 'memoria' in respuesta:
                # Obtener estadísticas de memoria...
                memory = psutil.virtual_memory()
                total_memory = round(memory.total / (1024 ** 3), 2)  # Convertir a GB
                available_memory = round(memory.available / (1024 ** 3), 2)  # Convertir a GB
                lee_voice(f"La memoria total es de {total_memory} GB")
                lee_voice(f"La memoria disponible es de {available_memory} GB")
                
            elif 'cpu' in respuesta:
                # Obtener estadísticas de CPU...
                cpu_percent = psutil.cpu_percent(interval=1)
                info = cpuinfo.get_cpu_info()
                nombre_procesador = info['brand_raw']
                lee_voice("Tienes un procesador " + nombre_procesador)    
                lee_voice(f"Y el uso de la CPU es del {cpu_percent} por ciento")   
            
            elif 'todo' in respuesta:
                # Obtener estadisticas de todos los componentes posibles
                memory = psutil.virtual_memory()
                total_memory = round(memory.total / (1024 ** 3), 2)  # Convertir a GB
                available_memory = round(memory.available / (1024 ** 3), 2)  # Convertir a GB
                lee_voice(f"La memoria total es de {total_memory} GB")
                lee_voice(f"La memoria disponible es de {available_memory} GB")
                
                cpu_count = psutil.cpu_count()
                cpu_percent = psutil.cpu_percent(interval=1)
                info = cpuinfo.get_cpu_info()
                nombre_procesador = info['brand_raw']
                lee_voice("Tienes un procesador " + nombre_procesador)    
                lee_voice(f"Tienes {cpu_count} procesadores lógicos en tu sistema.")
                lee_voice(f"Y el uso de la CPU es del {cpu_percent} por ciento") 
              
                disk_usage = psutil.disk_usage('/')
                disk_total = round(disk_usage.total / (1024 ** 3), 2)  # Convertir a GB
                disk_free = round(disk_usage.free / (1024 ** 3), 2)  # Convertir a GB
                lee_voice(f"El uso de disco total es de {disk_total} GB")
                lee_voice(f"Y el espacio libre en disco es de {disk_free} GB")               
                
            else:
                lee_voice('No te entendí, puedes volver a preguntarme por lo que desees')
        
        if 'celular' in voice_data:
            lee_voice('¡Con mucho gusto! Dime ¿qué quieres que monitoree?')
            respuesta = record_audio()
            respuesta = respuesta.lower()
            
            if 'captura' in respuesta:
                # Capturar una captura de pantalla
                adb_command('shell screencap /sdcard/screenshot.png')
                adb_command('pull /sdcard/screenshot.png')
                lee_voice("Captura de pantalla guardada como screenshot.png")
            
            elif 'almacenamiento' in respuesta or 'batería' in respuesta:
                # Almacenamiento disponible
                output, _ = adb_command('shell df -h /sdcard')
                storage_info = output.splitlines()[1].split()
                total_storage = storage_info[1]
                used_storage = storage_info[2]
                available_storage = storage_info[3]
                
                lee_voice("Almacenamiento disponible:")
                lee_voice(f"Total: {total_storage}B")
                lee_voice(f"Usado: {used_storage}B")
                lee_voice(f"Disponible: {available_storage}B")
                
                # Nivel de la batería
                output, _ = adb_command('shell dumpsys battery | grep level')
                battery_level = output.split(": ")[1]
                # Estado de carga de la batería
                output, _ = adb_command('shell dumpsys battery | grep status')
                battery_status = output.split(": ")[1]
                
                lee_voice(f"El nivel de batería es de {battery_level}%")
                lee_voice(f"Y el estado de carga de la batería es de {battery_status}%")
            
            elif 'modelo' in respuesta or 'dispositivo' in respuesta:
                # Modelo del dispositivo
                output, _ = adb_command('shell getprop ro.product.model')
                model = output
                # Versión de Android
                output, _ = adb_command('shell getprop ro.build.version.release')
                android_version = output
                
                lee_voice(f"El modelo de tu celular es el {model}")
                lee_voice(f"y la versión de Android es la {android_version}")
                
            else:
                lee_voice('No te entendí, puedes volver a preguntarme por lo que desees')
            
        if 'gracias' in voice_data:
            lee_voice('Con mucho gusto')


        if 'salir' in voice_data or 'chao' in voice_data:
            lee_voice('¡Hasta luego!')
            exit()


class Widget:
    """
    Clase que representa la interfaz gráfica del asistente virtual y sus comandos.
    """

    def __init__(self, iris):
        self.iris = iris

        root = Tk()
        root.title('Iris')
        root.geometry('900x400')

        # Fondo de la interfaz
        background_color = '#f2f2f2'
        root.configure(bg=background_color)

        # Imagen del asistente virtual
        img = ImageTk.PhotoImage(Image.open('iris.png'))
        panel = Label(root, image=img, bg=background_color)
        panel.pack(side='right', fill='both', expand='no')

        # Título del asistente virtual
        title_label = Label(root, text='Iris', font=('Railways', 24, 'bold'), bg=background_color)
        title_label.pack(side='top', fill='both', expand='no')

        # Texto del asistente virtual
        user_text = StringVar()
        user_text.set('Tu Asistente Virtual')
        user_label = Label(root, textvariable=user_text, font=("Century Gothic", 15, 'bold'), bg=background_color, fg='black')
        user_label.pack(side='top', fill='both', expand='yes')

        # Botón de Hablar
        btn = Button(root, text='Hablar', font=('railways', 10, 'bold'), bg='#ff4d4d', fg='white', command=self.clicked)
        btn.pack(fill='x', expand='no')

        # Botón de Cerrar
        btn2 = Button(root, text='Cerrar', font=('railways', 10, 'bold'), bg='#ffff4d', fg='black', command=root.destroy)
        btn2.pack(fill='x', expand='no')

        lee_voice('¿En qué puedo ayudarte?')

        root.mainloop()

    def clicked(self):
        """
        Maneja el evento de clic del botón 'Hablar'.
        """
        print("Trabajando...")
        voice_data = record_audio()
        self.iris.respond(voice_data)

if __name__ == '__main__':
    iris = Iris()
    time.sleep(1)

    while True:
        voice_data = record_audio()
        iris.respond(voice_data)

    speaker.runAndWait()
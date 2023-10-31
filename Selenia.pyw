import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import tkinter as tk
import threading
from PIL import Image, ImageTk

def ativar_comando_voz():
    global escuta_continua
    escuta_continua = False
    comando_voz_usuario()

    
def ativar_escuta_continua():
    global escuta_continua
    escuta_continua = True
    threading.Thread(target=escuta_continua_thread).start()

def fechar_programa():
    window.destroy()

def escuta_continua_thread():
    while escuta_continua:
        comando_voz_usuario()

def executa_comando():
    global comando_em_execucao
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')
            voz = audio.listen(source, timeout=10)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'selenia' in comando:
                comando = comando.replace('selenia', '')
                return comando

    except sr.UnknownValueError:
        print('Não foi possível entender o áudio')
    except sr.RequestError as e:
        print(f'Erro na solicitação do Google: {e}')
    
    comando_em_execucao = False
    return ''

def comando_voz_usuario():
    global comando_em_execucao
    comando_em_execucao = True
    comando = executa_comando()

    if not comando_em_execucao:
        return
    
    if 'horas' in comando or 'hora' in comando:
        hora = datetime.datetime.now().strftime('%H:%M')
        maquina.say(hora)
    elif 'procure por' in comando:
        procurar = comando.replace('procure por', '').strip()
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar, sentences=1)
        maquina.say(resultado)
    elif 'toque' in comando:
        musica = comando.replace('toque', '').strip()
        pywhatkit.playongo(musica)
        maquina.say(f'Tocando música {musica}')
    elif 'quem é você' in comando:
        mensagem = 'Eu sou um assistente pessoal desenvolvido por Kaio Lima Pimentel para auxiliar em tarefas cotidianas.'
        maquina.say(mensagem)

    maquina.runAndWait()
    comando_em_execucao = False

audio = sr.Recognizer()
maquina = pyttsx3.init()
escuta_continua = False
comando_em_execucao = False

window = tk.Tk()
window.title("Assistente de Voz")
window.geometry("1920x1080")  # Tamanho da janela

image = Image.open("1.jpg")
photo = ImageTk.PhotoImage(image)

background_label = tk.Label(window, image=photo)
background_label.place(relwidth=1, relheight=1)

label1 = tk.Label(window, text="Clique para Ativar o Comando de Voz:")
label3 = tk.Label(window, text="Clique para Ativar a Escuta Contínua:")

ativar_button = tk.Button(window, text="Ativar", command=ativar_comando_voz)
escuta_continua_button = tk.Button(window, text="Ativar", command=ativar_escuta_continua)
fechar_button = tk.Button(window, text="Fechar Programa", command=fechar_programa)

label1.pack(pady=20)
ativar_button.pack(pady=10)
label3.pack(pady=20)
escuta_continua_button.pack(pady=10)
fechar_button.pack(pady=20)

window.mainloop()

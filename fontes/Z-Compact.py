# fonte craido dia 04/10/2021
# alterado dia 08/12/2023 #
# adicionado barra de menu
# software incorporado a z-Corp
# 
######################3####
# autor: Jose Duarte
#Compactador de imagens para o site San Diego e criação
import PySimpleGUI as sg
import tinify
from glob import glob
import os.path
import shutil
import sys

sg.theme('Reddit')

def carregar_chave_do_arquivo():
    try:
        with open('chave.txt', 'r') as arquivo:
            chave_salva = arquivo.read().strip()
            return chave_salva
    except FileNotFoundError:
        return ''
def salvar_chave_no_arquivo(chave):
    with open('chave.txt', 'w') as arquivo:
        arquivo.write(chave)



def criar_janela_sobre():
    texto_sobre = """
    Z-Compact v1.0

    Desenvolvido por José Duarte

    Existe um limite de 500 imagens por mês

    Caso passe limite precisa uma nova chave

    Solicite uma nova chave para:

    Contato: duarte936@gmail.com
    """
    sg.popup_scrolled(texto_sobre, title='Sobre...', size=(40, 10))

def criar_janela_chave():
    chave_salva = carregar_chave_do_arquivo()
    layout_chave = [
        [sg.Text('Insira a chave:')],
        [sg.InputText(key='-CHAVE-', size=(30, 1))],
        [sg.Button('OK'), sg.Button('Cancelar')],
    ]

    window_chave = sg.Window('Inserir Chave', layout_chave)

    while True:
        event_chave, values_chave = window_chave.read()

        if event_chave == sg.WIN_CLOSED or event_chave == 'Cancelar':
            break
        elif event_chave == 'OK':
            chave_inserida = values_chave['-CHAVE-'].strip()  # Remover espaços em branco no início e no final
            if chave_inserida:
                sg.popup(f'Chave inserida: {chave_inserida}')
                salvar_chave_no_arquivo(chave_inserida)
                window_chave.close()
                sg.popup('Rode novamente...')
                sys.exit()  # Reinicia o programa
            else:
                sg.popup_error('Erro: O campo da chave não pode estar em branco.')

    window_chave.close()

menu_def = [['Arquivo',['Chave']],['Ajuda','Sobre...'],]
layout = [
    [sg.Menu(menu_def)],
    [sg.Text("Pasta de Imagens: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FolderBrowse(key="-IN-")],
    [sg.Button("Compactar")],
    [sg.Button("Compactar 2X")],
    [sg.Button('Exit', button_color=('white', 'firebrick3'))],
    [sg.Text('Imagens Compactadas')],
    [sg.Multiline(key='files', size=(70,10), autoscroll=True)],
    ]
#tinify.key = "WfxDjSlPmk9KhNJQ6s0qxQBSns2LFwgD"
tinify.key = carregar_chave_do_arquivo()  

window = sg.Window('Z-Compact', layout, icon='icon.ico')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        window.close()
        break
    if event in ('Exit', None):
        break
    elif event == 'Sobre...':
        criar_janela_sobre()
    elif event == 'Chave':
        criar_janela_chave()
    elif event == "Compactar":
        source_dir_name = (values["-IN2-"])
        filenames = os.listdir(source_dir_name)
        # it uses `key='files'` to access `Multiline` widget
        window['files'].update("\n".join(filenames))
        files = glob(source_dir_name + '\*')
        if os.path.exists('Compactadas'):
            shutil.rmtree('Compactadas')
        os.mkdir('Compactadas') 
        destination_dir_name =os.path.join(os.getcwd(), "Compactadas")
        for file in files:
            source = tinify.from_file(file)
            file_name, ext = os.path.splitext(file)
            file_name = file_name.replace(source_dir_name + "\\",'' )
            source.to_file(destination_dir_name + '\\' + file_name + ".jpg")
        filenames = sorted(os.listdir(destination_dir_name))
            # it use `key='files'` to `Multiline` widget
        window['files'].update("\n".join(filenames))
        sg.Popup('Tudo Certo!', 'Todas as imagens Foram Compactadas','Pasta de saida ' + destination_dir_name)
        
    elif event == "Compactar 2X":
       # print("duas vezes ok ")
        source_dir_name = ("Compactadas")
        window['files'].update("\n".join(filenames))
        files = glob(source_dir_name + '\*')
        if os.path.exists('Compactadas_2'):
            shutil.rmtree('Compactadas_2')
        os.mkdir('Compactadas_2') 
        destination_dir_name =os.path.join(os.getcwd(), "Compactadas_2")
        for file in files:
            source = tinify.from_file(file)
            file_name, ext = os.path.splitext(file)
            file_name = file_name.replace(source_dir_name + "\\",'' )
            source.to_file(destination_dir_name + '\\' + file_name + ".jpg")
        filenames = sorted(os.listdir(destination_dir_name))
            # it use `key='files'` to `Multiline` widget
        window['files'].update("\n".join(filenames))
        sg.Popup('Tudo Certo!', 'Todas as imagens Foram Compactadas 2 vezes','Pasta de saida ' + destination_dir_name)
        

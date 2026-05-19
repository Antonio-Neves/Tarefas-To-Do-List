# ----- Importações iniciais ----- #
import kivy
kivy.require('1.11.0')

import os
from kivy import Config
import platform
import json

# ----- Soluciona problemas de OpenGL e placas graficas antigas em windows -- #
if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
    Config.set('graphics', 'multisamples', '0')

# ----- Necessário para Video e Audio no Linux----- #
if platform.system() == 'Linux':
    os.environ['KIVY_VIDEO'] = 'ffpyplayer'

# ----- Configuração da janela e teclado ----- #
Config.set('graphics', 'resizable', True)
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', 700)
Config.set('graphics', 'height', 1000)
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp, sp

# Ajusta a janela automaticamente para cima quando o teclado do Android abrir
Window.softinput_mode = 'resize'

# ----- Lista das tarefas ----- #
listatarefas = []


def obter_caminho_json():
    # Obtém a pasta de dados segura alocada pelo sistema operativo (Android ou Linux)
    pasta_app = App.get_running_app().user_data_dir
    return os.path.join(pasta_app, "data_tarefas.json")


def carregar_dados():
    global listatarefas
    path_tarefas = obter_caminho_json()
    try:
        if os.path.exists(path_tarefas):
            with open(path_tarefas, 'r') as data:
                listatarefas = json.load(data)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")


def savedata():
    path_tarefas = obter_caminho_json()
    try:
        with open(path_tarefas, 'w') as task_data:
            json.dump(listatarefas, task_data)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def salvar_cor_tarefa(texto, cortarefa):
    for item in listatarefas:
        if item[0] == texto:
            item[1] = cortarefa
    savedata()


def remover_tarefa(texto):
    for item in listatarefas:
        if item[0] == texto:
            listatarefas.remove(item)
    savedata()


class Principal(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Carrega os dados salvos antes de renderizar os widgets
        carregar_dados()

        # ----- Adiciona no Inicio as tarefas guardadas ----- #
        for item in listatarefas:
            self.ids.boxtarefas.add_widget(Tarefas(item[0], item[1]))

        # --- Define a cor inicial das tarefas --- #
        self.cor_tarefa = (1, 1, 1, .3)

    def adicionar_tarefa(self, texto):
        if texto:
            self.ids.boxtarefas.add_widget(Tarefas(texto, self.cor_tarefa))
            self.ids.texto.text = ''  # --- Inicia o text input vazio --- #
            listatarefas.append([texto, self.cor_tarefa])
            savedata()


class Tarefas(FloatLayout):
    def __init__(self, texto, cor, **kwargs):
        super().__init__(**kwargs)

        # --- Variaveis texto e cor inicial da tarefa --- #
        self.texto = texto
        self.cor = tuple(cor)

        # --- Cores das tarefas --- #
        self.canvascolor = self.cor
        self.ids.btn_cor.canvascolor = self.cor

        # --- Variaveis das possiveis cores das tarefas ---#
        self.normal = (1, 1, 1, .3)
        self.azul = (0, 0, 1, 1)
        self.vermelho = (1, 0, 0, 1)
        self.verde = (0, 1, 0, 1)
        self.amarelo = (1, 1, 0, 1)

        # --- Texto da tarefas com tamanho dinâmico (sp) --- #
        self.ids.tarefa.text = self.texto
        self.ids.tarefa.font_size = sp(18)  # Garante leitura excelente no Android

    def cortarefa(self):
        if self.cor == (1, 1, 1, .3):
            self.cor = self.vermelho
        elif self.cor == self.vermelho:
            self.cor = self.verde
        elif self.cor == self.verde:
            self.cor = self.amarelo
        elif self.cor == self.amarelo:
            self.cor = self.normal

        self.ids.btn_cor.canvascolor = self.cor
        self.canvascolor = self.cor

        salvar_cor_tarefa(self.texto, self.cor)

    def remover_tarefa(self, texto):
        remover_tarefa(texto)


class Main(App):
    def build(self):
        self.title = 'Tarefas'

        # Altera aqui também para a extensão .png para evitar problemas no Android
        self.icon = 'Images/Logo.png'
        return Principal()


if __name__ == '__main__':
    Main().run()
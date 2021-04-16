
# coding: utf-8

#################################
#            Tarefas            #
#                               #
# Author: António Silva Neves   #
#           AN Informática      #
#################################


# ----- Importações iniciais ----- #
# import kivy
# kivy.require('1.11.0')

import os
from kivy import Config
import platform

# ----- Soluciona problemas de OpenGL e placas graficas antigas em windows -- #
if platform.system() == 'Windows':

	os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
	Config.set('graphics', 'multisamples', '0')

# ----- Configuração da janela ----- #
Config.set('graphics', 'resizable', True)
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', 350)
Config.set('graphics', 'heigth', 500)


# ----- Importações ----- #
import json
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


# ----- Cria pastas ----- #
try:
    os.mkdir(os.path.expanduser(
        "~/Tarefas App"))
except:
    pass


# ----- Lista das tarefas ----- #
listatarefas = []


# ----- Path arquivo .json ----- #
path_tarefas = os.path.expanduser(
    "~/Tarefas App/data_tarefas.json")


# ----- Cria .json e coloca na lista as tarefas guardadas ----- #	
try:  # ----- Previne erro falta arquivo .json ----- #
	with open(path_tarefas, 'r') as data:
		listatarefas = json.load(data)

except:
	pass


# --- Salva os dados em um ficheiro Json --- #
def savedata():

	with open(path_tarefas, 'w') as data:
		json.dump(listatarefas, data)


# --- Salva as cores das tarefas no ficheiro Json --- #
def salvar_cor_tarefa(texto, cortarefa):

	# --- Procura na lista o nome da tarefa em que foi alterada a cor  --- #
	for item in listatarefas:
		if item[0] == texto:
			item[1] = cortarefa

	savedata()


# --- Remove Tarefa da lista de Tarefas--- #
def remover_tarefa(texto):

	# --- Procura na lista o nome da tarefa e remove da lista --- #
	for item in listatarefas:

		if item[0] == texto:

			listatarefas.remove(item)

	savedata()


# ----- Classe Wid Principal ----- #
class Principal(FloatLayout):
	def __init__(self):
		super().__init__()

		# ----- Adiciona no Inicio as tarefas guardadas ----- #
		for item in listatarefas:
			self.ids.boxtarefas.add_widget(Tarefas(item[0], item[1]))

		# --- Define a cor inicial das tarefas --- #
		self.cor_tarefa = (1, 1, 1, .3)


	# --- Adiciona uma Tarefa --- #
	def adicionar_tarefa(self, texto):

		self.ids.boxtarefas.add_widget(Tarefas(texto, self.cor_tarefa))
		self.ids.texto.text = ''  # --- Inicia o text input vazio --- #
		listatarefas.append([texto, self.cor_tarefa])

		savedata()


# ----- Wid Tarefa ----- #
class Tarefas(FloatLayout):
	def __init__(self, texto, cor):
		super().__init__()

		# --- Variaveis texto e cor inicial da tarefa --- #
		self.texto = texto
		self.cor = tuple(cor)

		# --- Cores das tarefas --- #
		self.canvascolor = self.cor # --- cor da tarefa --- #
		self.ids.btn_cor.canvascolor = self.cor  # --- cor do botão da tarefa --- #

		# --- Variaveis das possiveis cores das tarefas ---#
		self.normal = (1, 1, 1, .3)
		self.azul = (0, 0, 1, 1)
		self.vermelho = (1, 0, 0, 1)
		self.verde = (0, 1, 0, 1)
		self.amarelo = (1, 1, 0, 1)

		# --- Texto da tarefas --- #
		self.ids.tarefa.text = self.texto


	# --- Alteração das cores da tarefa ao pressionar o botão cor --- #
	def cortarefa(self):		
	
		if self.cor == (1, 1, 1, .3):
			self.cor = self.vermelho
		elif self.cor == self.vermelho:
			self.cor = self.verde
		elif self.cor == self.verde:
			self.cor = self.amarelo
		elif self.cor == self.amarelo:
			self.cor = self.normal

		# --- Cores das tarefas --- #
		self.ids.btn_cor.canvascolor = self.cor
		self.canvascolor = self.cor

		# --- Salva as cores das tarefas --- #
		salvar_cor_tarefa(self.texto, self.cor)


	# --- Remove Tarefa da lista de Tarefas--- #
	def remover_tarefa(self, texto):

		remover_tarefa(texto)


# ----- Classe App ----- #
class Main(App):

	def build(self):
		self.title = 'Tarefas'
		self.icon = 'Images/Logo.ico'

		return Principal()


# ----- Inicia Aplicação ----- #
if __name__ == '__main__':
	Main().run()

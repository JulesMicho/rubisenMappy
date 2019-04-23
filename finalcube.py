import os
import time
import threading
import pygame
from pygame.locals import *
import asyncio
from bleak import BleakClient
from bleak import discover
from pynput.keyboard import Key, Controller, Listener
from functools import partial





keyboard = Controller()
pygame.init()

delay = 0.05
delay2 = 0.15
posImg = 700
posText = 775

flagConnectionDevice = 0

MODEL_NBR_UUID = "0000aadc-0000-1000-8000-00805f9b34fb"


# tableau des mouvements du cube, et des touches à simuler correspondantes
moves = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]
keys = ["space", "left", "right", "space", "left", "right", "space", "left", "right", "space", "left", "right"]

surfaceW = 1300
surfaceH= 700
toucheW = 50
toucheH = 50



pygame.display.set_caption("Driver Rubisen")
clickable_areas, rect_surf, firstClickAreas, firstRectSurf , resetImg, img, imgSelect= [],[],[],[],[] ,[] ,[] 

fond,cache,Bnon,Boui ,preset1 ,preset2 ,load1,load2,save1,save2,contactImg, fenetre, font,address = "","","","","","","","","","","","","",""





def imageDeclarationImport(): # load des images pour l'affichage de l'interface
	global img
	global imgSelect
	global resetImg
	global fond,cache,Bnon,Boui ,preset1 ,preset2 ,load1,load2,save1,save2,contactImg, fenetre, font


	font = pygame.font.SysFont("comicsansms", 24)
	fenetre = pygame.display.set_mode((surfaceW, surfaceW), RESIZABLE)
	

	pygame.display.set_caption("Driver Rubisen")

	fond = pygame.image.load("img/Dapper.png").convert()
	cache = pygame.image.load("img/Dapper1.png").convert()
	Bnon = pygame.image.load("img/Bnon.png").convert_alpha()
	Boui = pygame.image.load("img/Boui.png").convert_alpha()
	preset1 = pygame.image.load("img/preset1.png").convert()
	preset2 = pygame.image.load("img/preset2.png").convert()
	load1 = pygame.image.load("img/load1.png").convert()
	load2 = pygame.image.load("img/load2.png").convert()
	save1 = pygame.image.load("img/save1.png").convert()
	save2 = pygame.image.load("img/save2.png").convert()
	contactImg = pygame.image.load("img/contactImg.png").convert()






	for i in range (0, 17):
		resetImg.append(pygame.image.load("img/res" + str(i + 1) + ".png").convert())
	imgB = pygame.image.load("img/B.png").convert_alpha()
	imgBI = pygame.image.load("img/B'.png").convert_alpha()
	imgD = pygame.image.load("img/D.png").convert_alpha()
	imgDI = pygame.image.load("img/D'.png").convert_alpha()
	imgF = pygame.image.load("img/F.png").convert_alpha()
	imgFI = pygame.image.load("img/F'.png").convert_alpha()
	imgL = pygame.image.load("img/L.png").convert_alpha()
	imgLI = pygame.image.load("img/L'.png").convert_alpha()
	imgR = pygame.image.load("img/R.png").convert_alpha()
	imgRI = pygame.image.load("img/R'.png").convert_alpha()
	imgU = pygame.image.load("img/U.png").convert_alpha()
	imgUI = pygame.image.load("img/U'.png").convert_alpha()
	imgBSelect = pygame.image.load("img/B1.png").convert_alpha()
	imgBISelect = pygame.image.load("img/B'1.png").convert_alpha()
	imgDSelect = pygame.image.load("img/D1.png").convert_alpha()
	imgDISelect = pygame.image.load("img/D'1.png").convert_alpha()
	imgFSelect = pygame.image.load("img/F1.png").convert_alpha()
	imgFISelect = pygame.image.load("img/F'1.png").convert_alpha()
	imgLSelect = pygame.image.load("img/L1.png").convert_alpha()
	imgLISelect = pygame.image.load("img/L'1.png").convert_alpha()
	imgRSelect = pygame.image.load("img/R1.png").convert_alpha()
	imgRISelect = pygame.image.load("img/R'1.png").convert_alpha()
	imgUSelect = pygame.image.load("img/U1.png").convert_alpha()
	imgUISelect = pygame.image.load("img/U'1.png").convert_alpha()
	img = [imgU, imgUI, imgD, imgDI, imgF, imgFI, imgB, imgBI, imgL, imgLI, imgR, imgRI]
	imgSelect = [imgUSelect, imgUISelect, imgDSelect, imgDISelect, imgFSelect, imgFISelect, imgBSelect, imgBISelect, imgLSelect, imgLISelect, imgRSelect, imgRISelect]



def AffichageFenetreContactPygame(): #affiche une fenetre de contact
	fenetrea = pygame.display.set_mode((600, 300), RESIZABLE)
	contact = pygame.image.load("img/contact.png").convert()
	fenetre.blit(contact, (0,0))
	pygame.display.update()
	a = 0
	while a == 0:
		#await asyncio.sleep(0)
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP and event.button == 1:
				
				pygame.display.update()
				a = 1
				quit()


def lire(path): #fonction de lecture d'un fichier
	try:
		fichier  = open(path, "r")
		text  = fichier.readlines()
		fichier.close()
	except IOError:
		print("err ecrire")
		return 0
	for t in range(len(text)):
		text[t] = text[t][:-1]

	return text

def ecrire(pathplusNomfichier, text, modeOuverture ): #fonction écriture fichier
	try:
		fichier = open(pathplusNomfichier, modeOuverture)
		fichier.write(str(text) + '\n' )

		fichier.close()
	except IOError:
		print("err ecrire")
		return 0
	return 1

def enregistrer(filePath): #enregistre les combinaisons mouvements cube/ touches à simuler
	first = 1
	for i in keys:
		if first == 1:
			first=0
			ecrire(filePath,i,"w")
		else:
			ecrire(filePath,i,"a")
		

def loadenregistrer(filePath):#load les combinaisons mouvements cube/ touches à simuler

	global keys
	tempo=lire(filePath)
	if tempo != 0:
		reset()
		keys = tempo
		for i in range(0, 12):
			if i % 2 == 0:
				fenetre.blit(font.render(keys[i], 1, (0, 0, 0)), (posText, 50 * (i + 1)))
			if i % 2 == 1:
				fenetre.blit(font.render(keys[i], 1, (0, 0, 0)), (posText + 300, 50 * i))
	else:
		print("echec lecture save")



def reset():#reset les combinaisons mouvements cube/ touches à simuler
	global keys
	for i in range(0, 12):
		keys[i] = 0
		if i % 2 == 0:
			fenetre.blit(cache, (posText, 50 * (i + 1)))
		if i % 2 == 1:
			fenetre.blit(cache, (posText + 300, 50 * i))

def initFirstClickAreas(tabDevices): #déclare les zones cliquables pour PyGame pour la fenetre de connexion d'un device 
	for i in range(len(tabDevices)):
		firstClickAreas.append(pygame.Rect((550, 25 * (i+1)), (200, 50)))
		firstRectSurf.append(pygame.Surface(firstClickAreas[i].size))


def initclickable_areas(): #déclare les zones cliquables pour PyGame pour la fenetre des combinaisons mouvements cube/ touches à simuler
	for i in range(0, 20):
		if i % 2 == 1 and i <= 13:
			clickable_areas.append(pygame.Rect((600, 50 * i - 5), (200, 55)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i % 2 == 0 and i <= 13:
			clickable_areas.append(pygame.Rect((600 + 300, 50 * (i - 1) - 5), (200, 55)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 14:
			clickable_areas.append(pygame.Rect((1200, 200), (50, 50)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 15:
			clickable_areas.append(pygame.Rect((1175, 400), (50, 18)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 16:
			clickable_areas.append(pygame.Rect((1225, 400), (50, 18)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 17:
			clickable_areas.append(pygame.Rect((1175, 525), (50, 18)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 18:
			clickable_areas.append(pygame.Rect((1225, 525), (50, 18)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))
		if i == 19:
			clickable_areas.append(pygame.Rect((1200, 625), (50, 50)))
			rect_surf.append(pygame.Surface(clickable_areas[i].size))






def press(indexKeyPressed): #simule la touche qui correspond au mouvement du cube
	if len(keys[indexKeyPressed]) == 1:
		keyboard.press(keys[indexKeyPressed])
		time.sleep(delay)
		keyboard.release(keys[indexKeyPressed])
	else:
		if keys[indexKeyPressed] == "space":

			keyboard.press(Key.space)
			keyboard.release(Key.space)
		if keys[indexKeyPressed] == "alt":
			keyboard.press(Key.alt)
			keyboard.release(Key.alt)
		if keys[indexKeyPressed] == "shift":
			keyboard.press(Key.shift)
			keyboard.release(Key.shift)
		if keys[indexKeyPressed] == "right":
			keyboard.press(Key.right)
			keyboard.release(Key.right)
		if keys[indexKeyPressed] == "pause":
			keyboard.press(Key.pause)
			keyboard.release(Key.pause)
		if keys[indexKeyPressed] == "left":
			keyboard.press(Key.left)
			keyboard.release(Key.left)
		if keys[indexKeyPressed] == "esc":
			keyboard.press(Key.esc)
			keyboard.release(Key.esc)
		if keys[indexKeyPressed] == "enter":
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)
		if keys[indexKeyPressed] == "down":
			keyboard.press(Key.down)
			keyboard.release(Key.down)
		if keys[indexKeyPressed] == "delete":
			keyboard.press(Key.delete)
			keyboard.release(Key.delete)
		if keys[indexKeyPressed] == "ctrl":
			keyboard.press(Key.ctrl)
			keyboard.release(Key.ctrl)
		if keys[indexKeyPressed] == "ctrl_r":
			keyboard.press(Key.ctrl_r)
			keyboard.release(Key.ctrl_r)
		if keys[indexKeyPressed] == "ctrl_l":
			keyboard.press(Key.ctrl_l)
			keyboard.release(Key.ctrl_l)
		if keys[indexKeyPressed] == "up":
			keyboard.press(Key.up)
			keyboard.release(Key.up)
		if keys[indexKeyPressed] == "f1":
			keyboard.press(Key.f1)
			keyboard.release(Key.f1)
		if keys[indexKeyPressed] == "f2":
			keyboard.press(Key.f2)
			keyboard.release(Key.f2)
		if keys[indexKeyPressed] == "f3":
			keyboard.press(Key.f3)
			keyboard.release(Key.f3)
		if keys[indexKeyPressed] == "f4":
			keyboard.press(Key.f4)
			keyboard.release(Key.f4)
		if keys[indexKeyPressed] == "f5":
			keyboard.press(Key.f5)
			keyboard.release(Key.f5)
		if keys[indexKeyPressed] == "f6":
			keyboard.press(Key.f6)
			keyboard.release(Key.f6)
		if keys[indexKeyPressed] == "f7":
			keyboard.press(Key.f7)
			keyboard.release(Key.f7)
		if keys[indexKeyPressed] == "f8":
			keyboard.press(Key.f8)
			keyboard.release(Key.f8)
		if keys[indexKeyPressed] == "f9":
			keyboard.press(Key.f9)
			keyboard.release(Key.f9)
		if keys[indexKeyPressed] == "f10":
			keyboard.press(Key.f10)
			keyboard.release(Key.f10)
		if keys[indexKeyPressed] == "f11":
			keyboard.press(Key.f11)
			keyboard.release(Key.f11)
		if keys[indexKeyPressed] == "f12":
			keyboard.press(Key.f12)
			keyboard.release(Key.f12)




class GiikerMove(): # class qui correspond à l'etat du cube
	def __init__(self, value):
		face = value // 16
		amount = value % 16

		self.face = ["?", "B", "D", "L", "U", "R", "F"][face]
		self.amount = [0, 1, 2, -1][amount]

	def __str__(self):
		return self.face + { 0: "0", 1: "", 2: "2", -1: "'" }[self.amount]



def change_handle(sender, data): #lorsque le cube change d'état, cette fonction est appelée
	movesC = list(map(GiikerMove, data[16:]))
	last_move = movesC[0]
	try:

		print("index", moves.index(last_move.__str__()))
		press(moves.index(last_move.__str__()))
	except:
		print("failed find index")



async def run(other, loop): #lance une connexion avec un device/cube
	
	global flagConnectionDevice
	while flagConnectionDevice != 1: # attendre que certaines conditions soient remplies pour lancer la connexion
		await asyncio.sleep(1)
	
	
	try :
		async with BleakClient(address, loop=loop) as client:
			value = await client.read_gatt_char(MODEL_NBR_UUID)



			print("len initial value : ", len(value))
			print("initial value : {0}".format("".join(map(chr, value))))
			recent_moves = list(map(GiikerMove, value[16:]))
			last_move = recent_moves[0]
			print(last_move)


			print("listening cube : ")
			fenetre.blit(pygame.transform.scale(Boui, (60, 90)), (1185, 20))
			await client.start_notify(MODEL_NBR_UUID, change_handle) # si la connexion fonctionne, la fonction change_handle sera lancée dès la réception de nouvelles informations venant du cube.
			while True:
				await asyncio.sleep(1)
				
	except:

		print("failed to connect")
		fenetre.blit(pygame.transform.scale(Bnon, (60, 90)), (1185, 20))





def AffichageDevicesPyGame(tabDevices): # affiche les devices détectés sur la fenetre
	fenetre.blit(pygame.transform.scale(cache, (surfaceW, surfaceW)), (0,0))
	if len(tabDevices) == 0:
		fenetre.blit(font.render("Aucun cube trouvé,", 1, (0, 0, 0)), (500, 300))
		fenetre.blit(font.render("vérifiez votre connexion Bluetooth.", 1, (0, 0, 0)), (500, 350))
	else:
		for i in range(len(tabDevices)):
			fenetre.blit(font.render(tabDevices[i][0] + " : " + tabDevices[i][1], 1, (0, 0, 0)), (525, 25 * (i+1)))
	pygame.display.update()
	initFirstClickAreas(tabDevices)


def AffichageMainFenetrePygame(moves, keys): # affiche des elements de la fenêtre principale
	x = 650
	y = 50


	fenetre.blit(fond, (0,0))
	fenetre.blit(pygame.transform.scale(resetImg[0], (50, 50)), (1200, 200))
	fenetre.blit(preset1, (1175,350))
	fenetre.blit(preset2, (1175,475))
	fenetre.blit(contactImg, (1200,625))

	for val in range (len(moves)):
		if val % 2 == 0:
			fenetre.blit(pygame.transform.scale(imgSelect[val], (50, 50)), (posImg, 50 * (val + 1) - 5))
			fenetre.blit(font.render(moves[val], 1, (0, 0, 0)),(x, y))
			fenetre.blit(font.render(keys[val], 1, (0, 0, 0)),(posText, y))
		if val % 2 == 1:
			fenetre.blit(pygame.transform.scale(imgSelect[val], (50, 50)), (posImg + 300, 50 * val - 5))
			fenetre.blit(font.render(moves[val], 1, (0, 0, 0)),(x + 300, y - 50))
			fenetre.blit(font.render(keys[val], 1, (0, 0, 0)),(posText + 300, y - 50))
		y = y + 50
	




def on_press(index,key):  # fonction qui gère l'assignation d'une touche à un mouvement du cube.
	keypressed = '{0}'.format(key)
	
	if len(keypressed) - 2 == 1:
		keypressed = keypressed.replace("\'",'')
		keys[index - 1] = keypressed
		if (index) % 2 == 1:
			fenetre.blit(font.render(keypressed, 1, (0, 0, 0)), (posText, 50 * (index)))
			
		if (index) % 2 == 0:
			fenetre.blit(font.render(keypressed, 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
		

	else:
		if  "Key." in keypressed:
			keypressed = keypressed.replace("Key.",'')
			#
			

			if "delete" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("delete", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "delete"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("delete", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "delete"
				quit = 0
			if "tab" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("tab", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "tab"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("tab", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "tab"
				quit = 0
			if "enter" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("enter", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "enter"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("enter", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "enter"
				quit = 0
			if "esc" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("esc", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "esc"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("esc", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "esc"
				quit = 0
			if "space" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("space", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "space"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("space", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "space"
				quit = 0


			if "up" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("up", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "up"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("up", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "up"
				quit = 0
			if "down" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("down", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "down"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("down", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "down"
				quit = 0
			if "right" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("right", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "right"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("right", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "right"
				quit = 0
			if "left" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("left", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "left"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("left", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "left"
				quit = 0
			if "f1" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f1", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f1"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f1", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f1"
				quit = 0
			if "f2" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f2", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f2"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f2", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f2"
				quit = 0
			if "f3" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f3", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f3"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f3", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f3"
				quit = 0
			if "f4" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f4", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f4"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f4", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f4"
				quit = 0
			if "f5" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f5", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f5"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f5", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f5"
				quit = 0
			if "f6" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f6", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f6"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f6", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f6"
				quit = 0
			if "f7" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f7", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f7"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f7", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f7"
				quit = 0
			if "f8" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f8", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f8"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f8", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f8"
				quit = 0
			if "f9" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f9", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f9"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f9", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f9"
				quit = 0
			if "f10" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f10", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f10"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f10", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f10"
				quit = 0
			if "f11" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f11", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f11"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f11", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f11"
				quit = 0
			if "f12" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("f12", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "f12"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("f12", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "f12"
				quit = 0
			if "shift" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("shift", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "shift"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("shift", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "shift"
				quit = 0
			if "shift_l" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("shift_l", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "shift_l"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("shift_l", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "shift_l"
				quit = 0
			if "ctrl_r" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("ctrl_r", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "ctrl_r"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("ctrl_r", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "ctrl_r"
				quit = 0
			if "ctrl_l" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("ctrl_l", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "ctrl_l"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("ctrl", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "ctrl_l"
				quit = 0
			if "alt_gr" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(cache, (posImg, 50 * index - 5))
					fenetre.blit(font.render("alt_gr", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "alt_gr"
				if (index - 1) % 2 == 1:
					fenetre.blit(cache, (posImg + 300, 50 * index - 5))
					fenetre.blit(font.render("alt_gr", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "alt_gr"
				quit = 0
			if "alt_l" == keypressed:
				if (index - 1) % 2 == 0:
					fenetre.blit(font.render("alt_l", 1, (0, 0, 0)), (posText, 50 * index))
					keys[index - 1] = "alt_l"
				if (index - 1) % 2 == 1:
					fenetre.blit(font.render("alt_l", 1, (0, 0, 0)), (posText + 300, 50 * (index - 1)))
					keys[index - 1] = "alt_l"
				quit = 0




		else:
			print("invalid key")
	enregistrer("save/currentsave.txt")
	print("key added")
	print(keys)
	return False




def on_release(key):
	pass



def HandleEventTouchePression(index, keys): # gère l'evenement de pression d'une touche clavier

	e = partial(on_press,index)
	with Listener(on_press=e, on_release=on_release) as listener:
		listener.join()


# asyncr

async def EventDeviceDiscoverClickPyGame(tabDevices):# gère l'événement de clique de l'utilisateur pour sélectionner une device
	global address
	a = 0
	while a == 0:
		levent = pygame.event.get()
		if len(levent) == 0:
			await asyncio.sleep(0.1)
		else:
			for event in levent:
				if event.type == QUIT:
					asyncio.get_event_loop().stop()
					return False
				if event.type == MOUSEBUTTONUP and event.button == 1: # 1= clique gauche
					for element in range (len(firstClickAreas)):
						if firstClickAreas[element].collidepoint(event.pos):
							if element < (len(firstClickAreas)):
								
								print(element)
								address = tabDevices[element][1][0:-1]
								a = 1

async def HandleEventMainPyGame(): # gère la detection d'évenements de type clique sur le Fenêtre principale.
	while 1:
		levent = pygame.event.get()
		if len(levent) == 0:
			await asyncio.sleep(0.1)
		else:
			for event in levent:
				if event.type == QUIT:
					asyncio.get_event_loop().stop()
					return False
				if event.type == MOUSEBUTTONUP and event.button == 1: # 1= clique gauche
					for element in range (len(clickable_areas)):
						if clickable_areas[element].collidepoint(event.pos):
							if (element - 1) % 2 == 0 and element <= 13:
								fenetre.blit(cache, (posImg, 50 * element - 5))
								fenetre.blit(cache, (posText, 50 * element - 5))
								pygame.display.update()
								fenetre.blit(pygame.transform.scale(img[element - 1], (50, 50)), (posImg, 50 * element - 5))
								pygame.display.update()
								print("click : " + str(element))
								HandleEventTouchePression(element, keys)
								fenetre.blit(cache, (posImg - 25, 50 * element - 5))
								fenetre.blit(pygame.transform.scale(imgSelect[element - 1], (50, 50)), (posImg, 50 * element - 5))
							if (element - 1) % 2 == 1 and element <= 13:
								fenetre.blit(cache, (posImg + 300, 50 * (element - 1) - 5))
								fenetre.blit(cache, (posText + 300, 50 * (element - 1) - 5))
								pygame.display.update()
								fenetre.blit(pygame.transform.scale(img[element - 1], (50, 50)), (posImg + 300, 50 * (element - 1) - 5))
								pygame.display.update()
								print("click : " + str(element))
								HandleEventTouchePression(element, keys)
								fenetre.blit(cache, (posImg + 275, 50 * (element - 1) - 5))
								fenetre.blit(pygame.transform.scale(imgSelect[element - 1], (50, 50)), (posImg + 300, 50 * (element - 1) - 5))
							if element == 14:
								reset()
								for i in range(2 * len(resetImg)):
									fenetre.blit(pygame.transform.scale(resetImg[i % len(resetImg)], (50, 50)), (1200, 200))
									pygame.display.update()
									time.sleep(0.5/36)
								fenetre.blit(pygame.transform.scale(resetImg[0], (50, 50)), (1200, 200))
								pygame.display.update()
							if element >= 15 and element <= 18:
								
								if (element - 14) % 2 == 0:
									if (element - 14) == 2:
										fenetre.blit(load1, (1175,350))
										pygame.display.update()
										time.sleep(delay2)
										fenetre.blit(preset1, (1175,350))
										
										loadenregistrer("save/save1.txt")
									if (element - 14) == 4:
										fenetre.blit(load2, (1175,475))
										pygame.display.update()
										time.sleep(delay2)
										fenetre.blit(preset2, (1175,475))
										loadenregistrer("save/save2.txt")
								else:
									if (element - 14) == 1:
										fenetre.blit(save1, (1175,350))
										pygame.display.update()
										time.sleep(delay2)
										fenetre.blit(preset1, (1175,350))
										enregistrer("save/save1.txt")
									if (element - 14) == 3:
										fenetre.blit(save2, (1175,475))
										pygame.display.update()
										time.sleep(delay2)
										fenetre.blit(preset2, (1175,475))
										enregistrer("save/save2.txt")
							if element == 19:
								AffichageFenetreContactPygame()
				pygame.display.update()




async def main():
	global flagConnectionDevice
	
	
	imageDeclarationImport() # déclare des variables globales pour l'affichage

	loadenregistrer("save/currentsave.txt") #load les mouvements récents

	devices = await discover() # découvre les devices bluetooth
	tabDevices = []
	for d in devices:
		tempo = (d.__str__().split(" "))
		if tempo[1][0:2] == "Gi":
			tabDevices.append((tempo[1],tempo[0]) )
	
	AffichageDevicesPyGame(tabDevices) # afficher les devices détectés pour que l'utilisateur en selectionne un
	await EventDeviceDiscoverClickPyGame(tabDevices) # utilisaeur clique sur un device affiché

	flagConnectionDevice = 1 #pour libérer la connexion au cube

	AffichageMainFenetrePygame(moves, keys) #affiche les combinaisons du cube sur l'écran
	initclickable_areas()
	#******************************************************
	await HandleEventMainPyGame()
	return True


##############################################################""

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(run(address, loop), main()))
					# lance la connexion et l'affichage en asynchrone


quit()

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import ctypes
import requests
import atexit
import subprocess
import enet
evtNone=0
evtConnect=1
evtRecv=2
evtDisconnect=3
import pickle
import pyperclip
import wx
import sound_lib
from sound_lib import stream, output
from threading import Thread
from accessible_output2 import outputs
from copy import copy
screenReader=outputs.auto.Auto()
import pygame
output=output.Output()
cachedFiles={}
isWindowActive=False
isGameWindowActive=isWindowActive
keepResponding=True
from pygame.locals import *
app=wx.App()
pygame.init()
screen=pygame.display.set_mode()
pygame.display.set_caption("python BGT window")
keysDown=pygame.key.get_pressed()
oldKeys=copy(keysDown)
pgClock=pygame.time.Clock()
class NetworkError(Exception):
	def __init__(self, reason):
		self.reason=reason
	def __str__(self):
		return self.reason
def exit():
	os._exit(1)
atexit.register(exit)
def fileExists(fileName):
	return os.path.isfile(fileName)
def dirCreate(dirName):
	os.mkdir(dirName)
def dirExists(dirName):
	return os.path.isdir(dirName)
def showWindow(windowName):
	pygame.display.set_caption(windowName)
def question(title, message):
	dial=wx.MessageDialog(None, message, title, wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
	answer=dial.ShowModal()
	dial.Destroy()
	if answer==wx.ID_YES: return 1
	elif answer==wx.ID_NO: return 2
	elif answer==wx.ID_CANCEL: return 3
	else: return 0
def inputBox(title, message, defaultValue=""):
	textTyped=wx.GetTextFromUser(message, title, default_value=defaultValue)
	return textTyped
def alert(title, message, infoSound=True):
	if infoSound:
		wx.MessageBox(message, title, wx.OK|wx.ICON_INFORMATION)
	else:
		wx.MessageBox(message, title, wx.OK|wx.ICON_NONE)
def hideWindow():
	pygame.display.set_mode(flags=HIDDEN)
def backWindow():
	pygame.display.set_mode()
showGameWindow=showWindow
hideGameWindow=hideWindow
backGameWindow=backWindow
def run(program, args=None, wait=True, background=True):
	p=subprocess.Popen(program, args, shell=background==False)
	if wait: p.wait()
def isAdmin():
	try:
		is_admin=os.getuid()==0
	except AttributeError:
		is_admin=ctypes.windll.shell32.IsUserAnAdmin()!=0
	return is_admin
class timer:
	def __init__(self, paused=True):#paused by default
		self.paused=paused
		self.pausedTime=0
		if self.paused==False: self.start()
	def start(self):
		self.paused=False
		self.pausedTime=0
		self.initialTime=pygame.time.get_ticks()
	@property
	def time(self):
		if self.paused: return self.pausedTime
		return self.pausedTime+pygame.time.get_ticks()-self.initialTime
	elapsed=time
	def pause(self):
		self.pausedTime=self.time
		self.paused=True
	def resume(self):
		self.initialTime=pygame.time.get_ticks()
		self.paused=False
class vector:
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x=x; self.y=y; self.z=z

class networkEvent:
	def __init__(self, type, peerId=0, channel=0, message=""):
		self.type=type
		self.peerId=peerId
		self.channel=channel
		self.message=message

class network:
	def __init__(self):
		self.type=None
		self.active=False
	def setupServer(self, port, channelLimit=0, maxPeers=100):
		try:
			self.host=enet.Host(enet.Address(b"localhost", port), maxPeers, channelLimit, 0, 0)
		except MemoryError:
			raise NetworkError("A server is already hosted on that port!")
		self.type="server"
		self.active=True
	def setupClient(self, channelLimit=0, maxPeers=1):
		self.host=enet.Host(None, maxPeers, channelLimit, 0, 0)
		self.active=True
		self.type="client"
	def connect(self, host, port, channels=0):
		peer=self.host.connect(enet.Address(host.encode("ASCII"), port), channels)
		return peer.outgoingPeerID
	def sendUnreliable(self, peerId, message, channel=0):
		for peer in self.host.peers:
			if self.type=="server":
				if peer.incomingPeerID==peerId:
					peer.send(channel, enet.Packet(message.encode("ASCII")))
			elif self.type=="client":
				if peer.outgoingPeerID==peerId:
					peer.send(channel, enet.Packet(message.encode("ASCII")))
	def sendReliable(self, peerId, message, channel=0):
		for peer in self.host.peers:
			if self.type=="server":
				if peer.incomingPeerID==peerId:
					peer.send(channel, enet.Packet(message.encode("ASCII"), flags=enet.PACKET_FLAG_RELIABLE))
			elif self.type=="client":
				if peer.outgoingPeerID==peerId:
					peer.send(channel, enet.Packet(message.encode("ASCII"), flags=enet.PACKET_FLAG_RELIABLE))
	def getPeerList(self):
		peerList=[]
		for peer in self.host.peers:
			if peer.state==enet.PEER_STATE_DISCONNECTED:
				continue
			if self.type=="client":
				peerList.append(peer.outgoingPeerID)
			elif self.type=="server":
				peerList.append(peer.incomingPeerID)
		return peerList
	def getPing(self, peerId):
		for peer in self.host.peers:
			if self.type=="client":
				if peer.outgoingPeerID==peerId:
					return peer.roundTripTime
			elif self.type=="server":
				if peer.incomingPeerID==peerId:
					return peer.roundTripTime
	def setBandwidthLimits(self, incomingBandwidth, outgoingBandwidth):
		self.host.incomingBandwidth=incomingBandwidth; self.host.outgoingBandwidth=outgoingBandwidth
	@property
	def bytesSent(self):
		return self.host.totalSentData
	@property
	def bytesReceived(self):
		return self.host.totalReceivedData
	@property
	def connectedPeers(self):
		peerCount=0
		for peer in self.host.peers:
			if not peer.state==enet.PEER_STATE_CONNECTED:
				continue
			peerCount+=1
		return peerCount
	def disconnectPeer(self, peerId):
		for peer in self.host.peers:
			if self.type=="client":
				if peerId==peer.outgoingPeerID:
					peer.disconnect()
			elif self.type=="server":
				if peerId==peer.incomingPeerID:
					peer.disconnect()
	def disconnectPeerSoftly(self, peerId):
		for peer in self.host.peers:
			if self.type=="client":
				if peerId==peer.outgoingPeerID:
					peer.disconnect_later()
			elif self.type=="server":
				if peerId==peer.incomingPeerID:
					peer.disconnect_later()
	def disconnectPeerForcefully(self, peerId):
		for peer in self.host.peers:
			if self.type=="client":
				if peerId==peer.outgoingPeerID:
					peer.disconnect_now()
			elif self.type=="server":
				if peerId==peer.incomingPeerID:
					peer.disconnect_now()
	def destroy(self):
		for peer in self.host.peers:
			peer.disconnect_now()
		self.host=None

	def getPeerAddress(self, peerId):
		for peer in self.host.peers:
			if self.type=="client":
				if peerId==peer.outgoingPeerID:
					return peer.address.host
			elif self.type=="server":
				if peerId==peer.incomingPeerID:
					return peer.address.host
	def request(self):
		evt=self.host.service(0)
		if evt.type==enet.EVENT_TYPE_NONE:
			return networkEvent(evtNone)
		elif evt.type==enet.EVENT_TYPE_CONNECT:
			if self.type=="client": return networkEvent(evtConnect, evt.peer.outgoingPeerID)
			elif self.type=="server": return networkEvent(evtConnect, evt.peer.incomingPeerID)
		elif evt.type==enet.EVENT_TYPE_RECEIVE:
			return networkEvent(evtRecv, evt.peer.outgoingPeerID, evt.channelID, evt.packet.data.decode("ASCII"))
		elif evt.type==enet.EVENT_TYPE_DISCONNECT:
			if self.type=="client": return networkEvent(evtDisconnect, evt.peer.outgoingPeerID)
			elif self.type=="server": return networkEvent(evtDisconnect, evt.peer.incomingPeerID)
		else:
			return -1

class sound:
	def __init__(self):
		self.handle=None
		self.freq=44100
		self.paused=False
	def load(self, fileName):
		if self.handle:
			self.close()
		if not fileName in cachedFiles:
			file=open(fileName, "rb")
			fileContent=file.read()
			cachedFiles[fileName]=fileContent
		self.handle=stream.FileStream(mem=True, file=cachedFiles[fileName], length=len(cachedFiles[fileName]))
		self.freq=self.handle.get_frequency()

	def stream(self, fileName):
		if self.handle:
			self.close()
		self.handle =stream.FileStream(file=fileName)
		self.freq=self.handle.get_frequency()

	def play(self):
		self.handle.looping=False
		self.handle.play()

	def pause(self):
		if self.paused: return
		if not self.playing: return
		self.handle.pause()
		self.paused=True

	def resume(self):
		if self.playing: return
		self.handle.play()
		self.paused=False

	def playLogo(self, skipKey=K_RETURN):
		self.skiped=False
		self.play()
		while self.playing:
			if keyPressed(skipKey):
				self.skiped=True
				self.stop()
			wait(5)

	def playWait(self, timeLeft=None, looping=False):
		self.handle.looping=looping
		self.play()
		if timeLeft:
			while self.playing and self.length-self.position>timeLeft: wait(5)
		else:
			while self.playing: wait(5)

	def playLooped(self):
		self.handle.looping=True
		self.handle.play()

	def stop(self):
		if self.handle and self.handle.is_playing:
			self.handle.stop()
			self.handle.set_position(0)

	def stopAndPlay(self):
		self.stop()
		self.play()

	def fadeOut(self, fadeTime):
		if self.handle and self.handle.is_playing:
			self.handle.slide_attribute("volume", 0, fadeTime//1000)

	def speakerTest(self, time=3000):
		if self.handle and self.handle.is_playing:
			self.pan=-100
			self.handle.slide_attribute("pan", 1, time//1000)
			while self.playing: wait(5)

	@property
	def active(self):
		return self.handle.is_active()

	@property
	def volume(self):
		if not self.handle:
			return False
		return round(math.log10(self.handle.volume)*20)
	@volume.setter
	def volume(self,value):
		if not self.handle:
			return False
		self.handle.set_volume(10**(float(value)/20))

	@property
	def pitch(self):
		if not self.handle:
			return False
		return (self.handle.get_frequency()/self.freq)*100

	@pitch.setter
	def pitch(self, value):
		if value>400: value=400
		if not self.handle:
			return False
		self.handle.set_frequency((float(value)/100)*self.freq)

	@property
	def position(self):
		return round(self.handle.bytes_to_seconds()*1000)

	@property
	def length(self):
		return round(self.handle.length_in_seconds()*1000)
	__len__=length

	@property
	def timeLeft(self):
		return self.length-self.position

	@property
	def pan(self):
		if not self.handle:
			return False
		return self.handle.get_pan()*100

	@pan.setter
	def pan(self, value):
		if not self.handle:
			return False
		self.handle.set_pan(float(value)/100)

	@property
	def playing(self):
		if self.handle is None:
			return False
		try:
			result=self.handle.is_playing
		except BassError:
			return False
		return result

	def close(self):
		if self.handle:
			self.handle.free()


def loadSound(fileName):
	s=sound()
	s.load(fileName)
	return s
def streamSound(fileName):
	s=sound()
	s.stream(fileName)
	return s
class gameMenu:
	def __init__(self, intro=None, introSound=None, wrap=False, escape=True, enterSound=None, clickSound=None, wrapSound=None, edgeSound=None, items=[]):
		self.intro=intro
		self.introSound=introSound
		self.wrap=wrap
		self.escape=escape
		self.enterSound=enterSound
		self.clickSound=clickSound
		self.wrapSound=wrapSound
		self.edgeSound=edgeSound
		self.items=items
	def show(self):
		self.selection=None
		self.currentSelection=1
		if self.enterSound:
			self.__enterObj=loadSound(self.enterSound)
		if self.clickSound:
			self.__clickObj=loadSound(self.clickSound)
		if self.wrapSound:
			self.__wrapObj=loadSound(self.wrapSound)
		if self.edgeSound:
			self.__edgeObj=loadSound(self.edgeSound)
		if self.introSound:
			self.__introSoundObj=loadSound(self.introSound)
			self.__introSoundObj.playLogo()
			self.__introSoundObj.close()
		if self.intro:
			out(self.intro)
		if os.path.isfile(self.items[0]):
			self.currentSound=loadSound(self.items[0])
			self.currentSound.play()
		else:
			out(self.items[0])
		while self.selection==None:
			if self.escape and keyPressed(K_ESCAPE):
				self.selection=0
			self.down=keyPressed(K_DOWN)
			self.up=keyPressed(K_UP)
			if self.down:
				if not self.currentSelection==len(self.items):
					self.currentSelection+=1
					if self.clickSound:
						self.__clickObj.stopAndPlay()
				else:
					if self.wrap:
						if self.wrapSound: self.__wrapObj.stopAndPlay()
						self.currentSelection=1
					else:
						if self.edgeSound: self.__edgeObj.stopAndPlay()
			if self.up:
				if not self.currentSelection==1:
					self.currentSelection-=1
					if self.clickSound:
						self.__clickObj.stopAndPlay()
				else:
					if self.wrap:
						if self.wrapSound: self.__wrapObj.stopAndPlay()
						self.currentSelection=len(self.items)
					else:
						if self.edgeSound: self.__edgeObj.stopAndPlay()
			if self.down or self.up:
				if hasattr(self, "currentSound") and self.currentSound.active:
					self.currentSound.close()
				if os.path.isfile(self.items[self.currentSelection-1]):
					self.currentSound=loadSound(self.items[self.currentSelection-1])
					self.currentSound.play()
				else:
					out(self.items[self.currentSelection-1], interrupt=True)
			if keyPressed(K_RETURN):
				self.selection=self.currentSelection
				self.selectionName=self.items[self.selection-1]
				if self.enterSound:
					self.__enterObj.play()
			if self.selection==0:
				self.selectionName=""
			wait(5)
	def add(self, *items):
		for item in items:
			self.items.append(item)
def keyPressed(keyCode):
	return keysDown[keyCode] and not oldKeys[keyCode]
def keyReleased(keyCode):
	return oldKeys[keyCode] and not keysDown[keyCode]
def keyDown(keyCode):
	return keysDown[keyCode]
def forceScreenReader(screenReaderName):
	global screenReader
	if screenReaderName=="nvda":
		screenReader=outputs.nvda.NVDA()
	elif screenReaderName=="jaws":
		screenReader=outputs.jaws.Jaws()
	elif screenReaderName=="window_eyes":
		screenReader=outputs.window_eyes.WindowEyes()
	elif screenReaderName=="system_access":
		screenReader=outputs.system_access.SystemAccess()
	elif screenReaderName=="sapi4":
		screenReader=outputs.sapi4.Sapi4()
	elif screenReaderName=="sapi5":
		screenReader=outputs.sapi5.SAPI5()
	else:
		screenReader=outputs.auto.Auto()
def updateScreenReader():
	global screenReader
	screenReader=outputs.auto.Auto()
def silence():
	outputs.nvda.NVDA().silence()
def speak(msg, interrupt=False):
	msg=str(msg)
	screenReader.speak(msg, interrupt=interrupt)
def out(msg, interrupt=False):
	msg=str(msg)
	if isinstance(screenReader, outputs.sapi5.SAPI5):
		speak(msg, interrupt=interrupt)
	else:
		screenReader.output(msg, interrupt=interrupt)
cbReadText=pyperclip.paste
cbCopyText=pyperclip.copy
clipboardCopyText=cbCopyText
clipboardReadText=cbReadText
def getFunc(url):
	global contentGet
	global geted
	contentGet=requests.get(url).content
	geted=True
def urlGet(url):
	global geted
	geted=False
	getThread=Thread(target=getFunc, args=(url,))
	getThread.daemon=True
	getThread.start()
	while not geted==True: wait(5)
	return contentGet
def serialize(dict, file):
	pickle.dump(dict, open(file, "wb"))
def deserialize(file):
	return pickle.load(open(file, "rb"))
def positionSound1d(sound, listenerX, sourceX, panStep=1, volumeStep=1):
	positionSoundCustom1d(sound, listenerX, sourceX, panStep=panStep, volumeStep=volumeStep, startPan=0.0, startVolume=0.0)
def positionSoundCustom1d(sound, listenerX, sourceX, panStep=1, volumeStep=1, startPan=0.0, startVolume=0.0):
	finalPan=startPan
	finalVolume=startVolume
	if sourceX<listenerX:
		delta=listenerX-sourceX
		finalPan-=delta*panStep
		finalVolume-=delta*volumeStep
	elif sourceX>listenerX:
		delta=sourceX-listenerX
		finalPan+=delta*panStep
		finalVolume-=delta*volumeStep
	if finalPan>100: finalPan=100
	elif finalPan<-100: finalPan=-100
	if finalVolume>100: finalVolume=100
	elif finalVolume<-100: finalVolume=-100
	if not sound.pan==finalPan:
		sound.pan=finalPan
	if not sound.volume==finalVolume:
		sound.volume=finalVolume
def positionSound2d(sound, listenerX, sourceX, listenerY, sourceY, panStep=1, volumeStep=1, pitchDecrease=5):
	positionSoundCustom2d(sound, listenerX, sourceX, listenerY, sourceY, panStep=panStep, volumeStep=volumeStep, pitchDecrease=pitchDecrease, startPan=0.0, startVolume=0.0, startPitch=100.0)
def positionSoundCustom2d(sound, listenerX, sourceX, listenerY, sourceY, panStep=1, volumeStep=1, pitchDecrease=5, startPan=0.0, startVolume=0.0, startPitch=100.0):
	finalPan=startPan
	finalVolume=startVolume
	finalPitch=startPitch
	if sourceX<listenerX:
		delta=listenerX-sourceX
		finalPan-=delta*panStep
		finalVolume-=delta*volumeStep
	elif sourceX>listenerX:
		delta=sourceX-listenerX
		finalPan+=delta*panStep
		finalVolume-=delta*volumeStep
	if sourceY>listenerY:
		finalPitch-=pitchDecrease
		deltaY=sourceY-listenerY
		finalVolume-=deltaY*volumeStep
	if finalPan>100: finalPan=100
	elif finalPan<-100: finalPan=-100
	if finalVolume>100: finalVolume=100
	elif finalVolume<-100: finalVolume=-100
	if finalPitch>400: finalPitch=400
	elif finalPitch<10: finalPitch=10
	if not sound.pan==finalPan:
		sound.pan=finalPan
	if not sound.volume==finalVolume:
		sound.volume=finalVolume
	if not sound.pitch==finalPitch:
		sound.pitch=finalPitch
def readEnvironmentVariable(name):
	return os.environ.get(name, "")
def waitKey(keyCode=K_RETURN):
	while not keyPressed(keyCode): wait(5)
def exHandler(type, ex, tb):
	line=str(tb.tb_lineno)
	exType=type.__name__
	exDescript=str(ex)
	alert("python BGT runtime error", "an error occurred on line "+line+". \n"+exType+": "+exDescript)
	exit()
sys.excepthook=exHandler

def wait(time=5):
	global keysDown
	global oldKeys
	global isWindowActive
	waitTimer=timer(paused=False)
	while waitTimer.elapsed<time:
		if keepResponding:
			pygame.display.update()
			pgClock.tick(60)
			for evt in pygame.event.get():
				if evt.type==pygame.QUIT:
					os._exit(1)
			oldKeys=copy(keysDown)
			keysDown=pygame.key.get_pressed()
		isWindowActive=pygame.display.get_active()
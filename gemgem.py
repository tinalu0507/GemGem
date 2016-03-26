#!/usr/bin/python
from Tkinter import *
import random

def run(rows, cols):

	root=Tk()
	global canvas
	global BLANK
	BLANK=""
	canvas=Canvas(root, width=cols*30+60, height=rows*30+60)
	canvas.pack()
	root.resizable(width=0, height=0)
	class Struct: pass
	canvas.data=Struct()
	canvas.data.rows=rows
	canvas.data.cols=cols
	init()
	root.bind("<ButtonPress-1>", leftMousePressed)
	root.bind("<Key>", keyPressed)
	drawGame()
	placePieces()
	if len(canvas.data.pieceschosen)==2:
		exchangepieces()

	canvas.data.score=0
	redrawAll()
	if canvas.data.isGameOver==False:
		timerFired()
	root.mainloop()

def init():
	#canvas.data.pause=False
	#canvas.data.instructions=False
	#img1=Image.open(gem1.png)
	emptyColor="black"
	canvas.data.emptyColor=emptyColor
	jewelPieceColors = [ "red", "magenta", "pink", "cyan", "green", "orange", "blue"]
	#canvas.data.tetrisPieces= tetrisPieces
	canvas.data.jewelPieceColors = jewelPieceColors

	global Pieces
	Pieces=[]
	for row in range(canvas.data.rows):
		Pieces.append([])
		for col in range(canvas.data.cols):
			Pieces[row].append(canvas.data.jewelPieceColors[random.randint(0, len(canvas.data.jewelPieceColors)-1)])
	canvas.data.Pieces=Pieces

	canvas.data.pieceschosen=[]
	canvas.data.score=0
	canvas.data.time=60
	canvas.data.isGameOver=False

	while clearpieces()==True:
		refillpieces()

	#newFallingPiece()

def drawGame():
 	canvas.create_rectangle(0, 0, canvas.data.cols*30+60, canvas.data.rows*30+60, fill="black")
 	drawBoard()
 	#drawFallingPiece()

def drawBoard():
 	for row in range(canvas.data.rows):
 		for col in range(canvas.data.cols):
 			drawCell(row, col, canvas.data.emptyColor)

def drawCell(row, col, color):
	canvas.create_rectangle(col*30+30 , row*30+30, col*30+60, row*30+60, fill=color, outline="DarkCyan", width=2)

def placePieces():
	for row in range(canvas.data.rows):
		for col in range(canvas.data.cols):
			drawPiece(row, col, Pieces[row][col])

def drawPiece(row ,col , color):
	canvas.create_oval(col*30+30+15-10, row*30+30+15-10, col*30+30+15+10, row*30+30+15+10, fill=color, outline=color)

def redrawAll():
	drawGame()
	placePieces()
	drawScore()
	drawtime()
	for piece in canvas.data.pieceschosen:
		drawhighlight(piece[0], piece[1])
	if canvas.data.isGameOver==True:
		drawisgameover()

def drawhighlight(row, col):
	canvas.create_rectangle(col*30+30 , row*30+30, col*30+60, row*30+60, fill=canvas.data.emptyColor, outline="Yellow", width=5)
	drawPiece(row, col, Pieces[row][col])

def drawScore():
	canvas.create_text(60, 20, text="Score:"+ str(canvas.data.score), fill="yellow", font="Ariel 16")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*30+40, text="press r to restart", fill="Yellow")

def drawtime():
	canvas.create_text(200, 20, text="Time:"+ str(canvas.data.time), fill="yellow", font="Ariel 16")

def drawisgameover():
	canvas.create_rectangle(0, 0, canvas.data.cols*30+60, canvas.data.rows*30+60, fill="black")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15, text="Game Over", fill="yellow", font="Ariel 20")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15+30, text="Your score is"+" "+str(canvas.data.score), fill="yellow", font="Ariel 16")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15+60, text="press r to restart", fill="yellow", font="Ariel 16")

def keyPressed(event):
	key = event.keysym
	if key=="r":
		init()
		if canvas.data.isGameOver==True:
			canvas.data.isGameOver=False
	redrawAll()

def findMatches():
	clearlist=[]
	length=0
	for row in range(canvas.data.rows):
		for col in range(1, canvas.data.cols):
			if Pieces[row][col]==Pieces[row][col-1]:
				length+=1
			if Pieces[row][col]!=Pieces[row][col-1]:
				if length>=2:
					match=[]
					for col in range(col-length-1, col):
						match.append((row,col))
					clearlist.append(match)
				length=0
			if col==canvas.data.cols-1:
				if length>=2:
					match=[]
					for col in range(col-length, col+1):
						match.append((row, col))
					clearlist.append(match)
				length=0

	for col in range(canvas.data.cols):
		for row in range(1, canvas.data.rows):
			if Pieces[row][col]==Pieces[row-1][col]:
				length+=1
			if Pieces[row][col]!=Pieces[row-1][col]:
				if length>=2:
					match=[]
					for row in range(row-length-1, row):
						match.append((row,col))
					clearlist.append(match)
				length=0
			if row==canvas.data.rows-1:
				if length>=2:
					match=[]
					for row in range(row-length, row+1):
						match.append((row, col))
					clearlist.append(match)
				length=0
	canvas.data.clearlist=clearlist
	if clearlist==[]:
		return False
	else:
		return True

def clearpieces():
	findMatches()
	if canvas.data.clearlist!=[]:
		for match in canvas.data.clearlist:
			canvas.data.score+=(len(match)-3+1)**2
			for position in match:
				row, col=position
				Pieces[row][col] = BLANK
		canvas.after(200, clearpieces)
		return True
	return False

def refillpieces():
	for row in range(canvas.data.rows):
		for col in range(canvas.data.cols-1):
			if Pieces[row][col]==BLANK:
				c=Pieces[row][col]
				Pieces[row][col]=Pieces[row][col+1]
				Pieces[row][col+1]=c
	for col in range(canvas.data.cols):
		for row in range(canvas.data.rows-1, 0, -1):
			if Pieces[row][col]==BLANK:
				c=Pieces[row][col]
				Pieces[row][col]=Pieces[row-1][col]
				Pieces[row-1][col]=c
	for row in range(canvas.data.rows):
		for col in range(canvas.data.cols):
			if Pieces[row][col]==BLANK:
				Pieces[row][col]=canvas.data.jewelPieceColors[random.randint(0, len(canvas.data.jewelPieceColors)-1)]

def leftMousePressed(event):
	if canvas.data.isGameOver==False: 
		row=int((event.y-30)/30)
		col=int((event.x-30)/30)
		if row in range(canvas.data.rows) and col in range(canvas.data.cols) and len(canvas.data.pieceschosen)<2:
			canvas.data.pieceschosen.append((row,col))
		exchangepieces()
		redrawAll()
		clearpieces()
    #canvas.after(500, redrawAll())
		refillpieces()
    #canvas.after(500, redrawAll())
		while clearpieces()==True:
			refillpieces()



def exchangepieces():
	if len(canvas.data.pieceschosen)==2:
		row1, col1=canvas.data.pieceschosen[0]
		row2, col2=canvas.data.pieceschosen[1]
		if (abs(row1-row2)==1 and col1==col2) or (abs(col1-col2)==1 and row1==row2):
			c=Pieces[row1][col1]
			Pieces[row1][col1]=Pieces[row2][col2]
			Pieces[row2][col2]=c
			if findMatches()==False:
				c=Pieces[row1][col1]
				Pieces[row1][col1]=Pieces[row2][col2]
				Pieces[row2][col2]=c
		canvas.data.pieceschosen=[]
	redrawAll()

def timerFired():
	if canvas.data.isGameOver==False:
		canvas.data.time-=1
	if canvas.data.time==0:
		canvas.data.isGameOver=True
	redrawAll()
	delay = 1000
	canvas.after(delay, timerFired)

run(8,8)
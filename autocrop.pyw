# Requires Python3, Pillow, Tkinter

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import io

# Where to stop, cropx, cropy, space
file = 0
padyval=5

def autocropit():
	# cropx.get() 				Width of crop square
	# cropy.get() 				Height of crop square
	# startx.get() 				The X Position to start
	# starty.get() 				The Y Position to start
	# space.get() 				The space between crops
	# room  					T/F: Whether or not to go until you run out of space
	# repeat.get() 				How many times to repeat the crop
	# direction.get() 			"Horizontally" "Vertically" or "Both"
	# file 						Returns path to file
	print(om.get())
	print("Loading file:  %s" % file)
	# Load the file
	original = Image.open(file)
	original.load()
	# Paranoia makes me define this first
	letsRepeat = 0

	if room.get() == "def":
		x = int(startx.get())
		loopsx = 0
		loopsy = 0
		if om.get() == "Horizontally" or direction.get() == "Both":
			while x < original.size[0]:
				loopsx += 1
				x += int(cropx.get()) + int(space.get())
			x = 0
			letsRepeat = loopsx
		if om.get() == "Vertically" or direction.get() == "Both":
			while x < original.size[1]:
				loopsy += 1
				x = x + int(cropx.get()) + int(space.get())
			letsRepeat = loopsy
		# Take the smaller of the two so as not to overflow
		if om.get() == "Both":
			if loopsx > loopsy:
				letsRepeat = loopsy
			else:
				letsRepeat = loopsx
	else:
		letsRepeat = repeat.get()
	
	print("Crop cycle will loop %s times" % letsRepeat)

	# Now that we've established how many times, let's actually do it
	locx = int(startx.get())
	locy = int(starty.get())
	counter = 0
	while (counter < int(letsRepeat)):
		counter = counter + 1
		try:
			copy = original.crop((locx,locy,locx+int(cropx.get()),locy+int(cropy.get()))).save("%s.png" % counter)
		except:
			print("It didn't work")
		if om.get() == "Horizontally":
			locx = locx + int(cropx.get()) + int(space.get())
		if om.get() == "Vertically":
			locy = locy + int(cropy.get()) + int(space.get())
		if om.get() == "Both":
			print("I have yet to incorporate this! Sorry!")

	messagebox.showinfo("All Set!","The image has been cropped to your specifications.")		

	return True

def clear_label_image():
	try:
		label.configure(image='')
		label2.configure(image='')
		label3.configure(image='')
		label.image=''
		label2.image=''
		label3.image=''
	except:
		print("Is a field set to null?")
def keyup(e):
	clear_label_image()
	try:
		genpreview()
	except:
		print("Something went wrong on the keyup handler")

main = Tk()
main.minsize(width=100,height=100)
main.title("AutoCrop")

options = Frame(main, padx=5, pady=5)

main.bind_all("<Key>", keyup)

# For when widgets need to be next to each other
firstRow = Frame(options)	# First
secondRow = Frame(options)
fourthRow = Frame(options)
sixthRow = Frame(options)

##
# First Row
##
Label(firstRow,text="I want to crop every ").pack(side=LEFT, pady=padyval)
cropx = Entry(firstRow, width=3)
cropx.insert(0,"64")
cropx.pack(side=LEFT, pady=padyval)
Label(firstRow,text="px by ").pack(side=LEFT, pady=padyval)
cropy = Entry(firstRow, width=3)
cropy.insert(0,"64")
cropy.pack(side=LEFT, pady=padyval)
Label(firstRow,text="px with a spacing of ").pack(side=LEFT, pady=padyval)
space = Entry(firstRow, width=3)
space.insert(0,"12")
space.pack(side=LEFT,pady=padyval)
Label(firstRow,text="px").pack(side=LEFT, pady=padyval)
firstRow.pack(anchor=W)

##
# Second Row
##
Label(secondRow,text="Start at ").pack(side=LEFT, pady=padyval)
startx = Entry(secondRow,width=4)
startx.insert(0,"0")
startx.pack(side=LEFT, pady=padyval)
Label(secondRow,text=" x ").pack(side=LEFT, pady=padyval)
starty = Entry(secondRow,width=4)
starty.insert(0,"0")
starty.pack(side=LEFT, pady=padyval)

secondRow.pack(anchor=W)

##
# Third/Fourth Row
##
room = StringVar()
room.set("def")
roomT = Radiobutton(fourthRow, text="Stop when I run out of room", variable=room, value="def")
roomF = Radiobutton(fourthRow, text="Crop exactly ", variable=room, value="cust")
roomT.select()
roomF.deselect()
roomT.pack()
roomF.pack(side=LEFT, pady=padyval)
repeat = Entry(fourthRow,width=3)
repeat.insert(0,"12")
repeat.pack(side=LEFT, pady=padyval)
Label(fourthRow,text=" times").pack(side=LEFT, pady=padyval)

fourthRow.pack(anchor=W)

##
# Direction
##
direction = StringVar(options)  # I need to double check that these do nothing
direction.set("Horizontally")   # But I don't have the time right now

directionset = ("Horizontally","Vertically","Both")
om = ttk.Combobox(options, values=directionset, state='readonly')
om.current(0)
om.pack(anchor=W,pady=padyval)

##
# Choose File
##
def askopenfile():
	global file
	file = askopenfilename(filetypes=(("PNG files","*.png"),("JPEG files","*.jpg"),("All files","*.*")))
	print(file)
	genpreview()

Button(sixthRow,text="Browse for File",command=askopenfile).pack()
sixthRow.pack(anchor=W,pady=padyval)

Button(options,text="AutoCrop It",command=autocropit).pack(anchor=W,pady=padyval)

##
# Image Preview
##
def genpreview():
	tryme = [startx.get(),starty.get(),cropx.get(),cropy.get()]
	for x in tryme:
		if int(x) is None:
			x = 0

	locx = int(startx.get())
	locy = int(starty.get())
	original = Image.open(file)
	original.load()
	
	pos1 = io.BytesIO()
	pos2 = io.BytesIO()
	pos3 = io.BytesIO()
	pos4 = io.BytesIO()

	copy =  original.crop((locx,
		locy,
		locx+int(cropx.get()),
		locy+int(cropy.get()))).save(pos1,format="PNG")

	spaceaddx = int(space.get()) + int(cropx.get())
	spaceaddy = int(space.get()) + int(cropy.get())

	copy2 = original.crop((locx+spaceaddx,					#locx+int(cropx.get())+int(space.get()),
			locy,
			locx+spaceaddx+int(cropx.get()),
			locy+int(cropy.get()))).save(pos2,format="PNG")

	copy3 = original.crop((locx,
		locy+spaceaddy,						#locy+int(cropx.get())+int(space.get()),
		locx+int(cropx.get()),
		locy+spaceaddy+int(cropy.get()))).save(pos3,format="PNG")

	# Not even gonna bother with copy4 rn
	
	pos1.seek(0)
	pos2.seek(0)
	pos3.seek(0)

	pos1 = Image.open(pos1)
	pos2 = Image.open(pos2)
	pos3 = Image.open(pos3)

	if om.get() == "Horizontally":
		pos3 = pos3.convert('LA')
	if om.get() == "Vertically":
		pos2 = pos2.convert('LA')

	prev = [ ImageTk.PhotoImage(pos1), ImageTk.PhotoImage(pos2), ImageTk.PhotoImage(pos3) ]

	xpos = 250
	ypos = 100

	global label, label2, label3, label4

	label = Label(options, image=prev[0])
	label.place(anchor=E, x=xpos, y=ypos)
	label.image = prev[0]
	label2 = Label(options, image=prev[1])
	label2.place(anchor=E, x=xpos+int(cropx.get())+int(space.get()), y=ypos)
	label2.image = prev[1]
	label3 = Label(options, image=prev[2])
	label3.place(anchor=E, x=xpos, y=ypos+int(cropy.get())+int(space.get()))
	label3.image = prev[2]

	label.configure(image=prev[0])
	label2.configure(image=prev[1])
	label3.configure(image=prev[2])

options.pack()
options.focus_set()
main.mainloop()

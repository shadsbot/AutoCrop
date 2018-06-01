from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, ttk 
import io 
from CropImage import Crop

main = Tk()
main.minsize(width=100,height=100)
main.title("AutoCrop Sprite Ripper")

mainframe = Frame(main, padx=5, pady=5)
verticalPadding = 5

cimage = Crop()

rows = [Frame(mainframe), Frame(mainframe), Frame(mainframe), Frame(mainframe)]

##
# First row
##
Label(rows[0],text="Crop every ").pack(side=LEFT,pady=verticalPadding)
cropx = Spinbox(rows[0], from_=0, to=9999, width=3)
cropx.delete(0,"end")
cropx.insert(0,"64")
cropx.pack(side=LEFT, pady=verticalPadding)

Label(rows[0],text="px by ").pack(side=LEFT, pady=verticalPadding)
cropy = Spinbox(rows[0], from_=0, to=9999, width=3)
cropy.delete(0,"end")
cropy.insert(0,"64")
cropy.pack(side=LEFT, pady=verticalPadding)

Label(rows[0],text="px with a spacing of ").pack(side=LEFT, pady=verticalPadding)
space = Spinbox(rows[0], from_=0, to=9999, width=3)
space.delete(0,"end")
space.insert(0,"12")
space.pack(side=LEFT, pady=verticalPadding)
Label(rows[0], text="px").pack(side=LEFT, pady=verticalPadding)
rows[0].pack(anchor=W)

##
# Second row
##
Label(rows[1], text="Start at ").pack(side=LEFT, pady=verticalPadding)
startx = Spinbox(rows[1], from_=0, to=9999, width=3)
startx.delete(0,"end")
startx.insert(0,"0")
startx.pack(side=LEFT, pady=verticalPadding)
Label(rows[1], text=" x ").pack(side=LEFT, pady=verticalPadding)
starty = Spinbox(rows[1], from_=0, to=9999, width=3)
starty.delete(0,"end")
starty.insert(0,"0")
starty.pack(side=LEFT, pady=verticalPadding)
rows[1].pack(anchor=W)

##
# Third row
##
custCrop = StringVar()
custCrop.set("False")
numCropsOpts = [Radiobutton(rows[2], text="Stop when I run out of room", variable=custCrop, value="False"),Radiobutton(rows[2], text="Crop exactly ", variable=custCrop, value="True")]
numCropsOpts[0].select()
numCropsOpts[1].deselect()
numCropsOpts[0].pack()
numCropsOpts[1].pack(side=LEFT, pady=verticalPadding)
repeat = Spinbox(rows[2], from_=0, to=9999, width=3)
repeat.delete(0,"end")
repeat.insert(0,"12")
repeat.pack(side=LEFT, pady=verticalPadding)
Label(rows[2], text=" times").pack(side=LEFT, pady=verticalPadding)
rows[2].pack(anchor=W)

dropdown = StringVar(mainframe)
directions = ("Horizontally →","Vertically ↓","Both ↴")

directionChoice = ttk.Combobox(mainframe, values=directions, textvariable=dropdown, state='readonly')
directionChoice.current(0)
directionChoice.pack(anchor=W, pady=verticalPadding)

def updatePreview():
	PILfile = cimage.generatePreview()
	canv.image = ImageTk.PhotoImage(PILfile)
	width,height = PILfile.size
	canv.config(scrollregion=(0,0,width,height))
	canv.itemconfig(imgtag, image = canv.image)

def askopenfile():
	global file
	file = askopenfilename(filetypes=(("PNG files","*.png"),("JPEG files","*.jpg"),("All files","*.*")))
	cimage.setImage(file)
	updatePreview()

Button(mainframe, text="Browse for File", command=askopenfile).pack(anchor=W,pady=verticalPadding,fill=X)

def go():
    cimage.crop()
    messagebox.showinfo("All Set!","The image has been cropped to your specifications.")
    return None

Button(mainframe,text="AutoCrop It",command=go).pack(anchor=W,pady=verticalPadding, fill=X)

canv = Canvas(mainframe, relief=SUNKEN)
canv.config(width=0, height=0)
scrollbarVertical = Scrollbar(canv, orient=VERTICAL)
scrollbarHorizontal = Scrollbar(canv, orient=HORIZONTAL)
scrollbarVertical.config(command=canv.yview)
scrollbarHorizontal.config(command=canv.xview)

canv.config(yscrollcommand=scrollbarVertical.set)
canv.config(xscrollcommand=scrollbarHorizontal.set)

scrollbarHorizontal.pack(side=BOTTOM, fill=X)
scrollbarVertical.pack(side=RIGHT, fill=Y)

canv.pack(side=LEFT, expand=YES, fill=BOTH, ipady=100)

tmpImage = Image.new('RGB',(160,60), color='silver')
tmpImagedraw = ImageDraw.Draw(tmpImage)
tmpImagedraw.text((10,10), "No image selected", fill=(0,0,0))
im = tmpImage
# im = Image.open("./example.png")
width,height = im.size
canv.config(scrollregion=(0,0,width,height))
im2 = ImageTk.PhotoImage(im)
imgtag = canv.create_image(0,0,anchor="nw",image=im2)

def keyup(self):
    cimage.setDirection(directionChoice.get())
    cimage.setPadding(int(space.get()))
    cimage.setUserCrops(custCrop.get(), int(repeat.get()))
    cimage.setSize( int(cropx.get()), int(cropy.get()) )
    cimage.setOffset( int(startx.get()), int(starty.get()) )
    updatePreview()

main.bind_all("<Key>", keyup)
main.bind_all("<Button-1>", keyup)

mainframe.pack()
mainframe.focus_set()
main.mainloop()
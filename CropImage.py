from PIL import Image, ImageTk, ImageDraw

class Crop:
	"""Object that contains the tools to manipulate a spritesheet"""

	def __init__(self, file="example.png", cropSize=[64,64], padding=0, offset=[0,0], direction="Both", numberCrops=0, useUserCrops=False):
		self.direction = direction
		self.offset = {"x" : offset[0], "y" : offset[1]}
		self.padding = padding
		self.cropSize = { "x" : cropSize[0], "y" : cropSize[1] }
		self.numberCrops = numberCrops
		self.useUserCrops = useUserCrops
		try:
			self.image = Image.open(file)
			self.image.load()
		except:
			self.image = Image.new('RGB',(160,60), color='red')
			self.imagedraw = ImageDraw.Draw(self.image)
			self.imagedraw.text((10,10), "No image selected", fill=(0,0,0))

	def setImage(self, file):
		try:
			self.image = Image.open(file)
			self.image.load()
		except:
			self.image = Image.new('RGB',(160,60), color='red')
			self.imagedraw = ImageDraw.Draw(self.image)
			self.imagedraw.text((10,10), "Image not found", fill=(0,0,0))

	def setDirection(self, direction):
		self.direction = direction[:-2]
	
	def setPadding(self, pad):
		self.padding = pad

	def setUserCrops(self, userCrops, number=0):
		if (userCrops == "True"):
			userCrops = True
		else:
			userCrops = False
		self.numberCrops = number
		self.useUserCrops = userCrops
	
	def setSize(self, x, y):
		self.cropSize = { "x" : x, "y" : y }
	
	def setOffset(self, x, y):
		self.offset = { "x" : x, "y" : y }
	
	def horizontalLoops(self):
		if self.useUserCrops:
			return self.numberCrops
		horizontalCrops = 0
		index = self.offset["x"]
		while (index < self.image.size[0]):
			index = index + self.cropSize["x"] + self.padding
			if (index <= self.image.size[0]):
				horizontalCrops = horizontalCrops + 1
		return horizontalCrops
	
	def verticalLoops(self):
		if self.useUserCrops:
			return self.numberCrops
		verticalCrops = 0
		index = self.offset["y"]
		while (index < self.image.size[1]):
			index = index + self.cropSize["y"] + self.padding
			if (index <= self.image.size[1]):
				verticalCrops = verticalCrops + 1
		return verticalCrops

	def crop(self):
		if self.direction == "Both":
			for x in range(0,self.verticalLoops()):
				currentYLoc = self.offset["y"] + ( x * (self.cropSize["y"]+self.padding) )
				row = str(x) + "-"
				self.cropHorizontally(currentYLoc,row)
		elif self.direction == "Vertically":
			self.cropVertically()
		elif self.direction == "Horizontally":
			self.cropHorizontally()
				
	def cropHorizontally(self, currentYLoc=0, name=""):
		if (currentYLoc == 0):
			currentYLoc = self.offset["y"]
		try:
			for x in range(0,self.horizontalLoops()):
				xposition = self.offset["x"] + (x * (self.cropSize["x"]+self.padding))
				copy = self.image.crop((xposition, currentYLoc, xposition + self.cropSize["x"], currentYLoc + self.cropSize["y"]))
				copy.save("%s%s.png" % (name,x))
			return True
		except:
			print("An error occured during the cropHorizontally routine.")
			return False
	def cropVertically(self):
		try:
			for x in range(0,self.verticalLoops()):
				yposition = self.offset["y"] + (x * (self.cropSize["y"]+self.padding))
				copy = self.image.crop((self.offset["x"], yposition, self.offset["x"] + self.cropSize["x"], yposition + self.cropSize["y"]))
				copy.save("%s.png" % x)
			return True
		except:
			print("An error occured during the cropVertically routine.")
			return False

	def generatePreview(self):
		try:
			copy = self.image.copy()
			tmp = ImageDraw.Draw(copy)
			if (self.direction == "Both"):
				for x in range(0,self.verticalLoops()):
					currentYLoc = self.offset["y"] + ( x * (self.cropSize["y"]+self.padding) )
					for y in range(0,self.horizontalLoops()):
						xposition = self.offset["x"] + (y * (self.cropSize["x"]+self.padding))
						tmp.rectangle( (xposition,currentYLoc,xposition+self.cropSize["x"],currentYLoc+self.cropSize["y"]), outline='red' )
			if (self.direction == "Horizontally"):
				for x in range(0,self.horizontalLoops()):
					xposition = self.offset["x"] + (x * (self.cropSize["x"]+self.padding))
					tmp.rectangle( (xposition,self.offset["y"],xposition+self.cropSize["x"],self.offset["y"]+self.cropSize["y"]), outline='red' )
			if (self.direction == "Vertically"):
				for x in range(0,self.verticalLoops()):
					currentYLoc = self.offset["y"] + ( x * (self.cropSize["y"]+self.padding) )
					xposition = self.offset["x"]
					tmp.rectangle( (xposition,currentYLoc,xposition+self.cropSize["x"],currentYLoc+self.cropSize["y"]), outline='red' )
			return copy
		except:
			return False

	def debug(self):
		print(self.direction)
		print(self.offset)
		print(self.padding)
		print(self.cropSize)
		print(self.numberCrops)
		print(self.useUserCrops)
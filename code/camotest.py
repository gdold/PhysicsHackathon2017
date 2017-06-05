from PIL import Image, ImageDraw
from IPython.display import display
from random import randint, random
import numpy as np
from colorthief import ColorThief


im = Image.open("tundra.jpg")

draw = ImageDraw.Draw(im)
#draw.line((0, 0) + im.size, fill=128)
#draw.line((0, im.size[1], im.size[0], 0), fill=128)
#del draw

# im.size[0] --> width
# im.size[1] --> height
# foreground boundaries:

# Currently manual inputs...randomise at some point?
xmin = 600
xmax = 700
ymin = 0
ymax = 100

if(xmax > ymax):
	scale = xmax
else:
	scale = ymax

# WARNING: THIS WILL NOT WORK IF FORGROUND SIZE = BG SIZE, NEEDS BUFFER !!
im2 = im.crop(
	(
	   xmin-20,
	   ymin-20,
	   xmax+20,
	   ymax+20
	)
)

im2.save("temp.png")

img = ColorThief("temp.png")
palette = img.get_palette(color_count=5)		

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result)) 
    return result

def add_poly(x,y,scale,colour):
	points = [(x,y)]
	ts = [t/100.0 for t in range(101)]
	xtemp = x
	ytemp = y

	polypoints = 2 # multiply by 3 for actual number of polygon points

	for i in range(0,polypoints):
		theta = (2*3.1415926536)/(3*polypoints)
#		xtemp1 = xtemp + int(randint(5,scale)*np.cos(i*theta))
#		ytemp1 = ytemp + int(randint(5,scale)*np.sin(i*theta))
		xtemp1 = xtemp + randint(-scale,scale)
		ytemp1 = ytemp + randint(-scale,scale)
		if(xtemp1 < xmin):
			xtemp1 = xmin
		elif(xtemp1 > xmax):
			xtemp1 = xmax
		if(ytemp1 < ymin):
			ytemp1 = ymin
		elif(ytemp1 > ymax):
			ytemp1 = ymax

#		xtemp2 = xtemp + int(randint(5,scale)*np.cos((i+1)*theta))
#		ytemp2 = ytemp + int(randint(5,scale)*np.sin((i+1)*theta))
		xtemp2 = xtemp + randint(-scale,scale)  
		ytemp2 = ytemp + randint(-scale,scale)  
        	if(xtemp2 < xmin):
                	xtemp2 = xmin 
        	elif(xtemp2 > xmax):
                	xtemp2 = xmax
        	if(ytemp2 < ymin):
                	ytemp2 = ymin
        	elif(ytemp2 > ymax):
                	ytemp2 = ymax

#		xtemp3 = xtemp + int(randint(5,scale)*np.cos((i+2)*theta))
#		ytemp3 = ytemp + int(randint(5,scale)*np.sin((i+2)*theta))
		xtemp3 = xtemp + randint(-scale,scale)  
		ytemp3 = ytemp + randint(-scale,scale)  
        	if(xtemp3 < xmin):
                	xtemp3 = xmin 
        	elif(xtemp3 > xmax):
                	xtemp3 = xmax
        	if(ytemp3 < ymin):
                	ytemp3 = ymin
        	elif(ytemp3 > ymax):
                	ytemp3 = ymax
		xys = [(xtemp1,ytemp1),(xtemp2,ytemp2),(xtemp3,ytemp3)]
		bezier = make_bezier(xys)
		points.extend(bezier(ts))
		draw.polygon(points, fill = colour)
		return None

def rot_ellipse(x,y,scale,colour):
	points = [(x,y)]
	ts = [t/100.0 for t in range(101)]
	xtemp = x
	ytemp = y
	pi = 3.1415926536
	theta = 2*pi*(randint(1,100))/100

	xtemp1 = xtemp + int(randint(5,scale)*np.cos(theta))
	ytemp1 = ytemp + int(randint(5,scale)*np.sin(theta))

	if(xtemp1 < xmin):
		xtemp1 = xmin
	elif(xtemp1 > xmax):
		xtemp1 = xmax
	if(ytemp1 < ymin):
		ytemp1 = ymin
	elif(ytemp1 > ymax):
		ytemp1 = ymax

	miniscale = int(scale/4)

	xtemp2 = xtemp + int(randint(5,scale)*np.cos(theta+(pi/2)))
	ytemp2 = ytemp + int(randint(5,scale)*np.sin(theta+(pi/2)))

       	if(xtemp2 < xmin):
               	xtemp2 = xmin 
       	elif(xtemp2 > xmax):
               	xtemp2 = xmax
       	if(ytemp2 < ymin):
               	ytemp2 = ymin
       	elif(ytemp2 > ymax):
               	ytemp2 = ymax

	xtemp3 = xtemp - int(randint(5,scale)*np.cos(theta))
	ytemp3 = ytemp - int(randint(5,scale)*np.sin(theta))

       	if(xtemp3 < xmin):
               	xtemp3 = xmin 
       	elif(xtemp3 > xmax):
               	xtemp3 = xmax
       	if(ytemp3 < ymin):
               	ytemp3 = ymin
       	elif(ytemp3 > ymax):
               	ytemp3 = ymax

	xtemp4 = xtemp - int(randint(5,scale)*np.cos(theta+(pi/2)))
	ytemp4 = ytemp - int(randint(5,scale)*np.sin(theta+(pi/2)))

       	if(xtemp4 < xmin):
               	xtemp4 = xmin 
       	elif(xtemp4 > xmax):
               	xtemp4 = xmax
       	if(ytemp4 < ymin):
               	ytemp4 = ymin
       	elif(ytemp4 > ymax):
               	ytemp4 = ymax

	xys = [(xtemp1,ytemp1),(xtemp2,ytemp2),(xtemp3,ytemp3),(xtemp4,ytemp4),(xtemp1+1,ytemp1+1)]
	bezier = make_bezier(xys)
	points.extend(bezier(ts))

	draw.polygon(points, fill = colour)
	return None


scale2 = scale/20
colour = palette[0]
colour2 = palette[1]
colour3 = palette[3]

for x in range(0,250):
	x1 = randint(xmin,xmax)
	y1 = randint(ymin,ymax)
	x2 = randint(xmin,xmax)
	y2 = randint(ymin,ymax)
	x3 = randint(xmin,xmax)
	y3 = randint(ymin,ymax)
#	add_poly(x1,y1,scale,colour)
#	add_poly(x2,y2,scale2,colour2)
#	add_poly(x3,y3,scale3,colour3)
#	draw.ellipse((x1,y1,x1+randint(0,scale2),y1+randint(0,scale2)),colour,colour)
#	draw.ellipse((x2,y2,x2+randint(0,scale2),y2+randint(0,scale2)),colour2,colour2)	
#	draw.ellipse((x3,y3,x3+randint(0,scale2),y3+randint(0,scale2)),colour3,colour3)
	rot_ellipse(x1,y1,scale2,colour)
	if(randint(1,2)>1):
		rot_ellipse(x2,y2,scale2,colour2)
	if(randint(1,4)>3):
		rot_ellipse(x3,y3,scale2,colour3)


#im.save('out.png')

im.show()

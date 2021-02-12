import argparse
import cv2
import pandas as pd
import numpy as np

# creating the command line interface for taking and parsing
# the arguments from the CLI itself
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# reading the image using openCV
img = cv2.imread(img_path)

# declaring the global variables
clicked = False
r = g = b = xpos = ypos = 0

# reading csv file with pandas and giving names to each column in the dataset
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#  defining the draw function
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# defining the function to get the colour value in R , G , B
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R-int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B-int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# create a window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while(1):
    cv2.imshow("image",img)
    if(clicked):
        # filling entire rectangle
        # cv2.rectangle(image , startpoint , endpoint , color , thickness) and -1 fills entire rectangle
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)
        # creating the displayed text string
        text=getColorName(r,g,b)+' R = '+str(r)+' G = '+str(g)+' B = '+str(b)
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        # for very light colours which are hard to see 
        # we display them in black text
        if(r+g+b>=600):
            cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
        
    # exiting the infinite loop when the user presses the Esc key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# destroying all the window objects which were created
cv2.destroyAllWindows()
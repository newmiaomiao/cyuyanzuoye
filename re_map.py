import time
from PIL import Image
import numpy as np
from naoqi import ALProxy

robert_ip = "10.4.122.64" 
Navigation = ALProxy("ALNavigation", robert_ip, 9559)
motion = ALProxy("ALMotion", robert_ip, 9559)
Navigation.stopLocalization()
path = "/home/nao/.local/share/Explorer/2014-04-04T014047.973Z.explo" #path of the map (previously made) - Paste your path here
Navigation.loadExploration(path) #loads the map
Final_map = Navigation.getMetricalMap()
data = Final_map[4] #gets the data of the map 
size = Final_map[1] #size of the map
size2 = Final_map[2] #size of the map
img = np.array(data).reshape(size, size2)
img = (100 - img) * 2.5   #shapes the image to fit the map
img = np.array(img, np.uint8)
NewMap = Image.frombuffer('L',  (size, size2), img, 'raw', 'L', 0, 1)
print("Step 6: Shows the map on the computer")
NewMap.show() #Shows the map on the computer


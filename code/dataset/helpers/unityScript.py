import pyautogui
import pyperclip
import time
import random

total = 56

noiseScale = "375"
baseFrequency = "9"
noO = "8"

for x in range(34, 50):
    #print("This iterations random number will be:")
    #setSeed = random.randint(100000,999999)
    #print(str(x))
    setSeed = x

    pyautogui.click(x=908, y=9)
    time.sleep(0.2)
    pyautogui.click(x=130, y=550)
    time.sleep(0.2)
    pyautogui.click(x=130, y=150)
    time.sleep(0.2)

    # develwidget 
    pyautogui.click(x=1418, y=329)
    time.sleep(0.2)
    # terraingenwidget
    pyautogui.click(x=1480, y=521)
    time.sleep(0.2)

    # change to colored
    pyautogui.click(x=1649, y=534)
    time.sleep(0.2)
    pyautogui.click(x=1669, y=585)
    time.sleep(0.2)

    # settings
    pyautogui.click(x=1665, y=562)
    time.sleep(0.2)
    pyautogui.typewrite(noiseScale)
    time.sleep(0.4)
    pyautogui.click(x=1661, y=581)
    time.sleep(0.2)
    pyautogui.typewrite(baseFrequency)
    time.sleep(0.4)
    pyautogui.click(x=1654, y=636)
    time.sleep(0.2)
    pyautogui.typewrite(noO)
    time.sleep(0.4)
    pyautogui.click(x=1661, y=658)
    time.sleep(0.2)
    pyautogui.typewrite(str(setSeed) + "tobe5")
    time.sleep(0.2)

    # apply noise par
    pyautogui.click(x=1622, y=781)
    time.sleep(0.5)
    # paint the terrain
    pyautogui.click(x=1632, y=760)
    time.sleep(0.5)
    # generate htm maps
    pyautogui.click(x=1630, y=433)
    time.sleep(7)

    # save biome map
    #change to terraindebugplain
    pyautogui.click(x=144, y=201)
    time.sleep(0.3)

    # change to All and generate texture
    pyautogui.click(x=1668, y=661)
    time.sleep(0.3)
    pyautogui.click(x=1649, y=742)
    time.sleep(0.3)
    pyautogui.click(x=1685, y=702)
    time.sleep(1)

#######################################################

    pyautogui.click(x=908, y=9)
    time.sleep(0.2)
    pyautogui.click(x=130, y=150)
    time.sleep(0.2)

    # develwidget 
    pyautogui.click(x=1418, y=329)
    time.sleep(0.2)
    # terraingenwidget
    pyautogui.click(x=1480, y=521)
    time.sleep(0.2)

    # change to colored
    pyautogui.click(x=1649, y=534)
    time.sleep(0.2)
    pyautogui.click(x=1669, y=565)
    time.sleep(0.2)

    # settings
    pyautogui.click(x=1665, y=562)
    time.sleep(0.2)
    pyautogui.typewrite(noiseScale)
    time.sleep(0.2)
    pyautogui.click(x=1661, y=581)
    time.sleep(0.2)
    pyautogui.typewrite(baseFrequency)
    time.sleep(0.2)
    pyautogui.click(x=1654, y=636)
    time.sleep(0.2)
    pyautogui.typewrite(noO)
    time.sleep(0.2)
    pyautogui.click(x=1661, y=658)
    time.sleep(0.2)
    pyautogui.typewrite(str(setSeed) + "tobe5")
    time.sleep(0.2)

    # apply noise par
    pyautogui.click(x=1622, y=781)
    time.sleep(0.5)
    # paint the terrain
    pyautogui.click(x=1632, y=760)
    time.sleep(0.5)
    # generate htm maps
    pyautogui.click(x=1630, y=433)
    time.sleep(7)

    # save biome map
    #change to terraindebugplain
    pyautogui.click(x=144, y=201)
    time.sleep(0.3)

    # change to All and generate texture
    pyautogui.click(x=1668, y=661)
    time.sleep(0.3)
    pyautogui.click(x=1677, y=679)
    time.sleep(0.3)
    pyautogui.click(x=1685, y=702)
    time.sleep(1)

    print("generation " + str(x+1) + " of " + str(total) + " completed")
    
    #######################################
   
    print("starting numbering of " + str(x+1))
    pyautogui.click(x=521, y=1063)
    time.sleep(2)
    pyautogui.click(x=521, y=1)
    time.sleep(0.5)
    pyautogui.click(button='right', x=240, y=249)
    time.sleep(2)
    pyautogui.click(x=302, y=759)
    time.sleep(2)
    pyautogui.typewrite(str(x+1) + "_b")
    time.sleep(0.3)
    pyautogui.press('enter') 
    time.sleep(0.3) 

    pyautogui.click(button='right', x=249, y=224)
    time.sleep(2)
    pyautogui.click(x=307, y=737)
    time.sleep(2)
    pyautogui.typewrite(str(x+1) + "_h")
    time.sleep(0.3)
    pyautogui.press('enter') 
    time.sleep(0.3)

    pyautogui.click(x=722, y=1062)
    time.sleep(0.2)






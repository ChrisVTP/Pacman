# import app_class
from os import listdir
from os.path import exists
from wall_generator import *

WALLS_LIST = "wall_list"
if(not exists(WALLS_LIST)):
    exit(0)
files = [f for f in listdir(WALLS_LIST)]





class wall :
    def __init__(self) -> None:
        self.number = len(files)
        self.index = 0
    
    def getLink(self):
        return WALLS_LIST +"\\"+files[self.index]


    def Wall_Generator(self):
        tileMap = Map(16,31,"""
        ||||||||||||||||
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |.........||||||
        |.........||||||
        |.........||||||
        |.........||||||
        |.........||||||
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        |...............
        ||||||||||||||||
        """)
        while tileMap.add_wall_obstacle(extend=True):
            pass
    
        result = []
        for line in str(tileMap).splitlines():
            s = line[:14]
            # print (s+s[::-1])
            s += s[::-1]
            # print(s)
            result += [s]
        return result

    def generate(self):
        l = self.Wall_Generator()[1:]
        for i in range(len(l)):
            l[i] = l[i].replace("|","1")
            l[i] = l[i].replace(".","C")
        l[12]= l[12][:13]+ "DD"+ l[12][15:]
        l[13]= l[13][:11]+ "5" +  "0"*4 + "4" + l[13][17:]
        l[14]= l[14][:11]+  "0"*6 + l[14][17:]
        l[15]= l[15][:11]+ "2" +  "0"*4 + "3" + l[15][17:]
        l[29]= l[29][0]+"B"+l[29][2:13]+ "P" + l[29][14:-2]+ "B"+l[29][-1]
        l[1]= l[1][0]+"B" +l[1][2:-2]+ "B"+l[1][-1]

        return l



if __name__ == "__main__":
    a = wall()
    l = a.Wall_Generator()[1:]
    for i in range(len(l)):
        l[i] = l[i].replace("|","1")
        l[i] = l[i].replace(".","C")
    # print(len(l))
    l[12]= l[12][:13]+ "DD"+ l[13][15:]
    l[13]= l[13][:11]+ "5" +  "0"*4 + "4" + l[13][17:]
    l[14]= l[14][:11]+  "0"*6 + l[14][17:]
    l[15]= l[15][:11]+ "2" +  "0"*4 + "3" + l[13][17:]
    l[29]= l[29][0]+"B"+l[29][2:13]+ "P" + l[29][14:-2]+ "B"+l[29][-1]
    l[1]= l[1][0]+"B" +l[1][2:-2]+ "B"+l[1][-1]
    for i, line in enumerate(l):
        print(str(i) +": '"+line+"'")
        # print(type(i))
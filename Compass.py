try:
    from common_libs import base_classes
    from common_libs import Xy as Xy_
except:
    import base_classes
    import Xy as Xy_

import math
import statistics

Xy = Xy_.Xy

default_distance_on_xy_direction = 1

def decodeString(arg):
    direction = 0
    if arg in ["N","n"]:
        direction = 0
    elif arg in ["S","s"]:
        direction = 180
    elif arg in ["E","e"]:
        direction = 90
    elif arg in ["W","w"]:
        direction = 270
    return direction

class Bearing(base_classes.baseStruct):

    def toXy(self):
        if self.direction%90 == 0:
            if self.direction in [0,360]:
                xy = Xy(0,1)
            elif self.direction == 90:
                xy = Xy(1,0)
            elif self.direction == 180:
                xy = Xy(0,-1)
            elif self.direction == 270:
                xy = Xy(-1,0)
        else:
            x=0
            if self.direction < 360 and self.direction >180:
                x = -1
            elif self.direction >0 or self.direction <180:
                x=1
            y = x*math.tan(math.radians(self.direction))
            xy = Xy(x,y)
        h = math.sqrt(xy.x**2+xy.y**2)
        ratio_converter = default_distance_on_xy_direction/h
        xy *= ratio_converter
        return xy

    def __init__(self,arg):
        self.direction = 000
        self(arg)
        
    def __call__(self,arg):
        if isinstance(arg,str):
            values = []
            for char in arg:
                values.append(decodeString(char))
            self.direction = round(statistics.fmean(values))
        elif isinstance(arg,(int,float)):
            self.direction = round(arg)

    def __str__(self):
        return str(self.direction).zfill(3)

    def __repr__(self):
        return "Compass(" + self.__str__() + ")"

    def __int__(self):
        return round(self.direction())

    def __float__(self):
        return float(self.direction)
    
    def __eq__(self,other):
        if float(self) == float(other):
            return True
        else:
            return False

    def __lt__(self,other):
        if float(self) < float(other):
            return True
        else:
            return False

    def __gt__(self,other):
        if float(self) > float(other):
            return True
        else:
            return False

    def _le___(self,other):
        if float(self) <= float(other):
            return True
        else:
            return False

    def __ge__(self,other):
        if float(self) >= float(other):
            return True
        else:
            return False

    def __getitem__(self,key):
    
        if key == 0:
            return self.direction
        else:
            self.__missing__(key)

    def __setitem__(self,key,value):
        if key == 0:
            self.direction = value
        else:
            self.__missing__(key)
            
    def __missing__(self,key):
        raise ValueError("Key "+repr(key)+" not allowed in "+repr(type(self)))

    def __iter__(self):
        return (self.direction).__iter__()

    def __reversed__(self):
        return self.direction

    def __len__(self):
        return 1

    def _length_hint__(self):
        return 1
    
    def __hash__(self):
        return hash(self.direction)

class Compass(Bearing):
    pass

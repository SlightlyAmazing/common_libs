try:
    from common_libs import base_classes
    from common_libs import Xy as Xy_
except:
    import base_classes
    import Xy as Xy_

import math

Xy = Xy_.Xy

class Xyz(base_classes.baseStruct):
    
    def toXy(self):
        return Xy(self.x,self.y)

    def getNormalised(self):
        return Xyz(self)/self.getMagnitude()

    def getMagnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
        
    def __init__(self, *formal, **keyword):
        self._set(0,0,0)
        self(*formal, **keyword)
        
    def __call__(self,*formal,**keyword):
        if len(formal) == 1:
            if isinstance(formal[0],Xyz):
                self._set(formal[0].x,formal[0].y,formal[0].z)
            elif isinstance(formal[0],Xy):
                self._set(formal[0].x,formal[0].y,0)
            elif isinstance(formal[0],(float,int)):
                self._set(formal[0],formal[0],formal[0])
            elif isinstance(formal[0],(list,tuple)):
                self(*formal[0])
            elif isinstance(formal[0],dict):
                self(*formal[0])
        elif len(formal) == 2:
            if isinstance(formal[0], (float,int)) and isinstance(formal[1], (float,int)):
                self._set(formal[0],formal[1],0)
        elif len(formal) == 3:
            if isinstance(formal[0], (float,int)) and isinstance(formal[1], (float,int)) and isinstance(formal[2], (float,int)):
                self._set(formal[0],formal[1],formal[2])
        elif len(formal) == 3:
            if len(keyword) == 1:
                pass
            elif len(keyword) == 2:
                if "x" in keyword or "X" in keyword and "y" in keyword or "Y" in keyword:
                    self.__call__(keyword["x" if "x" in keyword else "X"],keyword["y" if "y" in keyword else "Y"],0)
            elif len(keyword) == 3:
                if "x" in keyword or "X" in keyword and "y" in keyword or "Y" in keyword and "z" in keyword or "Z" in keyword:
                    self.__call__(keyword["x" if "x" in keyword else "X"],keyword["y" if "y" in keyword else "Y"],keyword["z" if "z" in keyword else "Z"])
       
    def _set(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

    def __repr__(self):
        return "Xyz" + self.__str__()

    def __eq__(self,other):
        if isinstance(other,Xyz):        
            if self.x == other.x and self.y == other.y and self.z == other.z:
                return True
            else:
                return False

    def __lt__(self,other):
        if self.x <= other.x and self.y <= other.y and self.z < other.z:
            return True
        elif self.x <= other.x and self.y < other.y and self.z <= other.z:
            return True
        elif self.x < other.x and self.y <= other.y and self.z <= other.z:
            return True
        else:
            return False

    def __gt__(self,other):
        if self.x >= other.x and self.y >= other.y and self.y > other.y:
            return True
        elif self.x > other.x and self.y >= other.y and self.y >= other.y:
            return True
        elif self.x >= other.x and self.y > other.y and self.y >= other.y:
            return True
        else:
            return False

    def __le___(self,other):
        if self.x <= other.x and self.y <= other.y and self.z <= other.z:
            return True
        else:
            return False

    def __ge__(self,other):
        if self.x >= other.x and self.y >= other.y and self.z >= other.z:
            return True
        else:
            return False

    def __bool__(self):
        if self.x == 0 and self.y == 0 and self.z == 0 :
            return False
        else:
            return True

    def __len__(self):
        return 3

    def _length_hint__(self):
        return 3

    def __getitem__(self,key):
        if key == 0 or key == "x" or key == "X":
            return self.x
        elif key == 1 or key == "y" or key == "Y":
            return self.y
        elif key == 2 or key == "z" or key == "Z":
            return self.z
        else:
            self.__missing__(key)

    def __setitem__(self,key,value):
        if key == 0 or key == "x" or key == "X":
            self.x = value
        elif key == 1 or key == "y" or key == "Y":
            self.y = value
        elif key == 2 or key == "z" or key == "Z":
            self.z = value
        else:
            self.__missing__(key)
            
    def __missing__(self,key):
        raise ValueError("Key "+repr(key)+" not allowed in "+repr(type(self)))

    def __iter__(self):
        return (self.x,self.y,self.z).__iter__()

    def __reversed__(self):
        return (self.z,self.y,self.x)

    def __add__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x + other.x,self.y + other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x + other,self.y + other,self.z+other)
        else:
            return NotImplemented 

    def __iadd__(self,other):
        self = self.__add__(other)
        return self
    
    def __sub__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x - other.x,self.y - other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x - other,self.y - other,self.z - other)
        else:
            return NotImplemented    

    def __isub__(self,other):
        self = self.__sub__(other)
        return self
    
    def __mul__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x * other.x,self.y * other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x * other,self.y * other,self.z * other)
        else:
            return NotImplemented 
     
    def __imul__(self,other):
        self = self.__mul__(other)
        return self
               
    def __truediv__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x / other.x,self.y / other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x / other,self.y / other,self.z / other)
        else:
            return NotImplemented
     
    def __itruediv__(self,other):
        self = self.__truediv__(other)
        return self
           
    def __floordiv__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x // other.x, self.y // other.y, self.z // other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x // other.x,self.y // other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x // other,self.y // other,self.z // other)
        else:
            return NotImplemented
     
    def __ifloordiv__(self,other):
        self = self.__floordiv__(other)
        return self
               
    def __mod__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x % other.x, self.y % other.y, self.z % other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x % other.x,self.y % other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x % other,self.y % other,self.z % other)
        else:
            return NotImplemented

    def __imod__(self,other):
        self = self.__mod__(other)
        return self
    
    def __pow__(self,other):
        if isinstance(other,Xyz):
            return Xyz(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        elif isinstance(other,Xy):
            return Xyz(self.x ** other.x,self.y ** other.y,self.z)
        elif isinstance(other,int) or isinstance(other,float):
            return Xyz(self.x ** other,self.y ** other,self.z ** other)
        else:
            return NotImplemented
    
    def __ipow__(self,other):
        self = self.__pow__(other)
        return self

    def __neg__(self):
        return Xyz(-self.x,-self.y,-self.z)

    def __pos__(self):
        return Xyz(+self.x,+self.y,+self.z)

    def __abs__(self):
        return Xyz(abs(self.x),abs(self.y),abs(self.z))

    def __invert__(self):
        return Xyz(self.x.__invert__(),self.y.__invert__(),self.z.__invert__())

    def __round__(self,ndigits=None):
        return Xyz(round(self.x,ndigits),round(self.y,ndigits),round(self.z,ndigits))
    
    def __trunc__(self):
        return Xyz(math.trunc(self.x),math.trunc(self.y),math.trunc(self.z))

    def __floor__(self):
        return Xyz(math.floor(self.x),math.floor(self.y),math.floor(self.z))

    def __ceil__(self):
        return Xyz(math.ceil(self.x),math.ceil(self.y),math.ceil(self.z))

    def __hash__(self):
        return hash((self.x,self.y,self.z))

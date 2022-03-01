try:
    from common_libs import base_classes
except:
    import base_classes

import math

class Xy(base_classes.baseStruct):
    
    def toBearing(self):
        import Compass
        Bearing = Compass.Bearing
        
        if self.x == 0 and self.y >= 0:
            bearing = Bearing("N")
        elif self.x == 0 and self.y <0:
            bearing = Bearing("S")
        else:
            bearing = Bearing(math.degrees(math.atan(self.y/self.x)))
        return bearing

    def getNormalised(self):
        if self == Xy(0):
            return Xy(0)
        magnitude = math.sqrt(self.x**2+self.y**2)
        return Xy(self.x/magnitude,self.y/magnitude)
    
    def getSingleDirection(self):
        if abs(self.x) > abs(self.y):
            xy = Xy(self.x,0)
        else:
            xy = Xy(0,self.y)
        return xy.getNormalised()

    def cap(self,minXy,maxXy):
        if self.x <minXy.x:
            self.x = minXy.x
        if self.y < minXy.y:
            self.y = minXy.y
        if self.x > maxXy.x:
            self.x = maxXy.x
        if self.y > maxXy.y:
            self.y = maxXy.y

    def __init__(self, *formal, **keyword):
        self._set(0,0)
        self(*formal, **keyword)
        
    def __call__(self,*formal,**keyword):
        if len(formal) == 1:
            if isinstance(formal[0],Xy):
                self._set(formal[0].x,formal[0].y)
            elif isinstance(formal[0],(float,int)):
                self._set(formal[0],formal[0])
            elif isinstance(formal[0],(list,tuple)):
                self.__call__(formal[0][0],formal[0][1])
            elif isinstance(formal[0],dict):
                if "x" in formal[0] or "X" in formal[0] and "y" in formal[0] or "Y" in formal[0]:
                    self.__call__(formal[0]["x" if "x" in formal[0] else "X"],formal[0]["y" if "y" in formal[0] else "Y"])         
        elif len(formal) == 2:
            if isinstance(formal[0], (float,int)) and isinstance(formal[1], (float,int)):
                self._set(formal[0],formal[1])
        elif len(formal) == 0:
            if len(keyword) == 2:
                if "x" in keyword or "X" in keyword and "y" in keyword or "Y" in keyword:
                    self.__call__(keyword["x" if "x" in keyword else "X"],keyword["y" if "y" in keyword else "Y"])
       
    def _set(self,x,y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __repr__(self):
        return "Xy" + self.__str__()

    def __eq__(self,other):
        if isinstance(other,Xy):        
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False

    def __lt__(self,other):
        if self.x < other.x and self.y <= other.y:
            return True
        elif self.x <= other.x and self.y < other.y:
            return True
        else:
            return False

    def __gt__(self,other):
        if self.x > other.x and self.y >= other.y:
            return True
        elif self.x >= other.x and self.y > other.y:
            return True
        else:
            return False

    def __le___(self,other):
        if self.x <= other.x and self.y <= other.y:
            return True
        else:
            return False

    def __ge__(self,other):
        if self.x >= other.x and self.y >= other.y:
            return True
        else:
            return False

    def __bool__(self):
        if self.x == 0 and self.y == 0:
            return False
        else:
            return True

    def __len__(self):
        return 2

    def _length_hint__(self):
        return 2

    def __getitem__(self,key):
        if key == 0 or key == "x" or key == "X":
            return self.x
        elif key == 1 or key == "y" or key == "Y":
            return self.y
        else:
            self.__missing__(key)

    def __setitem__(self,key,value):
        if key == 0 or key == "x" or key == "X":
            self.x = value
        elif key == 1 or key == "y" or key == "Y":
            self.y = value
        else:
            self.__missing__(key)
            
    def __missing__(self,key):
        raise ValueError("Key "+repr(key)+" not allowed in "+repr(type(self)))

    def __iter__(self):
        return (self.x,self.y).__iter__()

    def __reversed__(self):
        return (self.y,self.x)

    def __add__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x + other.x,self.y + other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x + other,self.y + other)
        else:
            return NotImplemented 

    def __iadd__(self,other):
        self = self.__add__(other)
        return self
    
    def __sub__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x - other.x,self.y - other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x - other,self.y - other)     
        else:
            return NotImplemented    

    def __isub__(self,other):
        self = self.__sub__(other)
        return self
    
    def __mul__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x * other.x,self.y * other.y)
        elif isinstance(other,(int,float)):
            return Xy(self.x*other,self.y * other)
        else:
            return NotImplemented 
     
    def __imul__(self,other):
        self = self.__mul__(other)
        return self
               
    def __truediv__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x / other.x,self.y / other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x / other,self.y / other)
        else:
            return NotImplemented 
     
    def __itruediv__(self,other):
        self = self.__truediv__(other)
        return self
           
    def __floordiv__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x // other.x,self.y // other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x // other,self.y // other)
        else:
            return NotImplemented 
     
    def __ifloordiv__(self,other):
        self = self.__floordiv__(other)
        return self
               
    def __mod__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x % other.x,self.y % other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x % other,self.y % other)
        else:
            return NotImplemented 

    def __imod__(self,other):
        self = self.__mod__(other)
        return self
    
    def __pow__(self,other):
        if isinstance(other,Xy):
            return Xy(self.x ** other.x,self.y ** other.y)
        elif isinstance(other,int) or isinstance(other,float):
            return Xy(self.x ** other,self.y ** other)
        else:
            return NotImplemented 
    
    def __ipow__(self,other):
        self = self.__pow__(other)
        return self

    def __neg__(self):
        return Xy(-self.x,-self.y)

    def __pos__(self):
        return Xy(+self.x,+self.y)

    def __abs__(self):
        return Xy(abs(self.x),abs(self.y))

    def __invert__(self):
        return Xy(self.x.__invert__(),self.y.__invert__())

    def __round__(self,ndigits=None):
        return Xy(round(self.x,ndigits),round(self.y,ndigits))
    
    def __trunc__(self):
        return Xy(math.trunc(self.x),math.trunc(self.y))

    def __floor__(self):
        return Xy(math.floor(self.x),math.floor(self.y))

    def __ceil__(self):
        return Xy(math.ceil(self.x),math.ceil(self.y))

    def __hash__(self):
        return hash((self.x,self.y))

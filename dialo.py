import pgzrun
from pgzero.actor import Actor
class dialogue :
    __slots__ = (   'detail' )
    def __init__(self,detail):
        self.detail = detail
alldialogue = []
firstdia = [ ]
firstdia.append(Actor('duihua1',(500,300)))
firstdia.append(Actor('duihua2',(500,300)))
alldialogue.append(firstdia)
import pgzrun
from math import *
from random import *
from pgzero.actor import Actor
from pgzero.loaders import sounds
from pgzero.clock import clock
from pgzero.screen import Screen
from pgzero.rect import Rect
from pgzero.keyboard import keys
from mymapandnpc import *
from dialo import *
WIDTH = 1000
HEIGHT = 562

class condition:
    def __init__(self):
        self.fightpos = (1, 1)#对战对话的选择框出现位置
        #self.contin = True#
        self.showfight = False#是否显示对战对话框的位置
        self.showtalk = False#是否正在对话
        self.fightshuxing = 1#和玩家对战的npc的属性
        self.nowmap = 5#现在显示的地图编号
        self.talknum = 0#正在进行的对话
        self.fighting =False#是否在对战
        self.makesound =False#是否发出对话声音
        self.mapsound =False#是否发出地图声音
        self.mousepos = (-100,-100)#鼠标坐标
allcondition = condition()
class myself(Actor) :
    __slots__ = (
        'num'
    )
    def __init__(self,name,pos,num):
        super().__init__(name,pos)
        self.num = num
my = myself("down1",(520,281),0)
my_down = ['down1','down2','down3','down4']#移动时人物图像的变换
my_up = ['up1','up2','up3','up4']
my_left = ['left1','left2','left3','left4']
my_right = ['right1','right2','right3','right4']

fight =Actor("fight",(0,0))
talk = Actor("talk",(0,0))
def draw_npc():#画npc
    for i in allmap_info[allcondition.nowmap].actor_npc :
        i.draw()
def draw_fightandtalk ():#画对战，对话的选择框
    if allcondition.showfight :
        fight.x ,fight.y =  allcondition.fightpos
        fight.draw()
        talk.draw()
def draw_talk_dialogue():#画具体的对话
    if allcondition.showtalk ==1:   #如果开始对话
        out = choice(alldialogue)
        if allcondition.talknum <len(out):#如果对话还没有结束
            out [allcondition.talknum].draw()
            clock.schedule_unique(sounds.duihua.stop, 1.0)
        else :#对话结束重置状态
            allcondition.showtalk = 0
            allcondition.talknum = 0
def draw():
    screen.clear()
    allmap_actor[allcondition.nowmap].draw()#画地图
    draw_npc()#画npc
    my.draw()#画人物自己
    draw_fightandtalk()#画对战对话的选择框
    draw_talk_dialogue()#画对话
    temppos = (allcondition.mousepos[0]//31.25,allcondition.mousepos[1]//31.25)
    if temppos in allmap_info[allcondition.nowmap].actor_gaoshi :
        allmap_info[allcondition.nowmap].actor_gaoshi[temppos].draw()
def move_key_board ():#主地图中的按键检测
    if  allcondition.showtalk or allcondition.showfight :#如果正在对战或者对话
        return
    mainspeed = 5#人物移动速率
    pict_change_speed=0.15#人物图像的变换速率
    if keyboard[keys.SPACE]:
        my.angle += 0.3
    if keyboard[keys.UP]:
        if allmap_info[allcondition.nowmap].bool_go[int((my.center[1] - mainspeed) // 31.25)][int(my.center[0] // 31.25)] == 1 :
            if my.top > mainspeed:
                my.y -= mainspeed
                my.num += pict_change_speed
                my.image = my_up[int(my.num) % 4]
            elif allcondition.nowmap>1:
                allcondition.nowmap -= 2
                my.y = 562-my.height/2
    elif keyboard[keys.DOWN]:
        if allmap_info[allcondition.nowmap].bool_go[int((my.top + my.height + mainspeed) // 31.25)][int(my.center[0] // 31.25)] == 1 :
            if    my.bottom < 558 - mainspeed:
                my.y += mainspeed
                my.num += pict_change_speed
                my.image =my_down[int(my.num)%4]
            elif allcondition.nowmap<4 :
                allcondition.nowmap += 2
                my.y = my.height/2
    elif keyboard[keys.LEFT]:
        if allmap_info[allcondition.nowmap].bool_go[int((my.center[1]) // 31.25)][int(abs((my.left - mainspeed) )// 31.25)] == 1 :
            if  my.left > mainspeed:
                my.x -= mainspeed
                my.num += pict_change_speed
                my.image = my_left[int(my.num) % 4]
            elif allcondition.nowmap%2==1 :
                allcondition.nowmap -= 1
                my.x=1000-my.width/2
    elif keyboard[keys.RIGHT]:
        if allmap_info[allcondition.nowmap].bool_go[int((my.center[1]) // 31.25)][int((my.center[0] + mainspeed) // 31.25)] == 1 :
            if my.right < 996 - mainspeed:
                my.x += mainspeed
                my.num += pict_change_speed
                my.image = my_right[int(my.num) % 4]
            elif allcondition.nowmap%2 == 0 :
                allcondition.nowmap += 1
                my.x = my.width/2
def on_mouse_down(pos,button = mouse.RIGHT):#鼠标检测
    allcondition.mousepos = pos
    allcondition.fighting = False
    if button == mouse.LEFT and allcondition.showtalk==True:
        allcondition.talknum += 1
        allcondition.makesound = True
    elif button == mouse.LEFT  and fight.collidepoint(pos):
        allcondition.showfight=False
        allcondition.fighting =    True
    elif button == mouse.LEFT  and talk.collidepoint(pos) and allcondition.showtalk==False:
        allcondition.showtalk=True
        allcondition.showfight =False




def pos_update(nowmap = 0 ):
    move_key_board()

def sound_update() :#声音播放，包括地图音乐和对话音效
    if allcondition.makesound :
        sounds.duihua.set_volume(0.5)
        sounds.duihua.play()
        clock.schedule_unique(sounds.duihua.stop, 0.08)
        allcondition.makesound =False

    if  allcondition.fighting :
        sounds.mapbgm.stop()
        allcondition.mapsound =False
    elif not allcondition.mapsound :
        sounds.mapbgm.set_volume(0.5)
        sounds.mapbgm.play()
        allcondition.mapsound = True

        #sounds.duihua.play()
    print(allcondition.makesound)

def act_with_npc():#与npc互动
    for i in allmap_info[allcondition.nowmap].actor_npc :
        if i.collidepoint(my.pos):
            if  keyboard[keys.RETURN]:
                allcondition.showfight =True
                allcondition.fightpos = (i.pos[0]+i.width,i.pos[1])
                allcondition.fightshuxing = i.shuxing
                talk.pos = (fight.x,fight.y+fight.height/2+talk.height/2)



def update() :
    pos_update()
    act_with_npc()
    sound_update()
    pass

for i in allmap_info :
    allmap_actor.append(Actor(i.name, (500, 281)))

pgzrun.go()

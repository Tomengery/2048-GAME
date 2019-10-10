import tkinter as tk 
import time
import random

grid_size=256
tile_margin=4
tile_size=grid_size/4


class Tile :

    def __init__(self,area,posx,posy,val,tag):
        self.x_pos=posx
        self.y_pos=posy
        self.canvas=area
        self.value=val
        self.id=tag
        self.draw()

    def __del__(self):
        print('deleting tile %s' % self.id)
        self.erase()

    def draw(self):
        print('drawing tile %s' % self.id)
        self.tile=self.canvas.create_rectangle(tile_size*self.x_pos+tile_margin/2,
                                               tile_size*self.y_pos+tile_margin/2,
                                               tile_size*(self.x_pos+1)-tile_margin/2,
                                               tile_size*(self.y_pos+1)-tile_margin/2,
                                               width=tile_margin,
                                               fill="orange",
                                               tag=self.id)
        self.canvas.create_text(tile_size*self.x_pos+tile_size/2,
                                tile_size*self.y_pos+tile_size/2,
                                text=str(self.value),
                                tag=self.id)
        self.canvas.update_idletasks()
        self.canvas.update()

    def erase(self):
        self.canvas.delete(self.id)
        self.canvas.update_idletasks()
        self.canvas.update()

    def move(self,posx,posy):
        x_diff=posx-self.x_pos
        y_diff=posy-self.y_pos
        #animation removed bug hai
        #for i in range(0,32):
        #    self.canvas.move(self.id,(x_diff*tile_size)/32,(y_diff*tile_size)/32)
        #    time.sleep(1/64)
        self.canvas.move(self.id,(x_diff*tile_size),(y_diff*tile_size))
        self.canvas.update_idletasks()
        self.canvas.update()        
        self.x_pos=posx
        self.y_pos=posy



class Grid :
    
    def __init__(self,area) :
        self.canvas=area
        self.avail_tag=list(range(1,17))
        self.avail_tag_count=16
        #initially all empty tiles
        self.grid=[[0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]
        self.tiles={}
        self.canvas.create_rectangle(2,2,grid_size,grid_size,width=2)
        self.create_random()
        self.create_random()

    def create_random(self):
        if self.avail_tag_count == 0:
            print('can not create any more tiles')
        else :
            i=random.randint(0,self.avail_tag_count-1)
            for y in range(0,4):
                for x in range(0,4):
                    if (self.grid[y][x] == 0 and i == 0):
                        self.create_at(x,y,2)
                        return
                    elif self.grid[y][x] == 0:
                        i=i-1

    def create_at(self,x,y,value):
        if self.avail_tag_count == 0:
            print('can not create any more tiles')
        elif self.grid[y][x] != 0:
            print('Element already present at %d %d' % (x,y))
        else :       
            uid=self.avail_tag[0]
            self.avail_tag.remove(uid)
            self.avail_tag_count=self.avail_tag_count-1
            tile=Tile(self.canvas,x,y,value,'tile_'+str(uid))
            self.grid[y][x]=uid
            self.tiles[uid]=tile

        
    def destroy(self,uid):
        del self.tiles[uid]
        self.avail_tag.append(uid)
        self.avail_tag_count=self.avail_tag_count+1
        for y in range(0,4):
            for x in range(0,4):
                if self.grid[y][x] == uid:
                    self.grid[y][x]=0


    def move_tile(self,uid,x,y):
        t=self.tiles[uid]
        self.grid[t.y_pos][t.x_pos]=0
        self.grid[y][x]=uid
        t.move(x,y)
    
    def move(self,direction):
        if direction == 'up':
            print('moving up')
            for y in range(1,4):
                for x in range(0,4):
                    #ignore if no tile
                    if self.grid[y][x] != 0:
                        tile_1=self.grid[y][x]
                        temp=y
                        while True:
                            temp=temp-1
                            #reached border break loop
                            if temp == -1:
                                break
                            #simply move up if tile is empty
                            elif self.grid[temp][x] == 0:
                                self.move_tile(tile_1,x,temp)
                            #there is a tile above
                            else :
                                tile_2=self.grid[temp][x]
                                val_1=self.tiles[tile_1].value
                                val_2=self.tiles[tile_2].value
                                #check if they can join
                                if val_1 == val_2 :
                                    self.move_tile(tile_1,x,temp)
                                    self.destroy(tile_1)
                                    self.destroy(tile_2)
                                    self.create_at(x,temp,2*val_1)
                                break
        elif direction == 'down':
            print('moving down')
            for y in range(2,-1,-1):
                for x in range(0,4):
                    #ignore if no tile
                    if self.grid[y][x] != 0:
                        tile_1=self.grid[y][x]
                        temp=y
                        while True:
                            temp=temp+1
                            #reached border break loop
                            if temp == 4:
                                break
                            #simply move up if tile is empty
                            elif self.grid[temp][x] == 0:
                                self.move_tile(tile_1,x,temp)
                            #there is a tile above
                            else :
                                tile_2=self.grid[temp][x]
                                val_1=self.tiles[tile_1].value
                                val_2=self.tiles[tile_2].value
                                #check if they can join
                                if val_1 == val_2 :
                                    self.move_tile(tile_1,x,temp)
                                    self.destroy(tile_1)
                                    self.destroy(tile_2)
                                    self.create_at(x,temp,2*val_1)
                                break
        elif direction == 'right':
            print('moving right')
            for y in range(0,4):
                for x in range(2,-1,-1):
                    #ignore if no tile
                    if self.grid[y][x] != 0:
                        tile_1=self.grid[y][x]
                        temp=x
                        while True:
                            temp=temp+1
                            #reached border break loop
                            if temp == 4:
                                break
                            #simply move up if tile is empty
                            elif self.grid[y][temp] == 0:
                                self.move_tile(tile_1,temp,y)
                            #there is a tile above
                            else :
                                tile_2=self.grid[y][temp]
                                val_1=self.tiles[tile_1].value
                                val_2=self.tiles[tile_2].value
                                #check if they can join
                                if val_1 == val_2 :
                                    self.move_tile(tile_1,temp,y)
                                    self.destroy(tile_1)
                                    self.destroy(tile_2)
                                    self.create_at(temp,y,2*val_1)
                                break        
        elif direction == 'left':
            print('moving left')
            for y in range(0,4):
                for x in range(1,4):
                    #ignore if no tile
                    if self.grid[y][x] != 0:
                        tile_1=self.grid[y][x]
                        temp=x
                        while True:
                            temp=temp-1
                            #reached border break loop
                            if temp == -1:
                                break
                            #simply move left if tile is empty
                            elif self.grid[y][temp] == 0:
                                self.move_tile(tile_1,temp,y)
                            #there is a tile to the left
                            else :
                                tile_2=self.grid[y][temp]
                                val_1=self.tiles[tile_1].value
                                val_2=self.tiles[tile_2].value
                                #check if they can join
                                if val_1 == val_2 :
                                    self.move_tile(tile_1,temp,y)
                                    self.destroy(tile_1)
                                    self.destroy(tile_2)
                                    self.create_at(temp,y,2*val_1)
                                break
        self.create_random()


window=tk.Tk()
window.title("Play 2048")
play_area=tk.Canvas(window,height=grid_size,width=grid_size)
s=0
score_label=tk.Label(text='Score:- %d'%s)

my_grid=Grid(play_area)
up=tk.Button(text='up',height=2,width=6,command=lambda : my_grid.move('up'))
down=tk.Button(text='down',height=2,width=6,command=lambda : my_grid.move('down'))
left=tk.Button(text='left',height=2,width=6,command=lambda : my_grid.move('left'))
right=tk.Button(text='right',height=2,width=6,command=lambda : my_grid.move('right'))
up.grid(row=1,column=2)
down.grid(row=3,column=2)
left.grid(row=2,column=1)
right.grid(row=2,column=3)
score_label.grid(row=0,column=0)
play_area.grid(row=4,column=0)



print(my_grid.grid)
window.mainloop()


import pygame as pg
import random

class FramedPanel(pg.sprite.Sprite):

    def __init__(self,*group):
        super(FramedPanel,self).__init__(*group)
        self.image = pg.Surface((100,100))
        self.rect = pg.Rect(0,0,100,100)
        rr = random.randint
        self.image.fill((rr(0,255),rr(0,255),rr(0,255)))
        pg.draw.rect(self.image, (255,0,0), self.rect, 1)


class MyLayout(pg.sprite.OrderedUpdates):

    def __init__(self,width,height,row):
        self.size = (width,height)
        self.row = row
        self.moving = False
        self.offset = 0
        self.draw_slider = False
        self.slider = pg.Surface((5,5))
        self.slider.fill((255,255,255))
        super(MyLayout,self).__init__()

    def update_mousebuttondown(self,event):
        if self.draw_slider == True:
            if event.button == 4:
                if self.offset > 0:
                    self.offset -= 5
            elif event.button == 5:
                if self.offset < self.offset_max:
                    self.offset += 5
            elif event.button == 1:
                self.moving = True
                
    def update_mousemotion(self,event):
        if self.moving:
            self.offset -= event.rel[1]

    def update_mousebuttonup(self,event):
        self.moving = False


    def update_size(self,size):
        self.size = size


    def update_children(self):
        for s in self._spritelist:
            n = self._spritelist.index(s)
            width = int(self.size[0]/self.row)
            s.rect = pg.Rect(n%self.row*width,n//self.row*100-self.offset,width,100)               
            s.image = pg.transform.scale(s.image,(width,100))

    def update_slider(self):
      

        if len(self._spritelist) % self.row == 0:
            self.panel_height = len(self._spritelist)//self.row *100
        else:
            self.panel_height = (len(self._spritelist)//self.row + 1)*100
        if self.panel_height > self.size[1]:
            self.offset_max = self.panel_height - self.size[1]
            height = int(self.size[1]*1.0/self.panel_height*self.size[1])
            self.slider = pg.transform.scale(self.slider,(5,height))
            self.draw_slider = True
        else:
            self.draw_slider = False

        if self.offset >= self.offset_max:
            self.offset = self.offset_max
        elif self.offset <= 0:
            self.offset = 0  


    def update(self,*args):
        self.update_children()
        self.update_slider()
            
    def draw(self,surface):
        super(MyLayout,self).draw(surface)
        if self.draw_slider:
            delta_move = self.offset*1.0/self.panel_height*self.size[1]
            pg.draw.rect(surface,(0,0,0),(self.size[0]-5,0,5,self.size[1]))
            surface.blit(self.slider,(self.size[0]-5,delta_move))

class Game(object):

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width,self.height),pg.RESIZABLE)
        self.layout = MyLayout(self.width,self.height,3)
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        for i in range(30):
            FramedPanel(self.layout)
                
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
            if event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                self.screen_rect = self.screen.get_rect()
                self.layout.update_size(self.screen_rect.size)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.layout.update_mousebuttondown(event)
            if event.type == pg.MOUSEMOTION:
                self.layout.update_mousemotion(event)
            if event.type == pg.MOUSEBUTTONUP:
                self.layout.update_mousebuttonup(event)
            
    def draw(self):
        self.layout.draw(self.screen)


    def update(self,dt):
        self.layout.update()

    def run(self):
        dt = self.clock.tick(self.fps)
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    game = Game(800,600)
    game.run()
    pg.quit()

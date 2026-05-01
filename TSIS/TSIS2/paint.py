import pygame,sys
from datetime import datetime
from tools import PencilTool,LineTool,RectangleTool,SquareTool,CircleTool,RightTriangleTool,EquilateralTriangleTool,RhombusTool,EraserTool,FillTool,TextTool

window_title="Paint"
win_width,win_height=1100,720
toolbar_width,toolbar_height=160,win_height
canvas_x,canvas_y=toolbar_width,0
canvas_width,canvas_height=win_width-toolbar_width,win_height

brush_sizes={"small":2,"medium":5,"large":10}
brush_size_keys={pygame.K_1:"small",pygame.K_2:"medium",pygame.K_3:"large"}

color_palette=[(0,0,0),(255,255,255),(200,50,50),(50,200,50),(50,50,200),(255,200,0),(255,130,0),(160,0,200),(0,200,200),(200,80,160),(130,80,40),(160,160,160)]

bg_color=(45,45,50);canvas_color=(255,255,255)
accent_color=(90,160,255);text_color=(230,230,230);divider_color=(70,70,80)

class Button:
    padding=6
    def __init__(self,rect,label,value=None):
        self.rect=pygame.Rect(rect);self.label=label;self.value=value
    def draw(self,surface,font,active=False):
        color=accent_color if active else (70,70,80)
        pygame.draw.rect(surface,color,self.rect,border_radius=5)
        pygame.draw.rect(surface,divider_color,self.rect,1,border_radius=5)
        t=font.render(self.label,True,text_color)
        surface.blit(t,(self.rect.centerx-t.get_width()//2,self.rect.centery-t.get_height()//2))
    def is_clicked(self,pos):return self.rect.collidepoint(pos)

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((win_width,win_height))
        pygame.display.set_caption(window_title)
        self.clock=pygame.time.Clock()
        self.font_small=pygame.font.SysFont("segoeui",13)
        self.font_medium=pygame.font.SysFont("segoeui",15,True)
        self.font_large=pygame.font.SysFont("segoeui",17,True)
        self.canvas=pygame.Surface((canvas_width,canvas_height));self.canvas.fill(canvas_color)
        self.overlay=pygame.Surface((canvas_width,canvas_height),pygame.SRCALPHA)
        self.color=(0,0,0);self.brush_size=brush_sizes["medium"]
        self.tools={"pencil":PencilTool(),"line":LineTool(),"rect":RectangleTool(),"square":SquareTool(),
                    "circle":CircleTool(),"rtriangle":RightTriangleTool(),"etriangle":EquilateralTriangleTool(),
                    "rhombus":RhombusTool(),"eraser":EraserTool(),"fill":FillTool(),"text":TextTool()}
        self.active_tool_name="pencil"
        self._build_toolbar()

    def _build_toolbar(self):
        bw,bh,x,y=toolbar_width-20,30,10,10
        self.tool_buttons=[];self.size_buttons=[];self.color_swatches=[]
        tool_defs=[("Pencil","pencil"),("Line","line"),("Rectangle","rect"),("Square","square"),
                   ("Circle","circle"),("R.Triangle","rtriangle"),("Eq.Triangle","etriangle"),
                   ("Rhombus","rhombus"),("Eraser","eraser"),("Fill","fill"),("Text","text")]
        self._tool_label_pos=(x,y);y+=self.font_medium.get_height()+4
        for l,n in tool_defs:
            self.tool_buttons.append((Button((x,y,bw,bh),l,n),n));y+=bh+4
        y+=8;self._size_label_pos=(x,y);y+=self.font_medium.get_height()+4
        sw=(bw-8)//3
        for i,(l,n) in enumerate([("1 Small","small"),("2 Medium","medium"),("3 Large","large")]):
            self.size_buttons.append((Button((x+i*(sw+4),y,sw,bh),l,n),n))
        y+=bh+8;self._color_label_pos=(x,y);y+=self.font_medium.get_height()+4
        s=(bw-4)//4
        for i,c in enumerate(color_palette):
            rect=pygame.Rect(x+(i%4)*(s+2),y+(i//4)*(s+2),s,s)
            self.color_swatches.append((rect,c))

    def handle_events(self):
        mp=pygame.mouse.get_pos();cp=(mp[0]-canvas_x,mp[1]-canvas_y);on_canvas=mp[0]>=canvas_x
        tool=self.tools[self.active_tool_name]
        for e in pygame.event.get():
            if e.type==pygame.QUIT:return False
            elif e.type==pygame.KEYDOWN:
                if self.active_tool_name=="text" and tool.handle_key(e,self.canvas,self.color,self.brush_size):continue
                if e.key==pygame.K_s and (e.mod&pygame.KMOD_CTRL):self._save_canvas()
                elif e.key in brush_size_keys:self.brush_size=brush_sizes[brush_size_keys[e.key]]
            elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                tool.on_mouse_down(cp,self.canvas,self.color,self.brush_size) if on_canvas else self._handle_toolbar_click(mp)
            elif e.type==pygame.MOUSEMOTION and on_canvas:
                tool.on_mouse_move(cp,self.canvas,self.color,self.brush_size)
            elif e.type==pygame.MOUSEBUTTONUP and e.button==1 and on_canvas:
                tool.on_mouse_up(cp,self.canvas,self.color,self.brush_size)
        return True

    def _handle_toolbar_click(self,pos):
        for b,t in self.tool_buttons:
            if b.is_clicked(pos):self.active_tool_name=t;return
        for b,s in self.size_buttons:
            if b.is_clicked(pos):self.brush_size=brush_sizes[s];return
        for r,c in self.color_swatches:
            if r.collidepoint(pos):self.color=c;return

    def _save_canvas(self):
        f=f"canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(self.canvas,f);print(f"[Paint] Canvas saved → {f}")

    def draw(self):
        self.screen.fill(bg_color)
        self.screen.blit(self.canvas,(canvas_x,canvas_y))
        self._draw_overlay();self._draw_toolbar()
        pygame.display.flip()

    def _draw_overlay(self):
        self.overlay.fill((0,0,0,0))
        self.tools[self.active_tool_name].draw_preview(self.overlay,self.color,self.brush_size)
        self.screen.blit(self.overlay,(canvas_x,canvas_y))

    def _draw_toolbar(self):
        pygame.draw.rect(self.screen,bg_color,(0,0,toolbar_width,toolbar_height))
        pygame.draw.line(self.screen,divider_color,(toolbar_width,0),(toolbar_width,toolbar_height),2)
        self.screen.blit(self.font_medium.render("Tools",True,text_color),self._tool_label_pos)
        for b,t in self.tool_buttons:b.draw(self.screen,self.font_small,t==self.active_tool_name)
        self.screen.blit(self.font_medium.render("Brush Size",True,text_color),self._size_label_pos)
        cur=next((n for n,v in brush_sizes.items() if v==self.brush_size),None)
        for b,s in self.size_buttons:b.draw(self.screen,self.font_small,s==cur)
        self.screen.blit(self.font_medium.render("Colors",True,text_color),self._color_label_pos)
        for r,c in self.color_swatches:
            pygame.draw.rect(self.screen,c,r)
            pygame.draw.rect(self.screen,accent_color if c==self.color else divider_color,r,3 if c==self.color else 1)
        pr=pygame.Rect(10,win_height-50,toolbar_width-20,30)
        pygame.draw.rect(self.screen,self.color,pr);pygame.draw.rect(self.screen,accent_color,pr,2)
        self.screen.blit(self.font_small.render("Active color",True,text_color),(10,win_height-66))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit();sys.exit()

if __name__=="__main__":
    PaintApp().run()
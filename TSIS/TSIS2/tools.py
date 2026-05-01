import pygame,math
from collections import deque

class Tool:
    def __init__(self):
        self.active=False;self.start_pos=None
    def on_mouse_down(self,pos,canvas,color,size):
        self.active=True;self.start_pos=pos
    def on_mouse_move(self,pos,canvas,color,size):pass
    def on_mouse_up(self,pos,canvas,color,size):
        self.active=False;self.start_pos=None
    def draw_preview(self,surface,color,size):pass

class PencilTool(Tool):
    def __init__(self):
        super().__init__();self.last_pos=None
    def on_mouse_down(self,pos,canvas,color,size):
        super().on_mouse_down(pos,canvas,color,size)
        self.last_pos=pos;pygame.draw.circle(canvas,color,pos,size//2)
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active and self.last_pos:
            pygame.draw.line(canvas,color,self.last_pos,pos,size)
            pygame.draw.circle(canvas,color,pos,size//2)
        self.last_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        super().on_mouse_up(pos,canvas,color,size);self.last_pos=None

class LineTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_down(self,pos,canvas,color,size):
        super().on_mouse_down(pos,canvas,color,size);self.end_pos=pos
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            pygame.draw.line(canvas,color,self.start_pos,pos,size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            pygame.draw.line(surface,color,self.start_pos,self.end_pos,size)

class RectangleTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            pygame.draw.rect(canvas,color,self._make_rect(self.start_pos,pos),size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            pygame.draw.rect(surface,color,self._make_rect(self.start_pos,self.end_pos),size)
    @staticmethod
    def _make_rect(p1,p2):
        return pygame.Rect(min(p1[0],p2[0]),min(p1[1],p2[1]),abs(p2[0]-p1[0]),abs(p2[1]-p1[1]))

class SquareTool(RectangleTool):
    @staticmethod
    def _make_rect(p1,p2):
        s=min(abs(p2[0]-p1[0]),abs(p2[1]-p1[1]))
        x=p1[0] if p2[0]>=p1[0] else p1[0]-s
        y=p1[1] if p2[1]>=p1[1] else p1[1]-s
        return pygame.Rect(x,y,s,s)

class CircleTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            r=self._radius(self.start_pos,pos)
            if r>0:pygame.draw.circle(canvas,color,self.start_pos,r,size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            r=self._radius(self.start_pos,self.end_pos)
            if r>0:pygame.draw.circle(surface,color,self.start_pos,r,size)
    @staticmethod
    def _radius(c,e):return int(math.hypot(e[0]-c[0],e[1]-c[1]))

class RightTriangleTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            pygame.draw.polygon(canvas,color,self._points(self.start_pos,pos),size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            pygame.draw.polygon(surface,color,self._points(self.start_pos,self.end_pos),size)
    @staticmethod
    def _points(s,e):return[(s[0],s[1]),(e[0],s[1]),(s[0],e[1])]

class EquilateralTriangleTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            pygame.draw.polygon(canvas,color,self._points(self.start_pos,pos),size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            pygame.draw.polygon(surface,color,self._points(self.start_pos,self.end_pos),size)
    @staticmethod
    def _points(s,e):
        side=abs(e[0]-s[0]) or 1;d=1 if e[0]>=s[0] else -1
        bx2=s[0]+d*side;by=s[1];h=int(side*math.sqrt(3)/2)
        mx=(s[0]+bx2)//2;apex=(mx,by+(h if e[1]>=s[1] else -h))
        return[(s[0],by),(bx2,by),apex]

class RhombusTool(Tool):
    def __init__(self):
        super().__init__();self.end_pos=None
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:self.end_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        if self.active and self.start_pos:
            pygame.draw.polygon(canvas,color,self._points(self.start_pos,pos),size)
        super().on_mouse_up(pos,canvas,color,size);self.end_pos=None
    def draw_preview(self,surface,color,size):
        if self.active and self.start_pos and self.end_pos:
            pygame.draw.polygon(surface,color,self._points(self.start_pos,self.end_pos),size)
    @staticmethod
    def _points(s,e):
        x1,y1=min(s[0],e[0]),min(s[1],e[1])
        x2,y2=max(s[0],e[0]),max(s[1],e[1])
        mx,my=(x1+x2)//2,(y1+y2)//2
        return[(mx,y1),(x2,my),(mx,y2),(x1,my)]

class EraserTool(Tool):
    ERASE_COLOR=(255,255,255)
    def on_mouse_down(self,pos,canvas,color,size):
        super().on_mouse_down(pos,canvas,color,size)
        self.last_pos=pos;pygame.draw.circle(canvas,self.ERASE_COLOR,pos,size)
    def on_mouse_move(self,pos,canvas,color,size):
        if self.active:
            pygame.draw.line(canvas,self.ERASE_COLOR,self.last_pos,pos,size*2)
            pygame.draw.circle(canvas,self.ERASE_COLOR,pos,size)
        self.last_pos=pos
    def on_mouse_up(self,pos,canvas,color,size):
        super().on_mouse_up(pos,canvas,color,size);self.last_pos=None

class FillTool(Tool):
    def on_mouse_down(self,pos,canvas,color,size):
        super().on_mouse_down(pos,canvas,color,size);self._fill(canvas,pos,color)
    @staticmethod
    def _fill(canvas,start,fill):
        w,h=canvas.get_size();x0,y0=start
        if not(0<=x0<w and 0<=y0<h):return
        target=canvas.get_at((x0,y0))[:3]
        if target==fill[:3]:return
        q=deque([(x0,y0)]);vis={(x0,y0)}
        while q:
            x,y=q.popleft();canvas.set_at((x,y),fill)
            for nx,ny in((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0<=nx<w and 0<=ny<h and (nx,ny) not in vis and canvas.get_at((nx,ny))[:3]==target:
                    vis.add((nx,ny));q.append((nx,ny))

class TextTool(Tool):
    def __init__(self):
        super().__init__();self.cursor_pos=None;self.text_buffer="";self.font=None;self.is_typing=False
    def _get_font(self,size):return pygame.font.SysFont("monospace",max(16,size*3))
    def on_mouse_down(self,pos,canvas,color,size):
        self.cursor_pos=pos;self.text_buffer="";self.is_typing=True;self.font=self._get_font(size)
    def handle_key(self,e,canvas,color,size):
        if not self.is_typing:return False
        if e.key==pygame.K_RETURN:self._render(canvas,color);self.is_typing=False;self.text_buffer="";return True
        if e.key==pygame.K_ESCAPE:self.is_typing=False;self.text_buffer="";return True
        if e.key==pygame.K_BACKSPACE:self.text_buffer=self.text_buffer[:-1];return True
        if e.unicode and e.unicode.isprintable():self.text_buffer+=e.unicode;return True
        return False
    def draw_preview(self,surface,color,size):
        if self.is_typing and self.cursor_pos and self.font:
            surface.blit(self.font.render(self.text_buffer+"|",True,color),self.cursor_pos)
    def _render(self,canvas,color):
        if self.text_buffer and self.cursor_pos and self.font:
            canvas.blit(self.font.render(self.text_buffer,True,color),self.cursor_pos)
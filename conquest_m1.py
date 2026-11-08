# Sandbox Conquest - M1: Map & Movement
# Run: python3 conquest_m1.py

import tkinter as tk
import random

COLS, ROWS = 14, 9
CELL = 52
MAP_W = COLS * CELL
MAP_H = ROWS * CELL
PANEL_W = 260

FACTIONS = {
    0: ("Iron Legion", "#9ca3af"),
    1: ("Steppe Horde", "#f59e0b"),
    2: ("Arcane Covenant", "#a78bfa"),
    3: ("Wildfolk", "#34d399"),
}

TERRAIN = {
    0: ("Plains", "#1f3a2a"),
    1: ("Forest", "#14532d"),
    2: ("Mountains", "#374151"),
    3: ("River", "#1e3a8a"),
    4: ("City", "#78350f"),
}

class Province:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.terrain = random.choice([0,0,0,1,1,2,3,4])
        self.owner = None
        self.fort = random.randint(0,3)
        self.army = None  # (faction, count)

class Army:
    def __init__(self, faction, count):
        self.faction = faction
        self.count = count

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Sandbox Conquest — M1: Map & Movement")
        self.provs = [[Province(x,y) for x in range(COLS)] for y in range(ROWS)]
        self.selected = None  # province
        self.turn = 1
        self.current_faction = 0
        self.setup_map()

        self.canvas = tk.Canvas(root, width=MAP_W, height=MAP_H, bg="#0a0a0f", highlightthickness=0)
        self.canvas.pack(side="left")
        self.panel = tk.Frame(root, width=PANEL_W, bg="#141821")
        self.panel.pack(side="right", fill="y")
        self.panel.pack_propagate(False)

        self.info = tk.Label(self.panel, text="", justify="left", anchor="nw", bg="#141821", fg="#e6e9f0", font=("Consolas", 10), wraplength=PANEL_W-20)
        self.info.pack(padx=10, pady=10, fill="x")
        self.btn_end = tk.Button(self.panel, text="End Turn", command=self.end_turn, bg="#7c9cff", fg="#0b0d12", font=("Segoe UI", 11, "bold"))
        self.btn_end.pack(padx=10, pady=6, fill="x")
        self.btn_recruit = tk.Button(self.panel, text="Recruit +5", command=self.recruit, bg="#2a3142", fg="#e6e9f0")
        self.btn_recruit.pack(padx=10, pady=6, fill="x")

        self.canvas.bind("<Button-1>", self.on_click)
        self.render()

    def setup_map(self):
        # assign owners in blobs
        for y in range(ROWS):
            for x in range(COLS):
                # simple: distance-based faction seeds
                pass
        seeds = [(2,2,0),(COLS-3,2,1),(2,ROWS-3,2),(COLS-3,ROWS-3,3)]
        # flood fill-ish: assign nearest seed
        for y in range(ROWS):
            for x in range(COLS):
                best = min(seeds, key=lambda s: (s[0]-x)**2+(s[1]-y)**2)
                self.provs[y][x].owner = best[2]
        # add some armies
        for (sx,sy,f) in seeds:
            self.provs[sy][sx].army = Army(f, 20)

    def neighbors(self, p):
        res = []
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny = p.x+dx, p.y+dy
            if 0<=nx<COLS and 0<=ny<ROWS:
                res.append(self.provs[ny][nx])
        return res

    def on_click(self, e):
        x,y = e.x//CELL, e.y//CELL
        if not (0<=x<COLS and 0<=y<ROWS): return
        p = self.provs[y][x]
        if self.selected is None:
            if p.army and p.army.faction == self.current_faction:
                self.selected = p
        else:
            if p is self.selected:
                self.selected = None
            elif p in self.neighbors(self.selected):
                # move army
                if p.army and p.army.faction == self.selected.army.faction:
                    p.army.count += self.selected.army.count
                else:
                    p.army = self.selected.army
                self.selected.army = None
                self.selected = None
            else:
                if p.army and p.army.faction == self.current_faction:
                    self.selected = p
                else:
                    self.selected = None
        self.update_info()
        self.render()

    def recruit(self):
        if self.selected and self.selected.owner == self.current_faction:
            if self.selected.army is None:
                self.selected.army = Army(self.current_faction, 5)
            else:
                if self.selected.army.faction == self.current_faction:
                    self.selected.army.count += 5
            self.update_info(); self.render()

    def end_turn(self):
        self.current_faction = (self.current_faction+1)%4
        self.turn += 1 if self.current_faction==0 else 0
        self.selected = None
        self.update_info(); self.render()

    def update_info(self):
        lines = [f"Turn: {self.turn}", f"Active: {FACTIONS[self.current_faction][0]}", ""]
        if self.selected:
            p = self.selected
            tname,_ = TERRAIN[p.terrain]
            lines.append(f"Selected: ({p.x},{p.y})")
            lines.append(f"Terrain: {tname}")
            lines.append(f"Owner: {FACTIONS[p.owner][0] if p.owner is not None else 'None'}")
            lines.append(f"Fort: {p.fort}")
            if p.army:
                lines.append(f"Army: {FACTIONS[p.army.faction][0]} x{p.army.count}")
            else:
                lines.append("Army: none")
            lines.append("")
            lines.append("Click neighbor to move.")
        else:
            lines.append("Click an army to select.")
            lines.append("Then click adjacent province to move.")
        self.info.config(text="\n".join(lines))

    def render(self):
        self.canvas.delete("all")
        for y in range(ROWS):
            for x in range(COLS):
                p = self.provs[y][x]
                tname,tcol = TERRAIN[p.terrain]
                col = tcol
                if p.owner is not None:
                    # tint border by owner
                    pass
                x0,y0 = x*CELL, y*CELL
                self.canvas.create_rectangle(x0,y0,x0+CELL,y0+CELL, fill=col, outline="#0a0a0f", width=1)
                # owner flag corner
                if p.owner is not None:
                    fc = FACTIONS[p.owner][1]
                    self.canvas.create_rectangle(x0+2,y0+2,x0+10,y0+10, fill=fc, outline="")
                # terrain glyph
                glyph = {"Plains":"","Forest":"🌲","Mountains":"⛰","River":"~","City":"🏰"}.get(tname,"")
                if glyph:
                    self.canvas.create_text(x0+CELL//2, y0+CELL//2-6, text=glyph, font=("Segoe UI Emoji", 12), fill="#ffffff")
                # army
                if p.army:
                    fc = FACTIONS[p.army.faction][1]
                    cx,cy = x0+CELL//2, y0+CELL//2+8
                    r = 11
                    self.canvas.create_oval(cx-r,cy-r,cx+r,cy+r, fill=fc, outline="#000", width=1)
                    self.canvas.create_text(cx,cy, text=str(p.army.count), fill="#000", font=("Consolas", 9, "bold"))
                # selection highlight
                if p is self.selected:
                    self.canvas.create_rectangle(x0+1,y0+1,x0+CELL-1,y0+CELL-1, outline="#f5c542", width=3)
                # neighbor highlight
                if self.selected and p in self.neighbors(self.selected):
                    self.canvas.create_rectangle(x0+3,y0+3,x0+CELL-3,y0+CELL-3, outline="#7c9cff", width=2, dash=(3,2))
        self.update_info()

if __name__ == "__main__":
    root = tk.Tk()
    g = Game(root)
    root.mainloop()
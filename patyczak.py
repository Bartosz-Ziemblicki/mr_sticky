# tło mi nie działało, bo w wierszu 25 miałem wielkie a nie małe "x"
# składnia ze str. 239-241 (dot. na_osi_x i y) mi nie działała, więc dałem tę dłuższą wersję kodu
# funkcja kolizja_dół mi nie działała bo mają zapomniałem o y, więc oczekiwał program 2 paramentrów a dostawał 3

from tkinter import *
import random
import time

class Gra:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Pan Patyczak pędzi do wyjścia")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.płótno = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.płótno.pack()
        self.tk.update()
        self.wysokość_płótna=500
        self.szerokość_płótna=500
        self.tło = PhotoImage(file="tło.gif")
        sze = self.tło.width()
        wys = self.tło.height()
        for x in range(0, 5):
            for y in range(0, 5):           # 5 razy, bo tło ma 100x100px a gra 500x500px
                self.płótno.create_image(x*sze, y*wys, image=self.tło, anchor='nw')
        self.duszki = []
        self.biegnie = True
        self.tekst_wygrałeś = self.płótno.create_text(250, 250, text='YOU WIN!', fill='gold', font=('Times', 45), state='hidden') # Zad. 1.

    def pętlaGłówna(self):
        while 1:
            if self.biegnie == True:
                for duszek in self.duszki:
                    duszek.move()
            else:
                time.sleep(1)
                self.płótno.itemconfig(self.tekst_wygrałeś, state='normal') # Zad. 1.
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__ (self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def na_osi_x(wsp1, wsp2):
    if wsp1.x1 > wsp2.x1 and wsp1.x1 < wsp2.x2:
        return True
    elif wsp1.x2 > wsp2.x1 and wsp1.x2 < wsp2.x2:
        return True
    elif wsp2.x1 > wsp1.x1 and wsp2.x1 < wsp1.x2:
        return True
    elif wsp2.x2 > wsp1.x1 and wsp2.x2 < wsp1.x2:
        return True
    else:
        return False

def na_osi_y(wsp1, wsp2):
    if wsp1.y1 > wsp2.y1 and wsp1.y1 < wsp2.y2:
        return True
    elif wsp1.y2 > wsp2.y1 and wsp1.y2 < wsp2.y2:
        return True
    elif wsp2.y1 > wsp1.y1 and wsp2.y1 < wsp1.y2:
        return True
    elif wsp2.y2 > wsp1.y1 and wsp2.y2 < wsp1.y2:
        return True
    else:
        return False
    
def kolizja_lewa(wsp1, wsp2):
    if na_osi_y(wsp1, wsp2):    # sprawdzamy czy współrzędne na osi y przecinają się
        if wsp1.x1 <= wsp2.x2 and wsp1.x1 >= wsp2.x1:       # jeśli tak, to czy punkt x2 pierwszego obieku znajduje sie pomiędzy x1 i x2 drugiego
            return True
    return False

def kolizja_prawa(wsp1, wsp2):
    if na_osi_y(wsp1, wsp2):
        if wsp1.x2 >= wsp2.x1 and wsp1.x2 <= wsp2.x2:
            return True
    return False

def kolizja_góra(wsp1, wsp2):
    if na_osi_x(wsp1, wsp2):
        if wsp1.y1 <= wsp2.y2 and wsp1.y1 >= wsp2.y1:
            return True
    return False

def kolizja_dół(y, wsp1, wsp2):
    if na_osi_x(wsp1, wsp2):
        oblicz_y = wsp1.y2 + y      # tu sprawdzamy czy dolna część jeden obiekt jest dokładnie na drugim, żeby Pan Patyczak mógł spaść jeśli nie ma platformy pod nim
        if oblicz_y >= wsp2.y1 and oblicz_y <= wsp2.y2:
            return True
    return False

class Duszek:
    def __init__ (self, gra):
        self.gra = gra
        self.koniecGry = False
        self.współrzędne = None
    def move(self):
        pass
    def coords(self):
        return self.współrzędne

class DuszekPlatforma(Duszek):
    def __init__(self, gra, obrazek, x, y, szerokość, wysokość):
        Duszek.__init__(self, gra)   # odpalamy klasę nadrzędną, by użyć jej parametrów self i gra
        self.obrazek = obrazek
        self.image = gra.płótno.create_image(x, y, image=self.obrazek, anchor='nw')
        self.współrzędne = Coords(x, y, x + szerokość, y + wysokość)

class RuchomaPlatforma(DuszekPlatforma):    # Zad. 3.
    def __init__(self, gra, obrazek, x, y, szerokość, wysokość):    # Te same parametry co DuszekPlatforma.
        DuszekPlatforma.__init__(self, gra, obrazek, x, y, szerokość, wysokość)
        self.x = 2      # Platforma ma się ruszać.
        self.counter = 0
        self.last_time = time.time()    # Znacznik czasu.
        self.szerokość = szerokość
        self.wysokość = wysokość
    def coords(self):   # Funkcja jak u Pana Patyczaka, ale zamiast stałej szer/wys, odnosimy się do funkcji __init__.
        xy = self.gra.płótno.coords(self.image)
        self.współrzędne.x1 = xy[0]
        self.współrzędne.y1 = xy[1]
        self.współrzędne.x2 = xy[0] + self.szerokość
        self.współrzędne.y2 = xy[1] + self.wysokość
        return self.współrzędne
    def move(self):
        if time.time() - self.last_time > 0.03:
            self.last_time = time.time()
            self.gra.płótno.move(self.image, self.x, 0)
            self.counter = self.counter + 1
            if self.counter > 20:       # Gdy czas przekroczy 20, zmieniamy kierunek i zerujemy czas.
                self.x = self.x * -1
                self.counter = 0

class DuszekPatyczak(Duszek):
    def __init__ (self, gra):
        Duszek.__init__(self, gra)  # nie potrzebujemy więcej zmiennych bo Patyczak jest jeden
        self.obrazki_lewa = [
            PhotoImage(file="patyczak-L1.gif"),
            PhotoImage(file="patyczak-L2.gif"),
            PhotoImage(file="patyczak-L3.gif"),
        ]
        self.obrazki_prawa = [
            PhotoImage(file="patyczak-P1.gif"),
            PhotoImage(file="patyczak-P2.gif"),
            PhotoImage(file="patyczak-P3.gif"),
        ]
        self.image = gra.płótno.create_image(200, 470, image=self.obrazki_lewa[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.bieżący_obrazek = 0
        self.bieżący_obrazek_dodaj = 1
        self.licznik_skoków = 0         # żeby skok nie był w nieskończoność
        self.ostatni_czas = time.time() # ostatni czas zmiany obrazka w trakcie animacji
        self.współrzędne = Coords()
        gra.płótno.bind_all('<KeyPress-Left>', self.obrót_w_lewo)
        gra.płótno.bind_all('<KeyPress-Right>', self.obrót_w_prawo)
        gra.płótno.bind_all('<space>', self.skok)
    def obrót_w_lewo(self, zdarzenie):
        if self.y == 0:     # bo nie można skręcać w trakcie skoku
            self.x = -2
    def obrót_w_prawo(self, zdarzenie):
        if self.y == 0:
            self.x = 2
    def skok(self, zdarzenie):
        if self.y == 0:     # żeby nie skoczył gdy już skacze
            self.y = -4
            self.licznik_skoków = 0
    def animuj(self):
        if self.x !=0 and self.y == 0:          # czyli Patyczak porusza się w lewo lub prawo oraz skacze -> to wtedy należy animować postać
            if time.time() - self.ostatni_czas > 0.1:   # sprawdzamy co 1/10 sekundy
                self.ostatni_czas = time.time()         # resetujemy stoper
                self.bieżący_obrazek += self.bieżący_obrazek_dodaj  # dorzucamy kolejny obrazek (na początku ma wartość 1)
                if self.bieżący_obrazek >= 2:       # gdy dojdziemy do ostatniego obrazka, to wracamy
                    self.bieżący_obrazek_dodaj = -1
                if self.bieżący_obrazek <= 0:       # a gdy do pierwszego to znów liczymy do góry
                    self.bieżący_obrazek_dodaj = 1
        if self.x < 0:              # jeśli porusza się w lewo
            if self.y != 0:         # to jeśli skacze
                self.gra.płótno.itemconfig(self.image, image=self.obrazki_lewa[2])
            else:                   # a jeśli nie skacze
                self.gra.płótno.itemconfig(self.image, image=self.obrazki_lewa[self.bieżący_obrazek])
        elif self.x > 0:              # jeśli porusza się w prawo
            if self.y != 0:         # to jeśli skacze
                self.gra.płótno.itemconfig(self.image, image=self.obrazki_prawa[2])
            else:                   # a jeśli nie skacze
                self.gra.płótno.itemconfig(self.image, image=self.obrazki_prawa[self.bieżący_obrazek])
    def coords(self):
        xy = self.gra.płótno.coords(self.image)     # ustalamy współrzędne obrazka na płótnie
        self.współrzędne.x1 = xy[0]                 # początek Patyczaka w osi x
        self.współrzędne.y1 = xy[1]                 # początek Patyczaka w osi y
        self.współrzędne.x2 = xy[0] + 27            # koniec Patyczaka w osi x
        self.współrzędne.y2 = xy[1] + 30            # koniec Patyczaka w osi y
        return self.współrzędne
    def move(self):
        self.animuj()
        if self.y < 0:                              # Patyczak właśnie skacze
            self.licznik_skoków += 1                # dodajemy y 
            if self.licznik_skoków > 20:            # aż przekroczymy 20 i wtedy
                self.y = 4                          # Patyczk zaczyna spadać        # ! Tu błąd w książce bo zapomnieli wcięcia (str. 265)
        if self.y > 0:                              # Patyczak spada
            self.licznik_skoków -= 1
        wsp = self.coords()
        lewa = True
        prawa = True
        góra = True
        dół = True
        spadanie = True
        if self.y > 0 and wsp.y2 >= self.gra.wysokość_płótna:       # gdy spada ORAZ dotknie dolnej krawędzi
            self.y = 0                                              # to przestaje spadać
            dół = False                                             # już nie trzeba sprawdzać czy dalej spada
        elif self.y < 0 and wsp.y1 <= 0:                            # gdy idzie do góry ORAZ dotknie górnej krawędzi
            self.y = 0                                              # to przestaje iść do góry
            góra = False                                            # i nie trzeba już tego sprawdzać
        if self.x > 0 and wsp.x2 >= self.gra.szerokość_płótna:      # gdy idzie w prawo ORAZ dotknie prawej krawędzi
            self.x = 0                                              # to przestaje iść w prawo
            prawa = False                                           # już nie trzeba sprawdzać czy dalej spada
        elif self.x < 0 and wsp.x1 <= 0:                            # gdy idzie w lewo ORAZ dotknie lewej krawędzi
            self.x = 0                                              # to przestaje iść w lewo
            lewa = False                                            # i nie trzeba już tego sprawdzać
        for duszek in self.gra.duszki:                              # pętlą przechodzimy przez listę duszków
            if duszek == self:                                      # jeśli sprawdzanym duszkiem jestem ja sam to nie sprawdzam bo nie mogę się ze sobą zderzyć
                continue                                            # więc kontynuuję
            duszek_wsp = duszek.coords()                            # sprawdzamy duszka przez wywołanie funkcji coords i zapisanie w zmiennej jego współrzędnych
            if góra and self.y < 0 and kolizja_góra(wsp, duszek_wsp):   # sprawdzamy czy Patyczak a) dotyka górnej krawędzi, b) skacze i c) górną krawędzią nie zderzył się z duszkiem
                self.y = -self.y                                    # Patyczak zaczyna więc spadać
                góra = False                                        # właśnie dotknął góry, więc teraz nie musimy tego dalej sprawdzać
            if dół and self.y > 0 and kolizja_dół(self.y, wsp, duszek_wsp): # sprawdzamy czy Patyczak a) zmienna dół nadal jest True b) spada i c) dolną krawędzią nie zderzył się z duszkiem
                self.y = duszek_wsp.y1 - wsp.y2                     # sprawdzamy ile jest nad innym duszkiem?
                if self.y < 0:                                      # sprawdzamy czy Patyczak się wznosi
                    self.y = 0                                      # jeśli tak to ma przestać
                dół = False                                         # już nie musimy sprawdzać czy od góry lub dołu zderzył się z innym duszkiem
                góra = False
            if dół and spadanie and self.y == 0 and wsp.y2 < self.gra.wysokość_płótna and kolizja_dół(1, wsp, duszek_wsp):
                spadanie = False    # sprawdzamy że zmienna dół to True, że zmienna spadanie też True, nie spada, dolna krawędź nie dotknęłą dolnej krawędzi ekranu a górna górnej
            if lewa and self.x < 0 and kolizja_lewa(wsp, duszek_wsp):    # jeśli kolizja po lewej, porusza się w lewo i kolizja z duszkeim
                self.x = 0                                          # to ma przestać
                lewa = False
                if duszek.koniecGry:
                    self.end(duszek)
            if prawa and self.x > 0 and kolizja_prawa(wsp, duszek_wsp): # analogicznie
                self.x = 0
                prawa = False
                if duszek.koniecGry:
                    self.end(duszek)
        if spadanie and dół and self.y ==0 and wsp.y2 < self.gra.wysokość_płótna:   # powinien zacząć spadać w dół
            self.y = 4
        self.gra.płótno.move(self.image, self.x, self.y)

    def end(self, duszek):              # zadanie 2
        self.gra.biegnie = False
        duszek.otwartedrzwi()
        time.sleep(1)                   # czyli otwarte będą tylko przez sekundę
        self.gra.płótno.itemconfig(self.image, state='hidden')
        duszek.zamkniętedrzwi()

class DuszekDrzwi(Duszek):
    def __init__(self, gra, x, y, szerokość, wysokość):
        Duszek.__init__(self, gra)
        self.zamknięte_drzwi = PhotoImage(file = 'drzwi1.gif')          # Zad. 2. (animowane drzwi)
        self.otwarte_drzwi = PhotoImage(file = 'drzwi2.gif')
        self.image = gra.płótno.create_image(x, y, image=self.zamknięte_drzwi, anchor='nw')  # tworzymy wyświetlany obrazek za pomocą funkcji płótna create_image i w zmiennej obiektowej image zapisujemy zwracany identyfikator
        self.współrzędne = Coords(x, y, x + (szerokość / 2), y + wysokość)          # tutaj dzielimy szerokość na pół żeby Patyczak nie zatrzymał się obok drzwi tylko przed nimi
        self.koniecGry = True           # gdy Patyczak dotrze do drzwi to gra się kończy

    def otwartedrzwi(self):         # zadanie 2
        self.gra.płótno.itemconfig(self.image, image=self.otwarte_drzwi)
        self.gra.tk.update_idletasks()

    def zamkniętedrzwi(self):       # zadanie 2
        self.gra.płótno.itemconfig(self.image, image=self.zamknięte_drzwi)
        self.gra.tk.update_idletasks()
            
g = Gra()
platforma1 = DuszekPlatforma(g, PhotoImage(file="platforma1.gif"), 0, 480, 100, 10)
platforma2 = DuszekPlatforma(g, PhotoImage(file="platforma1.gif"), 150, 440, 100, 10)
platforma3 = DuszekPlatforma(g, PhotoImage(file="platforma1.gif"), 300, 400, 100, 10)
platforma4 = DuszekPlatforma(g, PhotoImage(file="platforma1.gif"), 300, 160, 100, 10)
platforma5 = RuchomaPlatforma(g, PhotoImage(file="platforma2.gif"), 175, 350, 66, 10)
platforma6 = DuszekPlatforma(g, PhotoImage(file="platforma2.gif"), 50, 300, 66, 10)
platforma7 = DuszekPlatforma(g, PhotoImage(file="platforma2.gif"), 170, 120, 66, 10)
platforma8 = DuszekPlatforma(g, PhotoImage(file="platforma3.gif"), 45, 60, 66, 10)
platforma9 = RuchomaPlatforma(g, PhotoImage(file="platforma3.gif"), 170, 250, 32, 10)
platforma10 = DuszekPlatforma(g, PhotoImage(file="platforma3.gif"), 230, 200, 32, 10)
g.duszki.append(platforma1)
g.duszki.append(platforma2)
g.duszki.append(platforma3)
g.duszki.append(platforma4)
g.duszki.append(platforma5)
g.duszki.append(platforma6)
g.duszki.append(platforma7)
g.duszki.append(platforma8)
g.duszki.append(platforma9)
g.duszki.append(platforma10)
drzwi = DuszekDrzwi(g, 45, 30, 40, 35)  # Zad. 2 wymusiło zmianę, bo teraz są 2 obrazki drzwi.
g.duszki.append(drzwi)
sf = DuszekPatyczak(g)
g.duszki.append(sf)             # dodajemy Patyczaka do listy duszków?
g.pętlaGłówna()

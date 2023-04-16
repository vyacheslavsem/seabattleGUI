import time
import random
import re

# ВВЕДЕМ ИМЕНОВАННЫЕ КОНСТАНТЫ
RAND = False     # Использовать AI для имитации Игрока 1

# Размерность игры
RX = 10         # Горизонтальная размерность поля
RY = 10         # Вертикальная размерность поля

# Подписи для поля - легенда координат
# Легенда горизонтальных координат
RH = []
for i in range(RX):
    RH.append(chr(ord('A')+i))
    
# Легенда вертикальных координат
RV = []
for i in range(RY):
    RV.append(" "*(2-len(str(i+1)))+str(i+1))

# Легенды (обозначения) игрового поля
F_SHIP = "S"
F_RESTRICTED = "#"
F_RESTRICTED_EXPOSED = "%"
F_MISS = "*"
F_WOUND = "x"
F_KILL = "X"


# Флаги отображения
ALL = [F_SHIP, F_RESTRICTED, F_RESTRICTED_EXPOSED, F_MISS, F_WOUND, F_KILL]
ALIED = [F_SHIP, F_MISS, F_WOUND, F_KILL]
ENEMY = [F_RESTRICTED_EXPOSED, F_MISS, F_WOUND, F_KILL]
BLOCKED = [F_KILL, F_MISS, F_RESTRICTED, F_RESTRICTED_EXPOSED]

# Состав флота
FLEET = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# Стратегия игроков
# Глобальная переменная



class Ship:
    
    def __init__(self, f, n):
        self.fleet = f  # Флот, в который входит корабль - он же игровое поле
        self.decks = n  # Количество палуб
        
        self.health = n         # Здоровье - количество целых палуб
        self.isSunk = False     # Потоплен или на плаву - На плаву

        res = -1 
        while res == -1:
            res = Ship.getPosition(self, RAND)
        
        self.coords = res
        
    def getPosition(self, r):
        decks = self.decks
        field = self.fleet
        
        rr = False
        if field.name == "A" and r == True:
            rr = True
        if field.name == "E":
            rr = True
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        rr = True
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        res = -1
        
        if rr == False:
            
            MSG = "Введите координаты вашего "+str(decks)+"-палубного корабля: "
            coord = -1
            while coord == -1:
                coord = validate_coord(input(MSG))
                if field.getFieldCoord(coord[0], coord[1], ALL) != "":
                    coord = -1
                    print("Здесь нельзя разместить корабль!")
                    continue
            
            MSG = "Введите направление размещения \t(U)p, (D)own, (L)eft, (R)ight: "
            direct = -1
            while direct == -1:
                direct = input(MSG)
                res = re.search(r"[UDLR]", direct.upper())
                if res == None:
                    direct = -1
                    continue
                direct = res[0]
                
        else:
            coord = -1
            while coord == -1:
                randcoord = str(RH[random.randint(0,RX-1)])+str(RV[random.randint(0, RY-1)])
                
                coord = validate_coord(randcoord)
                if coord == -1:
                    continue
            
                if field.getFieldCoord(coord[0], coord[1], ALL) != "":
                    coord = -1
                    #print("Здесь нельзя разместить корабль!")
                    continue
            
            direct = "UDLR"[random.randint(0,3)]
            
        di=[0]*4    # di = [0, 0, 0, 0]
        dj=[0]*4    # di = [0, 0, 0, 0]
        if direct == "U":
            di = [0, -1, -2, -3]
        if direct == "D":
            di = [0, 1, 2, 3]
        if direct == "L":
            dj = [0, -1, -2, -3]
        if direct == "R":
            dj = [0, 1, 2, 3]
                
        icoord = []
        jcoord = []
                
        for d in range(decks):
            icoord.append(coord[0]+di[d])
            jcoord.append(coord[1]+dj[d])
        
        # Проверяем, чтоб ни одна палуба не была за пределами поля
        # и не пыталась разместиться на занятой клетке
        for d in range(decks):
            i = icoord[d]
            j = jcoord[d]
            if Ship.isAtField(i, j) == False or Field.getFieldCoord(field, i, j, ALL) !="":
                if rr == False:
                    print("Здесь нельзя разместить корабль!")
                return -1
        # Проверки прошли - корабль может быть размещен по данным координатам
        # Печатаем рамку
        for d in range(decks):
           i = icoord[d]
           j = jcoord[d]
           
           Ship.putFrame(field, i, j, False)
        
        # Печатаем корабль поверх рамки
        for d in range(decks):
           i = icoord[d]
           j = jcoord[d]
           
           Field.putFieldCoord(field, i, j, F_SHIP)
        
        # Меняем результат функции с ошибки "-1" на координаты палуб
        res = (icoord, jcoord)
                
        return res
    
    def putFrame(f, i, j, exposed):
        field = f
        icoord = i
        jcoord = j
        
        if exposed == True:
            FLAG = F_RESTRICTED_EXPOSED
        else:
            FLAG = F_RESTRICTED
        
        di = [-1, 0, 1]
        dj = [-1, 0, 1]
        
        for i in range(3):
            for j in range(3):
                field_i = icoord+di[i]
                field_j = jcoord+dj[j]
                if Ship.isAtField(field_i, field_j) == True and\
                    field.getFieldCoord(field_i, field_j, ENEMY) !=F_MISS:
                    field.putFieldCoord(field_i, field_j, FLAG)
    
    def isAtField(i,j):
        res = False
        if (i >=0 and i < RY) and (j >= 0 and j < RX):
            res = True
        
        return res

class Field:
         
    def __init__(self,s):
        self.name = s
        self.__m = [""]*RX*RY
    
    def __str__(self):
        s=""
        for j in range(RX):
            for i in range(RY):
                s += format(self.__m[RX*i+j],"1")
                s+="."
            s += "\n"
            
        return s
    
    def getFieldCoord(self,i,j,F):
        v = self.__m[RX*i+j]
        if v in F:
            return v
        else: 
            return ""
    
    def putFieldCoord(self,i,j,v):
        self.__m[RX*i+j] = v


def validate_coord(s):
    ul=["",""]
    
    ul[0]=RH[-1].lower()
    ul[1]=RH[-1].upper()
    res = re.search(r"[a-"+ul[0]+r"A-"+ul[1]+r"]\s*\d{1,2}", s) 
    
    if res == None:
        return -1
    
    c = res[0]
        
    c[0].upper()
    j = RH.index(c[0].upper())
    
    
    n = re.findall(r"\d+",c)
    i = int(n[0])-1
    if i > RY-1:
        return -1
        
    return i,j


def draw_all(a,e,self):
    # Отрисовка союзного поля
    for i in range(RY):
        for j in range(RX):
            cell = a.getFieldCoord(i,j, ALIED)
            btn = self.fields["A"][i*RX+j]
            if cell != "" or btn.isEnabled() == True:
                draw_Coord(btn,cell)
            
    # Отрисовка вражеского поля
    for i in range(RY):
        for j in range(RX):
            cell = e.getFieldCoord(i,j, ENEMY)
            btn = self.fields["E"][i*RX+j]
            if cell != "" or btn.isEnabled() == True:
                draw_Coord(btn,cell)
            
def draw_Coord(btn, cell):
    if cell == F_SHIP:
        btn.setStyleSheet("border-style: solid;"
                           "border-width: 0px;"
                           "border-color: green;"
                           "image: url(ship.jpg);")
        #btn.setCheckable(True)
        #btn.toggle()
        #btn.setEnabled(False)
        return
    
    if cell == F_WOUND:
        btn.setStyleSheet("border-style: solid;"
                           "border-width: 0px;"
                           "border-color: green;"
                           "image: url(wound.jpg);")
        btn.setCheckable(True)
        btn.toggle()
        btn.setEnabled(False)
        return
    
    if cell == F_MISS:
        btn.setStyleSheet("border-style: solid;"
                           "border-width: 0px;"
                           "border-color: green;"
                           "image: url(miss.jpg);")
        btn.setCheckable(True)
        btn.toggle()
        btn.setEnabled(False)
        return
        
    if cell == F_KILL:
        btn.setStyleSheet("border-style: solid;"
                           "border-width: 0px;"
                           "border-color: green;"
                           "image: url(kill.jpg);")
        btn.setCheckable(True)
        btn.toggle()
        btn.setEnabled(False)
        return
    
    if cell == F_RESTRICTED or cell == F_RESTRICTED_EXPOSED:
        btn.setStyleSheet("border-style: solid;"
                           "border-width: 0px;"
                           "border-color: green;"
                           "background-color: blue;")
        btn.setCheckable(True)
        btn.toggle()
        btn.setEnabled(False)
        return
    
    #btn.setStyleSheet("border-style:solid;"
    #                  'border-width: 1px;'
    #                  "border-color: rgb(20,20,30);"
    #                  "background-color: rgb(20,30,150)")


def AI_move(f, s, self):
    # Объявляем переменную как глобальную
    strategy = self.strategy
    
    print(strategy)
    
    # Определяем, на каком поле будет удар
    field = f
    fleet = s
    
    # Генерируем коодинаты для нанесения удара
    res = -1
    while res == -1:
        # Если в стратегии нет элементов
        # то есть, ранее не было попадания
        #удар наносится совершенно случайно
        if len(strategy[field.name][1]) == 0:
            # Генерируем случайные координаты
            randcoord = str(RH[random.randint(0,RX-1)])+str(RV[random.randint(0, RY-1)])
            
            # Проверяем, что координаты игровые
            res = validate_coord(randcoord)
            if res == -1:
                continue
            # Проверяем, что на поле по координатам нанесения удара ничего нет
            if field.getFieldCoord(res[0], res[1], ENEMY) != "":
                # Если что-то есть - нужны другие координаты
                res = -1
        
        # Ранее было попадание, значит нужно добить
        else:
            # В каком направлении будем бить
            curr_strategy = strategy[field.name][0]
            
            # Прочитали в стратегии координаты следующего удара
            i = strategy[field.name][1][curr_strategy][0][0]
            j = strategy[field.name][1][curr_strategy][0][1]
            
            # Проверили, находятся ли эти координаты на игровом поле
            if Ship.isAtField(i, j) == False:
                # Если не на поле, нужны другие координаты из стратегии
                res = -1
                # Нужно сменить стратегию - направление удара
                change_strat(field,self)
                # Прервать итерацию цикла
                continue
            
            # Переводим координаты стратегии (i,j) в A1-J10
            randcoord=str(RH[j])+str(RV[i])
            
            # Проверяем, что координаты игровые
            res = validate_coord(randcoord)
            if res == -1:
                continue
            # Проверяем, что на поле по координатам нанесения удара ничего нет
            if field.getFieldCoord(res[0], res[1], ENEMY) != "":
                # Если что-то есть - нужны другие координаты
                res = -1
                # Нужна другая стратегия
                change_strat(field,self)
                
    i = res[0]
    j = res[1]
                
    res = check_move(self, i, j)
    self.ResLabel.setText(res)
    draw_all(self.Alied, self.Enemy, self)
    
    #time.sleep(0.5)
    
    if self.win == False:
        
        if res == "MISS":
            self.curr_field = self.Enemy
            self.curr_fleet = self.EFleet
        else:
            AI_move(self.curr_field, self.curr_fleet, self)
    
    
def check_move(self,i,j): 
    strategy = self.strategy            

    field = self.curr_field
    fleet = self.curr_fleet


    # Проверим результат удара
    if field.getFieldCoord(i, j, ALL) != F_SHIP:
        res = "MISS"
        field.putFieldCoord(i, j, F_MISS)
        
        if len(strategy[field.name][1]) != 0 and self.curr_field == self.Alied:
            change_strat(field,self)

    else:
        res = "WOUND"
        field.putFieldCoord(i, j, F_WOUND)
        
        if self.curr_field == self.Alied:
            if len(strategy[field.name][1]) == 0:
                # Создаем новую стратегию
                # Выбор случайного направления для следующих ударов
                curr_strategy = "UDLR"[random.randint(0,3)]
            
                # Описываем стратегию
                strategy[field.name] = [ # strategy["A"] / strategy["E"]
                                    # Текущее направление ударов
                                        curr_strategy,
                                        {
                                            # Стратегия ударов вверх
                                            "U": [[i-1,j],[i-2,j],[i-3,j]],
                                            # Стратегия ударов вниз
                                            "D": [[i+1,j],[i+2,j],[i+3,j]],
                                            # Стратегия ударов влево
                                            "L": [[i,j-1],[i,j-2],[i,j-3]],
                                            # Стратегия ударов вправо
                                            "R": [[i,j+1],[i,j+2],[i,j+3]]
                                        }
                                       ]
            else:
                # Второе попадание в корабль
                
                # Текущее направление удара
                curr_strategy = strategy[field.name][0]
                
                # Удалили из списка координат текущие,
                # по которым было попадание
                # чтобы не бить сюда в следующий раз
                del strategy[field.name][1][curr_strategy][0]
               
                # Определили, какие направления ударов еще есть в стратегии
                options = list(strategy[field.name][1].keys())
                
                # Если текущая результативная стратегия вертикальная
                # (2 попадания по вертикали)
                if curr_strategy == "U" or curr_strategy == "D":
                    
                    # можно убрать горизантальные направления,
                    # если они еще есть                                
                    if ("L" in options) == True:
                        del strategy[field.name][1]["L"]
                    
                    if ("R" in options) == True:
                        del strategy[field.name][1]["R"]
                
                # Если текущая результативная стратегия горизонтальная
                # (2 попадания по горизонтали)
                if curr_strategy == "R" or curr_strategy == "L":
                    
                    # можно убрать вертикальные направления,
                    # если они еще есть                
                    if ("U" in options) == True:
                        del strategy[field.name][1]["U"]
                    
                    if ("D" in options) == True:
                        del strategy[field.name][1]["D"]
                
        
        for ship in fleet:
            
            if i in ship.coords[0] and j in ship.coords[1]:
                ship.health -= 1
                
                if ship.health == 0:
                    ship.isSunk = True
                    res = "KILL"
                    
                    icoord = ship.coords[0]
                    jcoord = ship.coords[1]
                    
                    for d in range(ship.decks):
                        i = icoord[d]
                        j = jcoord[d]
                        Ship.putFrame(field, i, j, True)
                    
                    for d in range(ship.decks):
                        i = icoord[d]
                        j = jcoord[d]
                        field.putFieldCoord(i, j, F_KILL)
                    
                    fleet.remove(ship)
                    
                    if self.curr_field == self.Alied:
                        strategy[field.name][1]={}
    if len(self.curr_fleet) == 0:
        self.win = True
        res = "THE END!!!"
    return res

def change_strat(field, self):
    # Эта функция меняет стратегию на новую, допустимую
    # Стратегиядобивания - направление нанесения удара UDLR
    
    # объявляем переменную глобальной
    strategy = self.strategy
    
    # Прочитали текущую стратегию
    curr_strategy = strategy[field.name][0]
    
    # Удалили координаты по текущей стратегии
    del strategy[field.name][1][curr_strategy]
    
    # Прочитали набор оставшихся направлений нанесения удара
    options = list(strategy[field.name][1].keys())
    
    # Выбрали случайное направление удара
    curr_strategy = options[random.randint(0, len(options)-1)]
    
    # Внесли это направление в стратегию как текущую стратегию
    strategy[field.name][0] = curr_strategy
    
    
def NGStart(self):
    
    Alied = Field("A")
    Enemy = Field("E")
    
    self.ClearField()
    self.MoveLabel.setText('')
    
    print(Alied, Enemy)
    
    #print_all(Alied, Enemy, self)
    draw_all(Alied,Enemy, self)
     
    AFleet = []
    for decks in FLEET:
            AFleet.append(Ship(Alied,decks))
            #print_all(Alied, Enemy, self)
            draw_all(Alied,Enemy, self)
    
    EFleet = []
    for decks in FLEET:
            EFleet.append(Ship(Enemy,decks))
         
    #print_all(Alied, Enemy, self)
    draw_all(Alied,Enemy, self)

    # Текущий игрок - человек (A - Alied)
    curr_player = "A"
    # Текущее поля для хода - вражеское (Enemy)
    curr_field = Enemy
    # Текущий флот для удара - вражеский (Enemy)
    curr_fleet = EFleet
    
    nmove = 1
    win = False
    
    Game = [[Alied, Enemy],
            [AFleet, EFleet],
            [curr_player, curr_field, curr_fleet, nmove, win]]
    
    self.initGame(Game)

    
    


# \d    - любая цифра
# \d+   - Любая последовательность цифр (1 и более)
# \d*   - Любая последовательность цифр (0 и более)
# .     - Любой знак
# \w    - Любая буква, цифра или "_"
# \w+   - Любая последовательность букв, цифр или "_" (1 и более)
# \w*   - Любая последовательность букв, цифр или "_" (0 и более)
# \d{3} - Последовательность строго из 3 цифр 
# \d{1,3} - Последовательность из от 1 до 3 цифр
# [a-jA-J] - Любой символ из []
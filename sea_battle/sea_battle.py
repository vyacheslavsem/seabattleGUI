from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from s_b import *
import pickle

# ВВЕДЕМ ИМЕННЫЕ КОНСТАНТЫ
# Параметры окна
WIN_SPC =         30
F_LEGEND_SIZE =   30
F_CELL_SIZE =     30
F_SPC =           40

F_INNER_SPC =     30
LEGEND_SIZE =     30
IN_SIZE =         30


WIN_X = 2*WIN_SPC+(2*F_LEGEND_SIZE+F_CELL_SIZE*RX)*2+F_SPC
WIN_Y = 2*WIN_SPC+LEGEND_SIZE+2*F_LEGEND_SIZE+F_CELL_SIZE*RY+\
        F_INNER_SPC+LEGEND_SIZE+IN_SIZE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        
        self.setFixedSize(WIN_X,WIN_Y)
        self.setWindowTitle("Sea Battle")
        self.draw_GUI()
        
        self.fields = {}
        self.draw_Field("A")
        self.draw_Field("E")
        self.strategy = {"A":[0,{}], "E":[0,{}]}
        
    def draw_GUI(self):
        
        self.draw_Legend()
        
        # Создадим подписи интерфейса
        # Введите координаты
        self.Lbl = QLabel("Введите координаты:", self)
        self.Lbl.setGeometry(WIN_SPC + F_LEGEND_SIZE,
                             WIN_Y - WIN_SPC - IN_SIZE - LEGEND_SIZE,
                            F_CELL_SIZE*6,
                            LEGEND_SIZE)
        self.Lbl.setAlignment(Qt.AlignLeft)
        self.Lbl.setStyleSheet("border-style: solid;"
                               "border-width: 0px;"
                               "border-color: black;"
                               "font-size:15px;"
                               "font-family: Andale Mono;"
                               "font-weight: bold;")
        
        # Ход
        self.Lbl = QLabel("Ход:", self)
        self.Lbl.setGeometry(WIN_SPC+F_LEGEND_SIZE+\
                             F_CELL_SIZE*RX,
                             WIN_Y - WIN_SPC - IN_SIZE - LEGEND_SIZE,
                             F_SPC+2*F_LEGEND_SIZE,
                             LEGEND_SIZE)
        self.Lbl.setAlignment(Qt.AlignCenter)
        self.Lbl.setStyleSheet("border-style: solid;"
                               "border-width: 0px;"
                               "border-color: black;"
                               "font-size:15px;"
                               "font-family: Andale Mono;"
                               "font-weight: bold;")
        
        # Поле для ввода координат
        self.Coord = QLineEdit(self)
        self.Coord.setGeometry(WIN_SPC + F_LEGEND_SIZE,
                               WIN_Y - WIN_SPC - IN_SIZE,
                               F_CELL_SIZE*6,
                               IN_SIZE)
        self.Coord.setStyleSheet("border-style: solid;"
                                 "border-width: 3px;"
                                 "border-color: black;"
                                 "font-size:15px;"
                                 "font-family: Andale Mono;"
                                 "font-weight: bold;")
        
        # Кнопка ОК
        self.btnOK = QPushButton('OK', self)
        self.btnOK.setGeometry(WIN_SPC + F_LEGEND_SIZE + F_CELL_SIZE*7,
                               WIN_Y - WIN_SPC - IN_SIZE,
                               F_CELL_SIZE*2,
                               IN_SIZE)
        self.btnOK.clicked.connect(self.btnOK_clk)
        
        
        
        # Добавим поле для отображения хода
        self.MoveLabel = QLineEdit(self)
        self.MoveLabel.setGeometry(WIN_SPC+2*F_LEGEND_SIZE+\
                                   F_CELL_SIZE*RX,
                                   WIN_Y - WIN_SPC - IN_SIZE,
                                   F_SPC,
                                   IN_SIZE)
        self.MoveLabel.setAlignment(Qt.AlignCenter)
        self.MoveLabel.setStyleSheet("border-style: solid;"
                                     "border-width: 3px;"
                                     "border-color: black;"
                                     "font-size:15px;"
                                     "font-family: Andale Mono;"
                                     "font-weight: bold;")
        self.MoveLabel.setEnabled(False)
        self.MoveLabel.textChanged.connect(self.valCh)
        
        
        # Поле отображения результата хода
        self.ResLabel = QLabel('',self)
        self.ResLabel.setGeometry(WIN_SPC+3*F_LEGEND_SIZE+\
                                   F_CELL_SIZE*RX + F_SPC + F_CELL_SIZE,
                                   WIN_Y - WIN_SPC - IN_SIZE,
                                   F_CELL_SIZE*6,
                                   IN_SIZE)
        self.ResLabel.setAlignment(Qt.AlignCenter)
        self.ResLabel.setStyleSheet("border-style: solid;"
                                     "border-width: 0px;"
                                     "border-color: black;"
                                     "font-size:15px;"
                                     "font-family: Andale Mono;"
                                     "font-weight: bold;"
                                     "color: rgb(200,0,50)")
        
        # Добавить кнопку "Новая игра"
        self.NGbtn = QPushButton("Новая игра", self)
        self.NGbtn.setFixedSize(90, 35)
        self.NGbtn.move(WIN_X-WIN_SPC-100,
                        WIN_SPC+3*F_LEGEND_SIZE+F_CELL_SIZE*RY)
        self.NGbtn.clicked.connect(lambda : NGStart(self))
        
        # Добавить кнопку "Сохранить игру"
        self.SGbtn = QPushButton("Сохранить игру", self)
        self.SGbtn.setFixedSize(90, 35)
        self.SGbtn.move(WIN_X-WIN_SPC-100,
                        WIN_SPC+3*F_LEGEND_SIZE+F_CELL_SIZE*RY+40)
        self.SGbtn.clicked.connect(self.SGame)
        
        # Добавить кнопку "Загрузить игру"
        self.LGbtn = QPushButton("Загрузить игру", self)
        self.LGbtn.setFixedSize(90, 35)
        self.LGbtn.move(WIN_X-WIN_SPC-100,
                        WIN_SPC+3*F_LEGEND_SIZE+F_CELL_SIZE*RY+80)
        self.LGbtn.clicked.connect(self.LGame)
        
    
    def SGame(self):
        dumpfile = None
        SaveGame = [self.Alied,
                    self.Enemy,
                    self.AFleet,
                    self.EFleet,
                    self.curr_player,
                    self.curr_field,
                    self.curr_fleet,
                    self.nmove,
                    self.win,
                    self.strategy]
        
        try:
            dumpfile = open("seabattle.sav", "wb")
            print("Saving...")
            self.ResLabel.setText("Saving...")
            res = pickle.dump(SaveGame, dumpfile)
        except:
            print("Error Saving Game!\n")
            self.ResLabel.setText("Error Saving Game!")
        else:
            print("DONE!")
            self.ResLabel.setText("Saving...DONE!")
        finally:
            if dumpfile != None:
                dumpfile.close()
            
        
    def LGame(self):

        dumpfile = None
        
        try:
            dumpfile = open("seabattle.sav", "rb")
            print("Loading")
            SaveGame = pickle.load(dumpfile)
        except:
            print("Error Loading Game!\n")
            self.ResLabel.setText("ERROR Loading Game!")
        else:
            print("DONE!")
            self.ResLabel.setText("Loading...DONE!")
            
            self.Alied = SaveGame[0]
            self.Enemy = SaveGame[1]
            self.AFleet = SaveGame[2]
            self.EFleet = SaveGame[3]
            self.curr_player = SaveGame[4]
            self.curr_field = SaveGame[5]
            self.curr_fleet = SaveGame[6]
            self.nmove = SaveGame[7]
            self.win = SaveGame[8]
            self.strategy = SaveGame[9]
            
            self.ClearField()
            
            draw_all(self.Alied,self.Enemy,self)
            
        finally:
            if dumpfile != None:
                dumpfile.close()
            
    
    def valCh(self):
        text = self.MoveLabel.text()
        coord = validate_coord(text)
        i = coord[0]
        j = coord[1]

        res = check_move(self, i, j)
        self.ResLabel.setText(res)
        draw_all(self.Alied, self.Enemy, self)
        
        if res == "MISS":
            self.curr_field = self.Alied
            self.curr_fleet = self.AFleet
            AI_move(self.curr_field, self.curr_fleet, self)
            
    def initGame(self, game):
        self.game = game
        
        self.Alied = game[0][0]
        self.Enemy = game[0][1]
        self.AFleet = game[1][0]
        self.EFleet = game[1][1]
        self.curr_player = game[2][0]
        self.curr_field = game[2][1]
        self.curr_fleet = game[2][2]
        self.nmove = game [2][3]
        self.win = game[2][4]
        
    def btnOK_clk(self):

        
        coord = validate_coord(self.Coord.text())
        
        
        if coord != -1:
            f = str(RH[coord[1]])+str(RV[coord[0]])
            self.MoveLabel.setText(f)
            self.ResLabel.setText('')
        else:
            self.ResLabel.setText("Неверные координаты!")
            self.MoveLabel.setText('')
            return
        
        
    def draw_Legend(self): 
        # Создадим легенду полей
        # Легенда над полем союзника(СОЮЗНИК)
        labelA = QLabel("Союзник", self)
        labelA.setGeometry(WIN_SPC+F_LEGEND_SIZE,
                           WIN_SPC,
                           F_CELL_SIZE*RX,
                           F_LEGEND_SIZE)
        labelA.setAlignment(Qt.AlignCenter)
        labelA.setStyleSheet("border-style: solid;"
                             "border-width: 1px;"
                             "border-color: red;"
                             "font-size:30px;"
                             "font-family: Andale Mono;"
                             "font-weight: bold;")
        
        # Легенда над полем противинка(ПРОТИВНИК)
        labelE = QLabel("Противник", self)
        labelE.setGeometry(WIN_SPC+3*F_LEGEND_SIZE+F_CELL_SIZE*RX+F_SPC,
                           WIN_SPC,
                           F_CELL_SIZE*RX,
                           F_LEGEND_SIZE)
        labelE.setAlignment(Qt.AlignCenter)
        labelE.setStyleSheet("border-style: solid;"
                             "border-width: 1px;"
                             "border-color: blue;"
                             "font-size:30px;"
                             "font-family: Andale Mono;"
                             "font-weight: bold;")
        
        # Легенда координат полей
        # Горизонтальные координаты RH
        # Координаты союзника
        
        for i in range(RX):
            label = QLabel(RH[i],self)
            label.setGeometry(WIN_SPC+F_LEGEND_SIZE+F_CELL_SIZE*i,
                              WIN_SPC+F_LEGEND_SIZE,
                              F_CELL_SIZE,
                              F_LEGEND_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
            
        for i in range(RX):
            label = QLabel(RH[i],self)
            label.setGeometry(WIN_SPC+F_LEGEND_SIZE+F_CELL_SIZE*i,
                              WIN_SPC+F_LEGEND_SIZE*2+F_CELL_SIZE*RY,
                              F_CELL_SIZE,
                              F_LEGEND_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
            
            
        # Координаты противника    
        for i in range(RX):
            label = QLabel(RH[i],self)
            label.setGeometry(WIN_SPC+3*F_LEGEND_SIZE+\
                              F_SPC+F_CELL_SIZE*RX+F_CELL_SIZE*i,
                              WIN_SPC+F_LEGEND_SIZE,
                              F_CELL_SIZE,
                              F_LEGEND_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )   
            
        for i in range(RX):
            label = QLabel(RH[i],self)
            label.setGeometry(WIN_SPC+3*F_LEGEND_SIZE+\
                              F_SPC+F_CELL_SIZE*RX+F_CELL_SIZE*i,
                              WIN_SPC+F_LEGEND_SIZE*2+F_CELL_SIZE*RY,
                              F_CELL_SIZE,
                              F_LEGEND_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 ) 
            
        # Вертикальные координаты RV
        # Координаты союзника
        for i in range(RY):
            label = QLabel(RV[i],self)
            label.setGeometry(WIN_SPC,
                              WIN_SPC+2*F_LEGEND_SIZE+F_CELL_SIZE*i,
                              F_LEGEND_SIZE,
                              F_CELL_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
            
        for i in range(RY):
            label = QLabel(RV[i],self)
            label.setGeometry(WIN_SPC+F_CELL_SIZE*RX+F_LEGEND_SIZE,
                              WIN_SPC+2*F_LEGEND_SIZE+F_CELL_SIZE*i,
                              F_LEGEND_SIZE,
                              F_CELL_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
            
            
        # Координаты противника
        for i in range(RY):
            label = QLabel(RV[i],self)
            label.setGeometry(WIN_SPC+F_SPC+F_CELL_SIZE*RX+2*F_LEGEND_SIZE,
                              WIN_SPC+2*F_LEGEND_SIZE+F_CELL_SIZE*i,
                              F_LEGEND_SIZE,
                              F_CELL_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
            
        for i in range(RY):
            label = QLabel(RV[i],self)
            label.setGeometry(WIN_SPC+F_SPC+F_CELL_SIZE*RX*2+F_LEGEND_SIZE*3,
                              WIN_SPC+2*F_LEGEND_SIZE+F_CELL_SIZE*i,
                              F_LEGEND_SIZE,
                              F_CELL_SIZE)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: blue;"
                                 "font-size:18px;"
                                 "font-family: Book Antiqua;"
                                 )
        
        
    def draw_Field(self, name):
        
        if name == "A":
            FIELD_START = 0
            e = True
        else:
            FIELD_START = F_CELL_SIZE*RX+F_SPC+2*F_LEGEND_SIZE
            e = False
         
            
        self.fields[name]=[] 
        for j in range(RY):
            for i in range(RX):
                
                btn_name=RH[i]+RV[j]
                self.btn = QPushButton('', self)
                self.setObjectName(btn_name)
                self.btn.setFixedSize(F_CELL_SIZE, F_CELL_SIZE)
                self.btn.move(WIN_SPC+F_LEGEND_SIZE+FIELD_START+F_CELL_SIZE*i,
                              WIN_SPC+2*F_LEGEND_SIZE+F_CELL_SIZE*j)
                self.btn.setStyleSheet("border-style:solid;"
                                       'border-width: 1px;'
                                       "border-color: rgb(20,20,30);"
                                       "background-color: rgb(20,30,150)")
                self.btn.clicked.connect(lambda a, btn_name=btn_name: self.btn_clk(btn_name))
                self.fields[name].append(self.btn)
    
    def ClearField(self):
        for name in ["A", "E"]:
            for b in self.fields[name]:
                b.setStyleSheet("border-style:solid;"
                                'border-width: 1px;'
                                "border-color: rgb(20,20,30);"
                                "background-color: rgb(20,30,150);"
                                "background-image: none")
                b.setEnabled(True)            
    
    def btn_clk(self, name):
        self.MoveLabel.setText(name)
        
        
app = QApplication([])

win = MainWindow()
win.show()
print(WIN_X, WIN_Y)
app.exec()

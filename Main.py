import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import re
from PyQt5.QtCore import *
import googletrans
from googletrans import LANGUAGES, Translator
import pyqtgraph as pg

db = sqlite3.connect('Data.db')
cr = db.cursor()
cr.execute("Create table if not exists user(name text, email text, password text, ID int auto_increment primary key)")
task_cr = db.cursor()
task_cr.execute("Create table if not exists tasks(task text, email text)")
task_cr.execute("Create table if not exists pomodoro(task text, email text)")
task_cr.execute("Create table if not exists notes(title text, note text, email text)")


class WelcomePage(QWidget):
    def __init__(self):
        super(WelcomePage, self).__init__()

        with open('style/welcome.css') as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setWindowTitle('Productivity Club')
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(50, 0, 50, 50)

        welcome_text = QLabel("Welcome To")
        welcome_text.setObjectName('wel')

        txt2 = QLabel("Productivity Club")
        txt2.setObjectName("txt2")

        welcome_text.setAlignment(Qt.AlignCenter)
        txt2.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Login")
        sign_up_button = QPushButton("Sign Up")
        login_button.setObjectName("login")
        sign_up_button.setObjectName("login")

        main_layout.addWidget(welcome_text)
        main_layout.addWidget(txt2)
        main_layout.addWidget(login_button)
        main_layout.addWidget(sign_up_button)

        def go_to_login():
            Windows.setCurrentIndex(1)

        login_button.clicked.connect(go_to_login)

        def go_to_signup():
            Windows.setCurrentIndex(2)

        sign_up_button.clicked.connect(go_to_signup)
        self.setLayout(main_layout)


class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        with open("style/login.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Login")
        lb1.setObjectName("lb1")
        lb2 = QLabel("Enter Your Email And Password")
        lb2.setObjectName("lb2")

        lb1.setAlignment(Qt.AlignCenter)
        lb2.setAlignment(Qt.AlignCenter)

        email_field = QLineEdit()
        email_field.setPlaceholderText("Email")
        email_field.setObjectName("field")

        #0779C1
        btnToggle = QToolButton(email_field)
        btnToggle.setIcon(QIcon('Icons/email.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 29, 20, 20)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setPlaceholderText("Password")
        password_field.setObjectName("field")

        btnToggle = QToolButton(password_field)
        btnToggle.setIcon(QIcon('Icons/lock.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 29, 20, 20)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        login_btn = QPushButton("Login")
        login_btn.setObjectName("login")

        # main_layout.addWidget(back)
        main_layout.addWidget(lb1)
        main_layout.addWidget(lb2)
        main_layout.addWidget(email_field)
        main_layout.addWidget(password_field)
        main_layout.addWidget(login_btn)
        main_layout.insertSpacing(1, 50)
        main_layout.insertSpacing(2, 10)

        def go_back():
            Windows.setCurrentIndex(0)

        def check_input():
            cr.execute(f"select name , email , password from user "
                       f"where email='{email_field.text()}' and password='{password_field.text()}'")
            result = cr.fetchall()
            if email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif len(result) >= 1:
                # SET USER DATA
                home_page = Home(result[0][0], email_field.text(), password_field.text())
                Windows.addWidget(home_page)  # 8
                Windows.setCurrentIndex(Windows.count() - 1)
            else:
                QMessageBox.warning(self, "warning", "Email and Password are incorrect", QMessageBox.Ok)

        back.clicked.connect(go_back)
        login_btn.clicked.connect(check_input)
        self.setLayout(main_layout)


class SignPage(QWidget):
    def __init__(self):
        super(SignPage, self).__init__()

        with open("style/signup.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 0, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Sign Up")
        lb1.setObjectName("lb1")
        lb1.setAlignment(Qt.AlignCenter)

        name = QLineEdit()
        name.setPlaceholderText("Your Name")
        name.setObjectName("field")

        btnToggle = QToolButton(name)
        btnToggle.setIcon(QIcon('Icons/user.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 26, 15, 15)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        email_field = QLineEdit()
        email_field.setPlaceholderText("Email")
        email_field.setObjectName("field")

        btnToggle = QToolButton(email_field)
        btnToggle.setIcon(QIcon('Icons/email.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 26, 15, 15)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setPlaceholderText("Password")
        password_field.setObjectName("field")

        btnToggle = QToolButton(password_field)
        btnToggle.setIcon(QIcon('Icons/lock.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 26, 15, 15)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        co_password_field = QLineEdit()
        co_password_field.setEchoMode(QLineEdit.Password)
        co_password_field.setPlaceholderText("Confirm Password")
        co_password_field.setObjectName("field")

        btnToggle = QToolButton(co_password_field)
        btnToggle.setIcon(QIcon('Icons/lock.png'))
        btnToggle.setCursor(Qt.ArrowCursor)
        btnToggle.setGeometry(20, 26, 15, 15)
        btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; background-color: rgba(231, 231, 231, 0);}')

        signup_btn = QPushButton("Sign Up")
        signup_btn.setObjectName("signup")

        def sign():
            cr.execute(f"select email from user")
            emails = cr.fetchall()
            reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            is_email = re.fullmatch(reg, email_field.text())
            if name.text() == "" or email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif password_field.text() != co_password_field.text():
                QMessageBox.warning(self, "warning", "Password and Confirm Password aren't the same", QMessageBox.Ok)
            elif (email_field.text(),) in emails:
                QMessageBox.warning(self, "warning", "This Email is already used, Please use another one",
                                    QMessageBox.Ok)
            elif not is_email:
                QMessageBox.warning(self, "warning", "Please enter a valid email \nSuch as : Mostafa_12@gmail.com ",
                                    QMessageBox.Ok)
            else:
                cr.execute(
                    f"insert into user values('{name.text()}', '{email_field.text()}', '{password_field.text()}')")
                db.commit()
                # db.close()
                home_p = Home(name.text(), email_field.text(), password_field.text())
                Windows.addWidget(home_p)
                Windows.setCurrentIndex(Windows.count() - 1)

        signup_btn.clicked.connect(sign)

        def go_back():
            Windows.setCurrentIndex(0)

        back.clicked.connect(go_back)

        main_layout.addWidget(lb1)
        main_layout.addWidget(name)
        main_layout.addWidget(email_field)
        main_layout.addWidget(password_field)
        main_layout.addWidget(co_password_field)
        main_layout.addWidget(signup_btn)

        self.setLayout(main_layout)


class Btn(QPushButton):
    def __init__(self, path):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(50, 50))
        with open("style/btn.css") as file:
            style = file.read()
            self.setStyleSheet(style)


class Home(QWidget):
    def __init__(self, user_name, email, password):
        super().__init__()

        with open("style/home.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 30)

        home_icon = QPushButton()
        home_icon.setIcon(QIcon("Icons/home.png"))
        home_icon.setIconSize(QSize(40, 40))

        txt1 = QLabel("Name : " + user_name)
        txt1.setObjectName("name")
        change_name = QPushButton()
        change_name.setIcon(QIcon("Icons/pencil.png"))
        change_name.setIconSize(QSize(20, 20))
        change_name.setFixedSize(35, 35)
        change_name.setObjectName("pen")

        def c_name():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set name='{text}' where email='{email}' and password='{password}'")
                db.commit()
                txt1.setText("Name : " + text)

        change_name.clicked.connect(c_name)

        name_lay = QHBoxLayout()
        name_lay.addWidget(txt1)
        name_lay.addWidget(change_name)

        txt2 = QLabel("Email : " + email)
        txt2.setObjectName("name")
        change_email = QPushButton()
        change_email.setIcon(QIcon("Icons/pencil.png"))
        change_email.setIconSize(QSize(20, 20))
        change_email.setFixedSize(35, 35)
        change_email.setObjectName("pen")

        def c_email():
            text, ok = QInputDialog().getText(self, "Change Your Email", "Email :", QLineEdit.Normal)
            if ok:
                reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                is_email = re.fullmatch(reg, text)
                if is_email:
                    cr.execute("select email from user")
                    emails = cr.fetchall()
                    if (text,) in emails:
                        QMessageBox.warning(self, "warning", "This Email is already used, Please use another one",
                                            QMessageBox.Ok)
                    else:
                        cr.execute(f"update user set email='{text}' where email='{email}' and password='{password}'")
                        db.commit()
                        txt2.setText("Email : " + text)
                else:
                    QMessageBox.warning(self, "warning", "Please enter a valid email \nSuch as : Mostafa_12@gmail.com ",
                                        QMessageBox.Ok)

        change_email.clicked.connect(c_email)

        email_lay = QHBoxLayout()
        email_lay.addWidget(txt2)
        email_lay.addWidget(change_email)

        txt3 = QLabel("Password : " + len(password) * "*")
        txt3.setObjectName("name")
        change_pass = QPushButton()
        change_pass.setIcon(QIcon("Icons/pencil.png"))
        change_pass.setIconSize(QSize(20, 20))
        change_pass.setFixedSize(35, 35)
        change_pass.setObjectName("pen")

        def c_pass():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set password='{text}' where email='{email}' ")
                db.commit()
                txt3.setText("Password : " + len(text) * "*")
                password = text

        change_pass.clicked.connect(c_pass)

        pass_lay = QHBoxLayout()
        pass_lay.addWidget(txt3)
        pass_lay.addWidget(change_pass)

        txt4 = QLabel("Our Features")
        txt4.setObjectName("title")
        txt4.setAlignment(Qt.AlignCenter)

        hl1 = QHBoxLayout()
        hl2 = QHBoxLayout()

        vl1 = QVBoxLayout()
        vl2 = QVBoxLayout()
        vl3 = QVBoxLayout()
        vl4 = QVBoxLayout()
        vl5 = QVBoxLayout()
        vl6 = QVBoxLayout()
        task = Btn("Icons/task.png")
        l_task = QLabel("Tasks")
        l_task.setObjectName("IconLabel")
        l_task.setAlignment(Qt.AlignCenter)
        vl1.addWidget(task)
        vl1.addWidget(l_task)

        timer = Btn("Icons/timer.png")
        l_timer = QLabel("Pomodoro")
        l_timer.setObjectName("IconLabel")
        l_timer.setAlignment(Qt.AlignCenter)
        vl2.addWidget(timer)
        vl2.addWidget(l_timer)

        note = Btn("Icons/Note.png")
        l_note = QLabel("Note")
        l_note.setObjectName("IconLabel")
        l_note.setAlignment(Qt.AlignCenter)
        vl3.addWidget(note)
        vl3.addWidget(l_note)

        hl1.addLayout(vl1)
        hl1.addLayout(vl2)
        hl1.addLayout(vl3)

        converter = Btn("Icons/converter.png")
        l_converter = QLabel("Converter")
        l_converter.setObjectName("IconLabel")
        l_converter.setAlignment(Qt.AlignCenter)
        vl4.addWidget(converter)
        vl4.addWidget(l_converter)

        translator = Btn("Icons/translator.png")
        l_translator = QLabel("Translator")
        l_translator.setObjectName("IconLabel")
        l_translator.setAlignment(Qt.AlignCenter)
        vl5.addWidget(translator)
        vl5.addWidget(l_translator)

        graph = Btn("Icons/graph.png")
        l_graph = QLabel("Graph")
        l_graph.setObjectName("IconLabel")
        l_graph.setAlignment(Qt.AlignCenter)
        vl6.addWidget(graph)
        vl6.addWidget(l_graph)

        hl2.addLayout(vl4)
        hl2.addLayout(vl5)
        hl2.addLayout(vl6)

        btn_lay = QVBoxLayout()
        btn_lay.addLayout(hl1)
        btn_lay.addLayout(hl2)
        btn_lay.insertSpacing(1, 20)
        btn_lay.setSpacing(2)

        def to_task():
            task_page.set_email(email)
            Windows.addWidget(task_page)
            Windows.setCurrentIndex(Windows.count() - 1)

        task.clicked.connect(to_task)

        def to_timer():
            timer_page.set_data(email)
            Windows.addWidget(timer_page)
            Windows.setCurrentIndex(Windows.count() - 1)

        timer.clicked.connect(to_timer)

        def to_note():
            note_page.set_email(email)
            Windows.addWidget(note_page)
            Windows.setCurrentIndex(Windows.count() - 1)

        note.clicked.connect(to_note)

        def to_converter():
            Windows.setCurrentIndex(3)

        converter.clicked.connect(to_converter)

        def to_translator():
            Windows.setCurrentIndex(4)

        translator.clicked.connect(to_translator)

        def to_graph():
            Windows.setCurrentIndex(5)

        graph.clicked.connect(to_graph)

        main_layout.addWidget(home_icon)
        main_layout.addLayout(name_lay)
        main_layout.addLayout(email_lay)
        main_layout.addLayout(pass_lay)
        main_layout.addWidget(txt4)
        main_layout.addLayout(btn_lay)
        main_layout.setSpacing(20)
        main_layout.insertSpacing(4, 50)
        self.setLayout(main_layout)


class TaskButton(QPushButton):
    def __init__(self, task, email):
        super().__init__(f"   {task}")
        self.setIcon(QIcon("Icons/check.png"))

        def update():
            task_cr.execute(f"insert into pomodoro values ('{task}','{email}')")
            db.commit()
            task_cr.execute(f"delete from tasks where task='{task}' and email='{email}'")
            db.commit()
            task_page.ClearLayout(task_page.main_lay)
            task_page.reload_UI()

        self.clicked.connect(update)


class Task(QMainWindow):
    def __init__(self, email):
        super().__init__()
        # Mostafa
        self.email = email
        self.widget = QWidget()
        with open("Style/task.css") as file:
            style = file.read()
            self.widget.setStyleSheet(style)
        self.setStyleSheet("QScrollBar{ background-color: none }")

        self.scroll = QScrollArea()
        self.main_lay = QVBoxLayout()
        self.main_lay.setContentsMargins(20, 50, 20, 10)

        back = QPushButton(self.widget)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        self.logo = QPushButton()
        self.logo.setIcon(QIcon("Icons/task.png"))
        self.logo.setIconSize(QSize(60, 60))
        self.logo.setObjectName("logo")

        self.title = QLabel("To-Do List")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.add = QPushButton()
        self.add.setObjectName("add")
        self.add.setIcon(QIcon("Icons/add.png"))
        self.add.setIconSize(QSize(20, 20))
        self.add.setFixedWidth(40)

        note = QLabel("On clicking on a task \nit will be moved to Pomodoro technique")
        note.setObjectName("note")

        self.add_lay = QHBoxLayout()
        self.add_lay.addWidget(note)
        self.add_lay.addWidget(self.add)

        self.sub_title = QLabel("Your To-Do List")
        self.sub_title.setObjectName("sub")
        self.sub_title.setAlignment(Qt.AlignCenter)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.setCentralWidget(self.scroll)
        self.resize(300, 200)
        self.reload_UI()

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

    def add_item(self):
        text, ok = QInputDialog().getText(self.widget, "Add new task", "New Task : ", QLineEdit.Normal)
        if ok:
            task_cr.execute(f"insert into tasks values ('{text}','{self.email}')")
            db.commit()
            self.ClearLayout(self.main_lay)
            self.reload_UI()

    def set_email(self, email):
        self.email = email
        self.add.clicked.connect(self.add_item)
        self.ClearLayout(self.main_lay)
        self.reload_UI()

    def reload_UI(self):
        self.main_lay.addWidget(self.logo)
        self.main_lay.addWidget(self.title)
        self.main_lay.addLayout(self.add_lay)
        self.main_lay.addWidget(self.sub_title)
        self.main_lay.alignment()
        task_cr.execute(f"select task from tasks where email='{self.email}'")
        tasks = task_cr.fetchall()
        if len(tasks) == 0:
            self.sub_title.setText("Your To-Do List Is Empty")
        else:
            self.sub_title.setText("Your To-Do List")

        for task in tasks:
            add_task = TaskButton(task[0], self.email)
            add_task.setObjectName("task")
            self.main_lay.addWidget(add_task)
        self.main_lay.insertSpacing(2, 40)
        self.widget.setLayout(self.main_lay)

    def ClearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() == self.sub_title or \
                        child.widget() == self.title or \
                        child.layout() == self.add_lay or \
                        child.widget() == self.logo:
                    continue
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.ClearLayout(child.layout())


class Timer(QWidget):
    def __init__(self, email):
        super().__init__()
        with open("Style/promo.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        self.email = 'test'
        self.s = 0
        self.m = 25

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 150, 30, 30)
        self.main_layout.setSpacing(10)

        self.setWindowTitle("                                               MY Pomodoro")

        self.time_lab = QLabel("25:00", self)
        self.time_lab.setGeometry(180, 65, 150, 100)
        self.time_lab.resize(114, 60)
        self.time_lab.setObjectName("la")
        self.time_lab.setAlignment(Qt.AlignCenter)

        self.sub_tit = QLabel(" My Pomodoro")
        self.sub_tit.setObjectName("sub")
        self.sub_tit.setAlignment(Qt.AlignCenter)

        self.finish = QLabel("You finsh your tasks\n successfully \n go to 'To-Do List'\nand choose the tasks ")
        self.finish.setObjectName("sub")
        self.finish.setAlignment(Qt.AlignCenter)

        self.ti = QTimer()
        self.ti.setInterval(1000)

    def delete_data(self):
        task_cr.execute(f"delete from pomodoro where email='{self.email}'")
        db.commit()

    def stop(self):
        self.ti.stop()

    def start(self):
        self.ti.start()

    def re(self):
        self.m = 25
        self.s = 0
        self.time_lab.setText(f"25:00")

    def counter(self):
        if self.s == 0 and self.m == 0:
            self.stop()
            self.ClearLayout(self.main_layout)
            self.main_layout.addWidget(self.finish)
            self.add_but()
            self.delete_data()
            self.m = 25

        elif self.s == 0:
            self.m = self.m - 1
            self.s = 60
        else:
            self.s = self.s - 1
        self.time_lab.setText(f"{self.m}:{self.s}")

    def do_scroll(self):

        formla = QFormLayout()
        for i in self.tasks:
            btn = QPushButton("  " + i[0])
            btn.setObjectName("btn")
            btn.setIcon(QIcon("Icons/check-box (1).png"))
            formla.addRow(btn)
            formla.setObjectName("form")

        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("QScrollBar{ background-color: none }")
        groupbox = QGroupBox()
        groupbox.setLayout(formla)
        groupbox.resize(300, 100)
        self.scroll.setWidget(groupbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(300)

        self.main_layout.addWidget(self.scroll)
        self.add_but()

        self.start_but.clicked.connect(self.start)
        self.stop_but.clicked.connect(self.stop)
        self.return_but.clicked.connect(self.re)
        self.ti.timeout.connect(self.counter)

        self.setLayout(self.main_layout)

    def set_data(self, email):
        self.ClearLayout(self.main_layout)
        self.main_layout.addWidget(self.sub_tit)
        self.email = email
        task_cr.execute(f"select task from pomodoro where email='{self.email}'")
        self.tasks = task_cr.fetchall()
        if len(self.tasks) == 0:
            self.add_em_tit()
            self.setLayout(self.main_layout)
        else:
            self.do_scroll()

    def ClearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() == self.sub_tit:
                    continue
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.ClearLayout(child.layout())

    def add_but(self):
        self.start_but = QPushButton()
        self.start_but.setText("  Play  ")
        self.start_but.setIcon(QIcon("Icons/play-button.png"))
        self.start_but.setIconSize(QSize(15, 15))
        self.start_but.setObjectName("bn3")

        self.stop_but = QPushButton()
        self.stop_but.setText("  Stop  ")
        self.stop_but.setIcon(QIcon("Icons/stop.png"))
        self.stop_but.setIconSize(QSize(15, 15))
        self.stop_but.setObjectName("bn3")
        self.stop_but.resize(10, 20)

        self.return_but = QPushButton()
        self.return_but.setText("  Return  ")
        self.return_but.setIcon(QIcon("Icons/return.png"))
        self.return_but.setIconSize(QSize(20, 20))
        self.return_but.setObjectName("bn3")
        self.bn_lay = QHBoxLayout()

        self.bn_lay.addWidget(self.stop_but)
        self.bn_lay.addWidget(self.start_but)
        self.bn_lay.addWidget(self.return_but)
        self.main_layout.addLayout(self.bn_lay)
        
    def add_em_tit(self):
        self.empty_tit = QLabel("You list is Empty please go to\n 'To Do list'\n and choose the tasks")
        self.empty_tit.setObjectName("sub")
        self.empty_tit.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.empty_tit)

    def paintEvent(self, event):
        pa = QPainter(self)
        pa.setPen(QPen(Qt.cyan, 5, Qt.SolidLine))
        pa.setBrush(QBrush(Qt.darkCyan, Qt.SolidPattern))
        pa.drawEllipse(160, 25, 150, 150)


class NoteButton(QPushButton):
    def __init__(self, title, note, email):
        super().__init__(f"   {title}")
        self.setIcon(QIcon("Icons/pencil.png"))
        self.NoteEditText = None

        def show_note():
            self.NoteEditText = NoteText(title, note, email)
            self.NoteEditText.show()
            note_page.clear_layout(note_page.main_lay)
            note_page.reload_UI()

        self.clicked.connect(show_note)


class NoteText(QWidget):
    def __init__(self, title="", note="", email=""):
        super().__init__()
        with open("Style/NoteTextEdit.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        self.note = note
        self.title = title
        self.email = email
        self.top = 200
        self.left = 400
        self.width = 600
        self.height = 400

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()
        plainText = QPlainTextEdit()
        plainText.setObjectName("filed")
        plainText.setPlaceholderText("Type Your Note Here")
        plainText.setUndoRedoEnabled(False)
        plainText.setPlainText(self.note)
        plainText.setStyleSheet("QScrollBar{ background-color: none }")

        vbox.addWidget(plainText)

        def save_note():
            if plainText.toPlainText() != "":
                cr.execute(f"delete from notes where email='{self.email}' and title='{self.title}'")
                db.commit()
                cr.execute(f"insert into notes values ('{self.title}', '{plainText.toPlainText()}', '{self.email}')")
                db.commit()
                note_page.clear_layout(note_page.main_lay)
                note_page.reload_UI()
                self.close()

        def delete_note():
            cr.execute(f"delete from notes where email='{self.email}' and title='{self.title}'")
            db.commit()
            note_page.clear_layout(note_page.main_lay)
            note_page.reload_UI()
            self.close()

        save = QPushButton("Save Note")
        delete = QPushButton("Delete Note")
        save.setObjectName("btn")
        delete.setObjectName("btn")
        save.clicked.connect(save_note)
        delete.clicked.connect(delete_note)
        Buttons_lay = QHBoxLayout()
        Buttons_lay.addWidget(save)
        Buttons_lay.addWidget(delete)
        vbox.addLayout(Buttons_lay)
        self.setLayout(vbox)


class Note(QMainWindow):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.widget = QWidget()
        self.NoteEditText = None
        with open("Style/task.css") as file:
            style = file.read()
            self.widget.setStyleSheet(style)
        self.setStyleSheet("QScrollBar{ background-color: none }")

        self.scroll = QScrollArea()
        self.main_lay = QVBoxLayout()
        self.main_lay.setContentsMargins(20, 50, 20, 10)

        back = QPushButton(self.widget)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        self.logo = QPushButton()
        self.logo.setIcon(QIcon("Icons/Note.png"))
        self.logo.setIconSize(QSize(60, 60))
        self.logo.setObjectName("logo")

        self.title = QLabel("Notes")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.add = QPushButton()
        self.add.setObjectName("add")
        self.add.setIcon(QIcon("Icons/add.png"))
        self.add.setIconSize(QSize(20, 20))
        self.add.setFixedWidth(40)

        note = QLabel("Click to add new Note ")
        note.setObjectName("note")

        self.add_lay = QHBoxLayout()
        self.add_lay.addWidget(note)
        self.add_lay.addWidget(self.add)

        self.sub_title = QLabel("Your Notes")
        self.sub_title.setObjectName("sub")
        self.sub_title.setAlignment(Qt.AlignCenter)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.setCentralWidget(self.scroll)
        self.resize(300, 200)
        self.reload_UI()

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

    def add_item(self):
        self.NoteEditText = None
        title, ok = QInputDialog().getText(self.widget, "Add title to your note", "Your Title : ", QLineEdit.Normal)
        if ok:
            self.NoteEditText = NoteText(title, "", self.email)
            self.NoteEditText.show()
            self.clear_layout(self.main_lay)
            self.reload_UI()

    def set_email(self, email):
        self.email = email
        self.add.clicked.connect(self.add_item)
        self.clear_layout(self.main_lay)
        self.reload_UI()

    def reload_UI(self):
        self.main_lay.addWidget(self.logo)
        self.main_lay.addWidget(self.title)
        self.main_lay.addLayout(self.add_lay)
        self.main_lay.addWidget(self.sub_title)
        task_cr.execute(f"select title,note from notes where email='{self.email}'")
        notes = task_cr.fetchall()
        if len(notes) == 0:
            self.sub_title.setText("You don't have any Notes")
        else:
            self.sub_title.setText("Your Notes")

        for note in notes:
            add_note = NoteButton(note[0], note[1], self.email)
            add_note.setObjectName("task")
            self.main_lay.addWidget(add_note)
        self.main_lay.insertSpacing(2, 40)
        self.widget.setLayout(self.main_lay)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() == self.sub_title or \
                        child.widget() == self.title or \
                        child.layout() == self.add_lay or \
                        child.widget() == self.logo:
                    continue
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())


class Tab(QDialog):
    def __init__(self):
        super().__init__()

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)
        back.setStyleSheet(
            """
                QPushButton#back{
                    border: none;
                    background-color: rgba(22, 60, 134, 0);
                    border-radius: 10px;
                }
                QPushButton#back:hover{
                    background-color: #005aff;
                }

            """
        )

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

        title = QLabel("Converter", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-weight: bold;
            font-size: 30px;
            color: #4082c0;
        """)
        self.setWindowTitle("Convereter")
        self.setWindowIcon(QIcon("icon.png"))
        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.setContentsMargins(20, 40, 20, 0)
        vbox.setSpacing(30)
        tabwidget = QTabWidget()
        font = QFont("Times New Roman", 9)
        tabwidget.addTab(Tabsystem(), "Numeral System")
        tabwidget.addTab(Tablength(), "Length")
        self.setStyleSheet("QTabWidget{font-size: 14pt;}")
        tabwidget.tabBar().setTabTextColor(1, QColor("#123353"))

        tabwidget.setFont(font)
        tabwidget.addTab(Tabtime(), "Time")
        tabwidget.addTab(Tabdata(), "Data")
        tabwidget.addTab(Tabtemperature(), "Temperature")
        tabwidget.tabBar().setTabTextColor(0, QColor("#034973"))
        tabwidget.tabBar().setTabTextColor(1, QColor("#034973"))
        tabwidget.tabBar().setTabTextColor(2, QColor("#034973"))
        tabwidget.tabBar().setTabTextColor(3, QColor("#034973"))
        tabwidget.tabBar().setTabTextColor(4, QColor("#034973"))
        vbox.addWidget(tabwidget)
        self.setLayout(vbox)


class Tablength(QWidget):
    def __init__(self):
        super().__init__()

        with open("Style/converter.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        enterlabel = QLabel("Enter A Value")
        # enterlabel.setAlignment(Qt.AlignCenter)
        enterlabeledit = QLineEdit()
        enterlabeledit.setPlaceholderText("Type a value here")
        enterlabeledit.setObjectName("enter")
        fromlabel = QLabel("From")
        # fromlabel.setAlignment(Qt.AlignCenter)
        fromlabel.setObjectName("from")
        combobox = QComboBox()
        combobox.setObjectName("com")

        combobox.addItem("Inches")
        combobox.addItem("Feet")
        combobox.addItem("Yards")
        combobox.addItem("KiloMeters")
        combobox.addItem("Meters")
        combobox.addItem("CentiMeters")
        combobox.addItem("millimeters")
        font = QFont('Times New Roman', 12)
        combobox.setFont(font)
        combobox.setStyleSheet("QListView{background-color: white;}")
        tolabel = QLabel("To")
        # tolabel.setAlignment(Qt.AlignCenter)
        combobox2 = QComboBox()
        combobox2.setObjectName("com")
        combobox2.addItem("Inches")
        combobox2.addItem("Feet")
        combobox2.addItem("Yards")
        combobox2.addItem("KiloMeters")
        combobox2.addItem("Meters")
        combobox2.addItem("CentiMeters")
        combobox2.addItem("millimeters")
        font = QFont('Times New Roman', 12)
        combobox2.setFont(font)
        combobox2.setStyleSheet("QListView{background-color: white;}")

        buttonconvert = QPushButton("Convert")
        buttonconvert.setObjectName("button")
        result = QLabel("....")

        def convertlength():
            if combobox.currentText() == "Inches" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 12} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 36} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 39370} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 39.37} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 2.54} {combobox2.currentText()}")
            elif combobox.currentText() == "Inches" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 25.4} {combobox2.currentText()}")

            if combobox.currentText() == "Feet" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 12} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3281} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3.281} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 30.48} {combobox2.currentText()}")
            elif combobox.currentText() == "Feet" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 304.8} {combobox2.currentText()}")

            if combobox.currentText() == "Yards" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 36} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1094} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1.094} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 91.44} {combobox2.currentText()}")
            elif combobox.currentText() == "Yards" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 914.4} {combobox2.currentText()}")

            if combobox.currentText() == "KiloMeters" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 39370} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3281} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1094} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 100000} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloMeters" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+6} {combobox2.currentText()}")

            if combobox.currentText() == "Meters" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 39.37} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3.281} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1.094} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 100} {combobox2.currentText()}")
            elif combobox.currentText() == "Meters" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")

            if combobox.currentText() == "CentiMeters" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 2.54} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 30.48} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 91.44} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 100000} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 100} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "CentiMeters" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 10} {combobox2.currentText()}")

            if combobox.currentText() == "millimeters" and combobox2.currentText() == "Inches":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 25.4} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "Feet":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 304.8} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "Yards":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 914.4} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "KiloMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "Meters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "CentiMeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 10} {combobox2.currentText()}")
            elif combobox.currentText() == "millimeters" and combobox2.currentText() == "millimeters":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")

        buttonconvert.clicked.connect(convertlength)
        vbox = QVBoxLayout()
        vbox.addWidget(enterlabel)
        vbox.addWidget(enterlabeledit)
        vbox.addWidget(fromlabel)

        vbox.addWidget(combobox)
        vbox.addWidget(tolabel)
        vbox.addWidget(combobox2)
        vbox.addWidget(result)
        vbox.addWidget(buttonconvert)
        self.setLayout(vbox)


class Tabtime(QWidget):
    def __init__(self):
        super().__init__()
        with open("Style/converter.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        enterlabel = QLabel("Enter A Value")
        # enterlabel.setAlignment(Qt.AlignCenter)

        enterlabeledit = QLineEdit()
        enterlabeledit.setObjectName("enter")
        enterlabeledit.setPlaceholderText("Type a value here")

        fromlabel = QLabel("From")
        # fromlabel.setAlignment(Qt.AlignCenter)

        combobox = QComboBox()
        combobox.setObjectName("com")
        combobox.addItem("Century")
        combobox.addItem("Decade")
        combobox.addItem("Month")
        combobox.addItem("Week")
        combobox.addItem("Day")
        combobox.addItem("Hour")
        combobox.addItem("Minute")
        combobox.addItem("Second")
        font = QFont('Times New Roman', 12)
        combobox.setFont(font)
        combobox.setStyleSheet("QListView{background-color: white;}")

        tolabel = QLabel("To")
        # tolabel.setAlignment(Qt.AlignCenter)
        combobox2 = QComboBox()
        combobox2.setObjectName("com")
        combobox2.addItem("Century")
        combobox2.addItem("Decade")
        combobox2.addItem("Month")
        combobox2.addItem("Week")
        combobox2.addItem("Day")
        combobox2.addItem("Hour")
        combobox2.addItem("Minute")
        combobox2.addItem("Second")
        font = QFont('Times New Roman', 12)
        combobox2.setFont(font)
        combobox2.setStyleSheet("QListView{background-color: white;}")
        buttonconvert = QPushButton("Convert")
        buttonconvert.setObjectName("button")
        result = QLabel("....")

        def converttime():
            if combobox.currentText() == "Month" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 4} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 30} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 730} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 43800} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 2628003} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1200} {combobox2.currentText()}")
            elif combobox.currentText() == "Month" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 120} {combobox2.currentText()}")

            if combobox.currentText() == "Week" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 4} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 7} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 168} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 10080} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 604800} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 5214} {combobox2.currentText()}")
            elif combobox.currentText() == "Week" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 521.4} {combobox2.currentText()}")

            if combobox.currentText() == "Day" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 30} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 7} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 24} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1440} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 86400} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 36500} {combobox2.currentText()}")
            elif combobox.currentText() == "Day" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3650} {combobox2.currentText()}")

            if combobox.currentText() == "Hour" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 730} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 168} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 24} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 60} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3600} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 876000} {combobox2.currentText()}")
            elif combobox.currentText() == "Hour" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 87600} {combobox2.currentText()}")

            if combobox.currentText() == "Minute" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 43800} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 10080} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1440} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 60} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 60} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 5.256e+7} {combobox2.currentText()}")
            elif combobox.currentText() == "Minute" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 5.256e+6} {combobox2.currentText()}")

            if combobox.currentText() == "Second" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 2.628e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 604800} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 86400} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3600} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 60} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3.154e+9} {combobox2.currentText()}")
            elif combobox.currentText() == "Second" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 3.154e+8} {combobox2.currentText()}")

            if combobox.currentText() == "Century" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1200} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 5214} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 36500} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 876000} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 5.256e+7} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3.154e+9} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")
            elif combobox.currentText() == "Century" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 10} {combobox2.currentText()}")

            if combobox.currentText() == "Decade" and combobox2.currentText() == "Month":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 120} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Week":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 521.4} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Day":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3650} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Hour":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 87600} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Minute":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 5.256e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Second":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 3.154e+8} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Century":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 10} {combobox2.currentText()}")
            elif combobox.currentText() == "Decade" and combobox2.currentText() == "Decade":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text())} {combobox2.currentText()}")

        buttonconvert.clicked.connect(converttime)
        vbox = QVBoxLayout()
        vbox.addWidget(enterlabel)
        vbox.addWidget(enterlabeledit)
        vbox.addWidget(fromlabel)
        vbox.addWidget(combobox)
        vbox.addWidget(tolabel)
        vbox.addWidget(combobox2)
        vbox.addWidget(result)
        vbox.addWidget(buttonconvert)

        self.setLayout(vbox)

        ##############################


class Tabdata(QWidget):
    def __init__(self):
        super().__init__()
        with open("Style/converter.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        enterlabel = QLabel("Enter A Value")
        # enterlabel.setAlignment(Qt.AlignCenter)

        enterlabeledit = QLineEdit()
        enterlabeledit.setPlaceholderText("Type a value here")
        enterlabeledit.setObjectName("enter")
        fromlabel = QLabel("From")
        # fromlabel.setAlignment(Qt.AlignCenter)

        combobox = QComboBox()
        combobox.setObjectName("com")
        combobox.addItem("TeraByte")
        combobox.addItem("GigaByte")
        combobox.addItem("MegaByte")
        combobox.addItem("KiloByte")
        combobox.addItem("Byte")
        font = QFont('Times New Roman', 12)
        combobox.setFont(font)
        combobox.setStyleSheet("QListView{background-color: white;}")

        tolabel = QLabel("To")
        # tolabel.setAlignment(Qt.AlignCenter)
        combobox2 = QComboBox()
        combobox2.setObjectName("com")
        combobox2.addItem("TeraByte")
        combobox2.addItem("GigaByte")
        combobox2.addItem("MegaByte")
        combobox2.addItem("KiloByte")
        combobox2.addItem("Byte")
        font = QFont('Times New Roman', 12)
        combobox2.setStyleSheet("QListView{background-color: white;}")

        combobox2.setFont(font)
        buttonconvert = QPushButton("Convert")
        buttonconvert.setObjectName("button")
        result = QLabel("....")

        def converttime():
            if combobox.currentText() == "TeraByte" and combobox2.currentText() == "TeraByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "TeraByte" and combobox2.currentText() == "GigaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "TeraByte" and combobox2.currentText() == "MegaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "TeraByte" and combobox2.currentText() == "KiloByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+9} {combobox2.currentText()}")
            elif combobox.currentText() == "TeraByte" and combobox2.currentText() == "Byte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+12} {combobox2.currentText()}")

            if combobox.currentText() == "GigaByte" and combobox2.currentText() == "GigaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "GigaByte" and combobox2.currentText() == "TeraByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "GigaByte" and combobox2.currentText() == "MegaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "GigaByte" and combobox2.currentText() == "KiloByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "GigaByte" and combobox2.currentText() == "Byte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+9} {combobox2.currentText()}")

            if combobox.currentText() == "MegaByte" and combobox2.currentText() == "MegaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "MegaByte" and combobox2.currentText() == "TeraByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "MegaByte" and combobox2.currentText() == "GigaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "MegaByte" and combobox2.currentText() == "KiloByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "MegaByte" and combobox2.currentText() == "Byte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1e+6} {combobox2.currentText()}")

            if combobox.currentText() == "KiloByte" and combobox2.currentText() == "KiloByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloByte" and combobox2.currentText() == "TeraByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+9} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloByte" and combobox2.currentText() == "GigaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloByte" and combobox2.currentText() == "MegaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")
            elif combobox.currentText() == "KiloByte" and combobox2.currentText() == "Byte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) * 1000} {combobox2.currentText()}")

            if combobox.currentText() == "Byte" and combobox2.currentText() == "Byte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Byte" and combobox2.currentText() == "TeraByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+12} {combobox2.currentText()}")
            elif combobox.currentText() == "Byte" and combobox2.currentText() == "GigaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+9} {combobox2.currentText()}")
            elif combobox.currentText() == "Byte" and combobox2.currentText() == "MegaByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1e+6} {combobox2.currentText()}")
            elif combobox.currentText() == "Byte" and combobox2.currentText() == "KiloByte":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) / 1000} {combobox2.currentText()}")

        buttonconvert.clicked.connect(converttime)
        vbox = QVBoxLayout()
        vbox.addWidget(enterlabel)
        vbox.addWidget(enterlabeledit)
        vbox.addWidget(fromlabel)
        vbox.addWidget(combobox)
        vbox.addWidget(tolabel)
        vbox.addWidget(combobox2)
        vbox.addWidget(result)
        vbox.addWidget(buttonconvert)
        self.setLayout(vbox)


class Tabtemperature(QWidget):
    def __init__(self):
        super().__init__()
        with open("Style/converter.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        enterlabel = QLabel("Enter A Value")
        # enterlabel.setAlignment(Qt.AlignCenter)
        enterlabeledit = QLineEdit()
        enterlabeledit.setPlaceholderText("Type a value here")
        enterlabeledit.setObjectName("enter")
        fromlabel = QLabel("From")
        # fromlabel.setAlignment(Qt.AlignCenter)

        combobox = QComboBox()
        combobox.setObjectName("com")
        combobox.addItem("Degree Celsius")
        combobox.addItem("Fahrenheit")
        combobox.addItem("Kelvin")
        font = QFont('Times New Roman', 12)
        combobox.setStyleSheet("QListView{background-color: white;}")

        combobox.setFont(font)
        tolabel = QLabel("To")
        # tolabel.setAlignment(Qt.AlignCenter)
        combobox2 = QComboBox()
        combobox2.setObjectName("com")
        combobox2.addItem("Degree Celsius")
        combobox2.addItem("Fahrenheit")
        combobox2.addItem("Kelvin")
        font = QFont('Times New Roman', 12)
        combobox2.setStyleSheet("QListView{background-color: white;}")

        combobox2.setFont(font)
        buttonconvert = QPushButton("Convert")
        buttonconvert.setObjectName("button")
        result = QLabel("....")

        def converttemperature():
            if combobox.currentText() == "Degree Celsius" and combobox2.currentText() == "Degree Celsius":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Degree Celsius" and combobox2.currentText() == "Fahrenheit":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {(int(enterlabeledit.text()) * 9 / 5) + 32} {combobox2.currentText()}")
            elif combobox.currentText() == "Degree Celsius" and combobox2.currentText() == "Kelvin":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) + 273.15} {combobox2.currentText()}")

            if combobox.currentText() == "Fahrenheit" and combobox2.currentText() == "Fahrenheit":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Fahrenheit" and combobox2.currentText() == "Degree Celsius":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {(int(enterlabeledit.text()) - 32) * 5 / 9} {combobox2.currentText()}")
            elif combobox.currentText() == "Fahrenheit" and combobox2.currentText() == "Kelvin":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {((int(enterlabeledit.text()) - 32) * 5 / 9) + 273.15}  {combobox2.currentText()}")

            if combobox.currentText() == "Kelvin" and combobox2.currentText() == "Kelvin":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Kelvin" and combobox2.currentText() == "Degree Celsius":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {int(enterlabeledit.text()) - 273.15} {combobox2.currentText()}")
            elif combobox.currentText() == "Kelvin" and combobox2.currentText() == "Fahrenheit":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {((int(enterlabeledit.text()) - 273.15) * 9 / 5) + 32} {combobox2.currentText()}")

        buttonconvert.clicked.connect(converttemperature)
        vbox = QVBoxLayout()
        vbox.addWidget(enterlabel)
        vbox.addWidget(enterlabeledit)
        vbox.addWidget(fromlabel)
        vbox.addWidget(combobox)
        vbox.addWidget(tolabel)
        vbox.addWidget(combobox2)
        vbox.addWidget(result)
        vbox.addWidget(buttonconvert)
        self.setLayout(vbox)


class Tabsystem(QWidget):
    def __init__(self):
        super().__init__()
        with open("Style/converter.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        enterlabel = QLabel("Enter A Value")
        # enterlabel.setAlignment(Qt.AlignCenter)
        enterlabeledit = QLineEdit()
        enterlabeledit.setObjectName("enter")
        enterlabeledit.setPlaceholderText("Type a value here")
        fromlabel = QLabel("From")
        # fromlabel.setAlignment(Qt.AlignCenter)

        combobox = QComboBox()
        combobox.setObjectName("com")
        combobox.addItem("Decimal")

        font = QFont('Times New Roman', 12)
        combobox.setStyleSheet("QListView{background-color: white;}")

        combobox.setFont(font)
        tolabel = QLabel("To")
        # tolabel.setAlignment(Qt.AlignCenter)
        combobox2 = QComboBox()
        combobox2.setObjectName("com")
        combobox2.addItem("Binary")
        combobox2.addItem("Decimal")
        combobox2.addItem("Octal")
        combobox2.addItem("HexaDecimal")
        font = QFont('Times New Roman', 12)
        combobox2.setStyleSheet("QListView{background-color: white;}")

        combobox2.setFont(font)

        buttonconvert = QPushButton("Convert")
        buttonconvert.setObjectName("button")
        result = QLabel("....")


        def convertsystem():
            if combobox.currentText() == "Decimal" and combobox2.currentText() == "Decimal":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {enterlabeledit.text()} {combobox2.currentText()}")
            elif combobox.currentText() == "Decimal" and combobox2.currentText() == "Binary":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {bin(int(enterlabeledit.text()))} {combobox2.currentText()}")
            elif combobox.currentText() == "Decimal" and combobox2.currentText() == "HexaDecimal":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {hex(int(enterlabeledit.text()))} {combobox2.currentText()}")
            elif combobox.currentText() == "Decimal" and combobox2.currentText() == "Octal":
                result.setText(
                    f"{enterlabeledit.text()} {combobox.currentText()} = {oct(int(enterlabeledit.text()))} {combobox2.currentText()}")

        buttonconvert.clicked.connect(convertsystem)
        vbox = QVBoxLayout()
        vbox.addWidget(enterlabel)
        vbox.addWidget(enterlabeledit)
        vbox.addWidget(fromlabel)
        vbox.addWidget(combobox)
        vbox.addWidget(tolabel)
        vbox.addWidget(combobox2)
        vbox.addWidget(result)
        vbox.addWidget(buttonconvert)
        self.setLayout(vbox)


class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open('Style/Translator.css') as file:
            style = file.read()
            self.setStyleSheet(style)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

        self.setWindowTitle("Translator")

        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())

        self.trans_from = QComboBox()
        self.trans_from.addItems(self.language_list)
        self.trans_from.setCurrentText("english")

        self.trans_to = QComboBox()
        self.trans_to.addItems(self.language_list)
        self.trans_to.setCurrentText("arabic")

        From = QLabel("From")
        From.setAlignment(Qt.AlignCenter)
        To = QLabel("To")
        To.setAlignment(Qt.AlignCenter)

        text = QLabel("Translation :")
        title = QLabel("Translator")
        title.setAlignment(Qt.AlignCenter)
        text.setAlignment(Qt.AlignCenter)

        self.In_text = QLineEdit()
        self.In_text.setPlaceholderText("Enter a text to translate")
        self.Out_text = QLineEdit()
        self.Out_text.setPlaceholderText("Your Translation : ")

        logo = QPushButton()
        logo.setIcon(QIcon("Icons/translator.png"))
        logo.setObjectName("logo")
        logo.setIconSize(QSize(60, 60))

        btn_trans = QPushButton("Translate")
        btn_trans.clicked.connect(self.translate)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear)

        trans = QVBoxLayout()
        trans.setContentsMargins(20, 20, 20, 10)
        layout_1 = QHBoxLayout()
        layout_2 = QHBoxLayout()
        layout_3 = QHBoxLayout()
        trans.addWidget(logo)
        trans.addWidget(title)
        layout_1.addWidget(From)
        layout_1.addWidget(To)
        layout_2.addWidget(self.trans_from)
        layout_2.addWidget(self.trans_to)
        trans.addLayout(layout_1)
        trans.addLayout(layout_2)
        trans.addWidget(self.In_text)
        trans.addWidget(text)
        trans.addWidget(self.Out_text)
        layout_3.addWidget(btn_trans)
        layout_3.addWidget(btn_clear)
        trans.addLayout(layout_3)
        trans.setContentsMargins(30, 50, 30, 50)
        trans.setSpacing(20)
        self.setLayout(trans)

    def translate(self):
        text_1 = self.In_text.text()
        lang_1 = ""
        lang_2 = ""
        for lang in LANGUAGES:
            if LANGUAGES[lang] == self.trans_from.currentText():
                lang_1 = lang
            if LANGUAGES[lang] == self.trans_to.currentText():
                lang_2 = lang

        translate = Translator().translate(text_1, src=lang_1, dest=lang_2)
        self.Out_text.setText(translate.text)

    def clear(self):

        self.In_text.setText("")
        self.Out_text.setText("")


class GraphWindow(QMainWindow):
    def __init__(self, grade, exams, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.graphWidget.plot(exams, grade)


class Graph(QWidget):
    def __init__(self):
        super().__init__()
        # Maram
        with open('Style/graph.css') as file:
            style = file.read()
            self.setStyleSheet(style)
        self.graph = None
        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        def go_back():
            Windows.setCurrentIndex(6)

        back.clicked.connect(go_back)

        logo = QPushButton()
        logo.setIcon(QIcon("Icons/graph.png"))
        logo.setObjectName("logo")
        logo.setIconSize(QSize(60, 60))
        graph_text = QLabel("Performance analysis\n on a graph diagram")
        graph_text.setAlignment(Qt.AlignCenter)
        graph_text.setObjectName("per")
        graph_sub_text = QLabel("enter your grade from 1 to 100")
        graph_sub_text.setObjectName("graphh")

        grade_field = QLineEdit()
        grade_field.setObjectName("grade")
        graph_sub_text2 = QLabel("*there should be a space between each grade*")
        graph_sub_text2.setObjectName("graph")
        b1 = QPushButton('show graph')
        b1.setObjectName("show")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 50)
        main_layout.addWidget(logo)
        main_layout.addWidget(graph_text)
        main_layout.addWidget(graph_sub_text)
        main_layout.addWidget(graph_sub_text2)
        main_layout.addWidget(grade_field)
        main_layout.addWidget(b1)
        self.setLayout(main_layout)

        def show_graph():
            if self.graph is None:
                grade = grade_field.text().split()
                for i in range(0, len(grade), 1):
                    grade[i] = int(grade[i])
                exams = list(range(1, len(grade) + 1))
                self.graph = GraphWindow(grade, exams)
            self.graph.show()

        b1.clicked.connect(show_graph)


app = QApplication(sys.argv)
task_page = Task("test")
timer_page = Timer("test")
note_page = Note("1")
Windows = QStackedWidget()
Windows.setGeometry(550, 200, 400, 600)
Windows.setStyleSheet('background-color: #024772')
Windows.addWidget(WelcomePage())  # 0
Windows.addWidget(LoginPage())  # 1
Windows.addWidget(SignPage())  # 2
Windows.addWidget(Tab())  # 3
Windows.addWidget(TranslatorWindow())  # 4
Windows.addWidget(Graph())  # 5
Windows.show()
sys.exit(app.exec_())

# 00314f

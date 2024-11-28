import io
import sys
import threading
import wave

import bd

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, pyqtSignal, QLine, QUrl, QPropertyAnimation, QThread, QPoint
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QPushButton, \
    QGroupBox, QHBoxLayout, QLineEdit, QGridLayout, QFormLayout, QMessageBox
from PyQt6.QtMultimedia import QSoundEffect

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>900</width>
    <height>650</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTableWidget" name="table">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>30</y>
      <width>650</width>
      <height>400</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>1</pointsize>
     </font>
    </property>
    <property name="sizeAdjustPolicy">
     <enum>QAbstractScrollArea::AdjustToContents</enum>
    </property>
    <property name="rowCount">
     <number>15</number>
    </property>
    <property name="columnCount">
     <number>15</number>
    </property>
    <attribute name="horizontalHeaderVisible">
     <bool>false</bool>
    </attribute>
    <attribute name="verticalHeaderVisible">
     <bool>false</bool>
    </attribute>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row>
     <property name="text">
      <string/>
     </property>
    </row>
    <row/>
    <row/>
    <row/>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column>
     <property name="text">
      <string/>
     </property>
    </column>
    <column/>
    <column/>
    <column/>
    <column/>
    <column/>
   </widget>
   <widget class="Line" name="line">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>30</y>
      <width>16</width>
      <height>381</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
   </widget>
   <widget class="Line" name="end_line">
    <property name="geometry">
     <rect>
      <x>113</x>
      <y>30</y>
      <width>20</width>
      <height>381</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
   </widget>
   <widget class="QGroupBox" name="inspector">
    <property name="geometry">
     <rect>
      <x>690</x>
      <y>30</y>
      <width>191</width>
      <height>401</height>
     </rect>
    </property>
    <property name="title">
     <string>GroupBox</string>
    </property>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.select = False
        self.a = False
        self.select_object = False
        self.object = None

        self.notes = ['img_notes/note.png', 'img_notes/note2.png', 'img_notes/note3.png', 'img_notes/note4.png',
                      'img_notes/note5.png', 'img_notes/note6.png', 'img_notes/note7.png']
        self.sounds = ['music/do.wav', 'music/re.wav', 'music/mi.wav', 'music/fa.wav', 'music/sol.wav',
                       'music/lya.wav', 'music/si.wav',]
        self.list_notes = [None]

        self.initUI()
        t = threading.Thread(target=self.play_music, daemon=True, args=())
        t.start()

    def initUI(self):
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.table: QTableWidget = self.table
        self.table.currentItemChanged.connect(self.current_item_changed)
        self.table.setMouseTracking(True)
        self.table.setColumnCount(24)
        self.table.setRowCount(14)
        self.table.horizontalHeader().setDefaultSectionSize(25)
        self.table.verticalHeader().setDefaultSectionSize(25)

        rows = self.table.rowCount()
        columns = self.table.columnCount()
        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() & ~item.flags().ItemIsEditable)
                self.table.setItem(i, j, item)

        self.set_notes()

        self.line: QLine = self.line
        self.line.move(-5, 30)
        self.line.resize(50, 25 * 14)

        self.label_sec = QLabel(self)
        self.label_sec.resize(210, 40)
        self.label_sec.move(125, 385)

        self.end_line: QLine = self.end_line
        self.end_line.resize(50, 25 * 14)
        self.end_line.move(28, 30)
        self.set_animation()

        self.button_start_animation = QPushButton(self)
        self.button_start_animation.setIcon(QIcon('buttons/play.png'))
        self.button_start_animation.move(35, 385)
        self.button_start_animation.resize(40, 40)
        self.button_start_animation.clicked.connect(self.press_start_animation)
        self.start = True

        self.button_reset_animation = QPushButton(self)
        self.button_reset_animation.setIcon(QIcon('buttons/reset.png'))
        self.button_reset_animation.move(80, 385)
        self.button_reset_animation.resize(40, 40)
        self.button_reset_animation.clicked.connect(self.press_reset_animation)

        self.button_slider = QPushButton(self)
        self.button_slider.move(30, 5)
        self.button_slider.resize(25, 25)

        self.insp = Inspector(self.inspector, self.table)

        self.b = QPushButton(self)
        self.b.move(530, 390)
        self.b.clicked.connect(self.func)

    def func(self):
        for i in self.list_notes:
            i.table()

    def set_animation(self, duration=500):
        self.animation = QPropertyAnimation(self.line, b'pos')
        self.duration = duration
        self.label_sec.setText(f'Продолжительность в секундах: {duration / 1000}')
        self.animation.setDuration(self.duration)
        self.animation.setStartValue(QPoint(-5, 30))
        self.animation.setEndValue(QPoint(int(5 + (self.duration / 20) - 2), 30))
        self.animation.finished.connect(self.animation_is_finished)

    def press_start_animation(self):
        if self.start:
            self.start = False
            self.button_start_animation.setIcon(QIcon('buttons/pause.png'))
            self.animation.start()
        elif not self.start:
            self.start = True
            self.button_start_animation.setIcon(QIcon('buttons/play.png'))
            self.animation.stop()

    def press_reset_animation(self):
        self.animation.stop()
        self.line.move(-5, 30)
        self.button_start_animation.setIcon(QIcon('buttons/play.png'))
        self.start = True

    def animation_is_finished(self):
        self.start = True
        self.button_start_animation.setIcon(QIcon('buttons/play.png'))

    def mouseMoveEvent(self, event):
        if event.pos().x() >= 30 and event.pos().x() <= 610 and \
            event.pos().y() >= 5 and event.pos().y() <= 375:
            if event.pos().x() in [i for i in range(30, 606, 25)]:
                self.button_slider.move(event.pos().x(), 5)
                self.end_line.move(self.button_slider.pos().x() - 2, self.button_slider.pos().y() + 25)
                self.set_animation(int(((self.end_line.pos().x() - 3) / 25) * 500))

    def set_notes(self):
        step = 0
        start = 100
        for i in self.notes:
            sound_file = self.sounds[self.notes.index(i)]
            self.image = ImgNote(self, i, sound_file)
            image = self.image.get_img()
            self.image.move(start + step, 500)
            image.sound_file = sound_file
            image.pic_file = i
            image.clicked.connect(self.select_note)
            step += 50

    def current_item_changed(self, current: QTableWidgetItem):
        self.row, self.column = current.row(), current.column()
        if self.select:
            if self.row != None and self.column != None:
                self.table.setCellWidget(self.row, self.column, self.select_label)
                self.select = False
                self.insp.show(self.select_label)
                self.select_label.row = self.row
                self.select_label.col = self.column
                self.get_table_items()
                self.select_label = None
                # self.row, self.column = None, None
        elif self.select_object:
            if self.object.row != None and self.object.col != None:
                self.table.setCellWidget(self.row, self.column, self.object)
                self.select_object = False
                self.object.row = self.row
                self.object.col = self.column
                self.object = None
                # self.row, self.column = None, None

    def select_note(self):
        self.select = True
        # self.row, self.column = None, None
        clickedLabel: ClickedLabel = self.sender()
        image: QImage = clickedLabel.pixmap().toImage()
        self.insp.hide()
        self.select_label = ImgNote(self, clickedLabel.pic_file, clickedLabel.sound_file)
        self.select_label.clicked.connect(self.move_note)

    def move_note(self):
        self.object: ImgNote = self.sender()
        self.object.row = self.row
        self.object.col = self.column
        self.select_object = True
        self.insp.show(self.object)
        self.get_table_items()

    def get_table_items(self):
        self.list_notes = []
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.cellWidget(i, j)
                if isinstance(item, ImgNote) and item not in self.list_notes:
                    self.list_notes.append(item)
        self.list_notes = sorted(self.list_notes, key=lambda x: x.pos().x())

    def play_music(self):
        while True:
            if self.start:
                QThread.msleep(1)
            else:
                while not self.start:
                    for i in self.list_notes:
                        i: ImgNote
                        if i != None and i.row != None and i.col != None and \
                            self.animation.currentValue().x() == i.pos().x():
                            i.play_sound()
                    QThread.msleep(1)

    def closeEvent(self, event):
        self.start = True
        self.button_start_animation.setIcon(QIcon('buttons/play.png'))
        self.animation.stop()
        dlg = QMessageBox(self)
        reply = dlg.question(self, 'Уведомление', 'Хотите выйти?', QMessageBox.StandardButton.Ok,
                             QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Ok:
            event.accept()
        else:
            event.ignore()


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def files(self):
        self.sound_file = None
        self.pic_file = None

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class ImgNote(ClickedLabel):
    def __init__(self, a, pixmap: str, sound=None):
        super(ImgNote, self).__init__(a)
        self.image = ClickedLabel(self)
        self.pic = pixmap
        self.image.setPixmap(QPixmap(self.pic))
        self.sound = sound
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(self.sound))
        self.row = None
        self.col = None

    def get_img(self):
        return self.image

    def play_sound(self):
        self.effect.play()

    def table(self):
        source = wave.open(self.sound, mode="rb")
        params = source.getparams()
        frames = source.readframes(params.nframes)
        params = tuple(params)
        frames_count = params[3]
        new_params = '-'.join(map(lambda x: str(x), list(params)))
        source.close()

        bd.add_table('Bobr', f'{self.row}-{self.col}-{self.pic}|{new_params}', frames)


class Inspector:
    def __init__(self, ins, tab):
        self.inspector: QGroupBox = ins
        self.inspector.move(690, 23)
        self.inspector.resize(190, 408)
        self.inspector.setTitle('Инспектор')
        layout = QFormLayout()
        self.button_play_sound = QPushButton()
        self.button_play_sound.setIcon(QIcon('buttons/play.png'))
        self.button_play_sound.resize(40, 40)
        self.button_play_sound.clicked.connect(self.play_sound)
        self.edit_volume = QLineEdit()
        self.play_speed = QLineEdit()
        self.button_del_note = QPushButton('Удалить')
        self.button_del_note.clicked.connect(self.delete_note)
        layout.addWidget(self.button_play_sound)
        layout.addRow('Громкость:', self.edit_volume)
        layout.addRow('Скорость воспроизведения:', self.play_speed)
        layout.addWidget(self.button_del_note)
        layout.setContentsMargins(15, 20, 15, 0)
        layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.inspector.setLayout(layout)
        self.inspector.hide()

        self.table: QTableWidget = tab

    def show(self, note: ImgNote):
        self.inspector.show()
        self.note = note

    def hide(self):
        self.inspector.hide()

    def play_sound(self):
        self.note.play_sound()

    def delete_note(self):
        self.table.setCellWidget(self.note.row, self.note.col, None)
        self.note.row = None
        self.note.col = None
        self.inspector.hide()
        App().get_table_items()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
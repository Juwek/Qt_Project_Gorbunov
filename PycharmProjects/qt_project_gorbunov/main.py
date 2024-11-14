import io
import sys
from symtable import Class

from PyQt6 import uic
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel

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
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.table: QTableWidget
        self.table.currentItemChanged.connect(self.current_item_changed)
        self.table.setColumnCount(40)
        self.table.setRowCount(21)
        self.table.horizontalHeader().setDefaultSectionSize(25)
        self.table.verticalHeader().setDefaultSectionSize(25)

        rows = self.table.rowCount()
        columns = self.table.columnCount()
        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() & ~item.flags().ItemIsEditable)
                self.table.setItem(i, j, item)

        self.image = Note.img(self, QPixmap('note.png'))
        self.table.setCellWidget(5, 5, self.image)

        self.note = Note.img(self, QPixmap('note.png'))
        # self.note.move(100, 500)
        # self.note.clicked.connect(self.mouse_event)

    def current_item_changed(self, current: QTableWidgetItem):
        print(current.row(), current.column())

    def mouseMoveEvent(self, event):
        # self.object = Note.img(self, QPixmap('note.png'))
        self.note.move(event.pos().x(), event.pos().y())


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class Note(QMainWindow):
    def img(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.image = ClickedLabel(self)
        self.image.setPixmap(self.pixmap)
        return self.image


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
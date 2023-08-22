import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtWidgets
import sqlite3


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('admin.ui', self)
        self.loadContactsList.clicked.connect(self.load_contacts_list)
        self.loadStatistic.clicked.connect(self.load_statistics)

    def load_contacts_list(self):
        connection = sqlite3.connect('server_db.db3')
        cur = connection.cursor()
        sqlquery = "SELECT id, name FROM clients"
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.contactsList.insertRow(tablerow)
            self.contactsList.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.contactsList.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            tablerow += 1

    def load_statistics(self):
        connection = sqlite3.connect('server_db.db3')
        cur = connection.cursor()
        sqlquery = "SELECT * FROM login_history, clients WHERE login_history.name = clients.id"
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.Statistic.insertRow(tablerow)
            self.Statistic.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[5]))
            self.Statistic.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.Statistic.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            tablerow += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

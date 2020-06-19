
# Our Imports
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from datetime import date
from DB_Connetion import con,mycursor
from datetime import datetime


# Import the Ui
ui,_ = loadUiType('TEST_UI_CRUD.ui')


# Main App class 
class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_CLicks()
        self.Tablefill()



    def Handle_CLicks(self):
        self.pushButton.clicked.connect(self.InsertPeople)
        self.pushButton_2.clicked.connect(self.SearchPeople)
        self.pushButton_4.clicked.connect(self.delete_ppl)
        self.pushButton_3.clicked.connect(self.Update_ppl)


    def InsertPeople(self):
        #print("date")
        first = self.lineEdit.text()
        midl = self.lineEdit_2.text()
        last = self.lineEdit_3.text()
        birthday = str(self.dateEdit.date().toPyDate())

        sql = ("INSERT INTO students_test (First_Name,Middle_name,Last_Name,Birthday)"
 					"VALUES (%s,%s,%s,%s)")

        value = [first,midl,last,birthday]
        mycursor.execute(sql, value)
        con.commit()

        print(first,midl,last,birthday)
        self.Tablefill()



    def Tablefill(self):
        self.tableWidget.setColumnCount(0)
        sql = ("SELECT * FROM students_test")
        mycursor.execute(sql)
        all_data = mycursor.fetchall()
        self.tableWidget.setRowCount(len(all_data[1]))
        self.tableWidget.setColumnCount(len(all_data[0]))

        self.tableWidget.setItem(0,0, QTableWidgetItem("ID"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("First_Name"))
        self.tableWidget.setItem(0, 2 , QTableWidgetItem("Middle_name"))
        self.tableWidget.setItem(0, 3 , QTableWidgetItem("Last_Name"))
        self.tableWidget.setItem(0, 4 , QTableWidgetItem("Birthday"))
        self.tableWidget.setItem(0, 5 , QTableWidgetItem("Class"))
        
        for Row,allval in enumerate(all_data):
            for Column,value in enumerate(allval):
                self.tableWidget.setItem(Row+1,Column, QTableWidgetItem(str(value)))
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


    def SearchPeople(self):
        idSearch = self.lineEdit_4.text()
        sql = (f"SELECT * FROM students_test WHERE Student_ID = {idSearch}")
        mycursor.execute(sql)
        data = mycursor.fetchall()
        self.lineEdit_5.setText(data[0][1])
        self.lineEdit_7.setText(data[0][2])
        self.lineEdit_6.setText(data[0][3])
        date = data[0][4]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        self.dateEdit_2.setDate(date_object)
        print(date_object)

    def delete_ppl(self):
        idSearch = self.lineEdit_4.text()
        sql = (f"DELETE FROM students_test WHERE Student_ID = {idSearch}")
        mycursor.execute(sql)
        con.commit()
        print("Deleted")
        self.Tablefill()

    def Update_ppl(self):
        idSearch = self.lineEdit_4.text()
        fname = self.lineEdit_5.text()
        mname = self.lineEdit_7.text()
        lname = self.lineEdit_6.text()
        birthday = str(self.dateEdit_2.date().toPyDate())
        sql = (f"UPDATE students_test SET First_Name = '{fname}', Middle_name = '{mname}' , Last_Name = '{lname}' , Birthday = {birthday} WHERE Student_ID = {idSearch}")
        mycursor.execute(sql)
        con.commit()
        print("Updated")
        self.Tablefill()

# Main Function
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if  __name__ == "__main__":
    main()
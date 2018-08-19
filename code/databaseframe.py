import sys, os
import regex
import filemanage
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QScrollArea ,QTreeWidgetItem, QPushButton, QInputDialog, QLabel ,QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout,QHBoxLayout, QAbstractItemView
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from MainWindow import Ui_Form


class Call_UI(QWidget,Ui_Form):

    def __init__(self, parent = None, username='qwe', loginfr=None):
        username = username
        super(Call_UI, self).__init__(parent)
        self.setupUi(self)
        self.initUI(username)
        self.textEdit.setFocus()
        self.userlabel.setText('当前用户：'+username)
        self.loginfr = loginfr
        self.rgx = regex.RegMatch() #管理sql语句
        f = open(sys.path[0] + r'\table\users\users.txt','r',encoding = 'utf8')
        self.competence_lines = f.readlines()
        f.close()

    def initUI(self,username):
        QApplication.clipboard()   #获取系统剪贴板指针
        self.label = QLabel()
        self.label.setFont(QFont('微软雅黑',11))
        self.table = QTableWidget()
        self.horizontalLayout_2.addWidget(self.label,0, Qt.AlignTop)
        self.root = QTreeWidgetItem(self.treeW)
        self.root.setText(0, 'database')
        self.root.setIcon(0,QIcon(':/pic/database.png'))
        for f in filemanage.get_all_files(sys.path[0] + r'\table\dict'):
            item = QTreeWidgetItem(self.root)
            item.setText(0,f[:-4])      #去除文件扩展名
            item.setIcon(0, QIcon(':/pic/table.png'))
        self.treeW.expandAll()
        self.reset_btn.clicked.connect(self.label.clear)
        self.query_btn.clicked.connect(lambda: self.sql_manage(username))
        self.switch_btn.clicked.connect(self.question_when_switch)
        self.check_btn.clicked.connect(lambda: self.show_check_dialog(username))
        self.grant_btn.clicked.connect(self.show_grant_dialog)
        self.revoke_btn.clicked.connect(self.show_revoke_dialog)
        self.treeW.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeW.customContextMenuRequested.connect(self.generateMenu)

    def generateMenu(self, position):
        if self.treeW.currentItem():
            tablename = self.treeW.currentItem().text(0)
        row_num = -1
        for i in self.treeW.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num>=0:
            menu = QMenu()
            item1 = menu.addAction('查看数据表')
            item2 = menu.addAction('查看数据索引表')
            item3 = menu.addAction('查看数据字典')
            self.treeW.addTopLevelItem(self.root)
            action = menu.exec_(self.treeW.mapToGlobal(position))
            if action == item1:
                self.display_the_table(sys.path[0] + r'\table\tables\\'+tablename+'.txt')
            elif action == item2:
                dirlist = os.listdir(sys.path[0] + r'\table\index')
                item, ok = QInputDialog.getItem(self, '索引表', '请选择：', dirlist, 0, False)
                if ok:
                    self.display_the_table(sys.path[0] + r'\table\index\\'+item)
            elif action == item3:
                self.display_the_table(sys.path[0] + r'\table\dict\\'+tablename+'.txt')
            else:
                return

    def display_the_table(self, path):
        f = open(path,'r',encoding = 'utf8')
        lines = f.readlines()
        f.close()
        dlg = QDialog(self)
        if len(lines)>0:
            verticalHeaderLabels = ['No.'+str(i+1) for i,j in enumerate(lines)]
            rows_lenth = len(lines)
            columns_lenth = len(lines[0].split())
            dlg = QDialog(self)
            verticalLayout = QVBoxLayout(dlg)
            scrollAreaWidgetContents = QWidget()
            horizontalLayout = QHBoxLayout(scrollAreaWidgetContents)
            horizontalLayout.setContentsMargins(0, 0, 0, 0)
            scrollArea = QScrollArea()
            scrollArea.setWidgetResizable(True)
            scrollArea.setWidget(scrollAreaWidgetContents)
            if '_' in path:
                content = ''
                for i in lines:
                    content += i
                label = QLabel()
                label.setText(content.replace('], [', '],   ['))
                label.setFont(self.font)
                horizontalLayout.addWidget(label)
            else:
                table = QTableWidget()
                table.setRowCount(rows_lenth)
                table.setColumnCount(columns_lenth)
                table.setEditTriggers(QAbstractItemView.NoEditTriggers)     #表格设置为不可编辑
                table.setSelectionBehavior(QAbstractItemView.SelectRows)
                table.setVerticalHeaderLabels(verticalHeaderLabels)
                horizontalLayout.addWidget(table)
                for i in range(rows_lenth):
                    for j in range(columns_lenth):
                        tablecontent = lines[i].split()[j]
                        table.setItem(i,j, QTableWidgetItem(tablecontent))
            ok_btn = QPushButton('确定')
            ok_btn.clicked.connect(dlg.close)
            verticalLayout.addWidget(scrollArea)
            verticalLayout.addWidget(ok_btn, 0, Qt.AlignCenter)
        dlg.resize(700,450)
        dlg.show()

    def question_when_switch(self):
        reply = QMessageBox.warning(self, '切换用户', '跳转到登录窗口', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.close()
            self.loginfr.show()

    def show_check_dialog(self, username):
        dlg = QDialog(self)
        dlg.setWindowTitle('查看权限')
        verticalLayout = QVBoxLayout(dlg)
        ok_btn = QPushButton('确定')
        ok_btn.clicked.connect(dlg.close)
        label = QLabel()
        label.setFont(self.font)
        competence = ''
        for i in self.competence_lines:
            if username == i.split()[0]:
                competence += '操作：'+i.strip(' ').replace(username+' ','').replace(' ', '  数据库表：')
        label.setText('当前用户的权限有：\n'+competence)
        verticalLayout.addWidget(label)
        verticalLayout.addWidget(ok_btn,0,Qt.AlignCenter)
        dlg.setLayout(verticalLayout)
        dlg.setModal(True)
        dlg.show()

    def show_grant_dialog(self):
        text, _ = QInputDialog.getText(self, '授权', '请输入grant语句:')
        if text:
            result = self.rgx.matchsql(text)
            if result[0][0] == 'grant':
                res = filemanage.grant(sys.path[0] + r'\table',r'\users\users.txt', result[1:])
                QMessageBox.information(self, '结果', res, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, '错误', '不是正确的grant语句', QMessageBox.Ok)


    def show_revoke_dialog(self):
        text, _ = QInputDialog.getText(self, '撤销权限', '请输入revoke语句:')
        if text:
            result = self.rgx.matchsql(text)
            if result[0][0] == 'revoke':
                res = filemanage.revoke(sys.path[0] + r'\table',r'\users\users.txt', result[1:])
                QMessageBox.information(self, '结果', res, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, '错误', '不是正确的revoke语句', QMessageBox.Ok)

    def cannot_operate_dialog(self,message):
        QMessageBox.critical(self, '权限错误', message, QMessageBox.Ok)

    def check_competence(self, username, operation, tables):
        dirname = sys.path[0] + r'\table'
        competence = [i.strip().replace(username+' ','') for i in self.competence_lines if i.split()[0] == username]
        operation_and_table =[[],[]]
        operation_and_table[0]=list(set(j for i in competence for j in i.split()[0].split(',')))    #操作去重复
        operation_and_table[1] = [i.split()[-1] for i in competence]
        if operation not in operation_and_table[0]:
            return '当前用户没有'+operation+'权限'
        for i in tables:
            if filemanage.isExist(dirname+'\\dict\\',i+'.txt') and i not in operation_and_table[1]:
                return'不能对'+i+'表进行'+operation+'操作'
        return True

    def sql_manage(self,username):
        sql = self.textEdit.toPlainText()
        if sql:
            result = self.rgx.matchsql(sql)
            if result[0][0] == 'select':
                consequence = self.check_competence(username, 'select', result[1])
                if consequence != True:
                    self.cannot_operate_dialog(consequence)
                else:
                    self.select_data(result)
            else:
                self.table.hide()
                self.label.show()
                if result[0][0] == 'create table':      #第一个列表元素是sql操作标记
                    self.create_table(result)
                elif result[0][0] == 'insert':
                    consequence = self.check_competence(username, 'insert', result[1])
                    if consequence != True:
                        self.cannot_operate_dialog(consequence)
                    else:
                        self.insert_into(result)
                elif result[0][0] == 'update':
                    consequence = self.check_competence(username, 'update', result[1])
                    if consequence != True:
                        self.cannot_operate_dialog(consequence)
                    else:
                        self.update_table(result)
                elif result[0][0] == 'delete':
                    consequence = self.check_competence(username, 'delete', result[1])
                    if consequence != True:
                        self.cannot_operate_dialog(consequence)
                    else:
                        self.delete_data(result)
                elif result[0][0] == 'create index':
                    self.create_index(result)
                elif result[0][0] == 'drop table':
                    self.drop_table(result)
                elif result[0][0] == 'drop column':
                    self.drop_column(result)
                elif result[0][0] == 'add column':
                    self.add_column(result)
                elif result[0][0] == 'drop index':
                    self.drop_index(result)
                else:
                    self.label.setText(result)

    def create_table(self, result):
        dirname = sys.path[0] + r'\table'
        if not filemanage.isExist(dirname+'\\dict',result[1][0]+'.txt'):    #表是否已经存在
            filemanage.write_dict_to_file(dirname, result[1][0]+'.txt',result[2:])    #将表属性写入表字典
            item = QTreeWidgetItem(self.root)
            item.setText(0,result[1][0])
            item.setIcon(0, QIcon(':/pic/table.png'))
            self.label.setText(result[1][0] + '表创建成功.')
        else:
            self.label.setText('创建失败,'+result[1][0]+'表已经存在.')

    def insert_into(self, result):
        dirname = sys.path[0] + r'\table'
        if filemanage.isExist(dirname + '\\dict\\',result[1][0]+'.txt'):
            valid = filemanage.is_valid_arguments(dirname + '\\dict\\' + result[1][0] + '.txt', result[2])
            if valid != True:
                self.label.setText(valid)
            else:
                filemanage.write_data_to_file(dirname+'\\tables\\'+result[1][0]+'.txt', result[2])
                self.label.setText(result[1][0] + '表数据添加成功.')
        else:
            self.label.setText('数据添加失败,请确认是否已经创建了此表.')

    def update_table(self,result):
        dirname = sys.path[0] + r'\table'
        if filemanage.isExist(dirname + '\\dict\\',result[1][0]+'.txt'):
            valid = filemanage.is_valid_data(dirname + '\\dict\\' + result[1][0] + '.txt', result[2:])
            if valid != True:
                self.label.setText(valid)
            else:
                self.label.setText(filemanage.update_file(dirname, result[1][0] + '.txt', result[2:]))
        else:
            self.label.setText('数据库表更新失败,'+ result[1][0] +'表不存在.')

    def delete_data(self,result):
        dirname = sys.path[0] + r'\table'
        if filemanage.isExist(dirname + '\\dict\\',result[1][0]+'.txt'):
            if len(result) == 3:
                valid = filemanage.is_valid_data(dirname + '\\dict\\' + result[1][0] + '.txt', result[2:])
                if valid != True:
                    self.label.setText(valid)
                    return
            self.label.setText(filemanage.delete_file_data(dirname, result[1][0] + '.txt', result))
        else:
            self.label.setText('数据删除失败,'+ result[1][0] +'表不存在.')

    def select_data(self,result):
        dirname = sys.path[0] + r'\table'
        res = filemanage.select_data_from_file(dirname, result[1], result[2:])
        if isinstance(res, list):
            res = [i for i in res if i]
            rows_lenth = len(res)
            columns_lenth = len(res[0].split())
            self.label.hide()
            self.table.show()
            self.table.setRowCount(rows_lenth)
            self.table.setColumnCount(columns_lenth)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)     #表格设置为不可编辑
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.horizontalLayout_2.addWidget(self.table)
            print(res)
            for i in range(rows_lenth):
                for j in range(columns_lenth):
                    tablecontent = res[i].split()[j]
                    self.table.setItem(i,j, QTableWidgetItem(tablecontent))
        else:
            self.table.hide()
            self.label.show()
            self.label.setText(res)

    def create_index(self,result):
        dirname = sys.path[0] + r'\table'
        if filemanage.isExist(dirname + '\\dict\\',result[1][0]+'.txt'):
            res = filemanage.create_index_bytree(dirname, result[1][0], result[1:])
            self.label.setText(res)
        else:
            self.label.setText('不能建立索引,'+ result[1][0] +'表不存在.')

    def drop_table(self,result):
        dirname = sys.path[0] + r'\table'
        self.label.setText(filemanage.drop_table(dirname, result[-1][0]))
        self.root.takeChildren()
        for f in filemanage.get_all_files(sys.path[0] + r'\table\dict'):
            item = QTreeWidgetItem(self.root)
            item.setText(0,f[:-4])      #去除文件扩展名
            item.setIcon(0, QIcon(':/pic/table.png'))

    def drop_column(self, result):
        dirname = sys.path[0] + r'\table'
        self.label.setText(filemanage.drop_column(dirname, result[1][0], result[-1][0]))

    def add_column(self, result):
        dirname = sys.path[0] + r'\table'
        self.label.setText(filemanage.add_column(dirname, result[1][0], result[2:]))

    def drop_index(self, result):
        dirname = sys.path[0] + r'\table'
        self.label.setText(filemanage.drop_index(dirname, result[1][0], result[-1][0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Call_UI()
    win.show()
    sys.exit(app.exec_())
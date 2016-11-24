# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox 

from Ui_main import Ui_Dialog

import function
import os

class Dialog(QDialog, Ui_Dialog):
    
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent=None):
        """
        Constructor
        songList = function.getSongList()
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        function.getSongList()
        while True:
             if os.path.exists('mrock_song_client_android.xml'):
                 break
        self.setList(Dialog.songList)
        if not(self.checkBoxIsZip.isChecked()):
            self.checkBoxIsDel.hide()
     
    def on_checkBoxIsZip_clicked(self):
        if self.checkBoxIsZip.isChecked():
            self.checkBoxIsDel.show()
        else:
            self.checkBoxIsDel.hide()
        
    @pyqtSlot()
    def on_pushButton_clicked(self):
         song = self.selectBox.currentIndex()
         songPath = Dialog.songList[song][1]
         downAll = self.checkBoxDownAll.isChecked()
         isZip = self.checkBoxIsZip.isChecked()
         isDel = self.checkBoxIsDel.isChecked()
         if downAll:
            QMessageBox.information(self, '提示', '下载文件量巨大，请不要关闭窗口')
            for i in Dialog.songList:
                function.downSong(i[0])
                function.getPng(i[0]+'/')
         function.downSong(songPath)
         function.getPng(songPath+'/')
         if isZip:
             if isDel:
                 function.getZip(songPath+'/', songPath+'.zip', True)
             else:
                function.getZip(songPath+'/', songPath+'.zip', False)
         QMessageBox.information(self, '提示', '下载完成')
    
    def setList(self, songList):
        for i in songList:
            self.selectBox.addItem(i[0])

        
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
    

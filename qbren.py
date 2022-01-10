#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, string, glob
from PyQt4 import QtCore, QtGui, uic

#~ print("!\n+\n-\n---\n+++\n>\n<\n")

myname = os.path.splitext(os.path.basename(__file__))[0]
myfolder = os.path.dirname(os.path.realpath(__file__))
print("myname=%r"%myname)
print("myfolder=%r"%myfolder)

def logd(*args, **kwargs):
	if len(args)>1:
		print(args[0]%args[1:])
	else:
		print(*args)
	if kwargs:
		print("!", kwargs)


class MainWindow(QtGui.QMainWindow):
	def __init__(self, names):
		QtGui.QMainWindow.__init__(self)
		uic.loadUi(os.path.join(myfolder, "main-window.ui"), self)

		self.snames = names

		self.le_example.setText(self.snames[0])

		self.lw_snames.clear()
		self.lw_snames.addItems(self.snames)

		self.show()

		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.first_init)
		self.timer.start(0.0)
		#~ self.first_init()


	def do_rename(self):
		logd("do_rename:")

	def first_init(self):
		logd("on_timer:")
		self.cb_actions_changed()
		self.le_example_update_selection()


	def cb_actions_changed(self):
		act_idx = self.cb_actions.currentIndex()
		if act_idx==0: # delete symbols
			self.f_del_symbols.setVisible(True)
			self.f_replace.setVisible(False)
			self.f_change_ext.setVisible(False)
			self.f_insert.setVisible(False)
		elif act_idx==1: # insert symbols
			self.f_del_symbols.setVisible(False)
			self.f_replace.setVisible(False)
			self.f_change_ext.setVisible(False)
			self.f_insert.setVisible(True)
		elif act_idx==2: # replace symbols
			self.f_del_symbols.setVisible(False)
			self.f_replace.setVisible(True)
			self.f_change_ext.setVisible(False)
			self.f_insert.setVisible(False)
		elif act_idx==3: # change extension
			self.f_del_symbols.setVisible(False)
			self.f_replace.setVisible(False)
			self.f_change_ext.setVisible(True)
			self.f_insert.setVisible(False)
		else:
			logd("cb_actions_changed: unknown act_idx=%r", act_idx)
		self.lw_dnames_update()


	def le_example_update_selection(self):
		start_pos = self.sb_del_from_idx.value()
		count = self.sb_del_from_count.value()
		logd("le_example_update_selection: start_pos=%r, count=%r",
			start_pos, count)
		self.lw_dnames_update()
		self.le_example.blockSignals(True)
		self.le_example.setSelection(start_pos, count)
		self.le_example.blockSignals(False)


	def le_example_leaved(self):
		logd("le_example_leaved:")
		self.le_example_update_selection()


	def lw_snames_selchanged(self):
		self.le_example.setText(self.lw_snames.currentItem().text())
		self.le_example_update_selection()

	def sb_del_values_update(self):
		#~ logd("sb_del_values_update: hasSelectedText()=%r,"
			#~ " selectionStart()=%r",
			#~ self.le_example.hasSelectedText(),
			#~ self.le_example.selectionStart())
		start_pos = self.le_example.selectionStart()
		count = len(self.le_example.selectedText())
		if start_pos==-1 and count==0:
			return
		logd("sb_del_values_update: start_pos=%r, count=%r", start_pos, count)

		self.sb_del_from_idx.blockSignals(True)
		self.sb_del_from_count.blockSignals(True)

		self.sb_del_from_idx.setValue(start_pos)
		self.sb_del_from_count.setValue(count)

		self.sb_del_from_idx.blockSignals(False)
		self.sb_del_from_count.blockSignals(False)
		self.lw_dnames_update()


	def process_name(self, sn):
		act_idx = self.cb_actions.currentIndex()
		if act_idx==0: # delete symbols
			start_pos = self.sb_del_from_idx.value()
			count = self.sb_del_from_count.value()
			dn = sn[:start_pos] + sn[start_pos+count:]
		else:
			dn = "act_idx="+str(act_idx)+" " + sn
		return dn

	def lw_dnames_update(self):
		self.lw_dnames.clear()
		for i in range(self.lw_snames.count()):
			new_name = self.process_name(self.lw_snames.item(i).text())
			self.lw_dnames.addItem(new_name)

	def keyPressEvent(self, event):
		key = event.key()

		if key == QtCore.Qt.Key_Escape:
			self.close()

		elif key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
			self.do_rename()

		else:
			logd("keyPressEvent: key=%s", key)

	def closeEvent(self, event):
		logd("Exiting")
		event.accept()
		#~ result = QtGui.QMessageBox.question(self,
					  #~ "Confirm Exit...",
					  #~ "Are you sure you want to exit ?",
					  #~ QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
		#~ event.ignore()

		#~ if result == QtGui.QMessageBox.Yes:
			#~ event.accept()

def main():
	logd("Current dir: '%s'", os.getcwd())

	if len(sys.argv)>1:
		sfilenames = sys.argv[1:]
	else:
		sfilenames = glob.glob("*")

	# todo: check for unicode above 0xffff and ask to fix
	#~ sfilenames = strip_above_0xffff("|".join(sfilenames)).split("|")

	logd("\n".join(sfilenames))

	app = QtGui.QApplication(sys.argv)
	mw = MainWindow(sfilenames)
	sys.exit(app.exec())

if __name__=='__main__':
	main()

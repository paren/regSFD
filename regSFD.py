#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# regSFD'10
# (c)opyleft 2009 GULT <contacto at gultij dot org>
# Licensed under GPLv3 or any version higher; see license.txt for details
#
import gtk
from gtk import glade
from sqlite3 import dbapi2 as sqlite
import webbrowser
import sys

class RegSFD:
    def __init__(self):
        self.xml = glade.XML("regSFD.glade", None, None)
        self.xml.signal_connect("on_btnSave_clicked", self.on_save_click)
        self.xml.signal_connect("on_imagemenuitem3_activate", self.on_save_click)
        self.xml.signal_connect("on_btnCancel_clicked", self.on_cancel_click)
        self.xml.signal_connect("on_menuitem2_activate", self.on_cancel_click)
        self.xml.signal_connect("on_btnAbout_clicked", self.aboutBox)
        self.xml.signal_connect("on_imagemenuitem10_activate", self.aboutBox)
        self.xml.signal_connect("on_btnClose_clicked", lambda w: gtk.main_quit())
        self.xml.signal_connect("on_imagemenuitem5_activate", lambda w: gtk.main_quit())
        self.xml.signal_connect("on_window1_destroy", lambda w: gtk.main_quit())
        self.noReg = self.xml.get_widget("lblNoReg")
        self.name = self.xml.get_widget("txtName")
        self.age = self.xml.get_widget("sbAge")
        self.email = self.xml.get_widget("txtEmail")
        self.occupation = self.xml.get_widget("txtOccupation")
        self.noReg.set_label(str(self.getNoReg(1)))
        self.treeStore = gtk.TreeStore(str)
        self.treeView = self.xml.get_widget("treeview1")
        self.treeView.set_model(self.treeStore)
        self.addColumn("# Reg", 0)
        self.addColumn("Nombre", 1)
        self.addColumn("Edad", 2)
        self.addColumn("Email", 3)
        self.addColumn("Ocupación", 4)
        self.listStore = gtk.ListStore(int, str, int, str, str)
        self.treeList = self.xml.get_widget("treeview1")
        self.treeList.set_model(self.listStore)
        self.getRecords()

    def addColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(),text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.treeView.append_column(column)

    def populateGrid(self, data):
        self.listStore.append(data)

    def getNoReg(self, a):
        try:
            conn = sqlite.connect("regSFD.db")
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute("SELECT max(noReg) FROM regSFD")
            b = cur.fetchone()[0]
        finally:	
            cur.close()
            conn.close()
        if b:
            return a + b 
        else:
            return a

    def getRecords(self):
        try:
            conn = sqlite.connect("regSFD.db")
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute("SELECT noReg, name, age, email, occupation FROM regSFD ORDER BY noReg")
            rows = cur.fetchall()
            for row in rows:
                self.populateGrid(row)
        finally:
            cur.close()
            conn.close()
		
    def insert(self, name, age, email, occupation):
        values = (name, age, email, occupation)
        data = (self.getNoReg(1), values[0], values[1], values[2], values[3])
        i = 1
        try:
            conn = sqlite.connect("regSFD.db")
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute("INSERT INTO regSFD (name, age, email, occupation) VALUES (?, ?, ?, ?)", values)
            conn.commit()
            self.populateGrid(data)
        except:
            print "except"
            print sys.exc_info()
        finally:	
            cur.close()
            conn.close()

    def clear(self):
        self.name.set_text("")
        self.age.set_text("18")
        self.email.set_text("")
        self.occupation.set_text("")
		
    def errorMessage(self, message):
        print message
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.run()
        dialog.destroy()
		
    def aboutBox(self, w):
        license = open("license.txt", "r")
        authors = ["GULT <contacto at gultij dot org>"]
        about = gtk.AboutDialog()
        about.set_position(gtk.WIN_POS_CENTER)
        about.set_program_name("regSFD'10")
        about.set_version("0.1.0.0")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("sfdlogo.png"))
        about.set_copyright("(c)opyleft 2009 GULTJ")
        about.set_comments("regSFD'10 is a simple tool for register people assistant on SFD")
        about.set_license(license.read())
        about.set_wrap_license(True)
        about.set_website("http://www.gultij.org/")
        about.set_website_label("www.gultij.org")
        def showWebsite(about, link, user_data):
            webbrowser.open(link)
        gtk.about_dialog_set_url_hook(showWebsite)
        about.set_authors(authors)
        about.run()
        about.destroy()
		
    def on_save_click(self, w):
        name = self.name.get_text().upper()
        age = self.age.get_value_as_int()
        email = self.email.get_text().lower()
        occupation = self.occupation.get_text().upper()
        if name and age and email and occupation:
            self.insert(name, age, email, occupation)
            self.clear()
            self.noReg.set_label(str(self.getNoReg(1)))
        else:
            self.errorMessage("Tiene que capturar todos los campos antes de grabar.")
	
    def on_cancel_click(self, w):
        self.clear()
        self.noReg.set_label(str(self.getNoReg(1)))

if __name__ == "__main__":
    regSFD = RegSFD()
    gtk.main()

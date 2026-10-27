import sys
from PySide6.QtCore import Qt,QObject,QThread,Signal
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QListWidget,QLineEdit,QDialog,QFormLayout,QComboBox,QSpinBox,QFileDialog,QMessageBox
from . import backend as b
STYLE="""QWidget{background:#0b1020;color:#f6f8ff;font-family:'Segoe UI';font-size:13px}QPushButton{background:#1c2840;color:white;padding:12px;border:1px solid #345; border-radius:9px}QPushButton:hover{background:#116b75}QLineEdit,QSpinBox,QComboBox,QListWidget{background:#151d30;color:white;padding:9px;border:1px solid #345;border-radius:9px}QListWidget::item{padding:14px}QListWidget::item:selected{background:#166776}"""
class Worker(QObject):
    done=Signal(object,object)
    def __init__(self,fn): super().__init__();self.fn=fn
    def run(self):
        try:self.done.emit(self.fn(),None)
        except Exception as e:self.done.emit(None,str(e))
class Window(QMainWindow):
    def __init__(self):
        super().__init__();self.jobs=[];self.setWindowTitle("MH Andrio");self.resize(1000,670)
        root=QWidget();self.setCentralWidget(root);v=QVBoxLayout(root);v.setContentsMargins(28,24,28,24);v.setSpacing(15)
        title=QLabel("MH ANDRIO  ◈  Android Workspace");title.setStyleSheet("font-size:26px;font-weight:700;color:#10c9c3");v.addWidget(title)
        v.addWidget(QLabel("Create and manage isolated Android emulator instances"))
        self.list=QListWidget();v.addWidget(self.list)
        row=QHBoxLayout();v.addLayout(row)
        for label,fn in [("Refresh",self.refresh),("+ New Instance",self.create),("Start",self.start),("Stop",self.stop),("Install APK",self.apk),("Delete",self.delete)]:
            btn=QPushButton(label);btn.clicked.connect(fn);row.addWidget(btn)
        self.status=QLabel("Checking Android SDK...");v.addWidget(self.status);self.refresh()
    def job(self,fn,callback=None):
        self.status.setText("Working...")
        t=QThread(self);w=Worker(fn);w.moveToThread(t);t.started.connect(w.run)
        def finish(result,error):
            if error: self.status.setText("Error");QMessageBox.warning(self,"MH Andrio",error)
            else:
                self.status.setText("Ready")
                if callback:callback(result)
            t.quit()
        w.done.connect(finish);t.finished.connect(w.deleteLater);t.finished.connect(t.deleteLater)
        t.finished.connect(lambda:self.jobs.remove((t,w)) if (t,w) in self.jobs else None)
        self.jobs.append((t,w));t.start()
    def selected(self):
        item=self.list.currentItem()
        if not item: QMessageBox.information(self,"MH Andrio","Select an instance first");return None
        return item.text().split("   |")[0]
    def refresh(self):
        self.job(lambda:(b.devices(),b.running()),self.show)
    def show(self,data):
        names,active=data;self.list.clear()
        for name in names:self.list.addItem(name+"   |   "+("RUNNING" if name in active else "OFFLINE"))
        self.status.setText(f"{len(names)} instances • {len(active)} running • SDK: {b.SDK}")
    def create(self):
        def got(images):
            if not images: QMessageBox.warning(self,"MH Andrio","Install an Android x86_64 system image in Android Studio SDK Manager first.");return
            d=QDialog(self);d.setWindowTitle("New Android Instance");layout=QVBoxLayout(d);form=QFormLayout();layout.addLayout(form)
            name=QLineEdit();name.setPlaceholderText("MH_Android_01");form.addRow("Name",name)
            img=QComboBox();img.addItems(images);form.addRow("Android image",img)
            ram=QSpinBox();ram.setRange(512,16384);ram.setValue(2048);form.addRow("RAM (MB)",ram)
            cpu=QSpinBox();cpu.setRange(1,16);cpu.setValue(2);form.addRow("CPU cores",cpu)
            ok=QPushButton("Create");ok.clicked.connect(d.accept);layout.addWidget(ok)
            if d.exec():self.job(lambda:b.create(name.text(),img.currentText(),ram.value(),cpu.value()),lambda _:self.refresh())
        self.job(b.images,got)
    def start(self):
        n=self.selected()
        if n:self.job(lambda:b.start(n),lambda _:self.refresh())
    def stop(self):
        n=self.selected()
        if n:self.job(lambda:b.stop(n),lambda _:self.refresh())
    def apk(self):
        n=self.selected()
        if n:
            path,_=QFileDialog.getOpenFileName(self,"Install APK","","Android APK (*.apk)")
            if path:self.job(lambda:b.install(n,path),lambda r:QMessageBox.information(self,"MH Andrio",r))
    def delete(self):
        n=self.selected()
        if n and QMessageBox.question(self,"Delete",f"Permanently delete {n} and its data?")==QMessageBox.StandardButton.Yes:
            self.job(lambda:b.delete(n),lambda _:self.refresh())
    def closeEvent(self,event):
        if self.jobs:QMessageBox.information(self,"MH Andrio","Wait for current operation");event.ignore()
        else:super().closeEvent(event)
def main():
    app=QApplication(sys.argv);app.setStyle("Fusion");app.setStyleSheet(STYLE);w=Window();w.show();sys.exit(app.exec())

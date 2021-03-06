from PyQt5.QtGui import (QPixmap, QPainter, QPen, QColor)
from PyQt5.QtCore import Qt, QPoint
import sqlite3


class Detailer:
    def __init__(self, conn_type, conn_geometry):
        self.conn_type = conn_type
        # get the member properties both for beam and supporting member
        db = sqlite3.connect('./data/aisc.db')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        member = (conn_geometry['size'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d = data['d']
        self.bf = data['bf']
        self.tw = data['tw']
        self.tf = data['tf']
        member = (conn_geometry['size2'],)
        cur.execute("SELECT * FROM section WHERE size=?", member)
        data = dict(cur.fetchone())
        self.d2 = data['d']
        self.bf2 = data['bf']
        self.tw2 = data['tw']
        self.tf2 = data['tf']
        self.k2 = data['k']
        db.close()
        # retrieve data from conn_geometry
        if self.conn_type == 'ShearGusset' or self.conn_type == 'ShearCope':
            self.col = int(conn_geometry['col'])
            self.ev = float(conn_geometry['ev'])
            self.tg = float(conn_geometry['tg'])
        elif self.conn_type == 'ShearClip':
            self.g = float(conn_geometry['g'])
            self.ev = float(conn_geometry['ev'])
            self.ta = float(conn_geometry['ta'])
        elif self.conn_type == 'ShearEndPlate':
            self.g = float(conn_geometry['g'])
            self.ev = float(conn_geometry['ev'])
            self.te = float(conn_geometry['te'])
            self.W = float(conn_geometry['W'])
        # common parameters from conn_geometry
        self.dia = float(conn_geometry['dia'])
        self.nos = int(conn_geometry['nos'])
        self.spacing = float(conn_geometry['spacing'])
        self.eh = float(conn_geometry['eh'])
        self.H = float(conn_geometry['H'])
        self.c = float(conn_geometry['c'])
        self.support = conn_geometry['support']
        self.tr = 0.375    # rib plate thickness
        self.gap = 0.375   # clear distance between steel plates
        self.weld_clearance = 0.625   # clear distance between weld and steel plate
        # set scale for drawing with 400px x 400px canvas at starting point 50px top-left
        if self.support == 'Beam':
            self.scale = 300.0/(1.5*self.d2)
        elif self.support == 'Column Web':
            if self.bf2 > self.d:
                max_size = self.bf2
            else:
                max_size = self.d
            self.scale = 300.0/(2.0*max_size)
        elif self.support == 'Column Flange':
            if self.d2 > self.d:
                max_size = self.d2
            else:
                max_size = self.d
            self.scale = 300.0 / (2.0 * max_size)

    def drawDetail(self, canvas_label):
        canvas = QPixmap(400, 400)
        canvas.fill(color=Qt.white)
        canvas_label.setPixmap(canvas)
        painter = QPainter(canvas_label.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        # set starting point of drawing
        """if self.support == 'Beam' or self.support == 'Column Web':
            x_start = int((400 - self.scale*self.bf2 * 3)/2.0)
            y_start = int((400 - self.scale*self.d2 * 2)/2.0)
        else:
            x_start = int((400 - self.scale * self.d2 * 2) / 2.0)
            y_start = int((400 - self.scale * self.d * 2) / 2.0)"""
        x_start = 75
        y_start = 50 + int(self.scale * self.d2 / 4)
        self.drawSupport(pen, painter, x_start, y_start)
        self.drawBeam(pen, painter, x_start, y_start)
        self.drawGussetPlate(pen, painter, x_start, y_start)
        self.drawBolts(pen, painter, x_start, y_start)
        painter.end()

    def drawSupport(self, pen, painter, x_start, y_start):
        # set pen
        pen.setWidth(1)
        pen.setColor(QColor(10, 10, 10))
        painter.setPen(pen)
        x = x_start
        y = y_start
        if self.support == 'Beam':
            width = int(self.scale * self.bf2)
            height = int(self.scale * self.tf2)
            painter.drawRect(x, y, width, height)
            x = x + int(self.scale * (self.bf2 - self.tw2) / 2)
            y = y + int(self.scale * self.tf2)
            width = int(self.scale * self.tw2)
            height = int(self.scale * (self.d2 - 2*self.tf2))
            painter.drawRect(x, y, width, height)
            x = x_start
            y = y + int(self.scale * (self.d2 - 2*self.tf2))
            width = int(self.scale * self.bf2)
            height = int(self.scale * self.tf2)
            painter.drawRect(x, y, width, height)
        elif self.support == 'Column Web':
            x1 = x_start
            x2 = x_start
            y1 = y_start - int(self.scale*self.bf2/4.0)
            y2 = y_start + int(self.scale*self.d * 1.25)
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale*(self.bf2/2.0 - self.tw2/2.0))
            x2 = x1
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0))
            x2 = x1
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale * self.bf2)
            x2 = x1
            painter.drawLine(x1, y1, x2, y2)
            # draw rib plate
            if self.conn_type == 'ShearGusset':
                x = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0))
                y = y_start
                width = int(self.scale*(self.bf2 - self.tw2)/2.0)
                height = int(self.scale*self.tr)
                painter.drawRect(x, y, width, height)
                y = y_start + int(self.scale*(self.d - self.tr))
                painter.drawRect(x, y, width, height)

        elif self.support == 'Column Flange':
            x1 = x_start
            x2 = x_start
            y1 = y_start - int(self.scale * self.bf2 / 4.0)
            y2 = y_start + int(self.scale * self.d * 1.25)
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale*self.tf2)
            x2 = x_start + int(self.scale*self.tf2)
            painter.drawLine(x1, y1, x2, y2)
            y1 = y_start - int(self.scale * self.bf2 / 4.0)
            y2 = y_start + int(self.scale * self.d * 1.25)
            x1 = x_start + int(self.scale * (self.d2 - self.tf2))
            x2 = x_start + int(self.scale * (self.d2 - self.tf2))
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale * self.d2)
            x2 = x_start + int(self.scale * self.d2)
            painter.drawLine(x1, y1, x2, y2)

    def drawBeam(self, pen, painter, x_start, y_start):
        # pen setting
        pen.setWidth(2)
        pen.setColor(QColor('black'))
        painter.setPen(pen)
        if self.conn_type == 'ShearGusset':
            if self.support == 'Beam' or self.support == 'Column Web':
                x1 = x_start + int(self.scale*(self.bf2 + self.gap))
                y1 = y_start
                if self.d2 <= 12 or self.bf2 >= 12:
                    x2 = x1 + int(self.scale*((2*self.eh + self.spacing)*1.0))
                else:
                    x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 2.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale*self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1
                y1 = y_start
                y2 = y1 + int(self.scale * self.c)
                painter.drawLine(x1, y1, x2, y2)
                y1 = y2
                y2 = y2 + int(self.scale*self.H)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                y1 = y2
                y2 = y2 + int(self.scale * (self.d - self.c - self.H))
                painter.drawLine(x1, y1, x2, y2)
                if self.d2 <= 12 or self.bf2 >= 12:
                    x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                else:
                    x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 2.0))
                y1 = y2 - int(self.scale*self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + self.scale*self.tf
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
            else:
                x1 = x_start + int(self.scale * (self.d2 + self.weld_clearance))
                y1 = y_start
                x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1
                y1 = y_start
                y2 = y1 + int(self.scale * self.c)
                painter.drawLine(x1, y1, x2, y2)
                y1 = y2
                y2 = y2 + int(self.scale * self.H)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                y1 = y2
                y2 = y2 + int(self.scale * (self.d - self.c - self.H))
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                y1 = y2 - int(self.scale * self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + self.scale * self.tf
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
        elif self.conn_type == 'ShearCope':
            x1 = x_start + int(self.scale * (self.bf2 + self.gap))
            y1 = y_start
            x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)
            y1 = y1 + int(self.scale * self.tf)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)
            x2 = x1
            y1 = y_start
            y2 = y1 + int(self.scale * (self.c - self.gap))
            painter.drawLine(x1, y1, x2, y2)
            x1 = x_start + int(self.scale*(self.bf2/2.0 + self.tw2/2.0 + self.weld_clearance))
            x2 = x_start + int(self.scale * self.bf2)
            y1 = y_start + int(self.scale*self.c)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)
            x = x2 - int(self.scale*self.gap)
            y = y1 - int(self.scale*self.gap*2)
            arc_width = int(self.scale*self.gap*2)
            arc_height = arc_width
            painter.drawArc(x, y, arc_width, arc_height, 4320, 1440)

            x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.weld_clearance))
            x2 = x1
            y1 = y_start + int(self.scale * self.c)
            y2 = y1 + int(self.scale * self.H)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(x1, y1, x2, y2)
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)

            if self.d > (self.d2 - self.k2):
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.weld_clearance))
                x2 = x1
                y1 = y_start + int(self.scale * self.c) + int(self.scale * self.H)
                y2 = y_start + int(self.scale * (self.d - self.c))
                painter.drawLine(x1, y1, x2, y2)

                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.weld_clearance))
                x2 = x_start + int(self.scale * self.bf2)
                y1 = y_start + int(self.scale*(self.d - self.c))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x = x2 - int(self.scale*self.gap)
                y = y1
                arc_width = int(self.scale * self.gap * 2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 0, 1440)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                x2 = x1
                y1 = y1 + int(self.scale*self.gap)
                y2 = y_start + int(self.scale*self.d)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                y1 = y_start + int(self.scale*(self.d - self.tf))
                x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * self.d)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
            else:
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.weld_clearance))
                x2 = x_start + int(self.scale * (self.bf2 + self.gap)) + int(self.scale * ((2 * self.eh + self.spacing)
                                                                                           * 1.0))
                y1 = y_start + int(self.scale * (self.d - self.tf))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * self.d)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)

                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.weld_clearance))
                x2 = x1
                y1 = y_start + int(self.scale * self.c) + int(self.scale * self.H)
                y2 = y_start + int(self.scale * self.d)
                painter.drawLine(x1, y1, x2, y2)

        elif self.conn_type == 'ShearClip':
            if self.support == 'Beam':
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                y1 = y_start
                x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1
                y1 = y_start
                y2 = y1 + int(self.scale * (self.c - self.gap))
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale*(self.bf2/2.0 + self.tw2/2.0 + self.gap))
                x2 = x_start + int(self.scale * self.bf2)
                y1 = y_start + int(self.scale*self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x = x2 - int(self.scale*self.gap)
                y = y1 - int(self.scale*self.gap*2)
                arc_width = int(self.scale*self.gap*2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 4320, 1440)
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                x2 = x1
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale * self.H)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)

                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)

                if self.d > (self.d2 - self.k2):
                    x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                    x2 = x1
                    y1 = y_start + int(self.scale * self.c) + int(self.scale * self.H)
                    y2 = y_start + int(self.scale * (self.d - self.c))
                    painter.drawLine(x1, y1, x2, y2)

                    x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                    x2 = x_start + int(self.scale * self.bf2)
                    y1 = y_start + int(self.scale * (self.d - self.c))
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)
                    x = x2 - int(self.scale * self.gap)
                    y = y1
                    arc_width = int(self.scale * self.gap * 2)
                    arc_height = arc_width
                    painter.drawArc(x, y, arc_width, arc_height, 0, 1440)
                    x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                    x2 = x1
                    y1 = y1 + int(self.scale * self.gap)
                    y2 = y_start + int(self.scale * self.d)
                    painter.drawLine(x1, y1, x2, y2)
                    x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                    y1 = y_start + int(self.scale * (self.d - self.tf))
                    x2 = x1 + int(self.scale * ((2 * self.eh + self.spacing) * 1.0))
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)
                    y1 = y_start + int(self.scale * self.d)
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)
                else:
                    x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                    x2 = x_start + int(self.scale * (self.bf2 + self.gap)) + int(
                        self.scale * ((2 * self.eh + self.spacing)
                                      * 1.0))
                    y1 = y_start + int(self.scale * (self.d - self.tf))
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)
                    y1 = y_start + int(self.scale * self.d)
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)

                    x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                    x2 = x1
                    y1 = y_start + int(self.scale * self.c) + int(self.scale * self.H)
                    y2 = y_start + int(self.scale * self.d)
                    painter.drawLine(x1, y1, x2, y2)

            elif self.support == 'Column Web':
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + self.gap))
                y1 = y_start
                x2 = x_start + int(self.scale * ((self.bf2 + self.gap + 4.0 + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1
                y1 = y_start
                y2 = y_start + int(self.scale * self.c)
                painter.drawLine(x1, y1, x2, y2)
                y1 = y2
                y2 = y2 + int(self.scale * self.H)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                x2 = x1
                y1 = y_start + int(self.scale * self.c) + int(self.scale * self.H)
                y2 = y_start + int(self.scale * (self.d - self.c))
                painter.drawLine(x1, y1, x2, y2)
                # bottom flange
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.gap))
                x2 = x_start + int(self.scale * self.bf2)
                y1 = y_start + int(self.scale * (self.d - self.c))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x = x2 - int(self.scale * self.gap)
                y = y1
                arc_width = int(self.scale * self.gap * 2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 0, 1440)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                x2 = x1
                y1 = y1 + int(self.scale * self.gap)
                y2 = y_start + int(self.scale * self.d)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                y1 = y_start + int(self.scale * (self.d - self.tf))
                x2 = x1 + int(self.scale * ((4.0 + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * self.d)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
            elif self.support == 'Column Flange':
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                x1 = x_start + int(self.scale * (self.d2 + self.gap))
                y1 = y_start
                x2 = x_start + int(self.scale * ((self.d2 + self.gap + 4.0 + self.spacing) * 1.0))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.tf)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x2 = x1
                y1 = y_start
                y2 = y_start + int(self.scale * self.c)
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * self.c)
                y2 = y_start + int(self.scale * (self.c + self.H))
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.d2 + self.gap))
                x2 = x1
                y1 = y_start + int(self.scale * (self.c + self.H))
                y2 = y_start + int(self.scale * self.d)
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
                # bottom flange
                x1 = x_start + int(self.scale * (self.d2 + self.gap))
                x2 = x_start + int(self.scale * ((self.d2 + self.gap + 4.0 + self.spacing) * 1.0))
                y1 = y_start + int(self.scale * (self.d - self.tf))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * self.d)
                y2 = y1
                print(y1, y2)
                painter.drawLine(x1, y1, x2, y2)

    def drawGussetPlate(self, pen, painter, x_start, y_start):
        pen.setStyle(Qt.SolidLine)
        pen.setColor(QColor('blue'))
        painter.setPen(pen)
        if self.conn_type == 'ShearGusset':
            if self.support == 'Beam':
                x1 = x_start + int(self.scale*self.bf2)
                x2 = x1
                y1 = y_start + int(self.scale*self.tf2)
                y2 = y_start + int(self.scale * (self.c - self.gap))
                painter.drawLine(x1, y1, x2, y2)
                x = x2
                y = y2 - self.scale*self.gap
                arc_width = int(self.scale*self.gap*2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 2880, 1440)
                x1 = x_start + int(self.scale*(self.bf2 + self.gap))
                x2 = x1 + int(self.scale*(2*self.eh + self.spacing*(self.col-1)))
                y1 = y_start + int(self.scale*self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0))
                y1 = y1 + int(self.scale*self.H)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x2
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale*self.H)
                painter.drawLine(x1, y1, x2, y2)
            elif self.support == 'Column Web':
                x1 = x_start + int(self.scale * self.bf2)
                x2 = x1
                y1 = y_start + int(self.scale * self.tr)
                y2 = y_start + int(self.scale * (self.c - self.gap))
                painter.drawLine(x1, y1, x2, y2)
                x = x2
                y = y2 - self.scale * self.gap
                arc_width = int(self.scale * self.gap*2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 2880, 1440)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                x2 = x1 + int(self.scale * (2 * self.eh + self.spacing * (self.col - 1)))
                y1 = y_start + int(self.scale * self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap))
                x2 = x1 + int(self.scale * (2 * self.eh + self.spacing * (self.col - 1)))
                y1 = y_start + int(self.scale * (self.c + self.H))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x = x_start + int(self.scale * self.bf2)
                y = y1
                arc_width = int(self.scale * self.gap * 2)
                arc_height = arc_width
                painter.drawArc(x, y, arc_width, arc_height, 1440, 1440)
                x1 = x
                x2 = x
                y1 = y1 + int(self.scale*self.gap)
                y2 = y_start + int(self.scale * (self.d - self.tr))
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 + self.gap + 2 * self.eh + self.spacing * (self.col - 1)))
                x2 = x1
                y1 = y_start + int(self.scale * self.c)
                y2 = y_start + int(self.scale * (self.c + self.H))
                painter.drawLine(x1, y1, x2, y2)
            elif self.support == 'Column Flange':
                x1 = x_start + int(self.scale * self.d2)
                x2 = x1 + int(self.scale * (2 * self.eh + self.spacing * (self.col - 1)))
                y1 = y_start + int(self.scale * self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y_start + int(self.scale * (self.c + self.H))
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x2
                y1 = y_start + int(self.scale * self.c)
                y2 = y_start + int(self.scale * (self.c + self.H))
                painter.drawLine(x1, y1, x2, y2)

        elif self.conn_type == 'ShearCope':
            x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0))
            x2 = x1 + int(self.scale * (self.weld_clearance + self.eh*2))
            y1 = y_start + int(self.scale * self.c)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)
            y1 = y1 + int(self.scale * self.H)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)
            x1 = x2
            y1 = y_start + int(self.scale * self.c)
            y2 = y1 + int(self.scale * self.H)
            painter.drawLine(x1, y1, x2, y2)

        elif self.conn_type == 'ShearClip':
            if self.support == 'Beam' or self.support == 'Column Web':
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0))
                x2 = x1 + int(self.scale * 4.0)
                y1 = y_start + int(self.scale * self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.H)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x2
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale * self.H)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.bf2 / 2.0 + self.tw2 / 2.0 + self.ta))
                x2 = x1
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale * self.H)
                painter.drawLine(x1, y1, x2, y2)
            else:
                x1 = x_start + int(self.scale * self.d2)
                x2 = x1 + int(self.scale * 4.0)
                y1 = y_start + int(self.scale * self.c)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                y1 = y1 + int(self.scale * self.H)
                y2 = y1
                painter.drawLine(x1, y1, x2, y2)
                x1 = x2
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale * self.H)
                painter.drawLine(x1, y1, x2, y2)
                x1 = x_start + int(self.scale * (self.d2 + self.ta))
                x2 = x1
                y1 = y_start + int(self.scale * self.c)
                y2 = y1 + int(self.scale * self.H)
                painter.drawLine(x1, y1, x2, y2)

    def drawBolts(self, pen, painter, x_start, y_start):
        pen.setWidth(1)
        pen.setColor(QColor('green'))
        painter.setPen(pen)
        if self.conn_type == 'ShearGusset':
            if self.support == 'Beam' or self.support == 'Column Web':
                if self.col == 1:
                    x1 = x_start + int(self.scale * (self.bf2 + self.gap + self.eh))
                    y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                    x2 = x1
                    y2 = y1 + int(self.scale * (self.spacing * (self.nos - 1) + 1.5 * self.ev))
                    painter.drawLine(x1, y1, x2, y2)
                    for n in range(self.nos):
                        x1 = x_start + int(self.scale * (self.bf2 + self.gap + self.eh/2.0))
                        x2 = x_start + int(self.scale * (self.bf2 + self.gap + 1.5 * self.eh))
                        y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawLine(x1, y1, x2, y2)
                        x = x_start + int(self.scale * (self.bf2 + self.gap + self.eh))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale*self.dia/2.0, self.scale*self.dia/2.0)

                if self.col == 2:
                    x1 = x_start + int(self.scale * (self.bf2 + self.gap + self.eh))
                    x2 = x1
                    y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                    y2 = y1 + int(self.scale * (self.spacing * (self.nos/2 - 1) + 1.5 * self.ev))
                    painter.drawLine(x1, y1, x2, y2)
                    x1 = x_start + int(self.scale * (self.bf2 + self.gap + self.eh)) + int(self.scale * self.spacing)
                    x2 = x1
                    painter.drawLine(x1, y1, x2, y2)
                    col = int(self.nos/2)
                    for n in range(col):
                        x1 = x_start + int(self.scale * (self.bf2 + self.gap + self.eh/2.0))
                        x2 = x_start + int(self.scale * (self.bf2 + self.gap + self.spacing + 1.5 * self.eh))
                        y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawLine(x1, y1, x2, y2)
                        x = x_start + int(self.scale * (self.bf2 + self.gap + self.eh))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale*self.dia/2.0, self.scale*self.dia/2.0)
                        x = x_start + int(self.scale * (self.bf2 + self.gap + self.eh + self.spacing))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

            if self.support == 'Column Flange':
                if self.col == 1:
                    x1 = x_start + int(self.scale * (self.d2 + self.gap + self.eh))
                    y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                    x2 = x1
                    y2 = y1 + int(self.scale * (self.spacing * (self.nos - 1) + 1.5 * self.ev))
                    painter.drawLine(x1, y1, x2, y2)
                    for n in range(self.nos):
                        x1 = x_start + int(self.scale * (self.d2 + self.gap + self.eh / 2.0))
                        x2 = x_start + int(self.scale * (self.d2 + self.gap + 1.5 * self.eh))
                        y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawLine(x1, y1, x2, y2)
                        x = x_start + int(self.scale * (self.d2 + self.gap + self.eh))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

                if self.col == 2:
                    x1 = x_start + int(self.scale * (self.d2 + self.gap + self.eh))
                    x2 = x1
                    y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                    y2 = y1 + int(self.scale * (self.spacing * (self.nos / 2 - 1) + 1.5 * self.ev))
                    painter.drawLine(x1, y1, x2, y2)
                    x1 = x_start + int(self.scale * (self.d2 + self.gap + self.eh)) + int(self.scale * self.spacing)
                    x2 = x1
                    painter.drawLine(x1, y1, x2, y2)
                    col = int(self.nos / 2)
                    for n in range(col):
                        x1 = x_start + int(self.scale * (self.d2 + self.gap + self.eh / 2.0))
                        x2 = x_start + int(self.scale * (self.d2 + self.gap + self.spacing + 1.5 * self.eh))
                        y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawLine(x1, y1, x2, y2)
                        x = x_start + int(self.scale * (self.d2 + self.gap + self.eh))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)
                        x = x_start + int(self.scale * (self.d2 + self.gap + self.eh + self.spacing))
                        y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                        painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

        elif self.conn_type == 'ShearCope':
            x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + self.weld_clearance + self.eh))
            y1 = y_start + int(self.scale * (self.c + self.ev / 4))
            x2 = x1
            y2 = y1 + int(self.scale * (self.spacing * (self.nos - 1) + 1.5 * self.ev))
            painter.drawLine(x1, y1, x2, y2)
            for n in range(self.nos):
                x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + self.weld_clearance + self.eh / 2.0))
                x2 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + self.weld_clearance + 1.5 * self.eh))
                y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                painter.drawLine(x1, y1, x2, y2)
                x = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + self.weld_clearance + self.eh))
                y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

        elif self.conn_type == 'ShearClip':
            if self.support == 'Beam' or self.support == 'Column Web':
                x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + 4.0 - self.eh))
                y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                x2 = x1
                y2 = y1 + int(self.scale * (self.spacing * (self.nos - 1) + 1.5 * self.ev))
                painter.drawLine(x1, y1, x2, y2)
                for n in range(self.nos):
                    x1 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + 4.0 - 1.5 * self.eh))
                    x2 = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + 4.0 - 0.5 * self.eh))
                    y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    painter.drawLine(x1, y1, x2, y2)
                    x = x_start + int(self.scale * (self.bf2/2.0 + self.tw2/2.0 + 4.0 - self.eh))
                    y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

                pen.setWidth(4)
                painter.setPen(pen)
                for n in range(self.nos):
                    x1 = x_start + int(self.scale * (self.bf2 / 2.0 - self.dia))
                    x2 = x_start + int(self.scale * (self.bf2 / 2.0 + 1.5 * self.dia))
                    y1 = y_start + int(self.scale * (self.c + self.spacing * (n + 1)))
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)
            else:
                x1 = x_start + int(self.scale * (self.d2 + 4.0 - self.eh))
                y1 = y_start + int(self.scale * (self.c + self.ev / 4))
                x2 = x1
                y2 = y1 + int(self.scale * (self.spacing * (self.nos - 1) + 1.5 * self.ev))
                painter.drawLine(x1, y1, x2, y2)
                for n in range(self.nos):
                    x1 = x_start + int(self.scale * (self.d2 + 4.0 - 1.5 * self.eh))
                    x2 = x_start + int(self.scale * (self.d2 + 4.0 - 0.5 * self.eh))
                    y1 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    y2 = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    painter.drawLine(x1, y1, x2, y2)
                    x = x_start + int(self.scale * (self.d2 + 4.0 - self.eh))
                    y = y_start + int(self.scale * (self.c + self.ev + self.spacing * n))
                    painter.drawEllipse(QPoint(x, y), self.scale * self.dia / 2.0, self.scale * self.dia / 2.0)

                pen.setWidth(4)
                painter.setPen(pen)
                for n in range(self.nos):
                    x1 = x_start + int(self.scale * (self.d2 - 1.5 * self.dia))
                    x2 = x_start + int(self.scale * (self.d2 + 1.5 * self.dia))
                    y1 = y_start + int(self.scale * (self.c + self.spacing * (n + 1)))
                    y2 = y1
                    painter.drawLine(x1, y1, x2, y2)

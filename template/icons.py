"""Векторные иконки, рисуемые QPainter и окрашиваемые под тему."""

from PyQt6 import QtCore, QtGui

_SCALE = 3


def _icon(size, draw):
    pixmap = QtGui.QPixmap(size * _SCALE, size * _SCALE)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
    painter.scale(_SCALE, _SCALE)
    draw(painter, float(size))
    painter.end()
    pixmap.setDevicePixelRatio(_SCALE)
    return QtGui.QIcon(pixmap)


def _filled(color):
    brush = QtGui.QBrush(color)
    return brush


def gear(color, size=24):
    """Шестерёнка для кнопки настроек."""
    def draw(painter, s):
        center = s / 2
        painter.translate(center, center)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(_filled(color))
        teeth = 8
        body = s * 0.29
        tooth_h = s * 0.17
        tooth_w = s * 0.15
        for index in range(teeth):
            painter.save()
            painter.rotate(index * 360 / teeth)
            painter.drawRoundedRect(
                QtCore.QRectF(-tooth_w / 2, -body - tooth_h,
                              tooth_w, tooth_h + s * 0.05),
                tooth_w * 0.4, tooth_w * 0.4)
            painter.restore()
        painter.drawEllipse(QtCore.QPointF(0, 0), body, body)
        painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawEllipse(QtCore.QPointF(0, 0), s * 0.11, s * 0.11)
    return _icon(size, draw)


def moon(color, size=24):
    """Полумесяц — переход к тёмной теме."""
    def draw(painter, s):
        full = QtGui.QPainterPath()
        full.addEllipse(QtCore.QRectF(s * 0.12, s * 0.12, s * 0.76, s * 0.76))
        cut = QtGui.QPainterPath()
        cut.addEllipse(QtCore.QRectF(s * 0.42, s * 0.02, s * 0.76, s * 0.76))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(_filled(color))
        painter.drawPath(full.subtracted(cut))
    return _icon(size, draw)


def sun(color, size=24):
    """Солнце — переход к светлой теме."""
    def draw(painter, s):
        center = s / 2
        pen = QtGui.QPen(color)
        pen.setWidthF(s * 0.095)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(_filled(color))
        painter.drawEllipse(
            QtCore.QPointF(center, center), s * 0.19, s * 0.19)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        for index in range(8):
            painter.save()
            painter.translate(center, center)
            painter.rotate(index * 45)
            painter.drawLine(QtCore.QPointF(0, -s * 0.30),
                             QtCore.QPointF(0, -s * 0.44))
            painter.restore()
    return _icon(size, draw)


def filter_icon(color, size=24):
    """Воронка для кнопки сортировки."""
    def draw(painter, s):
        path = QtGui.QPainterPath()
        path.moveTo(s * 0.13, s * 0.19)
        path.lineTo(s * 0.87, s * 0.19)
        path.lineTo(s * 0.58, s * 0.50)
        path.lineTo(s * 0.58, s * 0.83)
        path.lineTo(s * 0.42, s * 0.74)
        path.lineTo(s * 0.42, s * 0.50)
        path.closeSubpath()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(_filled(color))
        painter.drawPath(path)
    return _icon(size, draw)


def _tray(painter, s, color):
    pen = QtGui.QPen(color)
    pen.setWidthF(s * 0.085)
    pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
    path = QtGui.QPainterPath()
    path.moveTo(s * 0.20, s * 0.58)
    path.lineTo(s * 0.20, s * 0.83)
    path.lineTo(s * 0.80, s * 0.83)
    path.lineTo(s * 0.80, s * 0.58)
    painter.drawPath(path)


def export_icon(color, size=24):
    """Стрелка из лотка — экспорт."""
    def draw(painter, s):
        _tray(painter, s, color)
        pen = QtGui.QPen(color)
        pen.setWidthF(s * 0.085)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QtCore.QPointF(s * 0.5, s * 0.64),
                         QtCore.QPointF(s * 0.5, s * 0.30))
        head = QtGui.QPainterPath()
        head.moveTo(s * 0.5, s * 0.13)
        head.lineTo(s * 0.33, s * 0.35)
        head.lineTo(s * 0.67, s * 0.35)
        head.closeSubpath()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(_filled(color))
        painter.drawPath(head)
    return _icon(size, draw)


def import_icon(color, size=24):
    """Стрелка в лоток — импорт."""
    def draw(painter, s):
        _tray(painter, s, color)
        pen = QtGui.QPen(color)
        pen.setWidthF(s * 0.085)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QtCore.QPointF(s * 0.5, s * 0.14),
                         QtCore.QPointF(s * 0.5, s * 0.38))
        head = QtGui.QPainterPath()
        head.moveTo(s * 0.5, s * 0.58)
        head.lineTo(s * 0.33, s * 0.36)
        head.lineTo(s * 0.67, s * 0.36)
        head.closeSubpath()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(_filled(color))
        painter.drawPath(head)
    return _icon(size, draw)

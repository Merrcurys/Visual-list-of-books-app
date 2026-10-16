"""Небольшие анимации интерфейса."""

from PyQt6.QtCore import (
    QEasingCurve, QEvent, QObject, QPropertyAnimation, QRect)


class HoverScale(QObject):
    """Плавное увеличение набора виджетов при наведении курсора."""

    def __init__(self, widgets, trigger, grow=8, lift=6, duration=150):
        super().__init__(trigger)
        self.widgets = list(widgets)
        self.base = self.widgets[0].geometry()
        self.grow = grow
        self.lift = lift
        self.anims = {}
        for widget in self.widgets:
            animation = QPropertyAnimation(widget, b"geometry", widget)
            animation.setDuration(duration)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.anims[widget] = animation
        trigger.installEventFilter(self)

    def _target(self):
        base = self.base
        return QRect(
            base.x() - self.grow // 2,
            base.y() - self.lift,
            base.width() + self.grow,
            base.height() + self.grow)

    def _animate(self, rect, raise_widgets):
        if raise_widgets:
            for widget in self.widgets:
                widget.raise_()
        for widget, animation in self.anims.items():
            animation.stop()
            animation.setStartValue(widget.geometry())
            animation.setEndValue(rect)
            animation.start()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            self._animate(self._target(), True)
        elif event.type() == QEvent.Type.Leave:
            self._animate(self.base, False)
        return False

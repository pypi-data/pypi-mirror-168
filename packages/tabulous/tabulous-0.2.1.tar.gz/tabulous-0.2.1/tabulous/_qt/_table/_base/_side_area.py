from __future__ import annotations
from typing import TYPE_CHECKING

from qtpy import QtWidgets as QtW, QtCore
from qtpy.QtCore import Qt

from ..._titlebar import QTitleBar


class QInnerSplitter(QtW.QSplitter):
    """The inner widget for QTableSideArea."""

    def __init__(self, parent: QtW.QWidget = None) -> None:
        super().__init__(Qt.Orientation.Vertical, parent)

    def sizeHint(self):
        h = 0
        w = self.width()
        nwidgets = self.count()
        for i in range(nwidgets):
            child = self.widget(i)
            h += child.minimumHeight()
            w = min(w, child.minimumWidth())
        return QtCore.QSize(w, h)


class QTableSideArea(QtW.QScrollArea):
    """The side scroll area of a table."""

    def __init__(self, parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        widget_inside = QInnerSplitter(self)
        self.setMinimumWidth(180)
        self.setWidget(widget_inside)
        self._widgets: list[QtW.QWidget] = []

    # fmt: off
    if TYPE_CHECKING:
        def widget(self) -> QInnerSplitter: ...
        def parentWidget(self) -> QtW.QSplitter: ...
    # fmt: on

    def addWidget(self, widget: QtW.QWidget, name: str = "") -> None:
        if widget in self._widgets:
            return

        dock = QSplitterDockWidget(widget, name=name)
        splitter = self.widget()
        splitter.addWidget(dock)
        self._widgets.append(widget)
        idx = splitter.count() - 1
        splitter.setCollapsible(idx, False)

        @dock._title_bar.closeSignal.connect
        def _():
            self.removeWidget(widget)

    def removeWidget(self, widget: QtW.QWidget) -> None:
        """Remove gi-en widget from the side area."""
        idx = -1
        for i, wdt in enumerate(self._widgets):
            if wdt is widget:
                # NOTE: To avoid the child of the dock widget get deleted,
                # it must be removed from its parent before the removal of
                # the dock widget.
                dock = wdt.parent()
                wdt.setParent(None)
                dock.setParent(None)
                idx = i
                break
        else:
            raise RuntimeError("Widget not found in the list.")

        del self._widgets[idx]

        if self.widget().count() == 0:
            self.parentWidget().setSizes([1, 0])


class QSplitterDockWidget(QtW.QWidget):
    def __init__(self, widget: QtW.QWidget, name: str = "") -> None:
        super().__init__()
        _layout = QtW.QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)
        title = QTitleBar(title=name, parent=self)
        _layout.addWidget(title)
        _layout.addWidget(widget)
        self.setLayout(_layout)

        self._title_bar = title
        self._widget = widget

    @property
    def close_btn(self):
        return self._title_bar._close_button

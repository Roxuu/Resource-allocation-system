from __future__ import annotations

import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QColor, QPainter, QPolygonF
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPolygonItem,
    QMenu,
)

from core.models.node import MyNode
from core.models.project_model import ProjectModel
from core.models.connection import Connect


class BaseNodeItem:
    def _init_node_base(self, node: MyNode, view: "HierarchyView") -> None:
        self.node = node
        self.view = view

        self.default_brush = QBrush(QColor("white"))
        self.selected_brush = QBrush(QColor("#fff2a8"))

        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self.setToolTip(node.hint)
        self._apply_selection_style()

    def _apply_selection_style(self) -> None:
        if self.isSelected():
            self.setBrush(self.selected_brush)
        else:
            self.setBrush(self.default_brush)

    def _handle_item_change(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            pos = value
            self.node.left = int(pos.x())
            self.node.top = int(pos.y())
            if self.view is not None:
                self.view.refresh_connections()
                self.view.notify_model_changed()

        elif change == QGraphicsItem.ItemSelectedHasChanged:
            self._apply_selection_style()

        return value

    def _open_context_menu(self, screen_pos) -> None:
        if self.view is not None:
            self.view.show_node_context_menu(self.node, screen_pos)

    def _open_edit_dialog(self) -> None:
        if self.view is not None:
            self.view.edit_node(self.node)

    def _handle_left_click(self) -> None:
        if self.view is not None:
            self.view.handle_node_left_click(self.node)


class GoalNodeItem(QGraphicsEllipseItem, BaseNodeItem):
    def __init__(self, node: MyNode, view: "HierarchyView") -> None:
        super().__init__(0, 0, node.width, node.height)
        self._init_node_base(node, view)
        self.setBrush(self.default_brush)
        self.setPen(QPen(Qt.black, 1.5))
        self.setPos(node.left, node.top)

    def itemChange(self, change, value):
        self._handle_item_change(change, value)
        return super().itemChange(change, value)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._handle_left_click()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self._open_edit_dialog()
        event.accept()

    def contextMenuEvent(self, event) -> None:
        self._open_context_menu(event.screenPos())
        event.accept()


class ProjectNodeItem(QGraphicsRectItem, BaseNodeItem):
    def __init__(self, node: MyNode, view: "HierarchyView") -> None:
        super().__init__(0, 0, node.width, node.height)
        self._init_node_base(node, view)
        self.setBrush(self.default_brush)
        self.setPen(QPen(Qt.black, 1.5))
        self.setPos(node.left, node.top)

    def itemChange(self, change, value):
        self._handle_item_change(change, value)
        return super().itemChange(change, value)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._handle_left_click()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self._open_edit_dialog()
        event.accept()

    def contextMenuEvent(self, event) -> None:
        self._open_context_menu(event.screenPos())
        event.accept()


class MainGoalNodeItem(QGraphicsEllipseItem, BaseNodeItem):
    def __init__(self, node: MyNode, view: "HierarchyView") -> None:
        super().__init__(0, 0, node.width, node.height)
        self._init_node_base(node, view)
        self.default_brush = QBrush(QColor("#dff0ff"))
        self.selected_brush = QBrush(QColor("#ffe58f"))
        self.setBrush(self.default_brush)
        self.setPen(QPen(Qt.black, 2))
        self.setPos(node.left, node.top)

    def itemChange(self, change, value):
        self._handle_item_change(change, value)
        return super().itemChange(change, value)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._handle_left_click()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self._open_edit_dialog()
        event.accept()

    def contextMenuEvent(self, event) -> None:
        self._open_context_menu(event.screenPos())
        event.accept()


class ArrowLineItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, color: QColor, src_node: MyNode, dst_node: MyNode, connection: Connect, view: "HierarchyView"):
        super().__init__(x1, y1, x2, y2)
        self.src_node = src_node
        self.dst_node = dst_node
        self.connection = connection
        self.view = view
        self.setPen(QPen(color, 1.5))
        self.setZValue(-10)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self.setToolTip(f"{src_node.hint} -> {dst_node.hint}")

    def mouseDoubleClickEvent(self, event) -> None:
        self.view.edit_connection(self.src_node, self.dst_node, self.connection)
        event.accept()

    def contextMenuEvent(self, event) -> None:
        self.view.show_connection_context_menu(
            self.src_node, self.dst_node, self.connection, event.screenPos()
        )
        event.accept()


class ArrowHeadItem(QGraphicsPolygonItem):
    def __init__(self, polygon: QPolygonF, color: QColor, src_node: MyNode, dst_node: MyNode, connection: Connect, view: "HierarchyView"):
        super().__init__(polygon)
        self.src_node = src_node
        self.dst_node = dst_node
        self.connection = connection
        self.view = view
        self.setBrush(QBrush(color))
        self.setPen(QPen(color, 1.0))
        self.setZValue(-10)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self.setToolTip(f"{src_node.hint} -> {dst_node.hint}")

    def mouseDoubleClickEvent(self, event) -> None:
        self.view.edit_connection(self.src_node, self.dst_node, self.connection)
        event.accept()

    def contextMenuEvent(self, event) -> None:
        self.view.show_connection_context_menu(
            self.src_node, self.dst_node, self.connection, event.screenPos()
        )
        event.accept()


class HierarchyView(QGraphicsView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self._node_items: dict[int, object] = {}
        self._connection_items: list[QGraphicsItem] = []
        self.project: ProjectModel | None = None

        self.on_model_changed = None
        self.on_edit_node = None
        self.on_delete_node = None
        self.on_start_connection = None
        self.on_finish_connection = None
        self.on_edit_connection = None
        self.on_delete_connection = None

    def clear_view(self) -> None:
        self._scene.clear()
        self._node_items.clear()
        self._connection_items.clear()
        self.project = None

    def load_project(self, project: ProjectModel) -> None:
        self.clear_view()
        self.project = project

        for index, node in enumerate(project.nodes):
            item = self._create_node_item(node, index)
            self._scene.addItem(item)
            self._node_items[id(node)] = item

        self.refresh_connections()
        self._scene.setSceneRect(self._scene.itemsBoundingRect().adjusted(-50, -50, 50, 50))
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def refresh_connections(self) -> None:
        for item in self._connection_items:
            self._scene.removeItem(item)
        self._connection_items.clear()

        if self.project is None:
            return

        for src_node in self.project.nodes:
            src_item = self._node_items.get(id(src_node))
            if src_item is None:
                continue

            for con in src_node.connect:
                dst_node = con.node
                if dst_node is None:
                    continue

                dst_item = self._node_items.get(id(dst_node))
                if dst_item is None:
                    continue

                items = self._draw_arrow_connection(src_item, dst_item, src_node, dst_node, con)
                self._connection_items.extend(items)

    def add_node_to_scene(self, node: MyNode) -> None:
        if self.project is None:
            return

        index = self.project.nodes.index(node)
        item = self._create_node_item(node, index)
        self._scene.addItem(item)
        self._node_items[id(node)] = item
        self.refresh_connections()
        self._scene.setSceneRect(self._scene.itemsBoundingRect().adjusted(-50, -50, 50, 50))

    def rebuild_scene(self) -> None:
        if self.project is not None:
            self.load_project(self.project)

    def notify_model_changed(self) -> None:
        if callable(self.on_model_changed):
            self.on_model_changed()

    def edit_node(self, node: MyNode) -> None:
        if callable(self.on_edit_node):
            self.on_edit_node(node)

    def delete_node(self, node: MyNode) -> None:
        if callable(self.on_delete_node):
            self.on_delete_node(node)

    def edit_connection(self, src_node: MyNode, dst_node: MyNode, connection: Connect) -> None:
        if callable(self.on_edit_connection):
            self.on_edit_connection(src_node, dst_node, connection)

    def delete_connection(self, src_node: MyNode, dst_node: MyNode, connection: Connect) -> None:
        if callable(self.on_delete_connection):
            self.on_delete_connection(src_node, dst_node, connection)

    def handle_node_left_click(self, node: MyNode) -> None:
        if callable(self.on_finish_connection):
            self.on_finish_connection(node)

    def show_node_context_menu(self, node: MyNode, screen_pos) -> None:
        menu = QMenu(self)

        start_connection_action = menu.addAction("Почати зв’язок")
        edit_action = menu.addAction("Редагувати вузол")
        delete_action = menu.addAction("Видалити вузол")

        action = menu.exec(screen_pos)

        if action == start_connection_action:
            if callable(self.on_start_connection):
                self.on_start_connection(node)
        elif action == edit_action:
            self.edit_node(node)
        elif action == delete_action:
            self.delete_node(node)

    def show_connection_context_menu(self, src_node: MyNode, dst_node: MyNode, connection: Connect, screen_pos) -> None:
        menu = QMenu(self)

        edit_action = menu.addAction("Редагувати зв’язок")
        delete_action = menu.addAction("Видалити зв’язок")

        action = menu.exec(screen_pos)

        if action == edit_action:
            self.edit_connection(src_node, dst_node, connection)
        elif action == delete_action:
            self.delete_connection(src_node, dst_node, connection)

    def _create_node_item(self, node: MyNode, index: int):
        if index == 0:
            return MainGoalNodeItem(node, self)
        if node.project:
            return ProjectNodeItem(node, self)
        return GoalNodeItem(node, self)

    def _draw_arrow_connection(
        self,
        src_item,
        dst_item,
        src_node: MyNode,
        dst_node: MyNode,
        connection: Connect
    ) -> list[QGraphicsItem]:
        color = QColor("black") if connection.positive else QColor("red")

        src_center = self._item_center(src_item)
        dst_center = self._item_center(dst_item)

        start_point = self._intersection_with_item_border(src_item, dst_center)
        end_point = self._intersection_with_item_border(dst_item, src_center)

        line = ArrowLineItem(
            start_point.x(), start_point.y(),
            end_point.x(), end_point.y(),
            color,
            src_node,
            dst_node,
            connection,
            self
        )
        self._scene.addItem(line)

        arrow_head = self._create_arrow_head(start_point, end_point, color, src_node, dst_node, connection)
        self._scene.addItem(arrow_head)

        return [line, arrow_head]

    def _create_arrow_head(
        self,
        start: QPointF,
        end: QPointF,
        color: QColor,
        src_node: MyNode,
        dst_node: MyNode,
        connection: Connect
    ) -> QGraphicsPolygonItem:
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 8.0

        p1 = end
        p2 = QPointF(
            end.x() - arrow_size * math.cos(angle - math.pi / 6),
            end.y() - arrow_size * math.sin(angle - math.pi / 6),
        )
        p3 = QPointF(
            end.x() - arrow_size * math.cos(angle + math.pi / 6),
            end.y() - arrow_size * math.sin(angle + math.pi / 6),
        )

        polygon = QPolygonF([p1, p2, p3])
        return ArrowHeadItem(polygon, color, src_node, dst_node, connection, self)

    def _item_center(self, item) -> QPointF:
        rect = item.rect()
        pos = item.pos()
        return QPointF(
            pos.x() + rect.width() / 2,
            pos.y() + rect.height() / 2,
        )

    def _intersection_with_item_border(self, item, external_point: QPointF) -> QPointF:
        rect = item.rect()
        center = self._item_center(item)

        dx = external_point.x() - center.x()
        dy = external_point.y() - center.y()

        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            return center

        if isinstance(item, (GoalNodeItem, MainGoalNodeItem)):
            rx = rect.width() / 2
            ry = rect.height() / 2

            angle = math.atan2(dy, dx)
            return QPointF(
                center.x() + rx * math.cos(angle),
                center.y() + ry * math.sin(angle),
            )

        if isinstance(item, ProjectNodeItem):
            half_w = rect.width() / 2
            half_h = rect.height() / 2

            scale_x = abs(dx) / half_w if half_w > 0 else float("inf")
            scale_y = abs(dy) / half_h if half_h > 0 else float("inf")
            scale = max(scale_x, scale_y)

            return QPointF(
                center.x() + dx / scale,
                center.y() + dy / scale,
            )

        return center

    def wheelEvent(self, event) -> None:
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)

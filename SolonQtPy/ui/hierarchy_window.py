from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QMessageBox

from core.models.node import MyNode
from core.models.project_model import ProjectModel
from core.models.connection import Connect
from ui.hierarchy_view import HierarchyView
from ui.node_dialog import NodeDialog
from ui.connection_dialog import ConnectionDialog


class HierarchyWindow(QMainWindow):
    def __init__(self, project: ProjectModel, file_path: str | None = None, parent=None) -> None:
        super().__init__(parent)

        self.project = project
        self.file_path = file_path
        self.is_modified = False
        self.connection_source_node: MyNode | None = None

        self.hierarchy_view = HierarchyView(self)
        self.hierarchy_view.on_model_changed = self.on_model_changed
        self.hierarchy_view.on_edit_node = self.edit_node
        self.hierarchy_view.on_delete_node = self.delete_node
        self.hierarchy_view.on_start_connection = self.start_connection
        self.hierarchy_view.on_finish_connection = self.finish_connection
        self.hierarchy_view.on_edit_connection = self.edit_connection
        self.hierarchy_view.on_delete_connection = self.delete_connection

        self.setCentralWidget(self.hierarchy_view)

        self.resize(1200, 800)
        self._refresh_view()
        self._update_title()
        self.statusBar().showMessage("Готово")

    def _refresh_view(self) -> None:
        self.hierarchy_view.load_project(self.project)

    def _update_title(self) -> None:
        title = "Граф проблеми"
        if self.file_path:
            title += f" - {self.file_path}"
        if self.is_modified:
            title += " *"
        self.setWindowTitle(title)

    def on_model_changed(self) -> None:
        self.is_modified = True
        self._update_title()

    def mark_saved(self, file_path: str | None = None) -> None:
        if file_path is not None:
            self.file_path = file_path
        self.is_modified = False
        self._update_title()

    def add_node(self, hint: str = "Нова ціль") -> None:
        offset = len(self.project.nodes) * 30
        node = self.project.create_node(
            hint=hint,
            left=120 + offset,
            top=120 + offset,
            width=24,
            height=24,
            project=False,
        )
        self.project.rebuild_sub_goal_lists()
        self.hierarchy_view.add_node_to_scene(node)
        self.is_modified = True
        self._update_title()

    def edit_node(self, node: MyNode) -> None:
        dialog = NodeDialog(node, self)
        if dialog.exec():
            dialog.apply_changes()
            self.project.rebuild_sub_goal_lists()
            self.hierarchy_view.rebuild_scene()
            self.is_modified = True
            self._update_title()

    def delete_node(self, node: MyNode) -> None:
        reply = QMessageBox.question(
            self,
            "Видалення вузла",
            f"Видалити вузол '{node.hint}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.No:
            return

        if self.connection_source_node is node:
            self.connection_source_node = None

        self.project.remove_node(node)
        self.hierarchy_view.rebuild_scene()
        self.is_modified = True
        self._update_title()

    def start_connection(self, node: MyNode) -> None:
        self.connection_source_node = node
        self.statusBar().showMessage(
            f"Почато створення зв’язку з '{node.hint}'. Клікніть по цільовому вузлу."
        )

    def finish_connection(self, target_node: MyNode) -> None:
        if self.connection_source_node is None:
            return

        source_node = self.connection_source_node

        if source_node is target_node:
            self.statusBar().showMessage("Не можна створити зв’язок вузла із самим собою.", 4000)
            self.connection_source_node = None
            return

        if source_node.connect.index_of(target_node) != -1:
            self.statusBar().showMessage("Такий зв’язок уже існує.", 4000)
            self.connection_source_node = None
            return

        source_node.connect.add(target_node)
        self.project.rebuild_sub_goal_lists()
        self.hierarchy_view.refresh_connections()

        self.is_modified = True
        self._update_title()

        self.statusBar().showMessage(
            f"Створено зв’язок: '{source_node.hint}' -> '{target_node.hint}'",
            4000
        )

        self.connection_source_node = None

    def edit_connection(self, src_node: MyNode, dst_node: MyNode, connection: Connect) -> None:
        dialog = ConnectionDialog(connection, self)
        if dialog.exec():
            dialog.apply_changes()
            self.hierarchy_view.refresh_connections()
            self.is_modified = True
            self._update_title()
            self.statusBar().showMessage(
                f"Зв’язок '{src_node.hint}' -> '{dst_node.hint}' змінено.",
                4000
            )

    def delete_connection(self, src_node: MyNode, dst_node: MyNode, connection: Connect) -> None:
        reply = QMessageBox.question(
            self,
            "Видалення зв’язку",
            f"Видалити зв’язок '{src_node.hint}' -> '{dst_node.hint}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.No:
            return

        src_node.connect.remove(dst_node)
        self.project.rebuild_sub_goal_lists()
        self.hierarchy_view.refresh_connections()
        self.is_modified = True
        self._update_title()
        self.statusBar().showMessage(
            f"Зв’язок '{src_node.hint}' -> '{dst_node.hint}' видалено.",
            4000
        )

    def closeEvent(self, event) -> None:
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Незбережені зміни",
                "У цьому вікні є незбережені зміни. Закрити без збереження?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
        event.accept()

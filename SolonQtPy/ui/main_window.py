from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QToolBar,
    QInputDialog,
)

from core.models.project_model import ProjectModel
from core.services.project_io import load_project, save_project
from ui.hierarchy_window import HierarchyWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.child_windows: list[HierarchyWindow] = []

        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle('СИСТЕМА ПІДТРИМКИ ПРИЙНЯТТЯ РІШЕНЬ " С о л о н - 3 "')
        self.resize(900, 500)

        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self.statusBar()

    def _build_actions(self) -> None:
        self.action_file_new = QAction("Нова", self)
        self.action_file_open = QAction("Відкрити...", self)
        self.action_file_save = QAction("Зберегти", self)
        self.action_file_save_as = QAction("Зберегти як...", self)
        self.action_file_print = QAction("Друк", self)
        self.action_file_print_setup = QAction("Установки принтера...", self)
        self.action_file_close = QAction("Закрити активне вікно", self)
        self.action_file_exit = QAction("Вихід", self)

        self.action_add_node = QAction("Додати вузол", self)

        self.action_search_goal = QAction("Вибір цілі зі списку", self)
        self.action_search_project = QAction("Вибір проекту зі списку", self)
        self.action_search_not_opening_node = QAction("Список не розкритих вершин", self)
        self.action_search_not_determin_chkv_node = QAction(
            "Список вершин, для яких не розраховані ЧКВ", self
        )

        self.action_non_group_estimate = QAction("Безпосередня оцінка", self)
        self.action_group_estimate = QAction("Запуск сервера для групової оцінки", self)

        self.action_valuation_project = QAction("Ефективність проектів", self)
        self.action_potential_valuation_project = QAction("Потенційна ефективність проектів", self)
        self.action_valuation_goal = QAction("Ефективність цілей", self)
        self.action_valuation_project_regard_fulfilment = QAction(
            "Урахування ступеня виконання", self
        )
        self.action_reach_degree_instead_effect = QAction(
            "Не ефективність а ступінь досягнення", self
        )

        self.action_help_contents = QAction("Зміст", self)
        self.action_help_search = QAction("Пошук допомоги по...", self)
        self.action_help_how_to_use = QAction("Як використовувати допомогу", self)
        self.action_help_about = QAction("Про...", self)

        self.action_search_not_opening_node.setVisible(False)
        self.action_search_not_determin_chkv_node.setVisible(False)

        self._connect_actions()

    def _build_menus(self) -> None:
        menubar = self.menuBar()

        self.menu_file = menubar.addMenu("Проблема")
        self.menu_file.addAction(self.action_file_new)
        self.menu_file.addAction(self.action_file_open)
        self.menu_file.addAction(self.action_file_save)
        self.menu_file.addAction(self.action_file_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_print)
        self.menu_file.addAction(self.action_file_print_setup)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_close)
        self.menu_file.addAction(self.action_file_exit)

        self.menu_edit = menubar.addMenu("Редагування")
        self.menu_edit.addAction(self.action_add_node)

        self.menu_search = menubar.addMenu("Вибір")
        self.menu_search.addAction(self.action_search_goal)
        self.menu_search.addAction(self.action_search_project)
        self.menu_search.addSeparator()
        self.menu_search.addAction(self.action_search_not_opening_node)
        self.menu_search.addAction(self.action_search_not_determin_chkv_node)

        self.menu_ratio = menubar.addMenu("Коефіцієнти впливу")
        self.menu_ratio.addAction(self.action_non_group_estimate)
        self.menu_ratio.addAction(self.action_group_estimate)

        self.menu_valuation = menubar.addMenu("Розрахувати")
        self.menu_valuation.addAction(self.action_valuation_project)
        self.menu_valuation.addAction(self.action_potential_valuation_project)
        self.menu_valuation.addAction(self.action_valuation_goal)
        self.menu_valuation.addAction(self.action_valuation_project_regard_fulfilment)
        self.menu_valuation.addAction(self.action_reach_degree_instead_effect)

        self.menu_help = menubar.addMenu("?")
        self.menu_help.addAction(self.action_help_contents)
        self.menu_help.addAction(self.action_help_search)
        self.menu_help.addAction(self.action_help_how_to_use)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_help_about)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Основна панель", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self.action_file_new)
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        toolbar.addAction(self.action_add_node)
        toolbar.addSeparator()
        toolbar.addAction(self.action_help_about)

    def _connect_actions(self) -> None:
        self.action_file_new.triggered.connect(self.on_file_new)
        self.action_file_open.triggered.connect(self.on_file_open)
        self.action_file_save.triggered.connect(self.on_file_save)
        self.action_file_save_as.triggered.connect(self.on_file_save_as)
        self.action_file_print.triggered.connect(self.on_file_print)
        self.action_file_print_setup.triggered.connect(self.on_file_print_setup)
        self.action_file_close.triggered.connect(self.on_file_close)
        self.action_file_exit.triggered.connect(self.on_file_exit)

        self.action_add_node.triggered.connect(self.on_add_node)

        self.action_search_goal.triggered.connect(self.on_search_goal)
        self.action_search_project.triggered.connect(self.on_search_project)
        self.action_search_not_opening_node.triggered.connect(self.on_search_not_opening_node)
        self.action_search_not_determin_chkv_node.triggered.connect(self.on_search_not_determin_chkv_node)

        self.action_non_group_estimate.triggered.connect(self.on_non_group_estimate)
        self.action_group_estimate.triggered.connect(self.on_group_estimate)

        self.action_valuation_project.triggered.connect(self.on_valuation_project)
        self.action_potential_valuation_project.triggered.connect(self.on_potential_valuation_project)
        self.action_valuation_goal.triggered.connect(self.on_valuation_goal)
        self.action_valuation_project_regard_fulfilment.triggered.connect(
            self.on_valuation_project_regard_fulfilment
        )
        self.action_reach_degree_instead_effect.triggered.connect(
            self.on_reach_degree_instead_effect
        )

        self.action_help_contents.triggered.connect(self.on_help_contents)
        self.action_help_search.triggered.connect(self.on_help_search)
        self.action_help_how_to_use.triggered.connect(self.on_help_how_to_use)
        self.action_help_about.triggered.connect(self.on_help_about)

    def _show_info(self, title: str, text: str) -> None:
        QMessageBox.information(self, title, text)

    def _show_warning(self, title: str, text: str) -> None:
        QMessageBox.warning(self, title, text)

    def _show_error(self, title: str, text: str) -> None:
        QMessageBox.critical(self, title, text)

    def _not_implemented(self, action_name: str) -> None:
        self._show_info("Поки не реалізовано", f"Дія '{action_name}' поки не реалізована.")

    def _get_active_hierarchy_window(self) -> HierarchyWindow | None:
        active_window = self.activeWindow()
        if isinstance(active_window, HierarchyWindow):
            return active_window

        for window in self.child_windows:
            if window.isActiveWindow():
                return window

        if len(self.child_windows) == 1:
            return self.child_windows[0]

        return None

    def _register_child_window(self, window: HierarchyWindow) -> None:
        self.child_windows.append(window)
        window.destroyed.connect(lambda: self._cleanup_closed_windows())

    def _cleanup_closed_windows(self) -> None:
        self.child_windows = [w for w in self.child_windows if w is not None and not w.isHidden()]

    def on_file_new(self) -> None:
        project = ProjectModel.create_demo()
        window = HierarchyWindow(project=project, file_path=None)
        self._register_child_window(window)
        window.show()

    def on_file_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Виберіть файл що містить проблему",
            "",
            "JSON files (*.json);;Усі файли (*.*)"
        )

        if not file_path:
            return

        try:
            project = load_project(file_path)
            window = HierarchyWindow(project=project, file_path=file_path)
            window.mark_saved(file_path)
            self._register_child_window(window)
            window.show()
        except Exception as e:
            self._show_error("Помилка відкриття", str(e))

    def on_file_save(self) -> None:
        window = self._get_active_hierarchy_window()
        if window is None:
            self._show_warning("Збереження", "Немає активного вікна графа.")
            return

        if not window.file_path:
            self.on_file_save_as()
            return

        try:
            save_project(window.file_path, window.project)
            window.mark_saved(window.file_path)
            self.statusBar().showMessage("Проєкт збережено", 3000)
        except Exception as e:
            self._show_error("Помилка збереження", str(e))

    def on_file_save_as(self) -> None:
        window = self._get_active_hierarchy_window()
        if window is None:
            self._show_warning("Збереження", "Немає активного вікна графа.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Виберіть файл для збереження проблеми",
            "",
            "JSON files (*.json);;Усі файли (*.*)"
        )

        if not file_path:
            return

        try:
            save_project(file_path, window.project)
            window.mark_saved(file_path)
            self.statusBar().showMessage("Проєкт збережено", 3000)
        except Exception as e:
            self._show_error("Помилка збереження", str(e))

    def on_file_print(self) -> None:
        self._not_implemented("Друк")

    def on_file_print_setup(self) -> None:
        self._not_implemented("Установки принтера")

    def on_file_close(self) -> None:
        window = self._get_active_hierarchy_window()
        if window is None:
            self._show_warning("Закриття", "Немає активного вікна графа.")
            return
        window.close()

    def on_file_exit(self) -> None:
        self.close()

    def on_add_node(self) -> None:
        window = self._get_active_hierarchy_window()
        if window is None:
            self._show_warning("Додавання вузла", "Немає активного вікна графа.")
            return

        text, ok = QInputDialog.getText(self, "Додати вузол", "Назва вузла:")
        if not ok:
            return

        hint = text.strip() or "Нова ціль"
        window.add_node(hint)

    def on_search_goal(self) -> None:
        self._not_implemented("Вибір цілі зі списку")

    def on_search_project(self) -> None:
        self._not_implemented("Вибір проекту зі списку")

    def on_search_not_opening_node(self) -> None:
        self._not_implemented("Список не розкритих вершин")

    def on_search_not_determin_chkv_node(self) -> None:
        self._not_implemented("Список вершин, для яких не розраховані ЧКВ")

    def on_non_group_estimate(self) -> None:
        self._not_implemented("Безпосередня оцінка")

    def on_group_estimate(self) -> None:
        self._not_implemented("Запуск сервера для групової оцінки")

    def on_valuation_project(self) -> None:
        self._not_implemented("Ефективність проектів")

    def on_potential_valuation_project(self) -> None:
        self._not_implemented("Потенційна ефективність проектів")

    def on_valuation_goal(self) -> None:
        self._not_implemented("Ефективність цілей")

    def on_valuation_project_regard_fulfilment(self) -> None:
        self._not_implemented("Урахування ступеня виконання")

    def on_reach_degree_instead_effect(self) -> None:
        self._not_implemented("Не ефективність а ступінь досягнення")

    def on_help_contents(self) -> None:
        self._not_implemented("Зміст")

    def on_help_search(self) -> None:
        self._not_implemented("Пошук допомоги")

    def on_help_how_to_use(self) -> None:
        self._not_implemented("Як використовувати допомогу")

    def on_help_about(self) -> None:
        QMessageBox.about(
            self,
            "Про програму",
            'СИСТЕМА ПІДТРИМКИ ПРИЙНЯТТЯ РІШЕНЬ "Солон-3"\nPython / Qt порт'
        )

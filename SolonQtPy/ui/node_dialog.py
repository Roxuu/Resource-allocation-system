from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

from core.models.node import MyNode


class NodeDialog(QDialog):
    def __init__(self, node: MyNode, parent=None) -> None:
        super().__init__(parent)
        self.node = node

        self.setWindowTitle("Властивості вузла")
        self.resize(350, 220)

        self.edit_hint = QLineEdit(self.node.hint)

        self.check_project = QCheckBox("Це проект")
        self.check_project.setChecked(self.node.project)

        self.spin_threshold = QSpinBox()
        self.spin_threshold.setRange(0, 100)
        self.spin_threshold.setValue(self.node.threshold)

        self.spin_fulfilment = QSpinBox()
        self.spin_fulfilment.setRange(0, 100)
        self.spin_fulfilment.setValue(self.node.fulfilment)

        self.spin_width = QSpinBox()
        self.spin_width.setRange(8, 300)
        self.spin_width.setValue(self.node.width)

        self.spin_height = QSpinBox()
        self.spin_height.setRange(8, 300)
        self.spin_height.setValue(self.node.height)

        form = QFormLayout()
        form.addRow("Назва:", self.edit_hint)
        form.addRow("", self.check_project)
        form.addRow("Поріг:", self.spin_threshold)
        form.addRow("Виконання %:", self.spin_fulfilment)
        form.addRow("Ширина:", self.spin_width)
        form.addRow("Висота:", self.spin_height)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def apply_changes(self) -> None:
        self.node.hint = self.edit_hint.text().strip() or "Без назви"
        self.node.project = self.check_project.isChecked()
        self.node.threshold = self.spin_threshold.value()
        self.node.fulfilment = self.spin_fulfilment.value()
        self.node.width = self.spin_width.value()
        self.node.height = self.spin_height.value()

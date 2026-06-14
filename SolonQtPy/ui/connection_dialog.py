from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
)

from core.models.connection import Connect


class ConnectionDialog(QDialog):
    def __init__(self, connection: Connect, parent=None) -> None:
        super().__init__(parent)
        self.connection = connection

        self.setWindowTitle("Властивості зв’язку")
        self.resize(320, 220)

        self.check_positive = QCheckBox("Позитивний зв’язок")
        self.check_positive.setChecked(self.connection.positive)

        self.spin_value_delay = QSpinBox()
        self.spin_value_delay.setRange(0, 1000000)
        self.spin_value_delay.setValue(int(self.connection.value_delay))

        self.spin_effect_out = QDoubleSpinBox()
        self.spin_effect_out.setRange(-1000000.0, 1000000.0)
        self.spin_effect_out.setDecimals(4)
        self.spin_effect_out.setValue(float(self.connection.effect_out))

        self.spin_direct_chkv = QDoubleSpinBox()
        self.spin_direct_chkv.setRange(-1000000.0, 1000000.0)
        self.spin_direct_chkv.setDecimals(4)
        self.spin_direct_chkv.setValue(float(self.connection.direct_chkv))

        form = QFormLayout()
        form.addRow("", self.check_positive)
        form.addRow("Затримка:", self.spin_value_delay)
        form.addRow("Effect Out:", self.spin_effect_out)
        form.addRow("Direct ChKV:", self.spin_direct_chkv)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def apply_changes(self) -> None:
        self.connection.positive = self.check_positive.isChecked()
        self.connection.value_delay = self.spin_value_delay.value()
        self.connection.effect_out = self.spin_effect_out.value()
        self.connection.direct_chkv = self.spin_direct_chkv.value()

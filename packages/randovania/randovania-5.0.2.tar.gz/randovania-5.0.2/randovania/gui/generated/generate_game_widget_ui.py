# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generate_game_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.preset_tree_widget import *  # type: ignore

class Ui_GenerateGameWidget(object):
    def setupUi(self, GenerateGameWidget):
        if not GenerateGameWidget.objectName():
            GenerateGameWidget.setObjectName(u"GenerateGameWidget")
        GenerateGameWidget.resize(409, 312)
        self.create_layout = QGridLayout(GenerateGameWidget)
        self.create_layout.setSpacing(6)
        self.create_layout.setContentsMargins(11, 11, 11, 11)
        self.create_layout.setObjectName(u"create_layout")
        self.create_layout.setContentsMargins(4, 4, 4, 0)
        self.create_preset_tree = PresetTreeWidget(GenerateGameWidget)
        __qtreewidgetitem = QTreeWidgetItem(self.create_preset_tree)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.create_preset_tree)
        self.create_preset_tree.setObjectName(u"create_preset_tree")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_preset_tree.sizePolicy().hasHeightForWidth())
        self.create_preset_tree.setSizePolicy(sizePolicy)
        self.create_preset_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.create_preset_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.create_preset_tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.create_preset_tree.setAlternatingRowColors(False)
        self.create_preset_tree.setRootIsDecorated(False)

        self.create_layout.addWidget(self.create_preset_tree, 2, 0, 1, 2)

        self.create_generate_race_button = QPushButton(GenerateGameWidget)
        self.create_generate_race_button.setObjectName(u"create_generate_race_button")

        self.create_layout.addWidget(self.create_generate_race_button, 4, 2, 1, 1)

        self.num_players_spin_box = QSpinBox(GenerateGameWidget)
        self.num_players_spin_box.setObjectName(u"num_players_spin_box")
        self.num_players_spin_box.setCursor(QCursor(Qt.ArrowCursor))
        self.num_players_spin_box.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.num_players_spin_box.setMinimum(1)

        self.create_layout.addWidget(self.num_players_spin_box, 4, 3, 1, 1)

        self.create_scroll_area = QScrollArea(GenerateGameWidget)
        self.create_scroll_area.setObjectName(u"create_scroll_area")
        self.create_scroll_area.setWidgetResizable(True)
        self.create_scroll_area_contents = QWidget()
        self.create_scroll_area_contents.setObjectName(u"create_scroll_area_contents")
        self.create_scroll_area_contents.setGeometry(QRect(0, 0, 196, 281))
        self.create_scroll_area_layout = QVBoxLayout(self.create_scroll_area_contents)
        self.create_scroll_area_layout.setSpacing(6)
        self.create_scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.create_scroll_area_layout.setObjectName(u"create_scroll_area_layout")
        self.create_scroll_area_layout.setContentsMargins(4, 4, 4, 4)
        self.create_preset_description = QLabel(self.create_scroll_area_contents)
        self.create_preset_description.setObjectName(u"create_preset_description")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.create_preset_description.sizePolicy().hasHeightForWidth())
        self.create_preset_description.setSizePolicy(sizePolicy1)
        self.create_preset_description.setMinimumSize(QSize(0, 40))
        self.create_preset_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.create_preset_description.setWordWrap(True)

        self.create_scroll_area_layout.addWidget(self.create_preset_description)

        self.create_scroll_area.setWidget(self.create_scroll_area_contents)

        self.create_layout.addWidget(self.create_scroll_area, 2, 2, 1, 2)

        self.create_generate_no_retry_button = QPushButton(GenerateGameWidget)
        self.create_generate_no_retry_button.setObjectName(u"create_generate_no_retry_button")

        self.create_layout.addWidget(self.create_generate_no_retry_button, 4, 0, 1, 1)

        self.create_generate_button = QPushButton(GenerateGameWidget)
        self.create_generate_button.setObjectName(u"create_generate_button")

        self.create_layout.addWidget(self.create_generate_button, 4, 1, 1, 1)


        self.retranslateUi(GenerateGameWidget)

        QMetaObject.connectSlotsByName(GenerateGameWidget)
    # setupUi

    def retranslateUi(self, GenerateGameWidget):
        ___qtreewidgetitem = self.create_preset_tree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GenerateGameWidget", u"Presets (Right click for actions)", None));

        __sortingEnabled = self.create_preset_tree.isSortingEnabled()
        self.create_preset_tree.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.create_preset_tree.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("GenerateGameWidget", u"Metroid Prime", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("GenerateGameWidget", u"Default Preset", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("GenerateGameWidget", u"Your Custom Preset", None));
        ___qtreewidgetitem4 = self.create_preset_tree.topLevelItem(1)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("GenerateGameWidget", u"Metroid Prime 2", None));
        self.create_preset_tree.setSortingEnabled(__sortingEnabled)

        self.create_generate_race_button.setText(QCoreApplication.translate("GenerateGameWidget", u"Generate for Race", None))
        self.num_players_spin_box.setSuffix(QCoreApplication.translate("GenerateGameWidget", u" players", None))
        self.create_preset_description.setText(QCoreApplication.translate("GenerateGameWidget", u"<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None))
        self.create_generate_no_retry_button.setText(QCoreApplication.translate("GenerateGameWidget", u"Generate without retry", None))
        self.create_generate_button.setText(QCoreApplication.translate("GenerateGameWidget", u"Generate", None))
        pass
    # retranslateUi


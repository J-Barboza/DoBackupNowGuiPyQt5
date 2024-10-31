import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QCheckBox, QLabel, QLineEdit, QMessageBox, QButtonGroup, QRadioButton
from backup import start_backup, load_last_backup, save_last_backup
from config import load_config, save_config

CONFIG_FILE = "config.json"
LAST_BACKUP_FILE = "last_backup.json"

class BackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.backup_groups = []
        self.current_group_index = None
        self.backup_info = load_last_backup(LAST_BACKUP_FILE)
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('Backup Application')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.group_label = QLabel('Backup Groups:')
        layout.addWidget(self.group_label)

        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        self.group_list.itemSelectionChanged.connect(self.on_group_select)

        self.add_group_button = QPushButton('Add Group')
        self.add_group_button.clicked.connect(self.add_group)
        layout.addWidget(self.add_group_button)

        self.remove_group_button = QPushButton('Remove Group')
        self.remove_group_button.clicked.connect(self.remove_group)
        layout.addWidget(self.remove_group_button)

        self.group_name_label = QLabel('Group Name:')
        layout.addWidget(self.group_name_label)
        self.group_name_entry = QLineEdit()
        layout.addWidget(self.group_name_entry)

        self.active_checkbutton = QCheckBox('Active')
        self.active_checkbutton.stateChanged.connect(self.update_group_status)
        layout.addWidget(self.active_checkbutton)

        self.source_label = QLabel('Source Directories:')
        layout.addWidget(self.source_label)

        self.source_list = QListWidget()
        layout.addWidget(self.source_list)

        self.add_source_button = QPushButton('Add Source')
        self.add_source_button.clicked.connect(self.add_source)
        layout.addWidget(self.add_source_button)

        self.remove_source_button = QPushButton('Remove Selected')
        self.remove_source_button.clicked.connect(self.remove_selected_sources)
        layout.addWidget(self.remove_source_button)

        self.dest_label = QLabel('Backup Destination:')
        layout.addWidget(self.dest_label)
        self.dest_edit = QLineEdit()
        layout.addWidget(self.dest_edit)

        self.browse_dest_button = QPushButton('Browse')
        self.browse_dest_button.clicked.connect(self.browse_destination)
        layout.addWidget(self.browse_dest_button)

        self.backup_type_var = QButtonGroup(self)

        self.full_backup_radio = QRadioButton("Full Backup")
        layout.addWidget(self.full_backup_radio)
        self.backup_type_var.addButton(self.full_backup_radio)
        
        self.incremental_backup_radio = QRadioButton("Incremental Backup")
        layout.addWidget(self.incremental_backup_radio)
        self.backup_type_var.addButton(self.incremental_backup_radio)

        self.full_backup_radio.toggled.connect(self.update_group_status)
        self.incremental_backup_radio.toggled.connect(self.update_group_status)

        # self.incremental_checkbutton = QCheckBox('Incremental Backup')
        # layout.addWidget(self.incremental_checkbutton)

        self.backup_button = QPushButton('Start Backup')
        self.backup_button.clicked.connect(self.start_backup)
        layout.addWidget(self.backup_button)

        self.setLayout(layout)

    def add_group(self):
        group_name = self.group_name_entry.text()
        if not group_name:
            QMessageBox.warning(self, 'Erro', 'Please enter a name for the group.')
            return
        group = {
            'name': group_name,
            'source_directories': [],
            'backup_destination': '',
            'incremental': self.incremental_checkbutton.isChecked(),
            'active': self.active_checkbutton.isChecked()
        }
        self.backup_groups.append(group)
        self.group_list.addItem(group_name)
        self.group_name_entry.clear()
        self.save_settings()

    def update_group_status(self):
        if self.current_group_index is not None:
            group = self.backup_groups[self.current_group_index]
            group["active"] = self.active_checkbutton.isChecked()
            group["name"] = self.group_name_entry.text()

            if self.full_backup_radio.isChecked():
                group["incremental"] = False
            elif self.incremental_backup_radio.isChecked():
                group["incremental"] = True

            self.save_settings()
            print(f"Group '{group['name']}' status updated to {'active' if group['active'] else 'inactive'}.")

    def remove_group(self):
        selected_items = self.group_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            index = self.group_list.row(item)
            self.group_list.takeItem(index)
            del self.backup_groups[index]
        self.save_settings()

    def on_group_select(self):
        selected_items = self.group_list.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        index = self.group_list.row(selected_item)
        group = self.backup_groups[index]

        self.group_name_entry.setText(group['name'])
        self.active_checkbutton.setChecked(group['active'])
        self.source_list.clear()
        self.source_list.addItems(group['source_directories'])
        self.dest_edit.setText(group['backup_destination'])

        if group.get("incremental", False):
            self.incremental_backup_radio.setChecked(True)
        else:
            self.full_backup_radio.setChecked(True)

        self.current_group_index = index

    def add_source(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.source_list.addItem(directory)
            if self.current_group_index is not None:
                self.backup_groups[self.current_group_index]['source_directories'].append(directory)
                self.save_settings()

    def remove_selected_sources(self):
        selected_items = self.source_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            index = self.source_list.row(item)
            self.source_list.takeItem(index)
            if self.current_group_index is not None:
                del self.backup_groups[self.current_group_index]['source_directories'][index]
        self.save_settings()

    def browse_destination(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.dest_edit.setText(directory)
            if self.current_group_index is not None:
                self.backup_groups[self.current_group_index]['backup_destination'] = directory
                self.save_settings()
    
    def start_backup(self):
        backups_executed = False

        for group in self.backup_groups:
            if group.get("active", True):  # Verificar se o grupo está ativo
                backups_executed = True  # Marcar que pelo menos um backup foi executado
                start_backup(
                    group["source_directories"],
                    group["backup_destination"],
                    group["incremental"],
                    group["name"],
                    self.backup_info
                )
            else:
                print(f"Backup for group {group['name']} is disabled.")

        if backups_executed:
            QMessageBox.information(self, 'Backup', 'Backup completed successfully.')
        else:
            QMessageBox.information(self, 'Backup', 'No active backups. No backups were performed.')

        self.save_settings()

    def load_settings(self):
        config = load_config(CONFIG_FILE)
        if config:
            self.backup_groups = config.get('backup_groups', [])
            for group in self.backup_groups:
                self.group_list.addItem(group['name'])

    def save_settings(self):
        config = {'backup_groups': self.backup_groups}
        save_config(CONFIG_FILE, config)
        save_last_backup(LAST_BACKUP_FILE, self.backup_info)

def main():
    app = QApplication(sys.argv)
    ex = BackupApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QColorDialog, QSpinBox, QApplication, QTabWidget,
                           QComboBox, QScrollArea, QMessageBox, QFontComboBox, QFileDialog,
                           QListWidgetItem, QGroupBox, QListWidget, QTableWidget, QTableWidgetItem,QInputDialog)
from PyQt6.QtCore import Qt, QSize,pyqtSignal
from PyQt6.QtGui import QColor, QIcon
import sys
import json
import os


import shutil


class ColorPicker(QWidget):
    def __init__(self, label_text, default_color="#000000", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        self.label = QLabel(label_text)
        self.label.setMinimumWidth(120)
        
        # Color input
        self.color_input = QLineEdit(default_color)
        self.color_input.setMaximumWidth(100)
        
        # Color button
        self.color_button = QPushButton()
        self.color_button.setFixedSize(30, 30)
        self.color_button.clicked.connect(self.show_color_dialog)
        
        # Set initial color
        self.set_color(default_color)
        
        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.color_input)
        layout.addWidget(self.color_button)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def show_color_dialog(self):
        color = QColorDialog.getColor(QColor(self.color_input.text()))
        if color.isValid():
            self.set_color(color.name())
    
    def set_color(self, color):
        self.color_input.setText(color)
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid #666666;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                border: 2px solid #333333;
            }}
        """)
    
    def get_color(self):
        return self.color_input.text()



class StyleEditor(QMainWindow):  
    style_updated = pyqtSignal(str)
    def __init__(self,main_window=None):
        super().__init__()
        self.main_window = main_window
        # Icon klasör yolu için değişken
        self.icon_directory = os.path.join("docs", "icon")

        # docs klasörünün varlığını kontrol et
        if not os.path.exists("docs"):
            os.makedirs("docs")

        # docs/icon klasörünün varlığını kontrol et
        if not os.path.exists(self.icon_directory):
            os.makedirs(self.icon_directory)

        self.init_ui()

# Yeni bir stil dosyası oluşturmak için yeni bir metod:
    def ensure_style_presets_file(self):
        """Stil önayarları dosyasının varlığını kontrol et ve yoksa oluştur"""
        presets_file = 'docs/style_presets.json'
        if not os.path.exists(presets_file):
            with open(presets_file, 'w') as f:
                json.dump({}, f)
    
    # init_ui metodunda değişiklikler yapmak için:

    def init_ui(self):
        """Arayüz bileşenlerini oluştur"""
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Tab widget oluştur
        tabs = QTabWidget()

        # Ana Program Stilleri sekmesi
        program_styles_tab = self.create_program_styles_tab()
        tabs.addTab(program_styles_tab, "Program Stilleri")

        # Buton Stilleri sekmesi
        button_styles_tab = self.create_button_styles_tab()
        tabs.addTab(button_styles_tab, "Buton Stilleri")

        # Kaydedilen Stiller sekmesi
        saved_styles_tab = self.create_saved_styles_tab()
        tabs.addTab(saved_styles_tab, "Kaydedilen Stiller")

        # Tabs'i ana layout'a ekle
        main_layout.addWidget(tabs)

        # Alt butonlar
        button_layout = QHBoxLayout()

        # Stil Kaydet butonu
        save_preset_button = QPushButton("Stil Kaydet")
        save_preset_button.setIcon(QIcon(os.path.join(self.icon_directory, "save.png")))
        save_preset_button.clicked.connect(self.save_style_preset)
        save_preset_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        save_button = QPushButton("Değişiklikleri Kaydet")
        save_button.setIcon(QIcon(os.path.join(self.icon_directory, "save.png")))
        save_button.clicked.connect(self.save_styles)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        reset_button = QPushButton("Varsayılan Ayarlara Dön")
        reset_button.setIcon(QIcon(os.path.join(self.icon_directory, "reset.png")))
        reset_button.clicked.connect(self.reset_styles)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        button_layout.addWidget(save_preset_button)  # Yeni stil kaydetme butonu
        button_layout.addWidget(save_button)
        button_layout.addWidget(reset_button)

        

        main_layout.addLayout(button_layout)

        self.setWindowTitle('Style Editor')
        self.setGeometry(300, 30, 900, 800)

        # Stil ayarlarını yükle
        self.load_styles()
        # Kaydedilmiş stilleri yükle
        self.load_style_presets()

    def create_program_styles_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)

        # Sol panel (stil ayarları) ve sağ panel (önizleme) için container
        main_container = QHBoxLayout()

        # Sol Panel - Stil Ayarları
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)

        # Ana Program Renkleri
        left_layout.addWidget(QLabel("<h3>Ana Program Renkleri</h3>"))

        self.background_color = ColorPicker("Arkaplan Rengi:", "#91B5D5")
        self.background_color.color_input.textChanged.connect(self.update_program_preview)
        self.text_color = ColorPicker("Yazı Rengi:", "#000000")
        self.text_color.color_input.textChanged.connect(self.update_program_preview)
        self.accent_color = ColorPicker("Vurgu Rengi:", "#CC3300")
        self.accent_color.color_input.textChanged.connect(self.update_program_preview)

        left_layout.addWidget(self.background_color)
        left_layout.addWidget(self.text_color)
        left_layout.addWidget(self.accent_color)

        # Font Ayarları
        left_layout.addWidget(QLabel("<h3>Font Ayarları</h3>"))

        font_layout = QHBoxLayout()

        font_label = QLabel("Font:")
        font_label.setMinimumWidth(120)
        self.font_family = QFontComboBox()
        self.font_family.setCurrentText("Segoe UI")
        self.font_family.currentFontChanged.connect(self.update_program_preview)

        font_size_label = QLabel("Boyut:")
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        self.font_size.valueChanged.connect(self.update_program_preview)

        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_family)
        font_layout.addWidget(font_size_label)
        font_layout.addWidget(self.font_size)
        font_layout.addStretch()

        left_layout.addLayout(font_layout)

        # Tablo Stilleri
        left_layout.addWidget(QLabel("<h3>Tablo Stilleri</h3>"))

        self.table_header_color = ColorPicker("Başlık Rengi:", "#4A4A4A")
        self.table_header_color.color_input.textChanged.connect(self.update_program_preview)
        self.table_alternate_color = ColorPicker("Alternatif Satır:", "#F5F5F5")
        self.table_alternate_color.color_input.textChanged.connect(self.update_program_preview)
        self.table_hover_color = ColorPicker("Hover Rengi:", "#E6E6E6")
        self.table_hover_color.color_input.textChanged.connect(self.update_program_preview)

        left_layout.addWidget(self.table_header_color)
        left_layout.addWidget(self.table_alternate_color)
        left_layout.addWidget(self.table_hover_color)

        # Tab Stilleri
        left_layout.addWidget(QLabel("<h3>Tab Stilleri</h3>"))

        self.tab_background = ColorPicker("Tab Arkaplan:", "#E6E6E6")
        self.tab_background.color_input.textChanged.connect(self.update_program_preview)
        self.tab_selected = ColorPicker("Seçili Tab:", "#CC3300")
        self.tab_selected.color_input.textChanged.connect(self.update_program_preview)
        self.tab_hover = ColorPicker("Hover Rengi:", "#CCCCCC")
        self.tab_hover.color_input.textChanged.connect(self.update_program_preview)

        left_layout.addWidget(self.tab_background)
        left_layout.addWidget(self.tab_selected)
        left_layout.addWidget(self.tab_hover)

        left_panel.setLayout(left_layout)

        # Sağ Panel - Önizleme
        right_panel = QGroupBox("Program Önizleme")
        right_layout = QVBoxLayout()

        # Sadece tablo önizlemesi
        self.preview_table = QTableWidget(3, 3)
        self.preview_table.setHorizontalHeaderLabels(["Başlık 1", "Başlık 2", "Başlık 3"])
        self.preview_table.setAlternatingRowColors(True)
        # Örnek veriler
        for i in range(3):
            for j in range(3):
                self.preview_table.setItem(i, j, QTableWidgetItem(f"Satır {i+1}, Sütun {j+1}"))
        right_layout.addWidget(self.preview_table)

        right_panel.setLayout(right_layout)

        # Sol ve sağ panelleri ana container'a ekle
        main_container.addWidget(left_panel, 1)  # 1 birim genişlik
        main_container.addWidget(right_panel, 1)  # 1 birim genişlik

        layout.addLayout(main_container)
        scroll.setWidget(content)

        # İlk önizlemeyi göster
        self.update_program_preview()

        return scroll

    def create_button_styles_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)

        # Buton seçimi için üst panel
        button_select_group = QGroupBox("Buton Seçimi")
        button_select_layout = QVBoxLayout()

        # Kategori seçimi
        category_layout = QHBoxLayout()
        category_label = QLabel("Kategori:")
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Çalışan İşlemleri",
            "Mesai İşlemleri",
            "Kullanıcı İşlemleri",
            "Rapor İşlemleri",
            "Genel İşlemler"
        ])
        self.category_combo.currentIndexChanged.connect(self.update_button_list)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)

        # Buton listesi
        self.button_list = QListWidget()
        self.button_list.itemSelectionChanged.connect(self.on_button_selected)

        button_select_layout.addLayout(category_layout)
        button_select_layout.addWidget(self.button_list)
        button_select_group.setLayout(button_select_layout)
        layout.addWidget(button_select_group)

        # Stil ayarları için grup
        style_group = QGroupBox("Stil Ayarları")
        style_layout = QVBoxLayout()

        # Renk ayarları
        # Renk ayarları bölümünde:
        self.button_background = ColorPicker("Normal Renk:", "#CC3300")
        self.button_background.color_input.textChanged.connect(self.update_preview)  # Sinyal bağlantısı eklendi
        self.button_hover = ColorPicker("Hover Rengi:", "#E63900")
        self.button_hover.color_input.textChanged.connect(self.update_preview)  # Sinyal bağlantısı eklendi
        self.button_text = ColorPicker("Yazı Rengi:", "#FFFFFF")
        self.button_text.color_input.textChanged.connect(self.update_preview)  # Sinyal bağlantısı eklendi
        
        style_layout.addWidget(self.button_background)
        style_layout.addWidget(self.button_hover)
        style_layout.addWidget(self.button_text)

        icon_layout = QHBoxLayout()
        icon_label = QLabel("İkon:")
        self.icon_path_input = QLineEdit()
        self.icon_path_input.setReadOnly(True)
        browse_button = QPushButton("Göz At")
        browse_button.clicked.connect(self.browse_icon)

        # İkon ayarları
        icon_layout = QHBoxLayout()
        icon_label = QLabel("İkon:")
        self.icon_path_input = QLineEdit()
        self.icon_path_input.setReadOnly(True)
        browse_button = QPushButton("Göz At")
        browse_button.clicked.connect(self.browse_icon)
    
        # İkon kaydetme butonu ekle
        save_icon_button = QPushButton("İkonu Kaydet")
        save_icon_button.clicked.connect(self.save_button_style)
        save_icon_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_path_input)
        icon_layout.addWidget(browse_button)
        icon_layout.addWidget(save_icon_button)
        style_layout.addLayout(icon_layout)
    
        # İkon boyutu ayarı ekle
        icon_size_layout = QHBoxLayout()
        icon_size_label = QLabel("İkon Boyutu:")
        self.icon_size = QSpinBox()
        self.icon_size.setRange(16, 48)
        self.icon_size.setValue(20)
        self.icon_size.valueChanged.connect(self.update_preview)
    
        icon_size_layout.addWidget(icon_size_label)
        icon_size_layout.addWidget(self.icon_size)
        icon_size_layout.addStretch()
        style_layout.addLayout(icon_size_layout)

        # Buton boyutları
        padding_layout = QHBoxLayout()
        padding_label = QLabel("İç Boşluk:")
        self.button_padding = QSpinBox()
        self.button_padding.setRange(4, 20)
        self.button_padding.setValue(8)
        self.button_padding.valueChanged.connect(self.update_preview)

        padding_layout.addWidget(padding_label)
        padding_layout.addWidget(self.button_padding)
        padding_layout.addStretch()
        style_layout.addLayout(padding_layout)

        # Köşe yuvarlaklığı
        radius_layout = QHBoxLayout()
        radius_label = QLabel("Köşe Yuvarlaklığı:")
        self.button_radius = QSpinBox()
        self.button_radius.setRange(0, 20)
        self.button_radius.setValue(4)
        self.button_radius.valueChanged.connect(self.update_preview)

        radius_layout.addWidget(radius_label)
        radius_layout.addWidget(self.button_radius)
        radius_layout.addStretch()
        style_layout.addLayout(radius_layout)

        style_group.setLayout(style_layout)
        layout.addWidget(style_group)

        # Önizleme bölümü
        preview_group = QGroupBox("Önizleme")
        preview_layout = QVBoxLayout()

        self.preview_button = QPushButton("Önizleme Butonu")
        self.preview_button.setMinimumHeight(40)
        preview_layout.addWidget(self.preview_button)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        layout.addStretch()
        scroll.setWidget(content)

        # Button listesini doldur
        self.update_button_list()

        return scroll
    
    def darken_color(self, color, factor=0.8):
        """Rengi koyulaştır"""
        color = QColor(color)
        h = color.hue()
        s = color.saturation()
        v = int(color.value() * factor)
        return QColor.fromHsv(h, s, v).name()
    
    def select_icon(self):
        """Icon seçme dialog'unu göster ve seçilen iconu kaydet"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Image files (*.png *.jpg *.ico *.svg)")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                source_path = selected_files[0]
                file_name = os.path.basename(source_path)
                destination_path = os.path.join(self.icon_path, file_name)
                
                try:
                    # Dosyayı icon  klasörüne kopyala
                    shutil.copy2(source_path, destination_path)
                    QMessageBox.information(
                        self, 
                        'Başarılı',
                        f'Icon başarıyla kaydedildi:\n{destination_path}'
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        'Hata',
                        f'Icon kaydedilirken hata oluştu:\n{str(e)}'
        
                    )


    def ensure_icon_directory(self):
        """Icon klasörünün varlığını kontrol et ve yoksa oluştur"""
        if not os.path.exists(self.icon_path):
            try:
                os.makedirs(self.icon_path)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Hata',
                    f'Icon klasörü oluşturulurken hata oluştu:\n{str(e)}'
                )
    
    def update_program_preview(self):
        """Program önizleme widgetlarını güncelle"""
        # Stil oluştur
        style = f"""
            QWidget {{
                background-color: {self.background_color.get_color()};
                color: {self.text_color.get_color()};
                font-family: '{self.font_family.currentText()}';
                font-size: {self.font_size.value()}px;
            }}
    
            QTableWidget {{
                background-color: white;
                alternate-background-color: {self.table_alternate_color.get_color()};
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                gridline-color: #E0E0E0;
            }}
    
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }}
    
            QHeaderView::section {{
                background-color: {self.table_header_color.get_color()};
                color: white;
                padding: 12px;
                font-weight: bold;
                border: none;
            }}
    
            QTabWidget::pane {{
                border: 2px solid {self.accent_color.get_color()};
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }}
    
            QTabBar::tab {{
                background-color: {self.tab_background.get_color()};
                color: {self.text_color.get_color()};
                padding: 12px 25px;
                margin: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }}
    
            QTabBar::tab:selected {{
                background-color: {self.tab_selected.get_color()};
                color: white;
            }}
    
            QTabBar::tab:hover:!selected {{
                background-color: {self.tab_hover.get_color()};
            }}
        """
    
        # Stili tablo önizlemesine uygula
        self.preview_table.setStyleSheet(style)
    

    def update_button_list(self):
        """Seçili kategoriye göre buton listesini güncelle"""
        self.button_list.clear()
        category = self.category_combo.currentText()

        buttons = {
            "Çalışan İşlemleri": [
                {"name": "Çalışan Ekle", "icon": "employeesadd.png"},
                {"name": "Çalışan Düzenle", "icon": "employeesedit.png"},
                {"name": "Çalışan Sil", "icon": "employeesdelete.png"}
            ],
            "Mesai İşlemleri": [
                {"name": "Mesai Ekle", "icon": "timemanagement.png"},
                {"name": "Mesai Düzenle", "icon": "timeedit.png"}
            ],
            "Kullanıcı İşlemleri": [
                {"name": "Kullanıcı Ekle", "icon": "adduser.png"},
                {"name": "Şifre Değiştir", "icon": "passwordedit.png"},
                {"name": "Kullanıcı Sil", "icon": "deletuser.png"}
            ],
            "Rapor İşlemleri": [
                {"name": "PDF Oluştur", "icon": "pdf.png"},
                {"name": "Excel İndir", "icon": "excel.png"},
                {"name": "Rapor Güncelle", "icon": "update.png"}
            ],
            "Genel İşlemler": [
                {"name": "Değişiklikleri Kaydet", "icon": "save.png"},
                {"name": "Varsayılana Dön", "icon": "reset.png"},
                {"name": "Giriş Yap", "icon": "login.png"}
            ]
        }

        if category in buttons:
            for button in buttons[category]:
                item = QListWidgetItem(button["name"])
                item.setData(Qt.ItemDataRole.UserRole, button)
                self.button_list.addItem(item)














    
    
    def browse_icon(self):
        """İkon seçme dialog'unu göster"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("İkon Dosyaları (*.png *.jpg *.ico *.svg)")
    
        if file_dialog.exec():
            source_path = file_dialog.selectedFiles()[0]
            
            # Seçili butonun bilgilerini al
            items = self.button_list.selectedItems()
            if not items:
                QMessageBox.warning(self, 'Uyarı', 'Lütfen önce bir buton seçin.')
                return
                
            button_data = items[0].data(Qt.ItemDataRole.UserRole)
            original_icon_name = button_data['icon']  # Örneğin "save.png"
            
            # Orijinal iconun yolu
            original_icon_path = os.path.join('docs', 'icon', original_icon_name)
            
            # Yeni isimler oluştur
            name, ext = os.path.splitext(original_icon_name)
            renamed_original = f"{name}1{ext}"  # Örneğin "save1.png"
            
            try:
                # docs/icon klasörünün varlığını kontrol et
                if not os.path.exists(os.path.join('docs', 'icon')):
                    os.makedirs(os.path.join('docs', 'icon'))
                
                # 1. Önce orijinal iconu yeniden adlandır (eğer varsa)
                if os.path.exists(original_icon_path):
                    new_path = os.path.join('docs', 'icon', renamed_original)
                    os.rename(original_icon_path, new_path)
                
                # 2. Yeni iconu orijinal isimle kaydet
                shutil.copy2(source_path, original_icon_path)
                
                # Icon path'i güncelle
                self.icon_path_input.setText(original_icon_path)
    
                # Stil dosyasını güncelle
                if self.save_button_style():
                    self.update_preview()
                    QMessageBox.information(
                        self, 
                        'Başarılı',
                        f'Icon başarıyla değiştirildi!\n'
                        f'Eski icon: {renamed_original}\n'
                        f'Yeni icon: {original_icon_name}'
                    )
    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Hata',
                    f'Icon değiştirilirken hata oluştu:\n{str(e)}'
                )
    
    def save_button_style(self):
        """Seçili butonun stilini kaydet"""
        try:
            items = self.button_list.selectedItems()
            if not items:
                return False
                
            button_data = items[0].data(Qt.ItemDataRole.UserRole)
            category = self.category_combo.currentText()
            style_key = f"{category}_{button_data['name']}"
            
            current_icon = self.icon_path_input.text()
            if current_icon:
                icon_name = os.path.basename(current_icon)
                
                # Stil dosyasını güncelle
                if os.path.exists('button_styles.json'):
                    with open('button_styles.json', 'r') as f:
                        styles = json.load(f)
                else:
                    styles = {}
    
                styles[style_key] = {
                    'background': self.button_background.get_color(),
                    'hover': self.button_hover.get_color(),
                    'text': self.button_text.get_color(),
                    'padding': self.button_padding.value(),
                    'radius': self.button_radius.value(),
                    'icon': icon_name
                }
    
                with open('button_styles.json', 'w') as f:
                    json.dump(styles, f, indent=4)
    
                return True
    
            return False
            
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Stil kaydedilirken hata oluştu: {str(e)}')
            return False

    


    def update_preview(self):
        """Önizleme butonunu güncelle"""
        items = self.button_list.selectedItems()
        if items:
            button_data = items[0].data(Qt.ItemDataRole.UserRole)
            self.preview_button.setText(button_data['name'])
    
            # Buton stilini güncelle
            style = f"""
                QPushButton {{
                    background-color: {self.button_background.get_color()};
                    color: {self.button_text.get_color()};
                    border: none;
                    border-radius: {self.button_radius.value()}px;
                    padding: {self.button_padding.value()}px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.button_hover.get_color()};
                }}
            """
            self.preview_button.setStyleSheet(style)
    
            # İkon kontrolü ve güncellemesi
            icon_path = self.icon_path_input.text()
            if icon_path and os.path.exists(icon_path):
                icon = QIcon(icon_path)
            elif 'icon' in button_data:
                default_icon_path = os.path.join(self.icon_directory, button_data['icon'])
                if os.path.exists(default_icon_path):
                    icon = QIcon(default_icon_path)
                else:
                    icon = QIcon()
            else:
                icon = QIcon()
    
            if not icon.isNull():
                self.preview_button.setIcon(icon)
                self.preview_button.setIconSize(QSize(self.icon_size.value(), self.icon_size.value()))
            else:
                self.preview_button.setIcon(QIcon())































                    

                    

    


    def update_button_preview(self):
        """Önizleme butonunu güncelle"""
        print("\nupdate_button_preview metodu başladı")
        items = self.button_list.selectedItems()
        if items:
            button_data = items[0].data(Qt.ItemDataRole.UserRole)
            print(f"Buton önizlemesi güncelleniyor: {button_data['name']}")

            # Stili ayarla
            style = f"""
                QPushButton {{
                    background-color: {self.button_background.get_color()};
                    color: {self.button_text.get_color()};
                    border: none;
                    border-radius: {self.button_radius.value()}px;
                    padding: {self.button_padding.value()}px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.button_hover.get_color()};
                }}
            """
            self.preview_button.setStyleSheet(style)

            # İkon ayarla
            if os.path.exists('button_styles.json'):
                print("Buton stilleri dosyası bulundu")
                try:
                    with open('button_styles.json', 'r') as f:
                        styles = json.load(f)

                    style_key = f"{self.category_combo.currentText()}_{button_data['name']}"
                    if style_key in styles:
                        print(f"Buton stili bulundu: {style_key}")
                        style = styles[style_key]

                        # İkon yolunu kontrol et
                        icon_path = None
                        if 'icon' in style:
                            icon_path = os.path.join(self.icon_directory, style['icon'])
                            print(f"Stil dosyasından icon yolu: {icon_path}")
                        else:
                            icon_path = os.path.join(self.icon_directory, button_data['icon'])
                            print(f"Varsayılan icon yolu: {icon_path}")

                        if os.path.exists(icon_path):
                            print("Icon dosyası bulundu")
                            self.preview_button.setIcon(QIcon(icon_path))
                            self.preview_button.setIconSize(QSize(self.icon_size.value(), self.icon_size.value()))
                        else:
                            print(f"Icon dosyası bulunamadı: {icon_path}")
                except Exception as e:
                    print(f"Stil yükleme hatası: {str(e)}")

            print("Buton önizlemesi güncelleme tamamlandı")

    def on_button_selected(self):
        """Seçili butona göre stil ayarlarını güncelle"""
        print("\non_button_selected metodu başladı")
        items = self.button_list.selectedItems()
        if items:
            print("Seçili buton bulundu")
            button_data = items[0].data(Qt.ItemDataRole.UserRole)

            # Mevcut stil ayarlarını yükle
            style_key = f"{self.category_combo.currentText()}_{button_data['name']}"
            print(f"Stil anahtarı: {style_key}")

            if os.path.exists('button_styles.json'):
                print("Stil dosyası bulundu")
                with open('button_styles.json', 'r') as f:
                    styles = json.load(f)
                    if style_key in styles:
                        print("Kayıtlı stil bulundu")
                        style = styles[style_key]

                        # Renk ayarları
                        self.button_background.set_color(style.get('background', '#CC3300'))
                        self.button_hover.set_color(style.get('hover', '#E63900'))
                        self.button_text.set_color(style.get('text', '#FFFFFF'))
                        self.button_padding.setValue(style.get('padding', 8))
                        self.button_radius.setValue(style.get('radius', 4))

                        # İkon ayarları
                        if 'icon' in style:
                            icon_path = os.path.join(self.icon_directory, style['icon'])
                        else:
                            icon_path = os.path.join(self.icon_directory, button_data['icon'])
                        self.icon_path_input.setText(icon_path)

                        print(f"İkon yolu ayarlandı: {icon_path}")
                    else:
                        print("Kayıtlı stil bulunamadı, varsayılan değerler kullanılıyor")
                        # Varsayılan değerler
                        self.button_background.set_color('#CC3300')
                        self.button_hover.set_color('#E63900')
                        self.button_text.set_color('#FFFFFF')
                        self.icon_path_input.setText(os.path.join(self.icon_directory, button_data['icon']))
                        self.button_padding.setValue(8)
                        self.button_radius.setValue(4)

                print("Önizleme güncelleniyor")
                self.update_preview()
                print("on_button_selected tamamlandı")



    def save_styles(self):
        """Stil ayarlarını kaydet"""
        try:
            # Tüm stil ayarlarını bir sözlükte topla
            styles = {
                'program': {
                    'background': self.background_color.get_color(),
                    'text': self.text_color.get_color(),
                    'accent': self.accent_color.get_color(),
                    'font_family': self.font_family.currentText(),
                    'font_size': self.font_size.value(),
                    'table_header': self.table_header_color.get_color(),
                    'table_alternate': self.table_alternate_color.get_color(),
                    'table_hover': self.table_hover_color.get_color(),
                    'tab_background': self.tab_background.get_color(),
                    'tab_selected': self.tab_selected.get_color(),
                    'tab_hover': self.tab_hover.get_color()
                },
                'button': {
                    'background': self.button_background.get_color(),
                    'hover': self.button_hover.get_color(),
                    'text': self.button_text.get_color(),
                    'padding': self.button_padding.value(),
                    'radius': self.button_radius.value(),
                    'icon_size': self.icon_size.value()
                }
            }
            
            # Ayarları docs klasöründeki JSON dosyasına kaydet
            with open('docs/style_settings.json', 'w') as f:
                json.dump(styles, f, indent=4)
            
            # Ana program stilini güncelle
            self.update_main_program_style(styles)
            
            # Başarılı mesajı göster
            QMessageBox.information(self, 'Başarılı', 
                'Stil ayarları kaydedildi ve ana programa uygulandı!\n'
                'Değişikliklerin tamamen uygulanması için ana programı yeniden başlatın.')
            
        except Exception as e:
            QMessageBox.critical(self, 'Hata',
                f'Stil ayarları kaydedilirken hata oluştu:\n{str(e)}')

    def update_main_program_style(self, styles):
        """Ana program stil dosyasını güncelle"""
        try:
            # Yeni CSS stilini oluştur
            new_style = f"""
            QMainWindow, QWidget {{
                background-color: {styles['program']['background']};
                color: {styles['program']['text']};
                font-family: '{styles['program']['font_family']}';
                font-size: {styles['program']['font_size']}px;
            }}

            QTabWidget::pane {{
                border: 2px solid {styles['program']['accent']};
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }}

            QTabBar::tab {{
                background-color: {styles['program']['tab_background']};
                color: {styles['program']['text']};
                padding: 12px 25px;
                margin: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }}

            QTabBar::tab:selected {{
                background-color: {styles['program']['tab_selected']};
                color: white;
            }}

            QTabBar::tab:hover:!selected {{
                background-color: {styles['program']['tab_hover']};
            }}

            QTableWidget {{
                background-color: white;
                alternate-background-color: {styles['program']['table_alternate']};
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                gridline-color: #E0E0E0;
            }}

            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }}

            QTableWidget::item:selected {{
                background-color: {styles['program']['accent']};
                color: white;
            }}

            QHeaderView::section {{
                background-color: {styles['program']['table_header']};
                color: white;
                padding: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #666666;
            }}

            QPushButton {{
                background-color: {styles['button']['background']};
                color: {styles['button']['text']};
                border: none;
                border-radius: {styles['button']['radius']}px;
                padding: {styles['button']['padding']}px;
                font-weight: bold;
                min-width: 100px;
            }}

            QPushButton:hover {{
                background-color: {styles['button']['hover']};
            }}

            QLineEdit, QDateEdit, QComboBox {{
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }}
            """

            # Ana program dosyasını aç ve güncelle
            if hasattr(self, 'style_updated'):
                self.style_updated.emit(new_style)

            # Continue with file updates as before
            try:
                with open('iremin_programı.py', 'r', encoding='utf-8') as file:
                    content = file.read()

                start = content.find('MAIN_STYLE = """')
                if start != -1:
                    end = content.find('"""', start + len('MAIN_STYLE = """'))
                    if end != -1:
                        new_content = (
                            content[:start + len('MAIN_STYLE = """')] + 
                            '\n' + new_style + 
                            content[end:]
                        )

                        # Save backup
                        with open('iremin_programı.py.bak', 'w', encoding='utf-8') as backup:
                            backup.write(content)

                        # Save updated file
                        with open('iremin_programı.py', 'w', encoding='utf-8') as file:
                            file.write(new_content)

                        return True

            except Exception as e:
                print(f"File update error: {str(e)}")

            return False

        except Exception as e:
            print(f"Style update error: {str(e)}")
            raise









    def load_styles(self):
        """Kayıtlı stil ayarlarını yükle"""
        try:
             # Stil ayarları dosyası docs klasöründe var mı kontrol et
            if os.path.exists('docs/style_settings.json'):
                with open('docs/style_settings.json', 'r') as f:
                    styles = json.load(f)

                # Program stillerini yükle
                program = styles.get('program', {})
                self.background_color.set_color(program.get('background', '#91B5D5'))
                self.text_color.set_color(program.get('text', '#000000'))
                self.accent_color.set_color(program.get('accent', '#CC3300'))
                
                # Font ayarlarını yükle
                font_family = program.get('font_family', 'Segoe UI')
                index = self.font_family.findText(font_family)
                if index >= 0:
                    self.font_family.setCurrentIndex(index)
                self.font_size.setValue(program.get('font_size', 12))
                
                # Tablo stillerini yükle
                self.table_header_color.set_color(program.get('table_header', '#4A4A4A'))
                self.table_alternate_color.set_color(program.get('table_alternate', '#F5F5F5'))
                self.table_hover_color.set_color(program.get('table_hover', '#E6E6E6'))
                
                # Tab stillerini yükle
                self.tab_background.set_color(program.get('tab_background', '#E6E6E6'))
                self.tab_selected.set_color(program.get('tab_selected', '#CC3300'))
                self.tab_hover.set_color(program.get('tab_hover', '#CCCCCC'))

                # Buton stillerini yükle
                button = styles.get('button', {})
                self.button_background.set_color(button.get('background', '#CC3300'))
                self.button_hover.set_color(button.get('hover', '#E63900'))
                self.button_text.set_color(button.get('text', '#FFFFFF'))
                self.button_padding.setValue(button.get('padding', 8))
                self.button_radius.setValue(button.get('radius', 4))
                self.icon_size.setValue(button.get('icon_size', 20))

                # Önizlemeyi güncelle
                self.update_button_preview()

        except Exception as e:
            print(f"Stil yükleme hatası: {str(e)}")

    def reset_styles(self):
        """Varsayılan stil ayarlarına dön"""
        reply = QMessageBox.question(
            self,
            'Varsayılan Ayarlar',
            'Tüm stiller varsayılan değerlere sıfırlanacak. Bu işlem geri alınamaz.\n\n'
            'Devam etmek istiyor musunuz?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Program stillerini sıfırla
                self.background_color.set_color('#91B5D5')
                self.text_color.set_color('#000000')
                self.accent_color.set_color('#CC3300')
                
                # Font ayarlarını sıfırla
                segoe_index = self.font_family.findText('Segoe UI')
                if segoe_index >= 0:
                    self.font_family.setCurrentIndex(segoe_index)
                self.font_size.setValue(12)
                
                # Tablo stillerini sıfırla
                self.table_header_color.set_color('#4A4A4A')
                self.table_alternate_color.set_color('#F5F5F5')
                self.table_hover_color.set_color('#E6E6E6')
                
                # Tab stillerini sıfırla
                self.tab_background.set_color('#E6E6E6')
                self.tab_selected.set_color('#CC3300')
                self.tab_hover.set_color('#CCCCCC')
                
                # Buton stillerini sıfırla
                self.button_background.set_color('#CC3300')
                self.button_hover.set_color('#E63900')
                self.button_text.set_color('#FFFFFF')
                self.button_padding.setValue(8)
                self.button_radius.setValue(4)
                self.icon_size.setValue(20)

                # Önizlemeyi güncelle
                self.update_button_preview()

                # Stil dosyasını sil
                if os.path.exists('style_settings.json'):
                    os.remove('style_settings.json')

                # Ana programdaki stilleri sıfırla ve kaydet
                self.save_styles()

                QMessageBox.information(self, 'Başarılı', 
                    'Tüm stiller varsayılan değerlere döndürüldü!')

            except Exception as e:
                QMessageBox.critical(self, 'Hata',
                    f'Sıfırlama sırasında hata oluştu:\n{str(e)}')
                








    def save_style_preset(self):
      """Mevcut stil ayarlarını önayar olarak kaydet"""
      try:
          # Stil adını kullanıcıdan al
          style_name, ok = QInputDialog.getText(
              self, 'Stil Kaydet', 
              'Stil adını giriniz:',
              QLineEdit.EchoMode.Normal
          )
          
          if ok and style_name:
              # Mevcut stil ayarlarını topla
              current_style = {
                  'program': {
                      'background': self.background_color.get_color(),
                      'text': self.text_color.get_color(),
                      'accent': self.accent_color.get_color(),
                      'font_family': self.font_family.currentText(),
                      'font_size': self.font_size.value(),
                      'table_header': self.table_header_color.get_color(),
                      'table_alternate': self.table_alternate_color.get_color(),
                      'table_hover': self.table_hover_color.get_color(),
                      'tab_background': self.tab_background.get_color(),
                      'tab_selected': self.tab_selected.get_color(),
                      'tab_hover': self.tab_hover.get_color()
                  },
                  'button': {
                      'background': self.button_background.get_color(),
                      'hover': self.button_hover.get_color(),
                      'text': self.button_text.get_color(),
                      'padding': self.button_padding.value(),
                      'radius': self.button_radius.value(),
                      'icon_size': self.icon_size.value()
                  }
              }
              
              # Stil önayarları dosyasını yükle veya oluştur
              presets_file = 'docs/style_presets.json'
              if os.path.exists(presets_file):
                  with open(presets_file, 'r') as f:
                      presets = json.load(f)
              else:
                  presets = {}
              
              # Yeni stili ekle
              presets[style_name] = current_style
              
              # Değişiklikleri kaydet
              with open(presets_file, 'w') as f:
                  json.dump(presets, f, indent=4)
              
              # Stil önizleme listesini güncelle
              self.load_style_presets()
              
              QMessageBox.information(self, 'Başarılı', f'"{style_name}" stili başarıyla kaydedildi!')
              
      except Exception as e:
          QMessageBox.critical(self, 'Hata', f'Stil kaydedilirken hata oluştu:\n{str(e)}')
    
    def create_saved_styles_tab(self):
        """Kaydedilen stilleri gösteren sekmeyi oluştur"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)

        # Stil listesi
        list_group = QGroupBox("Kaydedilmiş Stiller")
        list_layout = QVBoxLayout()

        self.style_list = QListWidget()
        self.style_list.itemSelectionChanged.connect(self.preview_selected_style)

        # Stil yönetim butonları
        button_layout = QHBoxLayout()

        load_button = QPushButton("Seçili Stili Yükle")
        load_button.clicked.connect(self.load_selected_style)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        delete_button = QPushButton("Seçili Stili Sil")
        delete_button.clicked.connect(self.delete_selected_style)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        button_layout.addWidget(load_button)
        button_layout.addWidget(delete_button)

        list_layout.addWidget(self.style_list)
        list_layout.addLayout(button_layout)
        list_group.setLayout(list_layout)

        # Önizleme bölümü
        preview_group = QGroupBox("Stil Önizleme")
        preview_layout = QVBoxLayout()

        # Örnek widgetlar
        # Tablo önizlemesi
        self.preview_table_saved = QTableWidget(3, 3)
        self.preview_table_saved.setHorizontalHeaderLabels(["Başlık 1", "Başlık 2", "Başlık 3"])
        self.preview_table_saved.setAlternatingRowColors(True)
        for i in range(3):
            for j in range(3):
                self.preview_table_saved.setItem(i, j, QTableWidgetItem(f"Örnek {i+1},{j+1}"))

        # Tab önizlemesi
        preview_tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        preview_tabs.addTab(tab1, "Sekme 1")
        preview_tabs.addTab(tab2, "Sekme 2")

        # Buton önizlemesi
        self.preview_button_saved = QPushButton("Örnek Buton")
        self.preview_button_saved.setMinimumHeight(40)

        preview_layout.addWidget(preview_tabs)
        preview_layout.addWidget(self.preview_table_saved)
        preview_layout.addWidget(self.preview_button_saved)

        preview_group.setLayout(preview_layout)

        # Ana layout'a ekle
        layout.addWidget(list_group)
        layout.addWidget(preview_group)

        scroll.setWidget(content)
        return scroll
    
    
    
    
    
    
    
    
    def load_style_presets(self):
        """Kaydedilmiş stilleri listele"""
        self.style_list.clear()
        try:
            if os.path.exists('docs/style_presets.json'):
                with open('docs/style_presets.json', 'r') as f:
                    presets = json.load(f)
                    for style_name in presets:
                        self.style_list.addItem(style_name)
        except Exception as e:
            print(f"Stil önayarları yüklenirken hata: {str(e)}")
    
    def preview_selected_style(self):
        """Seçili stili önizle"""
        try:
            items = self.style_list.selectedItems()
            if items:
                style_name = items[0].text()
                with open('docs/style_presets.json', 'r') as f:
                    presets = json.load(f)
                    if style_name in presets:
                        style = presets[style_name]
                        self.apply_style_preview(style)
        except Exception as e:
            print(f"Stil önizleme hatası: {str(e)}")
    
    def apply_style_preview(self, style):
        """Seçili stili önizleme widgetlarına uygula"""
        program = style.get('program', {})
        button = style.get('button', {})

        # Tablo ve genel widget stilleri
        preview_style = f"""
            QWidget {{
                background-color: {program.get('background', '#91B5D5')};
                color: {program.get('text', '#000000')};
                font-family: '{program.get('font_family', 'Segoe UI')}';
                font-size: {program.get('font_size', 12)}px;
            }}

            QTableWidget {{
                background-color: white;
                alternate-background-color: {program.get('table_alternate', '#F5F5F5')};
                border: 1px solid #CCCCCC;
            }}

            QHeaderView::section {{
                background-color: {program.get('table_header', '#4A4A4A')};
                color: white;
                padding: 8px;
                border: none;
            }}

            QTabWidget::pane {{
                border: 2px solid {program.get('accent', '#CC3300')};
                border-radius: 6px;
                background-color: white;
            }}

            QTabBar::tab {{
                background-color: {program.get('tab_background', '#E6E6E6')};
                padding: 8px 20px;
                margin: 2px;
            }}

            QTabBar::tab:selected {{
                background-color: {program.get('tab_selected', '#CC3300')};
                color: white;
            }}
        """

        # Buton stili
        button_style = f"""
            QPushButton {{
                background-color: {button.get('background', '#CC3300')};
                color: {button.get('text', '#FFFFFF')};
                border: none;
                border-radius: {button.get('radius', 4)}px;
                padding: {button.get('padding', 8)}px;
            }}
            QPushButton:hover {{
                background-color: {button.get('hover', '#E63900')};
            }}
        """

        self.preview_table_saved.setStyleSheet(preview_style)
        self.preview_button_saved.setStyleSheet(button_style)

    
    def load_selected_style(self):
        """Seçili stili mevcut ayarlara yükle"""
        try:
            items = self.style_list.selectedItems()
            if items:
                style_name = items[0].text()
                with open('docs/style_presets.json', 'r') as f:
                    presets = json.load(f)
                    if style_name in presets:
                        style = presets[style_name]
                        
                        # Program stillerini yükle
                        program = style.get('program', {})
                        self.background_color.set_color(program.get('background', '#91B5D5'))
                        self.text_color.set_color(program.get('text', '#000000'))
                        self.accent_color.set_color(program.get('accent', '#CC3300'))
                        
                        # Font ayarlarını yükle
                        font_family = program.get('font_family', 'Segoe UI')
                        index = self.font_family.findText(font_family)
                        if index >= 0:
                            self.font_family.setCurrentIndex(index)
                        self.font_size.setValue(program.get('font_size', 12))
                        
                        # Tablo stillerini yükle
                        self.table_header_color.set_color(program.get('table_header', '#4A4A4A'))
                        self.table_alternate_color.set_color(program.get('table_alternate', '#F5F5F5'))
                        self.table_hover_color.set_color(program.get('table_hover', '#E6E6E6'))
                        
                        # Tab stillerini yükle
                        self.tab_background.set_color(program.get('tab_background', '#E6E6E6'))
                        self.tab_selected.set_color(program.get('tab_selected', '#CC3300'))
                        self.tab_hover.set_color(program.get('tab_hover', '#CCCCCC'))
                        
                        # Buton stillerini yükle
                        button = style.get('button', {})
                        self.button_background.set_color(button.get('background', '#CC3300'))
                        self.button_hover.set_color(button.get('hover', '#E63900'))
                        self.button_text.set_color(button.get('text', '#FFFFFF'))
                        self.button_padding.setValue(button.get('padding', 8))
                        self.button_radius.setValue(button.get('radius', 4))
                        self.icon_size.setValue(button.get('icon_size', 20))
                        
                        # Önizlemeleri güncelle
                        self.update_program_preview()
                        self.update_button_preview()
                        
                        QMessageBox.information(self, 'Başarılı', f'"{style_name}" stili başarıyla yüklendi!')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Stil yüklenirken hata oluştu:\n{str(e)}')
    
    def delete_selected_style(self):
        """Seçili stili sil"""
        try:
            items = self.style_list.selectedItems()
            if items:
                style_name = items[0].text()
                reply = QMessageBox.question(
                    self, 
                    'Stil Sil',
                    f'"{style_name}" stilini silmek istediğinizden emin misiniz?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    with open('docs/style_presets.json', 'r') as f:
                        presets = json.load(f)
                    
                    if style_name in presets:
                        del presets[style_name]
                        
                        with open('docs/style_presets.json', 'w') as f:
                            json.dump(presets, f, indent=4)
                        
                        self.load_style_presets()
                        QMessageBox.information(self, 'Başarılı', f'"{style_name}" stili başarıyla silindi!')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Stil silinirken hata oluştu:\n{str(e)}')
    







        

def main():
    app = QApplication(sys.argv)
    editor = StyleEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
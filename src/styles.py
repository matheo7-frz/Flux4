"""Theme PS4 authentique - style XMB horizontal pour l'application."""

COLORS = {
    "bg_primary": "#003087",
    "bg_secondary": "#00246d",
    "bg_card": "#0d3f9e",
    "bg_card_hover": "#1a4fb8",
    "bg_input": "#002470",
    "accent": "#00d4ff",
    "accent_hover": "#00b8e6",
    "accent_light": "#33ddff",
    "text_primary": "#ffffff",
    "text_secondary": "#99ccff",
    "text_muted": "#6699cc",
    "border": "#0050aa",
    "danger": "#e74c3c",
    "danger_hover": "#c0392b",
    "success": "#2ecc71",
    "warning": "#f1c40f",
    "scrollbar_bg": "#001d5a",
    "scrollbar_handle": "#0050aa",
    "ps4_dark": "#00113a",
    "ps4_mid": "#001d5a",
    "ps4_highlight": "#00d4ff",
}

MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["bg_primary"]};
}}

QWidget {{
    color: {COLORS["text_primary"]};
    font-family: "SST", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}}

/* Barre superieure */
#top_bar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0, 10, 40, 230),
        stop:1 rgba(0, 17, 58, 200));
    min-height: 44px;
    max-height: 44px;
    border-bottom: 1px solid rgba(0, 80, 170, 80);
}}

#top_bar_title {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["ps4_highlight"]};
    letter-spacing: 4px;
    padding-left: 20px;
}}

#top_bar_info {{
    font-size: 12px;
    color: {COLORS["text_secondary"]};
    padding-right: 20px;
}}

/* Zone de navigation horizontale */
#nav_strip {{
    background: transparent;
    min-height: 120px;
    max-height: 120px;
}}

#nav_icon_btn {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(13, 63, 158, 160),
        stop:1 rgba(0, 36, 109, 160));
    border: 2px solid rgba(0, 80, 170, 120);
    border-radius: 10px;
    color: {COLORS["text_secondary"]};
    font-size: 11px;
    padding: 4px;
}}

#nav_icon_btn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 79, 184, 200),
        stop:1 rgba(13, 63, 158, 200));
    border-color: rgba(0, 212, 255, 120);
    color: {COLORS["text_primary"]};
}}

#nav_icon_btn_active {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0, 212, 255, 50),
        stop:1 rgba(0, 150, 200, 25));
    border: 2px solid {COLORS["ps4_highlight"]};
    border-radius: 10px;
    color: {COLORS["text_primary"]};
    font-size: 11px;
    font-weight: bold;
    padding: 4px;
}}

#nav_selected_label {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    letter-spacing: 1px;
}}

/* Zone de contenu principal */
#content_area {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_primary"]},
        stop:1 #001a4d);
    border-top: 1px solid rgba(0, 80, 170, 60);
}}

/* Barre inferieure */
#bottom_bar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0, 17, 58, 200),
        stop:1 rgba(0, 10, 40, 230));
    min-height: 32px;
    max-height: 32px;
    border-top: 1px solid rgba(0, 80, 170, 80);
}}

#bottom_bar_text {{
    font-size: 11px;
    color: {COLORS["text_muted"]};
    padding: 0px 20px;
}}

#bottom_bar_status {{
    font-size: 11px;
    color: {COLORS["text_secondary"]};
    padding: 0px 20px;
}}

/* Pages */
#page_title {{
    font-size: 20px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 6px 0px;
    letter-spacing: 1px;
}}

#page_subtitle {{
    font-size: 12px;
    color: {COLORS["text_secondary"]};
    padding: 0px 0px 10px 0px;
}}

/* Cartes */
#status_card {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS["bg_card"]},
        stop:1 {COLORS["bg_secondary"]});
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 16px;
}}

#status_card:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS["bg_card_hover"]},
        stop:1 {COLORS["bg_card"]});
    border-color: {COLORS["ps4_highlight"]};
}}

#card_title {{
    font-size: 10px;
    color: {COLORS["text_secondary"]};
    text-transform: uppercase;
    letter-spacing: 2px;
}}

#card_value {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 4px 0px;
}}

#card_value_success {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["success"]};
    padding: 4px 0px;
}}

#card_value_warning {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["warning"]};
    padding: 4px 0px;
}}

#card_value_danger {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["danger"]};
    padding: 4px 0px;
}}

/* Boutons */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]},
        stop:1 {COLORS["accent_hover"]});
    color: #000000;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent_light"]},
        stop:1 {COLORS["accent"]});
}}

QPushButton:pressed {{
    background-color: #0099cc;
}}

QPushButton:disabled {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_muted"]};
}}

#btn_secondary {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_card"]},
        stop:1 {COLORS["bg_secondary"]});
    border: 1px solid {COLORS["border"]};
    color: {COLORS["text_primary"]};
}}

#btn_secondary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_card_hover"]},
        stop:1 {COLORS["bg_card"]});
    border-color: {COLORS["ps4_highlight"]};
}}

#btn_danger {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["danger"]},
        stop:1 {COLORS["danger_hover"]});
    color: {COLORS["text_primary"]};
}}

#btn_danger:hover {{
    background-color: {COLORS["danger"]};
}}

#btn_success {{
    background-color: {COLORS["success"]};
    color: #000000;
}}

#btn_icon {{
    background: transparent;
    border: none;
    padding: 8px;
    border-radius: 6px;
}}

#btn_icon:hover {{
    background-color: rgba(0, 212, 255, 0.15);
}}

/* Champs de saisie */
QLineEdit {{
    background-color: {COLORS["bg_input"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 10px 14px;
    color: {COLORS["text_primary"]};
    font-size: 13px;
}}

QLineEdit:focus {{
    border-color: {COLORS["ps4_highlight"]};
    background-color: {COLORS["bg_secondary"]};
}}

QLineEdit::placeholder {{
    color: {COLORS["text_muted"]};
}}

/* ComboBox */
QComboBox {{
    background-color: {COLORS["bg_input"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 10px 14px;
    color: {COLORS["text_primary"]};
    font-size: 13px;
}}

QComboBox:hover {{
    border-color: {COLORS["ps4_highlight"]};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    color: {COLORS["text_primary"]};
    selection-background-color: {COLORS["ps4_highlight"]};
    selection-color: #000000;
}}

/* Checkbox */
QCheckBox {{
    spacing: 8px;
    color: {COLORS["text_primary"]};
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid {COLORS["border"]};
    background-color: {COLORS["bg_input"]};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS["ps4_highlight"]};
    border-color: {COLORS["ps4_highlight"]};
}}

/* Zone de defilement */
QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background-color: {COLORS["scrollbar_bg"]};
    width: 6px;
    margin: 0;
    border-radius: 3px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["scrollbar_handle"]};
    min-height: 30px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["ps4_highlight"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {COLORS["scrollbar_bg"]};
    height: 6px;
    margin: 0;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["scrollbar_handle"]};
    min-width: 30px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS["ps4_highlight"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* Barre de progression */
QProgressBar {{
    background-color: {COLORS["bg_input"]};
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    color: {COLORS["text_primary"]};
    font-size: 10px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS["accent"]},
        stop:1 {COLORS["accent_light"]});
    border-radius: 6px;
}}

/* Carte de jeu */
#game_card {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_card"]},
        stop:1 {COLORS["bg_secondary"]});
    border: 2px solid {COLORS["border"]};
    border-radius: 6px;
}}

#game_card:hover {{
    border-color: {COLORS["ps4_highlight"]};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_card_hover"]},
        stop:1 {COLORS["bg_card"]});
}}

#game_title {{
    font-size: 12px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 6px 8px 2px 8px;
}}

#game_id {{
    font-size: 10px;
    color: {COLORS["text_secondary"]};
    padding: 0px 8px 6px 8px;
}}

/* Separateur */
#separator {{
    background-color: {COLORS["border"]};
    max-height: 1px;
    margin: 8px 0px;
}}

/* Labels */
#label_section {{
    font-size: 15px;
    font-weight: bold;
    color: {COLORS["ps4_highlight"]};
    padding: 12px 0px 6px 0px;
    letter-spacing: 1px;
}}

#label_field {{
    font-size: 12px;
    color: {COLORS["text_secondary"]};
    padding: 4px 0px 2px 0px;
}}

/* MessageBox */
QMessageBox {{
    background-color: {COLORS["bg_secondary"]};
}}

QMessageBox QLabel {{
    color: {COLORS["text_primary"]};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}

/* Info-bulle */
QToolTip {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["ps4_highlight"]};
    border-radius: 4px;
    padding: 6px;
    font-size: 12px;
}}

/* Dialogue fichier */
QFileDialog {{
    background-color: {COLORS["bg_secondary"]};
}}
"""

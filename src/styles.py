"""PS4-inspired dark theme stylesheets for the application."""

COLORS = {
    "bg_primary": "#0e0e1a",
    "bg_secondary": "#151528",
    "bg_card": "#1a1a35",
    "bg_card_hover": "#222250",
    "bg_sidebar": "#0a0a18",
    "bg_input": "#1e1e3e",
    "accent": "#006fff",
    "accent_hover": "#0058cc",
    "accent_light": "#1a8fff",
    "text_primary": "#ffffff",
    "text_secondary": "#8888aa",
    "text_muted": "#555577",
    "border": "#2a2a50",
    "danger": "#e74c3c",
    "danger_hover": "#c0392b",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "scrollbar_bg": "#151528",
    "scrollbar_handle": "#2a2a50",
}

MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["bg_primary"]};
}}

QWidget {{
    color: {COLORS["text_primary"]};
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}}

/* Sidebar */
#sidebar {{
    background-color: {COLORS["bg_sidebar"]};
    border-right: 1px solid {COLORS["border"]};
    min-width: 220px;
    max-width: 220px;
}}

#sidebar_title {{
    font-size: 20px;
    font-weight: bold;
    color: {COLORS["accent"]};
    padding: 20px 16px 5px 16px;
}}

#sidebar_subtitle {{
    font-size: 11px;
    color: {COLORS["text_muted"]};
    padding: 0px 16px 20px 16px;
}}

#nav_button {{
    background: transparent;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    color: {COLORS["text_secondary"]};
    margin: 2px 8px;
}}

#nav_button:hover {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
}}

#nav_button_active {{
    background-color: {COLORS["accent"]};
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    color: {COLORS["text_primary"]};
    font-weight: bold;
    margin: 2px 8px;
}}

/* Pages */
#page_container {{
    background-color: {COLORS["bg_primary"]};
}}

#page_title {{
    font-size: 26px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 10px 0px;
}}

#page_subtitle {{
    font-size: 13px;
    color: {COLORS["text_secondary"]};
    padding: 0px 0px 15px 0px;
}}

/* Cards */
#status_card {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 20px;
}}

#status_card:hover {{
    background-color: {COLORS["bg_card_hover"]};
    border-color: {COLORS["accent"]};
}}

#card_title {{
    font-size: 12px;
    color: {COLORS["text_secondary"]};
    text-transform: uppercase;
    letter-spacing: 1px;
}}

#card_value {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 5px 0px;
}}

#card_value_success {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["success"]};
    padding: 5px 0px;
}}

#card_value_warning {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["warning"]};
    padding: 5px 0px;
}}

#card_value_danger {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["danger"]};
    padding: 5px 0px;
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS["accent"]};
    color: {COLORS["text_primary"]};
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS["accent_hover"]};
}}

QPushButton:pressed {{
    background-color: #004cbf;
}}

QPushButton:disabled {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_muted"]};
}}

#btn_secondary {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
}}

#btn_secondary:hover {{
    background-color: {COLORS["bg_card_hover"]};
    border-color: {COLORS["accent"]};
}}

#btn_danger {{
    background-color: {COLORS["danger"]};
}}

#btn_danger:hover {{
    background-color: {COLORS["danger_hover"]};
}}

#btn_success {{
    background-color: {COLORS["success"]};
}}

#btn_icon {{
    background: transparent;
    border: none;
    padding: 8px;
    border-radius: 6px;
}}

#btn_icon:hover {{
    background-color: {COLORS["bg_card"]};
}}

/* Input */
QLineEdit {{
    background-color: {COLORS["bg_input"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS["text_primary"]};
    font-size: 13px;
}}

QLineEdit:focus {{
    border-color: {COLORS["accent"]};
}}

QLineEdit::placeholder {{
    color: {COLORS["text_muted"]};
}}

/* ComboBox */
QComboBox {{
    background-color: {COLORS["bg_input"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS["text_primary"]};
    font-size: 13px;
}}

QComboBox:hover {{
    border-color: {COLORS["accent"]};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    color: {COLORS["text_primary"]};
    selection-background-color: {COLORS["accent"]};
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
    background-color: {COLORS["accent"]};
    border-color: {COLORS["accent"]};
}}

/* ScrollArea */
QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background-color: {COLORS["scrollbar_bg"]};
    width: 8px;
    margin: 0;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["scrollbar_handle"]};
    min-height: 30px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["accent"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {COLORS["scrollbar_bg"]};
    height: 8px;
    margin: 0;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["scrollbar_handle"]};
    min-width: 30px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS["accent"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* Progress Bar */
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
    background-color: {COLORS["accent"]};
    border-radius: 6px;
}}

/* Game Card */
#game_card {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
}}

#game_card:hover {{
    border-color: {COLORS["accent"]};
    background-color: {COLORS["bg_card_hover"]};
}}

#game_title {{
    font-size: 13px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 8px 10px 2px 10px;
}}

#game_id {{
    font-size: 11px;
    color: {COLORS["text_secondary"]};
    padding: 0px 10px 8px 10px;
}}

/* Separator */
#separator {{
    background-color: {COLORS["border"]};
    max-height: 1px;
    margin: 10px 0px;
}}

/* Label */
#label_section {{
    font-size: 16px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    padding: 15px 0px 8px 0px;
}}

#label_field {{
    font-size: 12px;
    color: {COLORS["text_secondary"]};
    padding: 5px 0px 3px 0px;
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

/* ToolTip */
QToolTip {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 6px;
    font-size: 12px;
}}

/* FileDialog */
QFileDialog {{
    background-color: {COLORS["bg_secondary"]};
}}
"""

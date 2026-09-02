import sys
import os
import webbrowser
from datetime import datetime

from PyQt5.QtCore import Qt, QThread, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QColor, QPalette, QPainter, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QFrame, QStackedWidget, QDialog, QDialogButtonBox,
    QStyle, QTextEdit
)

import config
from config import ICON_PATH, VERSION
from translations import t
from helper_funcs.folder_cover import handler
from helper_funcs.progress import set_progress_cb, set_cancel_checker, CancelledError, report

# ------------------------------------------------------
#  THEME — "Cinema Marquee": charcoal & ivory grounds,
#  marquee gold as the single accent.
# ------------------------------------------------------
class Theme:
    dark = {
        "Window": "#0C0E12",
        "Sidebar": "#101319",
        "Card": "#13161C",
        "Base": "#191D25",
        "Text": "#E9E5D9",
        "Muted": "#8B909C",
        "Border": "#262B35",
        "HoverBg": "#1B202A",
        "ActiveBg": "#222835",
        "Primary": "#E6B84C",
        "PrimaryHover": "#F0C766",
        "OnPrimary": "#171204",
        "Track": "#1A1E27",
        "Danger": "#D97757",
    }

    light = {
        "Window": "#F1EDE2",
        "Sidebar": "#F7F4EA",
        "Card": "#FBF9F2",
        "Base": "#FFFFFF",
        "Text": "#221E15",
        "Muted": "#7A7466",
        "Border": "#DDD6C4",
        "HoverBg": "#EBE6D8",
        "ActiveBg": "#E3DCC9",
        "Primary": "#A8741F",
        "PrimaryHover": "#8F611A",
        "OnPrimary": "#FFF9EC",
        "Track": "#E7E1D2",
        "Danger": "#B4472E",
    }

    @staticmethod
    def active(app):
        return Theme.light if app.property("theme_name") == "light" else Theme.dark

    @staticmethod
    def apply(app, theme_name):
        app.setProperty("theme_name", theme_name)
        c = Theme.active(app)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(c["Window"]))
        palette.setColor(QPalette.WindowText, QColor(c["Text"]))
        palette.setColor(QPalette.Base, QColor(c["Base"]))
        palette.setColor(QPalette.Text, QColor(c["Text"]))
        palette.setColor(QPalette.Button, QColor(c["Card"]))
        palette.setColor(QPalette.ButtonText, QColor(c["Text"]))
        palette.setColor(QPalette.Highlight, QColor(c["Primary"]))
        app.setPalette(palette)

        app.setStyleSheet(f"""
            * {{
                font-family: "Segoe UI", "Vazirmatn", "Tahoma";
                font-size: 13px;
                color: {c['Text']};
            }}
            QMainWindow, QWidget#root {{ background: {c['Window']}; }}

            QFrame#sidebar {{
                background: {c['Sidebar']};
                border-right: 1px solid {c['Border']};
            }}
            QLabel#brandTitle {{
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 17px; font-weight: 700; letter-spacing: 1px;
            }}
            QLabel#brandSub {{
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 9px; font-weight: 600; letter-spacing: 4px;
                color: {c['Primary']};
            }}
            QLabel#sideLbl {{ color: {c['Muted']}; font-size: 11px; }}

            QPushButton#nav {{
                background: transparent; border: none;
                text-align: left; padding: 9px 12px;
                border-left: 3px solid transparent; border-radius: 6px;
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 13px; letter-spacing: 0.6px;
                color: {c['Muted']};
            }}
            QPushButton#nav:hover {{ background: {c['HoverBg']}; color: {c['Text']}; }}
            QPushButton#nav[active="true"] {{
                background: {c['ActiveBg']}; color: {c['Text']};
                border-left: 3px solid {c['Primary']}; font-weight: 600;
            }}

            QPushButton#seg {{
                background: transparent; border: 1px solid {c['Border']};
                border-radius: 6px; padding: 4px 10px;
                font-size: 11px; color: {c['Muted']};
            }}
            QPushButton#seg:hover {{ color: {c['Text']}; }}
            QPushButton#seg[active="true"] {{
                background: {c['ActiveBg']}; color: {c['Text']}; font-weight: 600;
            }}

            QLabel#pageTitle {{
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 24px; font-weight: 700; letter-spacing: 0.5px;
            }}
            QLabel#pageSub {{ color: {c['Muted']}; font-size: 12px; }}
            QLabel#eyebrow {{
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 10px; font-weight: 600; letter-spacing: 2px;
                color: {c['Muted']};
            }}
            QLabel#hint {{ color: {c['Muted']}; font-size: 11px; }}
            QLabel#tiny {{ color: {c['Muted']}; font-size: 10px; }}

            QFrame#card {{
                background: {c['Card']};
                border: 1px solid {c['Border']};
                border-radius: 12px;
            }}

            QLineEdit {{
                background: {c['Base']};
                border: 1px solid {c['Border']};
                border-radius: 8px;
                padding: 8px 11px;
                selection-background-color: {c['Primary']};
                selection-color: {c['OnPrimary']};
            }}
            QLineEdit:focus {{ border: 1px solid {c['Primary']}; }}
            QLineEdit:disabled {{ color: {c['Muted']}; }}

            QPushButton#primary {{
                background: {c['Primary']}; color: {c['OnPrimary']};
                border: none; border-radius: 8px; padding: 10px 20px;
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 13px; font-weight: 600; letter-spacing: 1px;
            }}
            QPushButton#primary:hover {{ background: {c['PrimaryHover']}; }}
            QPushButton#primary:disabled {{ background: {c['Track']}; color: {c['Muted']}; }}

            QPushButton#ghost {{
                background: transparent; color: {c['Text']};
                border: 1px solid {c['Border']}; border-radius: 8px; padding: 8px 16px;
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 12px; letter-spacing: 0.6px;
            }}
            QPushButton#ghost:hover {{ background: {c['HoverBg']}; }}
            QPushButton#ghost:disabled {{ color: {c['Muted']}; }}

            QPushButton#ghostDanger {{
                background: transparent; color: {c['Danger']};
                border: 1px solid {c['Border']}; border-radius: 8px; padding: 8px 16px;
                font-family: "Bahnschrift", "Segoe UI";
                font-size: 12px; letter-spacing: 0.6px;
            }}
            QPushButton#ghostDanger:hover {{ border-color: {c['Danger']}; }}
            QPushButton#ghostDanger:disabled {{ color: {c['Muted']}; }}

            QTextEdit#log {{
                background: #101318;
                border: 1px solid {c['Border']};
                border-radius: 8px;
                padding: 8px;
                color: #C9CEDA;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 12px;
            }}

            QDialog {{ background: {c['Card']}; }}
            QLabel#dlgText {{ font-size: 13px; }}
        """)

# ------------------------------------------------------
#  FILM STRIP — the progress bar: a strip of film whose
#  sprocket holes ride over the marquee-gold fill.
# ------------------------------------------------------
class FilmStrip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(14)
        self._frac = 0.0
        self._busy = False
        self._phase = 0

        self._timer = QTimer(self)
        self._timer.setInterval(28)
        self._timer.timeout.connect(self._tick)

        self._anim = QPropertyAnimation(self, b"frac")
        self._anim.setDuration(350)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    @pyqtProperty(float)
    def frac(self):
        return self._frac

    @frac.setter
    def frac(self, v):
        self._frac = v
        self.update()

    def set_progress(self, frac):
        self._busy = False
        self._timer.stop()
        self._anim.stop()
        self._anim.setStartValue(self._frac)
        self._anim.setEndValue(max(0.0, min(1.0, frac)))
        self._anim.start()

    def set_busy(self, on=True):
        self._busy = on
        if on:
            self._anim.stop()
            self._frac = 0.0
            self._phase = 0
            self._timer.start()
        else:
            self._timer.stop()
        self.update()

    def reset(self):
        self._timer.stop()
        self._anim.stop()
        self._busy = False
        self._anim.setStartValue(self._frac)
        self._anim.setEndValue(0.0)
        self._anim.start()

    def _tick(self):
        self._phase += 3
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = Theme.active(QApplication.instance())
        w, h = self.width(), self.height()

        # track
        p.setPen(QColor(c["Border"]))
        p.setBrush(QColor(c["Track"]))
        p.drawRoundedRect(0, 0, w - 1, h - 1, 7, 7)

        # fill (determinate or indeterminate sweep)
        if self._busy:
            fw = int(w * 0.28)
            period = 2 * max(1, (w - fw))
            m = self._phase % period
            x = m if m <= (w - fw) else period - m
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(c["Primary"]))
            p.drawRoundedRect(x, 0, fw, h, 7, 7)
        elif self._frac > 0:
            fw = int(w * self._frac)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(c["Primary"]))
            p.drawRoundedRect(0, 0, fw, h, 7, 7)

        # sprocket holes punched across the whole strip
        p.setBrush(QColor(c["Track"]))
        p.setPen(Qt.NoPen)
        x = 9
        while x + 7 < w:
            p.drawRoundedRect(x, (h - 5) // 2, 7, 5, 2, 2)
            x += 16

# ------------------------------------------------------
#  MODERN SWITCH (File / Folder selector)
# ------------------------------------------------------
class Switch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, checked=True):
        super().__init__()
        self.setFixedSize(44, 22)
        self._checked = checked
        self._x = 22 if checked else 4

        self.anim = QPropertyAnimation(self, b"posx")
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    @pyqtProperty(int)
    def posx(self):
        return self._x

    @posx.setter
    def posx(self, val):
        self._x = val
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(p.Antialiasing)
        c = Theme.active(QApplication.instance())
        p.setPen(QColor(c["Border"]))
        p.setBrush(QColor(c["Primary"]) if self._checked else QColor(c["Track"]))
        p.drawRoundedRect(0, 0, 43, 21, 11, 11)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(c["OnPrimary"]) if self._checked else QColor(c["Muted"]))
        p.drawEllipse(self._x, 4, 14, 14)

    def mousePressEvent(self, e):
        self._checked = not self._checked
        self.anim.stop()
        self.anim.setStartValue(self._x)
        self.anim.setEndValue(22 if self._checked else 4)
        self.anim.start()
        self.toggled.emit(self._checked)

    def isChecked(self):
        return self._checked

# ------------------------------------------------------
#  MESSAGE BOX
# ------------------------------------------------------
class CustomMessageBox(QDialog):
    def __init__(self, parent, icon, title, text):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(360)

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(28, 28))
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setObjectName("dlgText")

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        top = QHBoxLayout()
        top.addWidget(icon_label, 0, Qt.AlignTop)
        top.addSpacing(12)
        top.addWidget(text_label, 1)

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 18, 20, 14)
        main.addLayout(top)
        main.addSpacing(10)
        main.addWidget(button_box)

# ------------------------------------------------------
#  SMALL HELPERS
# ------------------------------------------------------
def eyebrow(text):
    lbl = QLabel(text)
    lbl.setObjectName("eyebrow")
    return lbl


class FieldBlock(QWidget):
    """Eyebrow label + widget (+ optional hint) in one vertical block."""
    def __init__(self, label_key, widget, hint_key=None, lang="en"):
        super().__init__()
        self.lang = lang
        self.label_key = label_key
        self.hint_key = hint_key
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)
        self.lbl = eyebrow(t(lang, label_key))
        v.addWidget(self.lbl)
        v.addWidget(widget, 1)
        self.hint = None
        if hint_key:
            self.hint = QLabel(t(lang, hint_key))
            self.hint.setObjectName("hint")
            self.hint.setWordWrap(True)
            v.addWidget(self.hint)

    def set_dynamic_hint(self, lang, key):
        self.hint_key = key
        if self.hint:
            self.hint.setText(t(lang, key))


class PathSelector(QWidget):
    def __init__(self, folder_only=False):
        super().__init__()
        self.folder_only = folder_only
        self.line = QLineEdit()
        self.line.setPlaceholderText(t("en", "ph.path"))

        self.browse = QPushButton(t("en", "btn.browse"))
        self.browse.setObjectName("ghost")
        self.browse.clicked.connect(self._select)

        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        h.addWidget(self.line, 1)

        if not folder_only:
            self.file_lbl = QLabel(t("en", "mode.file"))
            self.folder_lbl = QLabel(t("en", "mode.folder"))
            self.switch = Switch(True)
            for w in (self.file_lbl, self.switch, self.folder_lbl):
                h.addWidget(w)
            self.switch.toggled.connect(self._upd_mode_labels)
            self._upd_mode_labels(True)

        h.addWidget(self.browse)

    def _upd_mode_labels(self, is_folder):
        c = Theme.active(QApplication.instance())
        if is_folder:
            self.folder_lbl.setStyleSheet(f"color:{c['Primary']};font-weight:600;")
            self.file_lbl.setStyleSheet(f"color:{c['Muted']};")
        else:
            self.file_lbl.setStyleSheet(f"color:{c['Primary']};font-weight:600;")
            self.folder_lbl.setStyleSheet(f"color:{c['Muted']};")

    def _select(self):
        if self.folder_only or self.switch.isChecked():
            p = QFileDialog.getExistingDirectory(self, t("en", "dlg.folder"))
        else:
            p, _ = QFileDialog.getOpenFileName(self, t("en", "dlg.file"))
        if p:
            self.line.setText(p)

    def is_folder_selected(self):
        if hasattr(self, 'switch'):
            return self.switch.isChecked()
        return True

# ------------------------------------------------------
#  WORKER THREAD
# ------------------------------------------------------
class Worker(QThread):
    report = pyqtSignal(str, str, int, int)   # key, detail, current, total
    done = pyqtSignal(object)                 # result | "cancelled" | Exception

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self._stop = False

    def run(self):
        set_progress_cb(lambda k, d, cur, tot: self.report.emit(k, d, cur, tot))
        set_cancel_checker(lambda: self._stop)
        try:
            result = self.fn()
        except CancelledError:
            result = "cancelled"
        except Exception as e:
            result = e
        finally:
            set_progress_cb(None)
            set_cancel_checker(None)
        self.done.emit(result)

    def stop(self):
        self._stop = True

# ------------------------------------------------------
#  MAIN WINDOW
# ------------------------------------------------------
class MainWindow(QMainWindow):
    NAV_KEYS = ["nav.movies", "nav.series", "nav.api", "nav.about"]

    def __init__(self, lang="en"):
        super().__init__()
        self.setWindowTitle("Cover Movies")
        self.setMinimumSize(940, 660)
        self.worker = None
        self.lang = lang
        self._initial_theme = config.load_ui_prefs().get("theme", "dark")

        root = QWidget()
        root.setObjectName("root")
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._build_sidebar())

        content = QWidget()
        content_v = QVBoxLayout(content)
        content_v.setContentsMargins(28, 24, 28, 20)
        content_v.setSpacing(14)

        self.pages = QStackedWidget()
        self.page_movies = self._movies_page()
        self.page_series = self._series_page()
        self.page_api = self._api_page()
        self.page_about = self._about_page()
        for pg in (self.page_movies, self.page_series, self.page_api, self.page_about):
            self.pages.addWidget(pg)
        content_v.addWidget(self.pages, 1)

        content_v.addWidget(self._build_console())
        outer.addWidget(content, 1)
        self.setCentralWidget(root)

        self._load_api_fields()
        self._open(0, self.nav_btns[0])
        if not (config.OMDB_API_KEY and config.THEMOVIEDB_API_KEY):
            self._open(2, self.nav_btns[2])
        if self.lang != "en":
            QApplication.instance().setLayoutDirection(
                Qt.RightToLeft if self.lang == "fa" else Qt.LeftToRight)
            self.retranslate()
            self.toggle_theme(self._initial_theme)

    # ---------------------- SIDEBAR ----------------------
    def _build_sidebar(self):
        bar = QFrame()
        bar.setObjectName("sidebar")
        bar.setFixedWidth(210)
        v = QVBoxLayout(bar)
        v.setContentsMargins(16, 22, 16, 18)
        v.setSpacing(4)

        self.brand_title = QLabel("COVER MOVIES")
        self.brand_title.setObjectName("brandTitle")
        self.brand_sub = QLabel(t("en", "brand.sub"))
        self.brand_sub.setObjectName("brandSub")
        v.addWidget(self.brand_title)
        v.addWidget(self.brand_sub)
        v.addSpacing(22)

        self.nav_btns = []
        for i, key in enumerate(self.NAV_KEYS):
            btn = QPushButton(t("en", key))
            btn.setObjectName("nav")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=i, b=btn: self._open(idx, b))
            v.addWidget(btn)
            self.nav_btns.append(btn)

        v.addStretch(1)

        # theme segmented control
        self.side_theme_lbl = QLabel(t("en", "theme.label"))
        self.side_theme_lbl.setObjectName("sideLbl")
        theme_row = QHBoxLayout()
        theme_row.setSpacing(6)
        theme_row.addWidget(self.side_theme_lbl)
        theme_row.addStretch()
        self.seg_dark = QPushButton(t("en", "theme.dark"))
        self.seg_light = QPushButton(t("en", "theme.light"))
        for s in (self.seg_dark, self.seg_light):
            s.setObjectName("seg")
            s.setCursor(Qt.PointingHandCursor)
            theme_row.addWidget(s)
        self.seg_dark.clicked.connect(lambda: self.toggle_theme("dark"))
        self.seg_light.clicked.connect(lambda: self.toggle_theme("light"))
        v.addLayout(theme_row)

        # language segmented control
        self.side_lang_lbl = QLabel("Language")
        self.side_lang_lbl.setObjectName("sideLbl")
        lang_row = QHBoxLayout()
        lang_row.setSpacing(6)
        lang_row.addWidget(self.side_lang_lbl)
        lang_row.addStretch()
        self.seg_en = QPushButton("EN")
        self.seg_fa = QPushButton("فا")
        for s in (self.seg_en, self.seg_fa):
            s.setObjectName("seg")
            s.setCursor(Qt.PointingHandCursor)
            lang_row.addWidget(s)
        self.seg_en.clicked.connect(lambda: self.toggle_lang("en"))
        self.seg_fa.clicked.connect(lambda: self.toggle_lang("fa"))
        v.addLayout(lang_row)

        # ui size segmented control
        self.side_scale_lbl = QLabel(t("en", "scale.label"))
        self.side_scale_lbl.setObjectName("sideLbl")
        scale_row = QHBoxLayout()
        scale_row.setSpacing(6)
        scale_row.addWidget(self.side_scale_lbl)
        scale_row.addStretch()
        self.seg_scale_btns = {}
        for label in config.UI_SCALES:
            b = QPushButton(label)
            b.setObjectName("seg")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, s=label: self.set_ui_scale(s))
            scale_row.addWidget(b)
            self.seg_scale_btns[label] = b
        v.addLayout(scale_row)
        current = config.load_ui_prefs().get("ui_scale", "M")
        self._mark_scale(current)

        return bar

    def _open(self, index, active_btn):
        self.pages.setCurrentIndex(index)
        for b in self.nav_btns:
            b.setProperty("active", "false")
            b.style().unpolish(b)
            b.style().polish(b)
        active_btn.setProperty("active", "true")
        active_btn.style().unpolish(active_btn)
        active_btn.style().polish(active_btn)

    # ---------------------- PAGE SHELL ----------------------
    def _page_shell(self, title_key, sub_key):
        shell = QWidget()
        v = QVBoxLayout(shell)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)
        title = QLabel(t("en", title_key))
        title.setObjectName("pageTitle")
        sub = QLabel(t("en", sub_key))
        sub.setObjectName("pageSub")
        sub.setWordWrap(True)
        v.addWidget(title)
        v.addWidget(sub)
        v.addSpacing(12)
        shell._title = title
        shell._sub = sub
        shell._v = v
        return shell

    def _card(self):
        card = QFrame()
        card.setObjectName("card")
        cv = QVBoxLayout(card)
        cv.setContentsMargins(20, 18, 20, 18)
        cv.setSpacing(14)
        shell = QWidget()
        sv = QVBoxLayout(shell)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.addWidget(card)
        return shell, card, cv

    # ---------------------- PAGES ----------------------
    def _movies_page(self):
        shell = self._page_shell("movie.title", "movie.sub")

        _, card, cv = self._card()

        self.movie_path = PathSelector()
        self.movie_path_block = FieldBlock("lbl.path", self.movie_path, "hint.movie.folder")
        cv.addWidget(self.movie_path_block)

        self.movie_id = QLineEdit()
        self.movie_id.setPlaceholderText(t("en", "ph.id"))
        self.movie_id_block = FieldBlock("lbl.id", self.movie_id, "hint.id")
        cv.addWidget(self.movie_id_block)

        btn_row = QHBoxLayout()
        self.movie_btn = QPushButton(t("en", "btn.process.movie"))
        self.movie_btn.setObjectName("primary")
        self.movie_btn.setCursor(Qt.PointingHandCursor)
        self.movie_btn.clicked.connect(self.process_movie)
        self.movie_stop = self._make_stop_btn()
        btn_row.addWidget(self.movie_btn)
        btn_row.addWidget(self.movie_stop)
        btn_row.addStretch()
        cv.addLayout(btn_row)

        shell._v.addWidget(card)
        shell._v.addStretch(1)

        self.movie_path.switch.toggled.connect(self._movie_mode_changed)
        self._movie_mode_changed(True)
        return shell

    def _movie_mode_changed(self, is_folder):
        self.movie_id.setEnabled(not is_folder)
        if is_folder:
            self.movie_id.clear()
        self.movie_path_block.set_dynamic_hint(
            self.lang, "hint.movie.folder" if is_folder else "hint.movie.file")

    def _series_page(self):
        shell = self._page_shell("series.title", "series.sub")

        _, card, cv = self._card()

        self.series_path = PathSelector(folder_only=True)
        self.series_path_block = FieldBlock("lbl.path", self.series_path, "hint.series.folder")
        cv.addWidget(self.series_path_block)

        self.series_id = QLineEdit()
        self.series_id.setPlaceholderText(t("en", "ph.id"))
        self.series_id_block = FieldBlock("lbl.id", self.series_id, "hint.id")
        cv.addWidget(self.series_id_block)

        btn_row = QHBoxLayout()
        self.series_btn = QPushButton(t("en", "btn.process.series"))
        self.series_btn.setObjectName("primary")
        self.series_btn.setCursor(Qt.PointingHandCursor)
        self.series_btn.clicked.connect(self.process_series)
        self.series_stop = self._make_stop_btn()
        btn_row.addWidget(self.series_btn)
        btn_row.addWidget(self.series_stop)
        btn_row.addStretch()
        cv.addLayout(btn_row)

        shell._v.addWidget(card)
        shell._v.addStretch(1)
        return shell

    def _api_page(self):
        shell = self._page_shell("api.title", "api.sub")

        _, card, cv = self._card()

        self.omdb = QLineEdit()
        self.omdb_block = FieldBlock("lbl.omdb", self.omdb)
        cv.addWidget(self.omdb_block)

        self.tmdb = QLineEdit()
        self.tmdb_block = FieldBlock("lbl.tmdb", self.tmdb)
        cv.addWidget(self.tmdb_block)

        token_row = QWidget()
        th = QHBoxLayout(token_row)
        th.setContentsMargins(0, 0, 0, 0)
        th.setSpacing(8)
        self.token = QLineEdit()
        self.token.setEchoMode(QLineEdit.Password)
        self.token_show = QPushButton(t("en", "btn.show"))
        self.token_show.setObjectName("ghost")
        self.token_show.setFixedWidth(72)
        self.token_show.setCursor(Qt.PointingHandCursor)
        self.token_show.clicked.connect(self._toggle_token)
        th.addWidget(self.token, 1)
        th.addWidget(self.token_show)
        self.token_block = FieldBlock("lbl.token", token_row)
        cv.addWidget(self.token_block)

        btn_row = QHBoxLayout()
        self.api_save = QPushButton(t("en", "btn.save"))
        self.api_save.setObjectName("primary")
        self.api_save.setCursor(Qt.PointingHandCursor)
        self.api_save.clicked.connect(self.save_api_keys)
        self.api_test = QPushButton(t("en", "btn.test"))
        self.api_test.setObjectName("ghost")
        self.api_test.setCursor(Qt.PointingHandCursor)
        self.api_test.clicked.connect(self.test_api_keys)
        btn_row.addWidget(self.api_save)
        btn_row.addWidget(self.api_test)
        btn_row.addStretch()
        cv.addLayout(btn_row)

        shell._v.addWidget(card)

        links = QLabel('Get free keys: <a href="https://www.omdbapi.com/">omdbapi.com</a> · '
                       '<a href="https://www.themoviedb.org/">themoviedb.org</a>')
        links.setObjectName("hint")
        links.setOpenExternalLinks(True)
        shell._v.addWidget(links)
        shell._v.addStretch(1)
        return shell

    def _about_page(self):
        shell = self._page_shell("about.title", "about.sub")

        _, card, cv = self._card()

        self.about_body = QLabel(t("en", "about.body"))
        self.about_body.setWordWrap(True)
        cv.addWidget(self.about_body)

        self.about_attr = QLabel(t("en", "about.attr"))
        self.about_attr.setObjectName("tiny")
        self.about_attr.setWordWrap(True)
        cv.addWidget(self.about_attr)

        row = QHBoxLayout()
        self.about_version = QLabel(t("en", "about.version", detail=VERSION))
        self.about_version.setObjectName("hint")
        gh = QPushButton(t("en", "btn.github"))
        gh.setObjectName("ghost")
        gh.setCursor(Qt.PointingHandCursor)
        gh.clicked.connect(lambda: webbrowser.open("https://github.com/saeedsh78/cover-movies"))
        row.addWidget(self.about_version)
        row.addStretch()
        row.addWidget(gh)
        cv.addLayout(row)

        shell._v.addWidget(card)
        shell._v.addStretch(1)
        return shell

    def _toggle_token(self):
        hidden = self.token.echoMode() == QLineEdit.Password
        self.token.setEchoMode(QLineEdit.Normal if hidden else QLineEdit.Password)
        self.token_show.setText(t(self.lang, "btn.hide" if hidden else "btn.show"))

    # ---------------------- CONSOLE ----------------------
    def _build_console(self):
        card = QFrame()
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setContentsMargins(16, 12, 16, 14)
        v.setSpacing(10)

        status_row = QHBoxLayout()
        self.status_lbl = QLabel(t("en", "status.idle"))
        self.status_lbl.setObjectName("hint")
        self.counter_lbl = QLabel("")
        self.counter_lbl.setObjectName("hint")
        status_row.addWidget(self.status_lbl)
        status_row.addStretch()
        status_row.addWidget(self.counter_lbl)
        v.addLayout(status_row)

        self.film = FilmStrip()
        v.addWidget(self.film)

        self.log = QTextEdit()
        self.log.setObjectName("log")
        self.log.setReadOnly(True)
        self.log.setFixedHeight(175)
        v.addWidget(self.log)
        return card

    def _log_line(self, text, kind="normal"):
        colors = {
            "normal": "#C9CEDA",
            "muted": "#6E7686",
            "gold": "#E6B84C",
            "error": "#E08A7A",
            "info": "#7AA2F7"
        }
        color = colors.get(kind, "#C9CEDA")
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log.append(f'<span style="color:#6E7686;">{stamp}</span>&nbsp;&nbsp;<span style="color:{color};">{text}</span>')

    # ---------------------- WORKER STATE ----------------------
    def _make_stop_btn(self):
        btn = QPushButton(t("en", "btn.stop"))
        btn.setObjectName("ghostDanger")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setVisible(False)
        return btn

    def _set_running(self, running, stop_btn=None):
        self.movie_btn.setEnabled(not running)
        self.series_btn.setEnabled(not running)
        if running:
            self.film.set_busy(True)
            self.counter_lbl.setText("")
            if stop_btn:
                stop_btn.setVisible(True)
                stop_btn.setEnabled(True)
                stop_btn.setText(t(self.lang, "btn.stop"))
        else:
            self.film.set_busy(False)
            if stop_btn:
                stop_btn.setVisible(False)

    def _start_worker(self, fn, stop_btn):
        self.worker = Worker(fn)
        self.worker.report.connect(self._on_report)
        self.worker.done.connect(lambda result, sb=stop_btn: self._on_done(result, sb))
        self._set_running(True, stop_btn)
        self._log_line(t(self.lang, "log.start"), "muted")
        self.worker.start()

    def _on_done(self, result, stop_btn):
        self._set_running(False, stop_btn)
        self.worker = None
        if isinstance(result, str) and result == "cancelled":
            self._log_line(t(self.lang, "log.cancelled"), "muted")
            self.status_lbl.setText(t(self.lang, "status.cancelled"))
            self.film.reset()
        elif isinstance(result, Exception):
            text = str(result)
            if "ProxyError" in text or "Unable to connect to proxy" in text:
                self._log_line(t(self.lang, "log.proxy_error"), "error")
            else:
                self._log_line(t(self.lang, "log.error", detail=result), "error")
            self.status_lbl.setText(t(self.lang, "status.failed"))
            self.film.reset()
        else:
            self.status_lbl.setText(t(self.lang, "status.done"))

    def _on_report(self, key, detail, current, total):
        if key.startswith("status."):
            self.status_lbl.setText(t(self.lang, key, detail=detail))
            if total:
                self.counter_lbl.setText(f"{current + 1} / {total}")
                self.film.set_progress((current + 1) / total)
            return
        if key == "msg.wrong_file_t":
            self._log_line(t(self.lang, "msg.wrong_file"), "error")
        elif key == "msg.wrong_folder_t":
            self._log_line(t(self.lang, "msg.wrong_folder"), "error")
        elif key == "msg.series_dir_t":
            self._log_line(t(self.lang, "msg.series_dir"), "error")
        elif key in ("log.not_found", "log.skip_file", "log.move_fail", "log.poster_fail", "log.path_invalid", "log.no_video", "log.omdb_err", "log.tmdb_err", "log.token_err"):
            self._log_line(t(self.lang, key, detail=detail), "error")
        elif key in ("log.found", "log.icon", "log.season_poster", "log.summary", "log.saved", "log.test_result", "log.cast_saved", "log.omdb_ok", "log.tmdb_ok", "log.token_ok"):
            self._log_line(t(self.lang, key, detail=detail), "gold")
        elif key in ("log.testing_omdb", "log.testing_tmdb", "log.testing"):
            self._log_line(t(self.lang, key, detail=detail), "info")
        else:
            self._log_line(t(self.lang, key, detail=detail), "normal")

    # ---------------------- ACTIONS ----------------------
    def process_movie(self):
        if self.worker:
            return
        path = self.movie_path.line.text().strip()
        mid = self.movie_id.text().strip()
        is_folder = self.movie_path.is_folder_selected()

        if not path:
            self._msg(QMessageBox.Warning, "msg.need_path_t", "msg.need_path")
            return
        if is_folder and mid:
            self._msg(QMessageBox.Warning, "msg.wrong_folder_t", "msg.wrong_folder")
            return
        if not is_folder and not os.path.isfile(path):
            self._msg(QMessageBox.Warning, "msg.wrong_file_t", "msg.wrong_file")
            return
        kwargs = {"type_": "m"}
        if mid:
            kwargs["imdbid" if mid.startswith("tt") else "tmdbid"] = mid
        self._start_worker(lambda: handler(path, **kwargs), self.movie_stop)

    def process_series(self):
        if self.worker:
            return
        path = self.series_path.line.text().strip()
        mid = self.series_id.text().strip()
        if not path:
            self._msg(QMessageBox.Warning, "msg.need_path_t", "msg.need_path")
            return
        if not os.path.isdir(path):
            self._msg(QMessageBox.Warning, "msg.series_dir_t", "msg.series_dir")
            return
        kwargs = {"type_": "s"}
        if mid:
            kwargs["imdbid" if mid.startswith("tt") else "tmdbid"] = mid
        self._start_worker(lambda: handler(path, **kwargs), self.series_stop)

    def save_api_keys(self):
        config.change_api('omdb', api_key=self.omdb.text().strip())
        config.change_api('tmdb', api_key=self.tmdb.text().strip(), api_token=self.token.text().strip())
        config.reload_keys()
        self._log_line(t(self.lang, "log.saved"), "gold")
        self.status_lbl.setText(t(self.lang, "status.saved"))

    def test_api_keys(self):
        if self.worker:
            return
        self.api_test.setEnabled(False)
        self.api_save.setEnabled(False)
        self.status_lbl.setText(t(self.lang, "status.testing"))
        self.film.set_busy(True)
        self._log_line(t(self.lang, "log.testing"), "info")

        om_key = self.omdb.text().strip()
        tm_key = self.tmdb.text().strip()
        tm_tok = self.token.text().strip()

        def job():
            report("log.testing_omdb")
            om_ok, om_msg = config.api_test('omdb', custom_key=om_key)
            if om_ok:
                report("log.omdb_ok", om_msg)
            else:
                report("log.omdb_err", om_msg)

            report("log.testing_tmdb")
            tm_ok, tm_msg = config.api_test('tmdb', custom_key=tm_key)
            if tm_ok:
                report("log.tmdb_ok", tm_msg)
            else:
                report("log.tmdb_err", tm_msg)

            tok_ok, tok_msg = None, None
            if tm_tok:
                tok_ok, tok_msg = config.api_test('tmdb_token', custom_token=tm_tok)
                if tok_ok:
                    report("log.token_ok")
                else:
                    report("log.token_err", tok_msg)

            return om_ok, tm_ok, tok_ok

        self.worker = Worker(job)
        self.worker.report.connect(self._on_report)
        self.worker.done.connect(self._on_test_done)
        self.worker.start()

    def _on_test_done(self, result):
        self.film.reset()
        self.api_test.setEnabled(True)
        self.api_save.setEnabled(True)
        self.worker = None
        if isinstance(result, Exception):
            self.status_lbl.setText(t(self.lang, "status.failed"))
            self._log_line(t(self.lang, "log.error", detail=result), "error")
            return
        om_ok, tm_ok, tok_ok = result
        self.status_lbl.setText(t(self.lang, "status.idle"))
        self._log_line(
            t(self.lang, "log.test_result",
              om=t(self.lang, "ok" if om_ok else "invalid"),
              tm=t(self.lang, "ok" if tm_ok else "invalid")),
            "gold" if (om_ok and tm_ok) else "error")

    def _msg(self, icon_type, title_key, text_key):
        icon = self.style().standardIcon({
            QMessageBox.Information: QStyle.SP_MessageBoxInformation,
            QMessageBox.Warning: QStyle.SP_MessageBoxWarning,
            QMessageBox.Critical: QStyle.SP_MessageBoxCritical,
        }[icon_type])
        dlg = CustomMessageBox(self, icon, t(self.lang, title_key), t(self.lang, text_key))
        dlg.exec_()

    # ---------------------- THEME & LANGUAGE ----------------------
    def toggle_theme(self, name):
        Theme.apply(QApplication.instance(), name)
        prefs = config.load_ui_prefs()
        prefs["theme"] = name
        config.save_ui_prefs(prefs)
        for seg, on in ((self.seg_dark, name == "dark"), (self.seg_light, name == "light")):
            seg.setProperty("active", "true" if on else "false")
            seg.style().unpolish(seg)
            seg.style().polish(seg)
        if hasattr(self, "movie_path") and hasattr(self.movie_path, "switch"):
            self.movie_path._upd_mode_labels(self.movie_path.switch.isChecked())

    def toggle_lang(self, lang):
        self.lang = lang
        QApplication.instance().setLayoutDirection(Qt.RightToLeft if lang == "fa" else Qt.LeftToRight)
        self.retranslate()
        prefs = config.load_ui_prefs()
        prefs["lang"] = lang
        config.save_ui_prefs(prefs)
        for seg, on in ((self.seg_en, lang == "en"), (self.seg_fa, lang == "fa")):
            seg.setProperty("active", "true" if on else "false")
            seg.style().unpolish(seg)
            seg.style().polish(seg)

    # ---------------------- UI SCALE ----------------------
    def _mark_scale(self, current):
        for label, seg in self.seg_scale_btns.items():
            seg.setProperty("active", "true" if label == current else "false")
            seg.style().unpolish(seg)
            seg.style().polish(seg)

    def set_ui_scale(self, scale):
        if scale == config.load_ui_prefs().get("ui_scale", "M"):
            return
        prefs = config.load_ui_prefs()
        prefs["ui_scale"] = scale
        config.save_ui_prefs(prefs)
        self._mark_scale(scale)
        icon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
        dlg = CustomMessageBox(self, icon,
                               t(self.lang, "msg.restart_t"),
                               t(self.lang, "msg.restart"))
        dlg.exec_()

    def retranslate(self):
        L = self.lang
        self.brand_sub.setText(t(L, "brand.sub"))
        self.side_theme_lbl.setText(t(L, "theme.label"))
        self.side_lang_lbl.setText(t(L, "lang.label"))
        self.side_scale_lbl.setText(t(L, "scale.label"))
        self.seg_dark.setText(t(L, "theme.dark"))
        self.seg_light.setText(t(L, "theme.light"))

        for btn, key in zip(self.nav_btns, self.NAV_KEYS):
            btn.setText(t(L, key))

        for shell, tkey, skey in (
            (self.page_movies, "movie.title", "movie.sub"),
            (self.page_series, "series.title", "series.sub"),
            (self.page_api, "api.title", "api.sub"),
            (self.page_about, "about.title", "about.sub"),
        ):
            shell._title.setText(t(L, tkey))
            shell._sub.setText(t(L, skey))

        self.movie_path_block.lbl.setText(t(L, "lbl.path"))
        self.movie_id_block.lbl.setText(t(L, "lbl.id"))
        self.movie_id_block.hint.setText(t(L, "hint.id"))
        self.series_path_block.lbl.setText(t(L, "lbl.path"))
        self.series_path_block.hint.setText(t(L, "hint.series.folder"))
        self.series_id_block.lbl.setText(t(L, "lbl.id"))
        self.series_id_block.hint.setText(t(L, "hint.id"))
        self.omdb_block.lbl.setText(t(L, "lbl.omdb"))
        self.tmdb_block.lbl.setText(t(L, "lbl.tmdb"))
        self.token_block.lbl.setText(t(L, "lbl.token"))

        self.movie_btn.setText(t(L, "btn.process.movie"))
        self.series_btn.setText(t(L, "btn.process.series"))
        self.api_save.setText(t(L, "btn.save"))
        self.api_test.setText(t(L, "btn.test"))
        self.movie_stop.setText(t(L, "btn.stop"))
        self.series_stop.setText(t(L, "btn.stop"))
        self.token_show.setText(t(L, "btn.hide" if self.token.echoMode() == QLineEdit.Normal else "btn.show"))

        self.movie_id.setPlaceholderText(t(L, "ph.id"))
        self.series_id.setPlaceholderText(t(L, "ph.id"))
        self.movie_path.line.setPlaceholderText(t(L, "ph.path"))
        self.series_path.line.setPlaceholderText(t(L, "ph.path"))

        if hasattr(self.movie_path, "file_lbl"):
            is_folder = self.movie_path.switch.isChecked()
            self.movie_path.file_lbl.setText(t(L, "mode.file"))
            self.movie_path.folder_lbl.setText(t(L, "mode.folder"))
            self.movie_path.browse.setText(t(L, "btn.browse"))
            self._movie_mode_changed(is_folder)

        self.series_path.browse.setText(t(L, "btn.browse"))

        self.about_body.setText(t(L, "about.body"))
        self.about_attr.setText(t(L, "about.attr"))
        self.about_version.setText(t(L, "about.version", detail=VERSION))

        self.status_lbl.setText(t(L, "status.idle"))

    def _load_api_fields(self):
        self.omdb.setText(config.OMDB_API_KEY)
        self.tmdb.setText(config.THEMOVIEDB_API_KEY)
        self.token.setText(config.THEMOVIEDB_API_TOKEN.replace("Bearer ", ""))

# ------------------------------------------------------
#  RUN
# ------------------------------------------------------
def main():
    # scale + High-DPI flags must be set before QApplication exists
    prefs = config.load_ui_prefs()
    os.environ.setdefault("QT_SCALE_FACTOR",
                          config.UI_SCALES.get(prefs.get("ui_scale", "M"), "1.15"))
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    Theme.apply(app, prefs.get("theme", "dark"))
    w = MainWindow(lang=prefs.get("lang", "en"))
    w.setWindowIcon(QIcon(ICON_PATH))
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

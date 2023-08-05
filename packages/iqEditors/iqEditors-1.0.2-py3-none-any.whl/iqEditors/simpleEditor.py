# ----------------------------------------------------------------------------
# Description: iQEditor
# Project : iQLib (for iQMemo, iQNote, iQUtils)
#           https://gitflic.ru/project/nikodim/iqlib
# Date    : 17.09.2022
# Version : v 1.0.0
# Author  : KhAN (Alexander Khilchenko)
#           khan.programming@mail.ru, https://gitflic.ru/user/nikodim
# ----------------------------------------------------------------------------

import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QPushButton, QLabel, QMenu, QApplication, \
    QTextEdit, QAction, QMenu, QFileDialog, QInputDialog, QMessageBox, QDialog
from PyQt5.QtGui import QKeySequence, QSyntaxHighlighter, QFont, QColor, \
    QTextCharFormat, QTextCursor, QTextDocumentWriter, QCursor, QKeySequence, \
    QTextCharFormat, QFont, QTextCursor, QTextBlockFormat, QColor, \
    QTextDocumentWriter, QPixmap, QIcon, QDesktopServices, QTextDocument, \
    QTextBlockUserData
from PyQt5.QtCore import QRegExp, Qt, QUrl, QDir, QLockFile, QRegularExpression
# Подсветка кода
from pygments import highlight
from pygments.lexers import *
from pygments.formatter import Formatter
# Проверка синтаксиса
import enchant
from enchant import tokenize
from enchant.errors import TokenizerNotFoundError
# Модули из этой библиотеки
from iqEditors.commons import images, getImage

class iQEditor(QTextEdit):
    '''
    Текстовый редактор для форматированного текста без подсветки
    кода и орфографии
    подключение:
        from iqEditors import iQEditor
        self.editor = iQEditor()
    Обязательные параметры инициализации:
        self.MainWindow         -окно в котором находится редактор
        self.showExport = True  - если нужно отображение сохранения и експорта
    Шорткаты:
        отмена          - системно
        вернуть         - системно
        вырезать        - системно
        копировать      - системно
        вставить        - системно
        жирно           - системно
        курсив          - системно
        подчеркнуто     - системно
        ----------------------------------------------------------------------
        по левому краю  - CTRL+L
        по центру       - CTRL+C
        по правому краю - CTRL+R
        по ширине       - CTRL+J
        заголовок       - CTRL+H
        отменить формат - CTRL+ESC
        добавить отступ - CTRL+TAB
        спец блок       - CTRL+SHIFT+TAB
        вставить с форм.- CTRL+SHIFT+INS
        сохранить       - CTRL+S (системно)
        красный шрифт   - CTRL+1
        синий шрифт     - CTRL+2
        зеленый шрифт   - CTRL+3
        красный маркер  - CTRL+SHIFT+1
        синий маркер    - CTRL+SHIFT+2
        зеленый маркер  - CTRL+SHIFT+3
        заголовки (1-4) - CTRL+F1…F4
        список (нум)    - CTRL+F5
        список (марк)   - CTRL+F6
        список (марк)   - CTRL+F7
        список (марк)   - CTRL+F8
        найти следующий - F3
        найти предыдущий- SHIFT-F3
    Возможно создание нескольких экземпляров
    '''
    def __init__(self, parent=None):
        """
        Подсветка синтаксиса, проверка орфографии, поиск
        (Вложенный класс)
        """
        class Highlighter(QSyntaxHighlighter):
            # подсветка найденного
            findedText = ''
            """ 
            Подсветка только орфографии и найденного текста
            """
            # подсветка проверки орфографии
            err_format = QTextCharFormat()
            err_format.setUnderlineColor(Qt.red)
            err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            tokenizer = None
            token_filters = (tokenize.EmailFilter, tokenize.URLFilter)
            highlightingRules = []

            # формат подсветки поиска
            m_format = QTextCharFormat()
            m_format.setForeground(QColor(0,0,0))
            m_format.setBackground(QColor(255,255,0))
            m_pattern = QRegularExpression('')

            def __init__(self, parent=None):
                super(Highlighter, self).__init__(parent)

                # Инициализация подсветки проверки орфографии
                self._sp_dict = None
                self._chunkers = []
                self.setDict(enchant.Dict())

            def searchText(self,text):
                self.m_pattern = QRegularExpression(text)
                self.m_pattern.setPatternOptions(QRegularExpression.CaseInsensitiveOption)
                self.findedText = text
                # поиск без учета регистра
                self.rehighlight()

            def chunkers(self):
                return self._chunkers

            def dict(self):
                return self._sp_dict

            def setChunkers(self, chunkers):
                self._chunkers = chunkers
                self.setDict(self.dict())

            def setDict(self, sp_dict):
                try:
                    self.tokenizer = tokenize.get_tokenizer(sp_dict.tag, chunkers=self._chunkers, filters=self.token_filters)
                except TokenizerNotFoundError:
                    self.tokenizer = tokenize.get_tokenizer(chunkers=self._chunkers, filters=self.token_filters)
                self._sp_dict = sp_dict

                self.rehighlight()

            def highlightBlock(self, text):
                def spellcheckHL(text):
                    if not self._sp_dict:
                        return

                    misspellings = []
                    for (word, pos) in self.tokenizer(text):
                        if not self._sp_dict.check(word):
                            self.setFormat(pos, len(word), self.err_format)
                            misspellings.append((pos, pos + len(word)))

                    data = QTextBlockUserData()
                    data.misspelled = misspellings
                    self.setCurrentBlockUserData(data)

                # Подсветка проверки орфографии
                spellcheckHL(text)

                # Подсветка найденного текста, если установлен отбор
                matchIterator = self.m_pattern.globalMatch(text)
                while matchIterator.hasNext():
                    match = matchIterator.next()
                    self.setFormat(match.capturedStart(), match.capturedLength(), self.m_format);

                for pattern, format in self.highlightingRules:
                    expression = QRegExp(pattern)
                    index = expression.indexIn(text)
                    while index >= 0:
                        length = expression.matchedLength()
                        self.setFormat(index, length, format)
                        index = expression.indexIn(text, index + length)

        super().__init__(parent)
        if parent:
            self.MainWindow = parent
        self.statistic = {'слов':0, 'символов':0, 'без пробелов':0}
        self.filename = None
        self.showExport = False
        self.marker = {'красный шрифт':'#ff5255',
                       'синий шрифт':'#4696ff',
                       'зеленый шрифт': '#74ff4e',
                       'красный маркер':'#ff7e80',
                       'синий маркер': '#7c7cff',
                       'зеленый маркер': '#79ff77',
                       'текст под маркером':'#222222'}
        self.hightlighter = Highlighter(self.document())
        self.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextEditorInteraction | Qt.TextSelectableByMouse | Qt.TextEditable)
        self.setAcceptRichText(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)
        self.setAlignment(Qt.AlignJustify)
        self.setTabStopWidth(18)
        self.setAutoFormatting(QTextEdit.AutoAll)
        # импорт умолчаний
        self.clearedCharFormat = self.currentCharFormat()
        self.defaultTextBrush = self.clearedCharFormat.foreground()
        self.defaultBackgroundBrush = self.clearedCharFormat.background()
        self.defaultfont = self.clearedCharFormat.font()

        """Акции"""
        # Функции
        self.a_Undo = QAction(getImage('отменить'), 'Отменить', self, shortcut=QKeySequence.Undo, triggered = self.undo); self.a_Undo.setShortcutVisibleInContextMenu(True)
        self.a_Undo.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Redo = QAction(getImage('повторить'), 'Повторить', self, shortcut=QKeySequence.Redo, triggered=self.redo); self.a_Redo.setShortcutVisibleInContextMenu(True)
        self.a_Redo.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Cut = QAction(getImage('вырезать'), 'Вырезать', self, shortcut=QKeySequence.Cut, triggered=self.cut); self.a_Cut.setShortcutVisibleInContextMenu(True)
        self.a_Cut.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Copy= QAction(getImage('копировать'), 'Копировать', self, shortcut=QKeySequence.Copy, triggered=self.copy); self.a_Copy.setShortcutVisibleInContextMenu(True)
        self.a_Copy.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Paste=QAction(getImage('вставить'), 'Вставить', self, shortcut=QKeySequence.Paste, triggered=self.paste); self.a_Paste.setShortcutVisibleInContextMenu(True)
        self.a_selectAll  = QAction(getImage('выделить все'), 'Выделить все', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_5), triggered=self.set_SelectAll); self.addAction(self.a_selectAll); self.a_selectAll.setShortcutVisibleInContextMenu(True)
        self.a_selectAll.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_insertWithFormat= QAction(getImage('вставить с форматированием'), 'Вставить с форматированием', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_Insert), triggered=self.insertWithFormatting); self.addAction(self.a_insertWithFormat); self.a_insertWithFormat.setShortcutVisibleInContextMenu(True)
        self.a_insertWithFormat.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        # self.a_save = QAction(getImage('Сохранить'), 'Сохранить', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_S), triggered=self.save); self.addAction(self.a_save); self.a_save.setShortcutVisibleInContextMenu(True)
        self.a_save = QAction(getImage('Сохранить'), 'Сохранить', self, triggered=self.save); self.addAction(self.a_save); self.a_save.setShortcutVisibleInContextMenu(True)
        # self.a_save.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_saveAs   = QAction('Сохранить как...', self, triggered=self.saveAs); self.addAction(self.a_saveAs); self.a_save.setShortcutVisibleInContextMenu(True)
        self.a_i_Import = QAction(getImage('Импорт…'), 'Импорт…', self, triggered=self.importFile); self.addAction(self.a_i_Import); self.a_i_Import.setShortcutVisibleInContextMenu(True)

        # Форматирование
        self.a_Bold = QAction(getImage('жирно'), 'Жирно', self, shortcut=QKeySequence.Bold, triggered = self.set_Bold); self.addAction(self.a_Bold); self.a_Bold.setShortcutVisibleInContextMenu(True)
        self.a_Bold.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Italic = QAction(getImage('курсив'), 'Курсив', self, shortcut=QKeySequence.Italic, triggered=self.set_Italic); self.addAction(self.a_Italic); self.a_Italic.setShortcutVisibleInContextMenu(True)
        self.a_Italic.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Underline = QAction(getImage('подчеркнуто'), 'Подчеркнуто', self, shortcut=QKeySequence.Underline, triggered=self.set_Underline); self.addAction(self.a_Underline); self.a_Underline.setShortcutVisibleInContextMenu(True)
        self.a_Underline.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Center = QAction(getImage('по центру'), 'По центру', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_E), triggered=self.set_Center); self.addAction(self.a_Center); self.a_Center.setShortcutVisibleInContextMenu(True)
        self.a_Center.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Left = QAction(getImage('по левому краю'), 'По левому краю', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_L), triggered=self.set_Left); self.addAction(self.a_Left); self.a_Left.setShortcutVisibleInContextMenu(True)
        self.a_Left.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Right = QAction(getImage('по правому краю'), 'По правому краю', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_R), triggered=self.set_Right); self.addAction(self.a_Right); self.a_Right.setShortcutVisibleInContextMenu(True)
        self.a_Right.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_AllPage = QAction(getImage('по ширине страницы'), 'По ширине страницы', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_J), triggered=self.set_AllPage); self.addAction(self.a_AllPage); self.a_AllPage.setShortcutVisibleInContextMenu(True)
        self.a_AllPage.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_ClearFormat = QAction(getImage('отмена форматирования'),'Очистить форматирование', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_Escape), triggered=self.set_ClearFormat); self.addAction(self.a_ClearFormat); self.a_ClearFormat.setShortcutVisibleInContextMenu(True)
        self.a_ClearFormat.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_clearTextFont = QAction('Сбросить шрифт и цвет', self, triggered = self.clearFont)
        self.a_clearTextBlock = QAction('Сделать простым абзацем', self, triggered = self.clearBlock)

        # Печать
        self.a_i_Print      = QAction(getImage('Печать…'), 'Печать…', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_P), triggered=self.preview); self.addAction(self.a_i_Print); self.a_i_Print.setShortcutVisibleInContextMenu(True)
        self.a_i_Print.setShortcutContext(Qt.WidgetWithChildrenShortcut)

        # Вставка блоков
        self.a_NumList = QAction(getImage('нумированный список'), 'Нумерованный список', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F5),triggered = self.set_NumList); self.addAction(self.a_NumList);
        self.a_NumList.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_MarkList = QAction(getImage('маркированный список'), 'Маркированный список (точки)', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F6),triggered=self.set_MarkList); self.addAction(self.a_MarkList);
        self.a_MarkList.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_MarkList_1 = QAction(getImage('маркированный список'), 'Маркированный список (квадраты)', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F7),triggered=self.set_MarkList_1); self.addAction(self.a_MarkList_1);
        self.a_MarkList_1.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_MarkList_2 = QAction(getImage('маркированный список'), 'Маркированный список (круги)', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F8),triggered=self.set_MarkList_2); self.addAction(self.a_MarkList_2);
        self.a_MarkList_2.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_HiperLink  = QAction(getImage('гиперссылка'), 'Вставить гиперссылку', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F11),triggered=self.insert_HiperLink); self.addAction(self.a_i_HiperLink); self.a_i_HiperLink.setShortcutVisibleInContextMenu(True)
        self.a_i_HiperLink.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_Picture = QAction(getImage('картинка из файла'), 'Вставить картинку из файла', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F10),triggered=self.insert_Picture); self.addAction(self.a_i_Picture); self.a_i_Picture.setShortcutVisibleInContextMenu(True)
        self.a_i_Picture.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_HL = QAction(getImage('горизонтальная линия'), 'Вставить линию-разделитель', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F12),triggered=self.insert_HL); self.addAction(self.a_i_HL); self.a_i_HL.setShortcutVisibleInContextMenu(True)
        self.a_i_HL.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_Table = QAction(getImage('таблица'), 'Вставить таблицу', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F9),triggered=self.insert_Table); self.addAction(self.a_i_Table); self.a_i_Table.setShortcutVisibleInContextMenu(True)
        self.a_i_Table.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_SH = QAction(getImage('скриншот'), 'Вставить скриншот', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_F10), triggered=self.insert_ScreeneShot); self.addAction(self.a_i_SH); self.a_i_SH.setShortcutVisibleInContextMenu(True)
        self.a_i_SH.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_textBlock = QAction(getImage('специальный блок'), 'Преобразовать в специальный блок', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_Tab), triggered=self.set_TextBlock); self.addAction(self.a_textBlock); self.a_textBlock.setShortcutVisibleInContextMenu(True)
        self.a_textBlock.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_addMargin = QAction(getImage('добавить отступ'), 'Добавить отступ', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_Tab), triggered=self.set_addMargin); self.addAction(self.a_addMargin); self.a_addMargin.setShortcutVisibleInContextMenu(True)
        self.a_addMargin.setShortcutContext(Qt.WidgetWithChildrenShortcut)

        # заголовки
        self.a_Header1 = QAction(getImage('заголовок1'), 'Заголовок H1', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F1), triggered=self.set_Header1); self.addAction(self.a_Header1); self.a_Header1.setShortcutVisibleInContextMenu(True)
        self.a_Header1.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Header2 = QAction(getImage('заголовок2'), 'Заголовок H2', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F2), triggered=self.set_Header2); self.addAction(self.a_Header2); self.a_Header2.setShortcutVisibleInContextMenu(True)
        self.a_Header2.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Header3 = QAction(getImage('заголовок3'), 'Заголовок H3', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F3), triggered=self.set_Header3); self.addAction(self.a_Header3); self.a_Header3.setShortcutVisibleInContextMenu(True)
        self.a_Header3.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_Header4 = QAction(getImage('заголовок4'), 'Заголовок H4', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_F4), triggered=self.set_Header4); self.addAction(self.a_Header4); self.a_Header4.setShortcutVisibleInContextMenu(True)
        self.a_Header4.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        # заголовок по CTRL+H … пусть это будет №4
        self.a_Header = QAction(getImage('заголовок'), 'Заголовок', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_H), triggered=self.set_Header4); self.addAction(self.a_Header); self.a_Header.setShortcutVisibleInContextMenu(True)
        self.a_Header.setShortcutContext(Qt.WidgetWithChildrenShortcut)

        # Цвета
        self.a_redFont = QAction(getImage('красный шрифт'), 'Красный шрифт', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_1), triggered=self.set_redFont); self.addAction(self.a_redFont); self.a_redFont.setShortcutVisibleInContextMenu(True)
        self.a_redFont.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_blueFont= QAction(getImage('синий шрифт'), 'Синий шрифт', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_2), triggered=self.set_blueFont); self.addAction(self.a_blueFont); self.a_blueFont.setShortcutVisibleInContextMenu(True)
        self.a_blueFont.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_greenFont=QAction(getImage('зеленый шрифт'), 'Зеленый шрифт', self, shortcut=QKeySequence(Qt.CTRL+Qt.Key_3), triggered=self.set_greenFont); self.addAction(self.a_greenFont); self.a_greenFont.setShortcutVisibleInContextMenu(True)
        self.a_greenFont.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_redMarker = QAction(getImage('красный маркер'), 'Красный маркер', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_1), triggered=self.set_redMarker); self.addAction(self.a_redMarker); self.a_redMarker.setShortcutVisibleInContextMenu(True)
        self.a_redMarker.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_blueMarker= QAction(getImage('синий маркер'), 'Синий маркер', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_2), triggered=self.set_blueMarker); self.addAction(self.a_blueMarker); self.a_blueMarker.setShortcutVisibleInContextMenu(True)
        self.a_blueMarker.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_greenMarker=QAction(getImage('зеленый маркер'), 'Зеленый маркер', self, shortcut=QKeySequence(Qt.CTRL+Qt.SHIFT+Qt.Key_3), triggered=self.set_greenMarker); self.addAction(self.a_greenMarker); self.a_greenMarker.setShortcutVisibleInContextMenu(True)
        self.a_greenMarker.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        #  поиск
        self.a_findForward      = QAction(getImage('искать вперед'), 'Найти следующий', self, shortcut=QKeySequence(Qt.Key_F3), triggered=self.findForward);
        self.addAction(self.a_findForward)
        self.a_findForward.setShortcutVisibleInContextMenu(True)
        self.a_findForward.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_findBack      = QAction(getImage('искать назад'), 'Найти предыдущий', self, shortcut=QKeySequence(Qt.SHIFT + Qt.Key_F3), triggered=self.findBack);
        self.addAction(self.a_findBack)
        self.a_findBack.setShortcutVisibleInContextMenu(True)
        self.a_findBack.setShortcutContext(Qt.WidgetWithChildrenShortcut)

    def findForward(self):
        logging.info(f'найти следующее: {self.hightlighter.findedText}')
        text = self.hightlighter.findedText
        cursor = self.textCursor()
        text_cursor = self.document().find(text, cursor)
        if not text_cursor.isNull():
            c = self.textCursor()
            c.setPosition(text_cursor.position())
            c.setPosition(text_cursor.position()-len(text),QTextCursor.KeepAnchor)
            self.setTextCursor(c)

    def findBack(self):
        logging.info(f'найти предыдущее: {self.hightlighter.findedText}')
        text = self.hightlighter.findedText
        cursor = self.textCursor()
        text_cursor = self.document().find(text, cursor,QTextDocument.FindBackward)
        if not text_cursor.isNull():
            c = self.textCursor()
            c.setPosition(text_cursor.position())
            c.setPosition(text_cursor.position()-len(text),QTextCursor.KeepAnchor)
            self.setTextCursor(c)

    def setMainWindow(self, window):
        """
        устанавливает главное окно, которое сворачивается и разворачивается
        при вставке скриншота
        """
        self.MainWindow = window

    def setShowExport (self, value):
        self.showExport = value

    def mousePressEvent(self, e):
        super().mousePressEvent(e)  # выполнились действия в родителе (стандарт)
        # дообработка клика по ссылке
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        # дообработка клика по ссылке
        if self.anchor:
            QDesktopServices.openUrl(QUrl(self.anchor))
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None

    def importFile(self):
        import os
        # fn, format = QFileDialog.getSaveFileName(self, "Экспорт в PDF", str(Path.home()), "PDF files (*.pdf);;ODT files (*.odt);;HTML files (*.html);;MarkDown files (*.md)")
        fn, format = QFileDialog.getOpenFileName(self,'Импорт файла',str(Path.home()), "HTML files (*.html);;MarkDown files (*.md)")
        if fn:
            if format == "HTML files (*.html)":
                with open(fn,"r") as f: self.insertHtml(f.read())
            elif format == "MarkDown files (*.md)":
                with open(fn,"r") as f: self.setMarkdown(f.read())

    def saveAs(self):
        self.filename = None
        self.save()

    def save(self):
        if self.filename:
            with open(self.filename, 'w') as f: f.write(self.toHtml())
        else:
            self.export()

    def preview(self):
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.print_(printer)

    def print(self):
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if self.noteEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QPrintDialog.PrintSelection)
        dlg.setWindowTitle("Печать записки")
        if dlg.exec_() == QPrintDialog.Accepted:
            self.noteEdit.print_(printer)
        del dlg

    def exportPDF(self, fn):
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fn)
        self.document().print_(printer)

    def exportODT(self, fn):
        writer = QTextDocumentWriter(fn)
        writer.write(self.document())

    def exportHTML(self, fn):
        with open(fn,'w') as f: f.write(self.toHtml())
        self.filename = fn

    def exportMD(self, fn):
        def getText(text):
            text = text.replace("/```","```")
            text = text.replace("```/","```")
            return text

        document = QTextDocument()
        htmlText = getText(self.toHtml())
        document.setHtml(htmlText)
        with open(fn,'w') as f: f.write(document.toMarkdown())
        self.filename = fn

    def export(self):
        import os
        fn, format = QFileDialog.getSaveFileName(self, "Экспорт в PDF", str(Path.home()), "PDF files (*.pdf);;ODT files (*.odt);;HTML files (*.html);;MarkDown files (*.md)")
        if fn:
            _, ext = os.path.splitext(fn)
            if format =='PDF files (*.pdf)':
                if ext=='': fn+='.pdf'
                self.exportPDF(fn)
            if format =='ODT files (*.odt)':
                if ext == '': fn += '.odt'
                self.exportODT(fn)
            if format =='HTML files (*.html)':
                if ext == '': fn += '.html'
                self.exportHTML(fn)
            if format =='MarkDown files (*.md)':
                if ext == '': fn += '.md'
                self.exportMD(fn)

    def insertWithFormatting(self):
        self.setAcceptRichText(True)
        self.paste()
        self.setAcceptRichText(False)

    def set_redFont(self):
        color = QColor()
        color.setNamedColor(self.marker['красный шрифт'])
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_blueFont(self):
        color = QColor()
        color.setNamedColor(self.marker['синий шрифт'])
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_greenFont(self):
        color = QColor()
        color.setNamedColor(self.marker['зеленый шрифт'])
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_redMarker(self):
        color = QColor()
        t_color= QColor()
        color.setNamedColor(self.marker['красный маркер'])
        t_color= QColor()
        t_color.setNamedColor(self.marker['текст под маркером'])
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        fmt.setForeground(t_color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_blueMarker(self):
        color = QColor()
        color.setNamedColor(self.marker['синий маркер'])
        t_color= QColor()
        t_color.setNamedColor(self.marker['текст под маркером'])
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        fmt.setForeground(t_color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_greenMarker(self):
        color = QColor()
        color.setNamedColor(self.marker['зеленый маркер'])
        t_color= QColor()
        t_color.setNamedColor(self.marker['текст под маркером'])
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        fmt.setForeground(t_color)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_addMargin(self):
        fmt = QTextBlockFormat()
        fmt.setLeftMargin(60)
        fmt.setRightMargin(0)
        self.textCursor().setBlockFormat(fmt)
        fmt = QTextCharFormat()

    def set_TextBlock(self):
        fmt = QTextBlockFormat()
        fmt.setLeftMargin(120)
        fmt.setRightMargin(120)
        self.textCursor().setBlockFormat(fmt)
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.StyleItalic)
        fmt.setFontItalic(True)
        self.mergeFormatOnParaOrSelection(fmt)
        self.setAlignment(Qt.AlignJustify)

    def set_Header(self, header):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        text = cursor.selectedText()
        cursor.removeSelectedText()
        text = f"<h{header}>{text}</h{header}>"
        self.insertHtml(text)

        logging.info(f"Установлен заголовок {header}")
        self.updateEditor()

    def set_Header1(self):
        self.set_Header(1)
        self.setAlignment(Qt.AlignCenter)

    def set_Header2(self):
        self.set_Header(2)

    def set_Header3(self):
        self.set_Header(3)

    def set_Header4(self):
        self.set_Header(4)
        self.setAlignment(Qt.AlignCenter)

    def set_MarkList(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.createList(QtGui.QTextListFormat.ListDisc)
        else:
            text = cursor.selectedText()
            cursor.createList(QtGui.QTextListFormat.ListDisc)
            cursor.insertText(text)
        logging.debug("Вставлен маркированный список")

    def set_MarkList_1(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.createList(QtGui.QTextListFormat.ListSquare)
        else:
            text = cursor.selectedText()
            cursor.createList(QtGui.QTextListFormat.ListSquare)
            cursor.insertText(text)
        logging.debug("Вставлен маркированный список")

    def set_MarkList_2(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.createList(QtGui.QTextListFormat.ListCircle)
        else:
            text = cursor.selectedText()
            cursor.createList(QtGui.QTextListFormat.ListCircle)
            cursor.insertText(text)
        logging.debug("Вставлен маркированный список")


    def set_NumList(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.createList(QtGui.QTextListFormat.ListDecimal)
        else:
            text = cursor.selectedText()
            cursor.createList(QtGui.QTextListFormat.ListDecimal)
            cursor.insertText(text)
        logging.debug("Вставлен нумированный список")

    def getStatistic(self):
        # получим и обновим статистику
        words = len(self.toPlainText().split())
        self.statistic['слов']=words
        s = len(self.toPlainText())
        self.statistic['символов'] = s
        a = self.toPlainText().replace(' ', '')
        a = a.replace('\n', '')
        s = len(a)
        self.statistic['без пробелов']=s
        return self.statistic

    def mergeFormatOnParaOrSelection(self, format):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # если ничго не выделено, то работаем с текущим абзацем
            cursor.select(QTextCursor.BlockUnderCursor)
        cursor.mergeCharFormat(format)
        self.mergeCurrentCharFormat(format)

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # если ничего не выделено, то работаем с текущим словом
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.mergeCurrentCharFormat(format)

    def set_Bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_Italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(True)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_Underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(True)
        self.mergeFormatOnWordOrSelection(fmt)

    def set_Center(self):
        self.setAlignment(Qt.AlignCenter)

    def set_Left(self):
        self.setAlignment(Qt.AlignLeft)

    def set_Right(self):
        self.setAlignment(Qt.AlignRight)

    def set_AllPage(self):
        self.setAlignment(Qt.AlignJustify)

    def set_ClearFormat(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        self.setAlignment(Qt.AlignJustify)

        fmb = cursor.blockFormat()
        fmb.setHeadingLevel(0)
        fmb.setLeftMargin(0)
        fmb.setRightMargin(0)
        fmb.setForeground(self.defaultTextBrush)
        fmb.setBackground(self.defaultBackgroundBrush)
        cursor.setBlockFormat(fmb)

        fmt = QTextCharFormat()
        fmt.setAnchor(False)
        fmt.setForeground(self.defaultTextBrush)
        fmt.setBackground(self.defaultBackgroundBrush)
        fmt.setFont(self.defaultfont)
        cursor.setCharFormat(fmt)

        logging.info("Форматирование блока сброшено")
        self.updateEditor()

    def clearFont(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        self.setAlignment(Qt.AlignJustify)

        fmt = QTextCharFormat()
        fmt.setForeground(self.defaultTextBrush)
        fmt.setBackground(self.defaultBackgroundBrush)
        fmt.setFont(self.defaultfont)
        cursor.setCharFormat(fmt)

        logging.info("Форматирование блока сброшено: удалена раскраска и сброшен шрифт")
        self.updateEditor()

    def clearBlock(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        self.setAlignment(Qt.AlignJustify)

        fmb = cursor.blockFormat()
        fmb.setHeadingLevel(0)
        fmb.setLeftMargin(0)
        fmb.setRightMargin(0)
        fmb.setForeground(self.defaultTextBrush)
        fmb.setBackground(self.defaultBackgroundBrush)
        cursor.setBlockFormat(fmb)
        fmt = QTextCharFormat()
        fmt.setAnchor(False)
        cursor.setCharFormat(fmt)

        logging.info("Форматирование блока сброшено до простого текста")
        self.updateEditor()


    def updateEditor(self):
        # todo обновление редактора
        logging.info("редактор обновлен")

    def set_SelectAll(self):
        self.selectAll()

    def showMenu(self):
        """Контекстное меню"""
        clearMenu = QMenu("Очистка форматирования")
        clearMenu.addAction(self.a_ClearFormat)
        clearMenu.addSeparator()
        clearMenu.addActions([self.a_clearTextBlock, self.a_clearTextFont])
        importM= QMenu()
        importM.setTitle('Импорт…')
        importM.addAction(self.a_i_Import)
        export = QMenu()
        export.setTitle('Экспорт…')
        # export.addActions([self.a_save, self.a_saveAs])
        export.addActions([self.a_saveAs])
        subMenu = QMenu()
        subMenu.setTitle('Специальная вставка')
        subMenu.addActions([self.a_NumList, self.a_MarkList, self.a_MarkList_1, self.a_MarkList_2])
        subMenu.addSeparator()
        subMenu.addActions([self.a_i_Table, self.a_i_Picture, self.a_i_SH, self.a_i_HiperLink,  self.a_i_HL])
        selections = QMenu()
        selections.setTitle('Выделения цветом')
        selections.addActions([self.a_redFont, self.a_blueFont, self.a_greenFont])
        selections.addSeparator()
        selections.addActions([self.a_redMarker, self.a_blueMarker, self.a_greenMarker])
        p = QMenu()
        p.setTitle('Преобразования')
        p.addActions([self.a_Header1,self.a_Header2,self.a_Header3,self.a_Header4])
        p.addSeparator()
        p.addActions([self.a_NumList, self.a_MarkList, self.a_MarkList_1, self.a_MarkList_2, self.a_textBlock, self.a_addMargin])
        menu = QMenu()
        menu.addActions([self.a_Undo,self.a_Redo])
        menu.addSeparator()
        menu.addAction(self.a_Paste)
        menu.addMenu(subMenu)
        #menu.addSeparator()
        menu.addAction(self.a_insertWithFormat)
        cursor = self.textCursor()
        if cursor.hasSelection():
            menu.addActions([self.a_Copy, self.a_Cut])
            menu.addSeparator()
            menu.addActions([self.a_Bold, self.a_Italic, self.a_Underline])
            menu.addSeparator()
            menu.addActions([self.a_Left, self.a_Center, self.a_Right])
            #menu.addSeparator()
            menu.addAction(self.a_AllPage)
            menu.addSeparator()
            menu.addMenu(p)
            menu.addMenu(selections)
            menu.addSeparator()
            menu.addMenu(clearMenu)
        if self.showExport:
            menu.addSeparator()
            menu.addMenu(export)
            menu.addMenu(importM)
            menu.addAction(self.a_i_Print)
        menu.addSeparator()
        menu.addAction(self.a_selectAll)
        menu.exec(QCursor.pos())

    def insert_HL(self):
        ht = '<hr><br>'
        self.insertHtml(ht)

    def insert_HiperLink(self):
        cursor = self.textCursor()
        htmlText = ''
        if not cursor.hasSelection():
            # введем гиперссылку в диалоге
            link, ok = QInputDialog.getText(self, 'Укажите параметр',
                                            'Гиперссылка:                                                                     ')
            if ok:
                htmlText = '<a href="%s">%s</a>' % (link, link)
        else:
            link = cursor.selectedText()
            cursor.removeSelectedText()
            htmlText = '<a href="%s">%s</a>' % (link, link)
        if htmlText != '':
            self.insertHtml(htmlText)

    def insert_Table(self):
        class Dialog(QDialog):
            def __init__(self, parent=None):
                QDialog.__init__(self, parent)
                Dialog = self
                Dialog.setWindowTitle("Ввод значений")
                Dialog.setWindowFlag(Qt.Dialog)
                Dialog.resize(250, 111)
                self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
                self.verticalLayout.setContentsMargins(5, 5, 5, 5)
                self.verticalLayout.setSpacing(0)
                self.label = QtWidgets.QLabel(Dialog)
                self.verticalLayout.addWidget(self.label)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout.addItem(spacerItem)
                self.gridLayout = QtWidgets.QGridLayout()
                self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
                self.gridLayout.setSpacing(0)
                self.label_3 = QtWidgets.QLabel(Dialog)
                self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
                self.label_2 = QtWidgets.QLabel(Dialog)
                self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
                self.rows = QtWidgets.QSpinBox(Dialog)
                self.rows.setMinimum(1)
                self.gridLayout.addWidget(self.rows, 1, 1, 1, 1)
                self.cols = QtWidgets.QSpinBox(Dialog)
                self.cols.setMinimum(1)
                self.cols.setMaximum(99)
                self.gridLayout.addWidget(self.cols, 0, 1, 1, 1)
                self.verticalLayout.addLayout(self.gridLayout)
                spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout.addItem(spacerItem1)
                self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
                self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
                self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
                self.verticalLayout.addWidget(self.buttonBox)
                self.label.setText("Укажите параметры таблицы:")
                self.label_2.setText("Количество строк :")
                self.label_3.setText("Количество колонок :")
                self.rows.setValue(10)
                self.cols.setValue(3)
                self.buttonBox.accepted.connect(Dialog.accepted)
                self.buttonBox.rejected.connect(Dialog.rejected)

            def accepted(self):
                self.accept()
                self.result = [self.rows.value(),self.cols.value()]
                self.hide()

            def rejected(self):
                self.reject()
                self.hide()

        htmlText=''
        dialog = Dialog(self)
        if dialog.exec():
            row, col = dialog.result
            # так ей привычней форматирование задать, и понятней…
            htmlText += '<table align="center" width = "90%" border = "1" cellspacing="0" cellpadding="5">\n'
            for i in range(int(row)):
                htmlText += '<tr>\n'
                for j in range(int(col)):
                    htmlText += '<td></td>'
                htmlText += '</tr>\n'
            self.textCursor().insertHtml(htmlText)
            dialog.destroy()

    # картинки
    def insertBase64Image(self, filename):
        img = QtGui.QImage(filename)
        size = [img.width(), img.height()]
        ba = QtCore.QByteArray()
        buffer = QtCore.QBuffer(ba)
        buffer.open(QtCore.QIODevice.WriteOnly)
        img.save(buffer, 'PNG')
        base64_data = ba.toBase64().data()
        res = base64_data.decode("utf-8")
        return res, size

    def unicalSyffix(self):
        import datetime
        now = datetime.datetime.now()
        res = str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
        return res

    def insert_Picture(self):
        try:
            fn, _ = QFileDialog.getOpenFileName(self, "Выберите файл картинки", None,
                                                "Картинки PNG (*.png);; Картинки JPG (*.jpg);;All Files (*)")
            Base64Data, size = self.insertBase64Image(fn)
            if size[0] <= 650:
                htmltext = '<img src="data:image/png;base64, %s">' % Base64Data
            else:
                htmltext = '<img width="650" src="data:image/png;base64, %s">' % Base64Data
            self.insertHtml(htmltext)
        except AttributeError:
            logging.debug("Ошибка вставки картинки")
            logging.info(htmltext)

    def getUserPath(self):
        import subprocess
        import os.path
        return subprocess.check_output(['xdg-user-dir'])  # это путь к десктопу средствами xdg и он точный если есть сам десктоп и XDG

    # скриншот
    def insert_ScreeneShot(self):
        """
        Вставка скриншота, работает тогда, когда в реременную Mainwindow прописано
        окно в котором находится виджет (для того, чтобы было что сворачивать и разворачивать)
        """
        import os
        try:
            path = self.getUserPath().decode('utf-8')
            path= path.strip('\n')
            path = path + '/' + str(self.unicalSyffix()) + '.png'
            state = self.MainWindow.windowState()
            self.MainWindow.showMinimized()

            os.system('gnome-screenshot -a -f "' + path + '"')
            Base64Data, size = self.insertBase64Image(path)
            if size[0] <= 650:
                htmltext = '<img src="data:image/png;base64, %s /">' % Base64Data
            else:
                htmltext = '<img width="650" src="data:image/png;base64, %s /">' % Base64Data
            self.insertHtml(htmltext)
            os.system('rm "' + path + '"')
            self.MainWindow.setWindowState(state)
        except AttributeError:
            logging.error('Вставка не удалась')



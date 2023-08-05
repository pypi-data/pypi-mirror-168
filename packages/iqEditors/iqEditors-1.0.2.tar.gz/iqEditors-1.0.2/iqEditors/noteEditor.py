# ----------------------------------------------------------------------------
# Description: iQNoteEditor
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
    QTextCharFormat, QTextBlockFormat, QColor, \
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
from iqEditors import iQEditor

class iQNoteEditor(iQEditor):
    '''
    Редактор для записок iQNote's, с подсветкой орфографии и блоков кода.
    Подключение
        from iqEditors import iQNoteEditor
        self.editor = iQNoteEditor()
    Обязательны к иннициализации
        self.MainWindow - окно
        self.showExport = True/False

    Шорткаты:
        Все что есть у iQEditor +
        F5 - вставка блока кода
        F6 - вставка блока кода python
        F7 - вставка блока кода java
        F8 - вставка блока кода bash
    Возможно создание нескольких экземпляров
    '''
    def __init__(self, *args, **kwargs):
        '''подсветка синтаксиса (вложенные классы)'''
        class QFormatter(Formatter):
            """форматтер для блока кода"""
            def __init__(self):
                def hex2QColor(c):
                    r=int(c[0:2],16)
                    g=int(c[2:4],16)
                    b=int(c[4:6],16)
                    return QtGui.QColor(r,g,b)

                Formatter.__init__(self)
                self.data=[]
                self.styles={}

                for token, style in self.style:
                    qtf=QtGui.QTextCharFormat()

                    if style['color']:
                        qtf.setForeground(hex2QColor(style['color']))
                    if style['bgcolor']:
                        qtf.setBackground(hex2QColor(style['bgcolor']))
                    if style['bold']:
                        qtf.setFontWeight(QtGui.QFont.Bold)
                    if style['italic']:
                        qtf.setFontItalic(True)
                    if style['underline']:
                        qtf.setFontUnderline(True)
                    self.styles[str(token)]=qtf

            def format(self, tokensource, outfile):
                global styles
                self.data=[]
                for ttype, value in tokensource:
                    l=len(value)
                    t=str(ttype)
                    self.data.extend([self.styles[t],]*l)

        class CodeHighlighter(QSyntaxHighlighter):
            """
            класс подсветки орфографии и синтаксиса в блоке кода,
            выденном как
            /``` <лексер>
            …
            ```/
            или как
            /```
            …
            ```/
            """
            # подсветка найденного
            findedText = ''
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
                super(CodeHighlighter, self).__init__(parent)

                # Инициализация подсветки блоков кода
                self.formatter=QFormatter()
                self.textLexer = get_lexer_by_name('text')
                self.currBlockMode = ' вне блока '
                self.CBFormat = QTextCharFormat()
                self.CBFormat.setForeground(QColor(120, 120, 120))
                self.StartExpression = QRegExp("\\/```")
                self.EndExpression = QRegExp("```\\/")

                # Инициализация подсветки проверки орфографии
                self._sp_dict = None
                self._chunkers = []
                self.setDict(enchant.Dict())

                # Правило подсветки комментариев, заключенных в кавычки
                # ковычки (стринги)
                quotationFormat = QTextCharFormat()
                quotationFormat.setForeground(QColor(120, 120, 120))
                self.highlightingRules.append((QRegExp("\".*\""), quotationFormat)) # для "…"
                self.highlightingRules.append((QRegExp("\'.*\'"), quotationFormat)) # для '…'
                self.highlightingRules.append((QRegExp("`.*`"),   quotationFormat))   # для `…`

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
                def getBlockMode(text):
                    text = text.replace('/``` ','')
                    text = text.replace('\n','')
                    return text

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

                self.setCurrentBlockState(0)
                startIndex = 0
                if self.previousBlockState() != 1:
                    startIndex = self.StartExpression.indexIn(text)

                # определим лексер для подсветки кода в блоке /``` … ```/ и его формат
                if text[:4]=='/```':
                    self.currBlockMode = getBlockMode(text)
                elif (text[:4]!='/```' and self.previousBlockState() != 1):
                    self.currBlockMode = ' вне блока '

                ## тут возможны три варианта значения self.currBlockMode:
                ##  '/```' — это значит что нужно просто подкрасить блок в тексте
                ##  ' вне блока ' — это значит что ничего не нужно делать
                ##  'строка' - где строка есть среди лексеров

                # получим лексер текущего блока
                try:
                    lexer = get_lexer_by_name(self.currBlockMode)
                except BaseException:
                    lexer = self.textLexer

                # Подсветка проверки орфографии
                spellcheckHL(text)

                # Подсветка найденного текста, если установлен отбор
                matchIterator = self.m_pattern.globalMatch(text)
                while matchIterator.hasNext():
                    match = matchIterator.next()
                    self.setFormat(match.capturedStart(), match.capturedLength(), self.m_format);

                # Подсветка по правилам
                # fixit: подсветка по правилам
                for pattern, format in self.highlightingRules:
                    expression = QRegExp(pattern)
                    index = expression.indexIn(text)
                    while index >= 0:
                        length = expression.matchedLength()
                        self.setFormat(index, length, format)
                        index = expression.indexIn(text, index + length)

                # закончим разбор блока до его окончания и раскрасим его
                while startIndex >= 0:
                    endIndex = self.EndExpression.indexIn(text, startIndex)

                    if endIndex == -1:
                        self.setCurrentBlockState(1)
                        BlockLength = len(text) - startIndex
                    else:
                        BlockLength = endIndex - startIndex + self.EndExpression.matchedLength()

                    # раскраска, собственно
                    if lexer==self.textLexer:
                        self.setFormat(startIndex, BlockLength, self.CBFormat)
                    else:
                        cb = self.currentBlock()
                        p = cb.position()
                        highlight(text,lexer,self.formatter)
                        for i in range(len(text)):
                            self.setFormat(i,1,self.formatter.data[i])

                    # окончание блока
                    startIndex = self.StartExpression.indexIn(text, startIndex + BlockLength);

        # -- тело класса редактора --------------------------------------------
        super().__init__()
        self.setAcceptDrops(True)
        self.filepath = None
        # self.restoreMainWindow = None
        self.MainWindow=None
        self.hightlighter = CodeHighlighter(self.document())

        """Акции"""
        # с хоткеями
        self.a_i_CodeBlock      = QAction(getImage('блок кода'), 'Блок кода', self, shortcut=QKeySequence(Qt.Key_F5), triggered=self.insert_CodeBlock);
        self.addAction(self.a_i_CodeBlock); self.a_i_CodeBlock.setShortcutVisibleInContextMenu(True)
        self.a_i_CodeBlock.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_CodeBlockPy    = QAction(getImage('блок кода python'), 'Блок кода (python)', self, shortcut=QKeySequence(Qt.Key_F6), triggered=self.insert_CodeBlockPy);
        self.addAction(self.a_i_CodeBlockPy); self.a_i_CodeBlockPy.setShortcutVisibleInContextMenu(True)
        self.a_i_CodeBlockPy.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_CodeBlockJava  = QAction(getImage('блок кода java'), 'Блок кода (java)', self, shortcut=QKeySequence(Qt.Key_F7), triggered=self.insert_CodeBlockJava);
        self.addAction(self.a_i_CodeBlockJava); self.a_i_CodeBlockJava.setShortcutVisibleInContextMenu(True)
        self.a_i_CodeBlockJava.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.a_i_CodeBlockBash      = QAction(getImage('блок кода bash'), 'Блок кода (bash)', self, shortcut=QKeySequence(Qt.Key_F8), triggered=self.insert_CodeBlockBash);
        self.addAction(self.a_i_CodeBlockBash); self.a_i_CodeBlockBash.setShortcutVisibleInContextMenu(True)
        self.a_i_CodeBlockBash.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        # без хоткея
        self.a_i_HtmlCode       = QAction(getImage('HTML код'), 'Вставить HTML код', self, triggered=self.insert_HtmlCode); self.addAction(self.a_i_HtmlCode); self.a_i_HtmlCode.setShortcutVisibleInContextMenu(True)

    def codeBlockGenerate(self, type=''):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            text = f"/``` {type}\n\n```/"
            cursor.insertText(text)
            cursor.movePosition(QTextCursor.Up,n=1)
            self.setTextCursor(cursor)
        else:
            selectedText = cursor.selectedText()
            text = f"/``` {type}\n{selectedText}\n```/"
            cursor.insertText(text)
        logging.debug(f"вставлен блок кода {type}")

    def insert_CodeBlock(self):
        self.codeBlockGenerate()

    def insert_CodeBlockPy(self):
        self.codeBlockGenerate('python')

    def insert_CodeBlockJava(self):
        self.codeBlockGenerate('java')

    def insert_CodeBlockBash(self):
        self.codeBlockGenerate('bash')

    def insert_HtmlCode(self):
        """вставка html кода"""
        id = QInputDialog(self)
        id.setWindowTitle('Ввод готового html кода')
        id.setLabelText('Вставьте html код (лучше всего из буфера обмена):')
        id.resize(500,20) # но высота ставится потом по размеру вывода
        id.exec()
        text =id.textValue()
        t=f'<div>{text}</div>'
        self.insertHtml(t)

    def setHighlighting(self, val: bool):
        if val:
            self.hightlighter.setDocument(self.document())
        else:
            self.hightlighter.setDocument(None)

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
        subMenu.addActions([self.a_i_CodeBlock, self.a_i_CodeBlockPy, self.a_i_CodeBlockJava, self.a_i_CodeBlockBash])
        subMenu.addSeparator()
        subMenu.addActions([self.a_i_Table, self.a_i_Picture, self.a_i_SH, self.a_i_HiperLink,  self.a_i_HL])
        subMenu.addSeparator()
        subMenu.addAction(self.a_i_HtmlCode)
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

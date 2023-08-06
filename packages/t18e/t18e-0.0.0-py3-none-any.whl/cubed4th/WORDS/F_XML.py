#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

     _           _    _____    ____    _   _
  /\| |/\       | |  / ____|  / __ \  | \ | |
  \ ` ' /       | | | (___   | |  | | |  \| |
 |_     _|  _   | |  \___ \  | |  | | | . ` |
  / , . \  | |__| |  ____) | | |__| | | |\  |
  \/|_|\/   \____/  |_____/   \____/  |_| \_|



)







"""  # __banner__


class LIB:  # { JavaScript Object Notation : words }

    """

    T{ ("Hello World") -> 'Hello ''World + }T

    """

    def __init__(self, e, t, **kwargs):
        pass

    @staticmethod
    def load(e):
        return (e.root.memory.get('<xml>', []), e.root.memory.get('<xml_stack>', []))

    @staticmethod
    def save(e, xml, xml_stack):
        e.root.memory['<xml>'] = xml
        e.root.memory['<xml_stack>'] = xml_stack


    @staticmethod  ### <!tag ###
    def sigil_langle_bang__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = ' '.join(token.split("'"))
        xml.append(token)
        LIB.save(e, xml, xml_stack)


    @staticmethod  ### <<tag ###
    def sigil_langle_langle__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = ' '.join(token[2:].split("'"))
        if token[-1] == '>': token = token[:-1]
        if not token.lower() in ['textarea']: xml.append('  '*len(xml_stack))
        xml.append('<' + token + '>')
        token = token.split(' ')[0]
        if not token.lower() in ['td', 'textarea']: xml.append("\n")
        if not token.lower() in []: xml_stack.append(token)
        LIB.save(e, xml, xml_stack)

    @staticmethod  ### }<<tag ###
    def sigil_rbrace_langle_langle__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = ' '.join(token[3:].split("'"))
        if token[-1] == '>': token = token[:-1]
        values = t.stack.pop()
        for k in values.keys():
            if not token[-1] == ' ':
                token = token + ' '
            token = token + k + '="' + values[k] + '"'
        if not token.lower() in ['textarea']: xml.append('  '*len(xml_stack))
        xml.append('<' + token + '>\n')
        token = token.split(' ')[0]
        if not token.lower() in ['td','textarea']: xml.append("\n")
        xml_stack.append(token)
        LIB.save(e, xml, xml_stack)


    @staticmethod  ### <</tag ###
    def sigil_langle_langle_divide__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = ' '.join(token[3:].split("'"))
        if not token.lower() in ['td', 'br', 'textarea']: xml.append('  '*len(xml_stack))
        xml.append('<' + token + ' />')
        token = token.split(' ')[0]
        if not token.lower() in ['td', 'br']: xml.append("\n")
        LIB.save(e, xml, xml_stack)

    @staticmethod  ### /> ###
    def sigil_divide_rangle__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = xml_stack.pop()
        if not token.lower() in ['td', 'textarea']: xml.append('  '*len(xml_stack))
        xml.append('</' + token + '>')
        xml.append('\n')
        LIB.save(e, xml, xml_stack)

    @staticmethod  ### </ ###
    def sigil_langle_divide__R(e, t, c, token, start):
        xml, xml_stack = LIB.load(e)
        token = xml_stack.pop()
        if not token.lower() in ['td', 'textarea']: xml.append('  '*len(xml_stack))
        xml.append('</' + token + '>')
        xml.append('\n')
        LIB.save(e, xml, xml_stack)



    @staticmethod  ### <XML> ###
    def word_langle_XML_rangle__R(e, t, c, s):
        e.root.memory['<xml>'] = []
        e.root.memory['<xml_stack>'] = []

    @staticmethod  ### <TXT> ###
    def word_langle_TXT_rangle__R(e, t, c, s):
        xml, xml_stack = LIB.load(e)
        xml.append(s)
        LIB.save(e, xml, xml_stack)

    @staticmethod  ### <ESC> ###
    def word_langle_ESC_rangle__R(e, t, c, s):
        xml, xml_stack = LIB.load(e)
        xml.append(str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("'", "&#x27;").replace("`", "&#x60;"))
        LIB.save(e, xml, xml_stack)

    @staticmethod  ### <!-- ###
    def sigil_langle_bang_minus_minus(e, t, c, token, start=False):
        """
        """
        if isinstance(token, str) and len(token) and token[-3:] == "-->":
            t.state = e.state_INTERPRET
            return

        t.state = LIB.sigil_langle_bang_minus_minus







###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re


class ClassifyByLineNo:
    """
    Helper to set specific class for groups of lines in TableizeLine.
    """

    def __init__(self, range_classes):
        self.range_classes = list(range_classes)

    def __call__(self, line_no):
        for (begin, end), css in self.range_classes:
            if line_no >= begin and line_no < end:
                return css
        return None


# cached regular expression to find ANSI color codes
COLCODE_RE = re.compile("\x1b\\[([0-9;]*m|[012]?K)")


class ANSIStyle:
    __slots__ = ("style", "color", "bgcolor")

    def __init__(self, style=0, color=0, bgcolor=0):
        self.style = style
        self.color = color
        self.bgcolor = bgcolor
        if isinstance(style, str):
            self.style = 0
            self.apply_code(style)

    def apply_code(self, code):
        """
        >>> ANSIStyle(1, 2, 3).apply_code('0')
        ANSIStyle(style=0, color=0, bgcolor=0)
        >>> ANSIStyle().apply_code('1;34')
        ANSIStyle(style=1, color=4, bgcolor=0)
        >>> ANSIStyle().apply_code('45')
        ANSIStyle(style=0, color=0, bgcolor=5)
        """
        if not code or code == "0":
            self.style = self.color = self.bgcolor = 0
        else:
            for subcode in [int(x, 10) for x in code.split(";")]:
                if subcode >= 40:
                    self.bgcolor = subcode - 40
                elif subcode >= 30:
                    self.color = subcode - 30
                else:
                    self.style = subcode
        return self

    def copy(self):
        return ANSIStyle(self.style, self.color, self.bgcolor)

    def code(self, base=None):
        if (self.style, self.color, self.bgcolor) == (0, 0, 0):
            return ""
        if not base:
            base = ANSIStyle()
        if self == base:
            return self.code()  # prevent a no change to become a reset
        codes = []
        if self.style != base.style:
            codes.append(str(self.style))
        if self.color != base.color:
            codes.append(str(30 + self.color))
        if self.bgcolor != base.bgcolor:
            codes.append(str(40 + self.bgcolor))
        return ";".join(codes)

    def css(self, base=None):
        """
        CSS class(es) for the current text style.

        >>> ANSIStyle().css()
        ''
        >>> ANSIStyle('1;32;43').css()
        'xterm-style-1 xterm-color-2 xterm-bgcolor-3'
        """
        if (self.style, self.color, self.bgcolor) == (0, 0, 0):
            return ""
        if not base:
            base = ANSIStyle()
        codes = []
        for key in self.__slots__:
            if getattr(self, key) != getattr(base, key):
                codes.append("xterm-{}-{}".format(key, getattr(self, key)))
        return " ".join(codes)

    def __repr__(self):
        return "ANSIStyle({})".format(
            ", ".join(
                "{}={!r}".format(key, getattr(self, key)) for key in self.__slots__
            )
        )

    def __eq__(self, other):
        return (
            isinstance(
                other,
                ANSIStyle,
            )
            and (self.style, self.color, self.bgcolor)
            == (other.style, other.color, other.bgcolor)
        )


class ANSI2HTML:
    """
    Class to convert ANSI codes into HTML classes.
    """

    def __init__(self, start_style=""):
        self.current_style = (
            start_style
            if isinstance(start_style, ANSIStyle)
            else ANSIStyle(start_style)
        )

    def _process(self, line):
        # we record and strip the newline format at end of line not to include
        # it in the formatting
        if line.endswith("\n"):
            newline = "\n"
            line = line[:-1]
        elif line.endswith("\r\n"):
            newline = "\r\n"
            line = line[:-2]
        else:
            newline = ""

        # special handling of styles at beginning of line
        m = COLCODE_RE.match(line)
        while m:
            line = line[m.end() :]
            if m.group(1).endswith("m"):
                self.current_style.apply_code(m.group(1)[:-1])
            m = COLCODE_RE.match(line)

        current_class = self.current_style.css()
        if current_class:
            yield '<span class="{}">'.format(current_class)
        else:
            yield "<span>"

        pos = 0
        while True:
            # look for a control sequence
            m = COLCODE_RE.search(line, pos)
            if not m:
                # no more codes to convert
                break
            # pass the chars so far
            if m.start() != pos:
                yield line[pos : m.start()]
            # parse the new code
            if m.group(1).endswith("m"):
                self.current_style.apply_code(m.group(1)[:-1])
                next_class = self.current_style.css()
            else:
                next_class = current_class

            if next_class != current_class:
                # we have a change, close previous span, open the new one
                yield '</span><span class="{}">'.format(next_class)
                current_class = next_class
            pos = m.end()  # update offset to end of control code

        if pos < len(line):  # flush what remains of the line
            yield line[pos:]
        yield "</span>" + newline  # close the global <span>

    def __call__(self, line):
        """
        Add HTML span tags for ansi colors.
        """
        return "".join(self._process(line))


class TableizeLine:
    """
    Add table row tags and optionally line numbers to lines.
    """

    def __init__(
        self, first_line_no=1, line_id_prefix="L", add_line_nos=False, row_class=None
    ):
        self.line_no = first_line_no

        line_format = '<tr id="{prefix}{{n}}"{{class_desc}}><td>'
        if add_line_nos:
            line_format += '<a href="#{prefix}{{n}}">{{n}}</a></td><td>'
        line_format += "{{text}}</td></tr>"

        if row_class is None or isinstance(row_class, str):
            self.row_class = lambda n: row_class
        else:
            self.row_class = row_class

        self._line_format = line_format.format(prefix=line_id_prefix)

    def __call__(self, line):
        """
        Add HTML tags.
        """
        # we record and strip the newline format at end of line not to include
        # it in the formatting
        if line.endswith("\n"):
            newline = "\n"
            line = line[:-1]
        elif line.endswith("\r\n"):
            newline = "\r\n"
            line = line[:-2]
        else:
            newline = ""

        css = self.row_class(self.line_no)
        class_desc = ' class="{}"'.format(css) if css else ""

        out = (
            self._line_format.format(n=self.line_no, class_desc=class_desc, text=line)
            + newline
        )
        self.line_no += 1
        return out


class WrapLine:
    """
    Wrap a line in HTML tags.
    """

    def __init__(self, tag, attrs={}):
        self._line_format = "<{tag}{attrs}>{{text}}</{tag}>".format(
            tag=tag,
            attrs=""
            if not attrs
            else " "
            + " ".join('{0}="{1}"'.format(item) for item in list(attrs.items())),
        )

    def __call__(self, line):
        """
        Add HTML tags.
        """
        # we record and strip the newline format at end of line not to include
        # it in the formatting
        if line.endswith("\n"):
            newline = "\n"
            line = line[:-1]
        elif line.endswith("\r\n"):
            newline = "\r\n"
            line = line[:-2]
        else:
            newline = ""
        return self._line_format.format(text=line) + newline

from .common import check_arg
import ldmud

def do_wrap(text, maxlen, firstindent, followindent):
    firstline = True            # Whether this is the first line
    count = 0                   # Used size in the current line
    result = ''                 # Result string (all lines)

    space = ' ' * firstindent   # Spaces before the current word.
    word = ''                   # The current word (all non-space characters)
    wordsize = 0                # The size of the current word
    escapeseq = 0               # Is an escape sequence being parsed?
                                #  0: No escape sequence
                                #  1: Just the ESC character (-> word)
                                #  2: CSI sequence started

    # The following always holds:
    #   count + len(space) + wordsize <= maxlen
    #   len(word) >= wordsize

    def do_add_word():
        nonlocal result, count, space, word, wordsize

        result += space + word
        count += len(space) + wordsize
        space = ''
        word = ''
        wordsize = 0

    def do_line_break(ch = '\n'):
        nonlocal result, count, firstline, space

        result += ch
        count = 0
        firstline = False
        space = ' ' * followindent

    for ch in text:
        if ch == '\n' or ch == '\r':
            do_add_word()
            do_line_break(ch)
            firstline = True
        elif ch == ' ':
            if wordsize:
                do_add_word()
                if count == maxlen:
                    do_line_break()
            else:
                if count + len(space) == maxlen:
                    do_add_word()
                    do_line_break()
                elif count > 0 or firstline:
                    do_add_word()

            if count > 0 or firstline:
                space += ch
        elif ch == '\x1b':
            word += ch
            escapeseq = 1
        elif escapeseq == 1:
            word += ch
            if ch == '[':
                escapeseq = 2
            else:
                escapeseq = 0
        elif escapeseq == 2:
            word += ch
            if ch.isalpha():
                escapeseq = 0
        else:
            if count + wordsize + len(space) == maxlen:
                if count == 0:
                    do_add_word()
                else:
                    space = ''
                do_line_break()

            word += ch
            wordsize += 1

    if len(word) or count:
        do_add_word()
        do_line_break()

    return result

def efun_wrap(text: str, maxlen: int = 0, left: int = 0) -> str:
    """
    SYNOPSIS
            string wrap(string text [, int len [, int left]])

    DESCRIPTION
            Line-wraps the given text at the column <len> (default: 75). All
            lines will be indented by <left> characters (default: 0).

    SEE ALSO
            wrap_say(E), left(E)
    """
    if text:
        check_arg("wrap()", 1, text, str)
    check_arg("wrap()", 2, maxlen, int)
    check_arg("wrap()", 3, left, int)

    if not text:
        return text

    if maxlen < 1:
        maxlen = 75
    if left >= maxlen or left < 0:
        left = 0

    return do_wrap(text, maxlen, left, left)

def efun_wrap_say(text1: str, text2: str, maxlen: int = 0, left: int = 0):
    """
    SYNOPSIS
            string wrap_say(string intro, string text [, int len [, int left]])

    DESCRIPTION
            Concatenates <intro> and <text> with a whitespace and line-wraps the
            result at column <len> (default: 75). The second and following lines
            will be indented by <left> characters.

    EXAMPLES
            wrap_say("Monty says:", "blablabla blablabla...");

            ->
            Monty says: blablabla blablabla blablabla blablabla blablabla blablabla
                    blablabla blablabla blablabla blablabla blablabla blablabla
                    blablabla blablabla ...

    SEE ALSO
            wrap(E), left(E)
    """
    check_arg("wrap_say()", 1, text1, str)
    check_arg("wrap_say()", 2, text2, str)
    check_arg("wrap_say()", 3, maxlen, int)
    check_arg("wrap_say()", 4, left, int)

    if maxlen < 1:
        maxlen = 75
    if left >= maxlen or left < 1:
        left = 8
        if left >= maxlen:
            left = (maxlen - 1) // 2

    if not text2:
        return do_wrap(text1, maxlen, 0, left)

    return do_wrap(text1 + " " + text2, maxlen, 0, left)

def efun_left(text: (str,int,), size: int, pad: str = " ") -> str:
    """
    SYNOPSIS
            string left(string text, int len [,string pattern])

    DESCRIPTION
            Returns a string of length <len> with the given <text> left-aligned.
            If the text is shorter it will be padded with <pattern>, which is a
            whitespace per default. If the text is longer it will be cut.
            ANSI escape sequences don't count as a character.

    EXAMPLES
            left("abc d", 8)          -> "abc d   "
            left("abc d", 8, ".")     -> "abc d..."
            left("abc def ghi", 8)    -> "abc def "

    SEE ALSO
            wrap(E), wrap_say(E)
    """
    if isinstance(text, int):
        if text == 0:
            return ""
        text = "%d" % (text,)
    check_arg("left()", 1, text, str)
    check_arg("left()", 2, size, int)
    check_arg("left()", 3, pad, str)

    if not len(pad):
        raise ValueError("Null pad string specified.")

    if '\x1b' in pad:
        raise ValueError("Pad string contains escape sequence.")

    count = 0
    result = ''
    escapeseq = 0

    def add_word(word):
        nonlocal count, result, escapeseq
        for ch in word:
            if count >= size:
                break

            if ch == '\x1b':
                result += ch
                escapeseq = 1
            elif escapeseq == 1:
                result += ch
                if ch == '[':
                    escapeseq = 2
                else:
                    escapeseq = 0
            elif escapeseq == 2:
                result += ch
                if ch.isalpha():
                    escapeseq = 0
            else:
                result += ch
                count += 1

    add_word(text)
    escapeseq = 0
    while count < size:
        add_word(pad)

    return result

def register():
    ldmud.register_efun("wrap", efun_wrap)
    ldmud.register_efun("wrap_say", efun_wrap_say)
    ldmud.register_efun("left", efun_left)

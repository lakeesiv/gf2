"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import sys


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        try:
            self.file = open(path, "r")
        except FileNotFoundError:
            raise Exception("Input file not found")
        self.names = names
        self.symbol_list = [self.HEADING, self.LOGIC, self.NUMBER, self.NAME,
                            self.EQUAL, self.DOT, self.COMMA, self.SEMICOLON,
                            self.OPEN_BRACKET, self.CLOSE_BRACKET, self.HASHTAG, self.EOF] = range(12)
        self.heading_list = ["[devices]", "[conns]", "[monit]"]
        [self.DEVICES_ID, self.CONNS_ID, self.MONIT_ID] = self.names.lookup(self.heading_list)
        self.logic_list = ["DTYPE", "NAND", "NOR", "XOR", "AND", "OR", "CLOCK", "SWITCH"]
        [self.DTYPE_ID, self.NAND_ID, self.NOR_ID, self.XOR_ID, 
        self.AND_ID, self.OR_ID, self.CLOCK_ID, self.SWITCH_ID] = self.names.lookup(self.logic_list)
        
        self.current_character = ""
        self.current_position = 0
        self.current_line = 0
        self.error_count = 0

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace

        if self.current_character.isalpha():  # Names
            name_string = self.get_name()
            self.name_string = name_string[0]
            if self.name_string in self.heading_list:
                symbol.type = self.HEADING
            elif self.name_string in self.logic_list:
                symbol.type = self.LOGIC
            else:
                symbol.type = self.NAME
            [symbol.id] = self.names.lookup([self.name_string])
        
        elif self.current_character.isdigit():  #Numbers
            symbol.id = self.get_number()
            symbol.type = self.NUMBER
            self.advance()
            
        elif self.current_character == "=":  #Definitions
            symbol.type = self.EQUAL
            self.advance()

        elif self.current_character == ".":  #Connections
            symbol.type = self.DOT
            self.advance()

        elif self.current_character == ",":  #Punctuations
            symbol.type = self.COMMA
            self.advance()

        elif self.current_character == ";":  #Punctuations
            symbol.type = self.SEMICOLON
            self.advance()

        elif self.current_character == "(":  #Inputs No.
            symbol.type = self.OPEN_BRACKET
            self.advance()

        elif self.current_character == ")":  #Inputs No.
            symbol.type = self.CLOSE_BRACKET
            self.advance()

        elif self.current_character == "#":  #Comments
            symbol.type = self.HASHTAG
            self.advance()
            while self.current_character != "\n":
                self.advance()

        elif self.current_character == "":   #End of file
            symbol.type = self.EOF
            self.advance()

        else:  #Not a valid character
            self.error(SyntaxError, "Character not valid")
            
        self.current_position += 1
        return symbol

    def get_name(self):
        """Return the name and the next character that is non-alphanumeric"""
        name = ""
        while self.current_character.isalnum() or self.current_character == "[" or self.current_character == "]":
            name += self.current_character
            self.advance()
        return [name, self.current_character]

    def get_number(self):
        """Return the numbers in the file and the next character"""
        number = ""
        while self.current_character.isdigit():
            number += self.current_character
            self.advance()
        return [int(number), self.current_character]

    def skip_spaces(self):
        """Skip all the spaces in the file"""
        while self.current_character.isspace():
            self.advance()

    def advance(self):
        """Advance to the next character in the file"""
        try:
            self.current_character = self.file.read(1)
        except FileNotFoundError:
            raise Exception("Input file not found")
        if self.current_character == "\n":  # End of line actions
            self.current_line += 1
            self.current_position = 0
        else:
            self.current_position += 1
        return self.current_character
   
    def get_current_line(self):
        """Return the current line from the file"""
        line = ""
        current_position = self.file.tell()
        self.file.seek(0)
        for _ in range(self.current_line + 1):
            line = self.file.readline()
        self.file.seek(current_position)
        return line
    
    def error(self, error_type, message):
        """Error handling method"""
        self.error_count += 1
        print(f"Error {self.error_count} - {error_type.__name__}: {message}")
        print(f"Line {self.current_line}: {self.get_current_line()}")
        print(" " * (self.current_position + 6) + "^")  # Marker to indicate the error position
        

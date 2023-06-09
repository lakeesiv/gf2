"""Map variable names and string names to unique integers.

Used in the Logic Simulator project. Most of the modules in the project
use this module either directly or indirectly.

Classes
-------
Names - maps variable names and string names to unique integers.
"""


from typing import List


class Names:

    """Map variable names and string names to unique integers.

    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
                                               error codes.

    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        """Initialise names list."""
        self.error_code_count = 0  # how many error codes have been declared
        self.names = []

    def unique_error_codes(self, num_error_codes):
        """Return a list of unique integer error codes."""
        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")
        self.error_code_count += num_error_codes
        return range(
            self.error_code_count - num_error_codes,
            self.error_code_count)

    def query(self, name_string):
        """Return the corresponding name ID for name_string.

        If the name string is not present in the names list, return None.
        """

        # First check if it is string
        if not isinstance(name_string, str):
            raise TypeError("The name must be a string")

        if name_string.isdigit():
            raise SyntaxError("The name must be a string")
        if not name_string.isalnum():
            raise SyntaxError("The name must be alphanumeric")

        # If the name string is present in the names list, return the index of
        # where it is, else return None
        if name_string in self.names:
            return self.names.index(name_string)
        else:
            return None

    def lookup(self, name_string_list: List[str]):
        """Return a list of name IDs for each name string in name_string_list.

        If the name string is not present in the names list, add it.
        """

        # Create a list of IDs
        id_list = []

        # First check that the name_string_list is a list, otherwise produce
        # SyntaxError
        if not isinstance(name_string_list, list):
            raise TypeError("Name string list must be a list")

        # Then check that each element in the list is a string, otherwise
        # produce TypeError

        for name_string in name_string_list:
            if not isinstance(name_string, str):
                raise TypeError("The name must be a string")

        # Check if the name is in the name list, and if not, add it to the list
        # and add the index to the id list too
        for name_string in name_string_list:
            if name_string not in self.names:
                self.names.append(name_string)
            id_list.append(self.names.index(name_string))

        # Return the list of name IDs for each name in the name list
        return id_list

    def get_name_string(self, name_id):
        """Return the corresponding name string for name_id.

        If the name_id is not an index in the names list, return None.
        """
        # First check that name_id provided is a valid number (i.e. is
        # positive)
        if name_id < 0:
            raise ValueError("The name_id is not correct")
        elif name_id < len(self.names):
            return self.names[name_id]
        else:
            return None

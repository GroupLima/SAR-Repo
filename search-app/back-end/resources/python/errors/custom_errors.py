class InvalidAROFormatError(Exception):
    def __init__(self, aro_string):
        super().__init__(f"Invalid ARO format: {aro_string}")

class InvalidPageInputError(Exception):
    def __init__(self, pages):
        super().__init__(f"Invalid page input: {pages}")

class InvalidVolumeInputError(Exception):
    def __init__(self, volumes):
        super().__init__(f"Invalid volume input: {volumes} \nPlease select only 1, 2, 4, 5, 6, 7, 8")

class InvalidDateInputError(Exception):
    def __init__(self, date):
        super().__init__(f"Invalid date input: {date} \nShould be in the form YYYY-MM-DD")

class BrowseError(Exception):
    def __init__(self, volume):
        super().__init__(f"Something went wrong using BrowseSearch class: '\n{volume}' is the value assigned to self.vol")
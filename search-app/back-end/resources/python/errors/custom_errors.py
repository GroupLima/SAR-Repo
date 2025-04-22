class InvalidAROFormatError(Exception):
    def __init__(self, aro_string):
        super().__init__(f"Invalid ARO format: {aro_string}")

class InvalidPageInputError(Exception):
    def __init__(self, pages):
        super().__init__(f"Invalid page input: {pages}")

class InvalidVolumeInputError(Exception):
    def __init__(self, volumes):
        super().__init__(f"Invalid volume input: {volumes}")
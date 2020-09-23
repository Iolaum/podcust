"""
Custodian Class for Demo container.
"""


class DemoCust:
    """
    Main class for handling the httpdemo container.

    The httpdemo container just spawns an a container with an apache web server
    service serving the Fedora Test page through http.

    :param name: The Repository name of the image this class is custodian for.
    """

    def __init__(self, name: str = "localhost/httpdemo"):
        """
        Initialize DemoCust class.
        """
        self.name

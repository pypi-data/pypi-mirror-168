from PyQt5.QtCore import QSettings

"""
    This is where Stec QObject are kept, this are not QWidgets
"""
class VSettings(QSettings):
    """
    Used to save setup data
    """
    def __init__(self, project : str = "stec-general"):
        """
        :param project:   default is "stec-opc" Should be the Project you or instance of the Project
        """
        super().__init__( project, QSettings.IniFormat)




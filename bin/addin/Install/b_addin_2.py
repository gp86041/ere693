import arcpy
import pythonaddins

class ButtonClass1(object):
    """Implementation for b_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class ButtonClass2(object):
    """Implementation for b_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
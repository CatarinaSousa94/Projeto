
class PropertyAppResult(object):

    def __init__(self):
        self.swaggerTypes = {
            'Type': 'str',
            'Href': 'str',
            'Name': 'str',
            'Description': 'str',
            'Content': 'AppResult'
        }

    def __str__(self):
        return str(self.Name)
    
    def __repr__(self):
        return str(self)
    

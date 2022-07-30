###################################################################################################
# CLASS NAME: item_class
# DESCRIPTION: Class to reprsent an item
# Attributes
#     - float
#           - TYPE:     FLOAT
#           - REQUIRED: YES
#     - description
#           - TYPE:     STRING
#           - REQUIRED: YES
#     - id
#           - TYPE:     STRING
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#  EXCEPTIONS
#      - Raised an exception if values don't meet minimum requirements
###################################################################################################
class item:
    def __init__(self, doc):
        self.price        =  doc.get('price')
        self.priceDisplay = "${:0,.2f}".format(self.price)
        self.description  =  doc.get('description')
        self.id           =  doc.get('id')

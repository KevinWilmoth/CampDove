###################################################################################################
# CLASS NAME: transaction
# DESCRIPTION: Class to reprsent a transaction
# Attributes
#     - camper_id:
#           - TYPE:     STRING
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#     - amount
#           - TYPE:     FLOAT
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#     - number
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  ""
#     - DayOfWeek
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  CURRENT DAY OF WEEK
#     - id
#           - TYPE:     STRING
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#  EXCEPTIONS
#      - Raised an exception if values don't meet minimum requirements
###################################################################################################
from datetime import datetime

def dayNameFromWeekday(weekday):
    if weekday == 0:
        return "Monday"
    if weekday == 1:
        return "Tuesday"
    if weekday == 2:
        return "Wednesday"
    if weekday == 3:
        return "Thursday"
    if weekday == 4:
        return "Friday"
    if weekday == 5:
        return "Saturday"
    if weekday == 6:
        return "Sunday"

class transaction:
    def __init__(self, request="", doc="",counter=""):
        if doc=="":
            self.camperId  = request.form['id']
            self.amount    = float(request.form['transaction_amount'])
            self.dayofWeek = dayNameFromWeekday(datetime.today().weekday())
            self.id        = str(hash(self.camperId + str(self.amount) + str(datetime.now())))
            self.counter   = counter
        else:
            self.camperId  =  doc.get('camper_id')
            self.amount    =  doc.get('amount')
            self.dayofWeek =  doc.get('day_of_week')
            self.id        =  doc.get('id')
            self.counter   =  counter
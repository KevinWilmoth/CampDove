###################################################################################################
# CLASS NAME: camper
# DESCRIPTION: Class to reprsent attributes of a Camp Dove Camper
# Attributes
#     - fname:
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  ''
#     - lname
#           - TYPE:     STRING
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#     - church
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  ''
#     - contactName
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  ''
#     - worker
#           - TYPE:     STRING
#           - REQUIRED: NO
#           - DEFAULT:  ''
#     - noLimit
#           - TYPE:     BOOL
#           - REQUIRED: NO
#           - DEFAULT:  FALSE
#     - weeklyLimit
#           - TYPE:     FLOAT
#           - REQUIRED: NO
#           - DEFAULT:  Depends on Value of prepaid_amount and noLimit
#     - dailyLimit
#           - CURRENTLY NOT USED
#     - prepaid_amount
#           - TYPE:     FLOAT
#           - REQUIRED: NO
#           - DEFAULT:  0.0
#     - TabClosed
#           - TYPE:     BOOL
#           - REQUIRED: NO
#           - DEFAULT:  FALSE
#     - id
#           - TYPE:     STRING
#           - REQUIRED: YES
#           - DEFAULT:  N/A
#  EXCEPTIONS
#      - Raised an exception if values don't meet minimum requirements
###################################################################################################
from datetime import datetime

class camper:
    def __init__(self, app, request="", doc="",):
        if doc=="":
            #Required Fields
            self.lname = request.form['camper_last_name']
            if(self.lname==""):
                app.logger.critical("[camper_class.__init__] last name must be set")
                raise Exception("Last Name must be set")  

            #Optional Fields
            self.fname = ""
            if 'camper_first_name' in request.form:
                self.fname = request.form['camper_first_name']

            self.church = ""
            if "church" in request.form:
                self.church = request.form['church']

            self.contactName = ""
            if "contact_name" in request.form:
                self.contactName = request.form['contact_name']  

            self.worker = ""
            if "worker_name" in request.form:
                self.worker = request.form['worker_name'] 

            self.noLimit = False    
            if "no_limit" in request.form:
                no_limit = True
    
            if 'weekly_limit' not in request.form:
                self.weeklyLimit = float(0.0)
            elif request.form['weekly_limit']=='':
                self.weeklyLimit = float(0.0)
            else:
                self.weeklyLimit   = float(request.form['weekly_limit'])

            if 'prepaid_amount' not in request.form:
                self.prepaid_amount = float(0.0)
            elif request.form['prepaid_amount']=='':
                self.prepaid_amount = float(0.0)
            else:
                self.prepaid_amount = float(request.form['prepaid_amount'])

            if self.noLimit==True:
                self.dailyLimit  = float(0.0)
                self.weeklyLimit = float(0.0)
            elif self.prepaid_amount > self.weeklyLimit:
                self.dailyLimit = float(self.prepaid_amount / 4)
            elif self.weeklyLimit > 0:
                self.dailyLimit = float(self.weeklyLimit / 4)
            else:
                self.dailyLimit = float(0.0)

            self.dailyLimitFormat  = "${:0,.2f}".format(self.dailyLimit)
            self.weeklyLimitFormat = "${:0,.2f}".format(self.weeklyLimit)
            self.prepaidFormat     = "${:0,.2f}".format(self.prepaid_amount)

            self.TabClosed = False
            if "id" in request.form:
                self.id = request.form["id"]
                app.logger.info("ID in Form [" + self.id + "]")
            else:
                self.id        =  str(hash(self.fname          +
                                      self.lname               +
                                      self.church              +
                                      self.contactName         +
                                      self.worker              +
                                      str(self.weeklyLimit)    +
                                      str(self.prepaid_amount) +
                                      str(self.noLimit)        +
                                      str(datetime.now())))
        else:
            self.fname          = doc.get('camper_first_name')
            self.lname          = doc.get('camper_last_name')
            self.church         = doc.get('home_church')
            self.contactName    = doc.get('contact_name')
            self.worker         = doc.get('workerName')
            self.noLimit        = doc.get('noLimit')
            self.weeklyLimit    = doc.get('weeklyLimit')
            self.dailyLimit     = doc.get('dailyLimit')
            self.prepaid_amount = doc.get('prepaid')
            self.id             = doc.get('id')
            self.dailyLimitFormat  = "${:0,.2f}".format(self.dailyLimit)
            self.weeklyLimitFormat = "${:0,.2f}".format(self.weeklyLimit)
            self.prepaidFormat     = "${:0,.2f}".format(self.prepaid_amount)
            self.TabClosed      = False
            if (doc.get("closed_status") in ["Refund", "PaidInFull", "Donation"]):
                self.TabClosed = True
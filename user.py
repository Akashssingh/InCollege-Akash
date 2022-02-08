#Potential class def for a user
#Currently not being used
#Developer: Tyler Smith
class User:
    def __init__(self, userName, password, firstName, lastName, email = 1, sms = 1, ads = 1, lang = 1):
        self.userName = userName
        self.password = password
        self.firstname = firstName
        self.lastName = lastName
        self.email = email
        self.sms = sms
        self.ads = ads
        self.lang = lang
    
    def updateEmail(self):
        if self.email == 1:
            self.email = 0
        else:
            self.email = 1

    def updateLang(self):
        if self.lang == 1:
            self.lang = 0
        else:
            self.lang = 1
    
    def updateAds(self):
        if self.ads == 1:
            self.ads = 0
        else:
            self.ads = 1

    def updateSMS(self):
        if self.sms == 1:
            self.sms = 0
        else:
            self.sms = 1

    def getEmail(self):
        return self.email

    def getSMS(self):
        return self.sms
    
    def getLang(self):
        return self.lang

    def getAds(self):
        return self.ads
    
    def getName(self):
        return self.firstname
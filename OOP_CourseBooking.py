#A cooperative runs both vocational and non-vocational courses. Participants get a course
#subsidy based on their monthly income and their age on the start date of course. To enrol in a
#course, a participant must first register as a member.

from _datetime import datetime, date
from abc import ABC, abstractmethod

class Member:
    '''The member class consist of:
    1.member ID auto denerated
    2.monthly income (undisclosed if no value enter by user)
    3. date of Birth & contact number
    4. calculation of age
    5. the string method to return information of member at main()
    '''  
    _nextId = 1
    
    def __init__(self, name, contact, dob, monIncome=None):
        self._memberId = type(self)._nextId
        type(self)._nextId += 1
        self._name = name
        self._contact = contact
        self._dob = dob
        self._monIncome = monIncome 
        
    @property
    def memberId(self):
        return self._memberId
    
    @property
    def monIncome(self):
        return self._monIncome
    
    def ageCalculation(self, thisDate):
        '''calculate the member age based on their birth of date'''
        memDob = self._dob
        age = thisDate.year - memDob.year - ((thisDate.month, thisDate.day) <\
        (memDob.month, memDob.day))
        if age < 0:
            print("Age cannot be negative")
        return age

    def __str__(self):
        income = 'Undisclosed' if self._monIncome is None else f'${self._monIncome}'
        return f"Id: {self.memberId:<3} Name: {self._name:<5} Contact: {self._contact}\
    Monthly Income: {income:<15} Date of Birth: {self._dob:%d %b %Y}"


class Course(ABC):
    '''The Course class consist of
    1. courseCode, title, description, fees parameter
    2. class method baseCancellationPenaltyRate
    3. cancellationPenaltyRate to calculate penalty rate based on days
    4. cancellationPenalty to calculate penalty amount based on monIncome, age, days 
    5. string method to return detail of courseCode, title, description, fees
    6. Abstract method getSubsidy
    7. subclass (Vocational and Non-Vocational course) 
    '''
     
    _baseCancellationPenaltyRate = 0.3
    
    def __init__(self, courseCode, title, description, fees):
        self._courseCode = courseCode
        self._title = title
        self._description = description
        self._fees = fees
        
    @property
    def courseCode(self):
        return self._courseCode
    
    @property
    def fees(self):
        return self._fees
    
    @abstractmethod
    def getSubsidy(self, monIncome, age):
        pass
    
    @classmethod
    def getBaseCancellationPenaltyRate(cls):
        return cls._baseCancellationPenaltyRate
    
    @classmethod
    def setBaseCancellationPenaltyRate(cls, baseCancelRate): 
        cls._baseCancellationPenaltyRate = baseCancelRate
    
    def cancellationPenaltyRate(self, days):
        '''calculate the penalty rate based on days'''
        if days > 7:
            return type(self)._baseCancellationPenaltyRate * 0 
        elif days >= 4 and days <= 7:
            return type(self)._baseCancellationPenaltyRate/2
        else:
            return type(self)._baseCancellationPenaltyRate
         
    def cancellationPenalty(self, monIncome, ageOfParticipant, days):
        '''calculate the penalty fee based on days, income, ageofparticipant'''
        penaltyfeePaid = self._fees - self.getSubsidy(monIncome,ageOfParticipant)  
        penaltyRate = self.cancellationPenaltyRate(days)  
        return  penaltyfeePaid * penaltyRate  
                  
    def __str__(self): #overriding by replacement
        return f"Course code:{self._courseCode:}  Title:{self._title}  Fees:${self._fees:.2f}\n    Description:{self._description}"
        

class VocationalCourse(Course):
    '''VocationalCourse class inherited from Course class, it implement:
    1.Calculation of getSubsidy based monIncome, age
    2.Calculation of cancellationPenaltyRate based on baseCancellationPenaltyRate(Course class) + cancellationPenaltyAddRate(VocationalCourse)
    3.String method to return the inherited detail(courseCode, title, description, fees) plus detail of industry '''
    _cancellationPenaltyAddRate = 0.1
    _specialisedIndustries = ["Engineering", "Electronic", "Computing"]
    
    def __init__(self, courseCode, title, description, fees, industry):#overriding by refinement
        super().__init__(courseCode, title, description, fees)
        self._industry = industry
        
    def getSubsidy(self, monIncome, age):
        '''calculate the subsidy based on age and income status''' 
        if monIncome is not None:
            if age >= 60:
                if self._industry in type(self)._specialisedIndustries:
                    #age 60 or above get 95% subsidy 
                    #less 10% if the course are in special industry
                    specialisedSubsidy = 0.95 - 0.1 
                    return self._fees * specialisedSubsidy
                else:
                    return self._fees * 0.95 
            elif age >= 55 and age < 60:
                if self._industry in type(self)._specialisedIndustries:  
                    specialisedSubsidy = 0.90 - 0.1 
                    return self._fees * specialisedSubsidy
                else:
                    return self._fees * 0.90
            else:
                if self._industry in type(self)._specialisedIndustries:
                    specialisedSubsidy = 0.80 - 0.1 
                    return self._fees * specialisedSubsidy
                else:
                    return self._fees * 0.80
        else: return 0
                    
    def cancellationPenaltyRate(self, days): #overriding by refinement
        '''Sum the penalty rate based on usual cancellation from parent class and 
        the cancellationPenaltyAddRate for all course in vocational class'''  
        penaltyRate = super().cancellationPenaltyRate(days) + \
        type(self)._cancellationPenaltyAddRate 
        return penaltyRate
    
    def __str__(self): #overriding by refinement
        return f"Vocational {super().__str__()}  Industry:{self._industry}"
    

class NonVocationalCourse(Course):
    '''VocationalCourse class inherited from Course class, it implement:
    1.Calculation of getSubsidy based monIncome, age
    2.String method to return the inherited detail(courseCode, title, description, fees)
    3.cancellationPenaltyRate does not apply here but it will auto return baseCancellationPenaltyRate from parent class(Course class)
     '''
    def __init__(self, courseCode, title, description, fees):#overriding by refinement
        super().__init__(courseCode, title, description, fees)
        
    def getSubsidy(self, monIncome, age):
        '''calculate the subsidy based on age and income status''' 
        if monIncome is None  : 
            noSubsidy = 0
            return noSubsidy 
            #income undisclosed no subsidy.
        if (monIncome > 1200 and age < 55) or (monIncome > 1200 and age >= 55) or (monIncome <= 1200 and age < 55): 
             #income more 1200 and age below 55 or age above 55. 0 subsidy
             #income less than 1200 and age below 55. 0 subsidy
            noSubsidy = 0
            return noSubsidy 
        if monIncome is not None:
            if age >= 55 and monIncome <= 1200:
            #age at least 55 and month income no more than 1200
            #get 50% subsidy
                subRate = self._fees * 0.50 
            #coursePaid = self._fees - subRate #fee after minus 95% 
                return subRate
                
    def __str__(self): #overriding by refinement
        return f"Non Vocational {super().__str__()}"       


class ScheduledCourse:
    '''The ScheduledCourse class consist of:
    1.property of course and scheduleDate 
    2.empty list for collection of participant
    3.searchParticipant method 
    4.addParticipant method 
    5.removeParticipant method 
    5. the string method to return information of member & schedule course at main()
    '''  
    def __init__(self, Course, scheduleDate):
        self._course = Course
        self._scheduleDate = scheduleDate 
        self._participant = []
        
    @property
    def course(self):
        return self._course
    
    @property
    def scheduleDate(self):
        return self._scheduleDate  
    
    @property
    def participant(self):
        return self._participant
    
    def searchParticipant(self, memberId):
        '''Searching method to check member ID from the list'''
        for mId in self._participant:
            if memberId == mId.memberId:
                #print(f"Id: {memberId} found!!")
                return True
        #print("the participant not found in list!!")
        return False
    
    def addParticipant(self, member):
        '''Add member to list if the ID is not found'''
        if member not in self._participant:
            self._participant.append(member) 
            #print("member added") 
            return True
        #print("existing member")
        return False
    
    def removeParticipant(self,member):
        '''Delete member from list if the ID found'''
        if member in self._participant:
            self._participant.remove(member) 
            #print("member removed") 
            return True
        #print("no member found")
        return False
    
    def __str__(self):
        '''print the participant list and course detail'''
        count = 0
        temp = f"Scheduled Date: {self._scheduleDate:%d %b %Y}\n{self._course}\nParticipant List:\n"
        for p in self._participant:
            count += 1
            temp += f"{p} Age:{p.ageCalculation(self._scheduleDate)}\n"
        temp += f"Number of Participant:{count}\n"
        return temp
       
       
class CooperativeException(Exception):
    ''' Exception class for exceptions raised in Cooperative application '''
    
    
class Cooperative:
    def __init__(self):
        self._courses = {}
        self._scheduledCourses = {}
        self._members = {}
        
    def getCourse(self, courseCode):
        '''Return course if course code are match'''
        if courseCode in self._courses.keys():
            #print("The code matching") 
            return self._courses[courseCode]
        #print("no code found")
        return None
    
    def getScheduledCourse(self, courseCode, scheduleDate):
        '''Return schedule course if course code and schedule date are match'''
        if (courseCode, scheduleDate) in self._scheduledCourses.keys():
            #print("The code and date matching")
            return self._scheduledCourses[(courseCode,  scheduleDate)] 
        #print("not schedule or code found")
        return None
    
    def getMember(self, mId):
        '''Return member if id are match'''
        if mId in self._members.keys():
            #print("The member id are match")
            return self._members[mId]
        #print("no member found")
        return None
    
    def addCourse(self, c):
        '''Add the course into course dict if does not exist.
        Raise CooperativeException if course code duplicate'''
        if c.courseCode not in self._courses.keys():
            self._courses[c.courseCode] = c
            #print("Add Course Operation is successful\n")
            return True
        raise CooperativeException(f"Duplicate course code {c.courseCode}\n")
    
    def addScheduledCourse(self, scCourse):
        '''Add schedule course into schedule dict if does not exist.
        Raise CooperativeException if course code and schedule date duplicate'''   
        if (scCourse.course.courseCode, scCourse.scheduleDate) in self._scheduledCourses.keys(): 
            raise CooperativeException(f"Duplicate schedule. Course with code {scCourse.course.courseCode} has already been scheduled on {scCourse.scheduleDate:%d %b %Y}\n")
        if (scCourse.course.courseCode, scCourse.scheduleDate) not in self._scheduledCourses.keys():    
            self._scheduledCourses[(scCourse.course.courseCode, scCourse.scheduleDate)] = scCourse 
            return True
         
    def addMember(self, member):
        '''Add member into member dict if ID does not exist.
        Raise CooperativeException if ID duplicate'''
        if member.memberId not in self._members:
            self._members[member.memberId] = member
            #print("Add Member operation is successful\n")
            return True
        raise CooperativeException(f"Duplicate member {member.memberId}\n")
     
    def getMemberCourseAndScheduleCourse(self, memId, courseCode, scheduleDate):
        '''Check member, course code and schedule date. Raise CooperativeException if one of them does not exist''' 
        if self.getMember(memId) is None:
            raise CooperativeException(f"No member id with Id {memId}\n")

        if self.getCourse(courseCode) is None:
            raise CooperativeException(f"No course with code {courseCode}\n")              
      
        if self.getScheduledCourse(courseCode, scheduleDate) is None: 
            raise CooperativeException(f"No schedule for course with code {courseCode} on {scheduleDate:%d %b %Y}\n")

        #print("member id, course, schedule date found in getMemberCourseAndScheduleCourse")
        return self._members[memId],self._courses[courseCode],self._scheduledCourses[(courseCode, scheduleDate)]  

    def enroll(self, memId, courseCode, scheduleDate): 
        m, c, sc = self.getMemberCourseAndScheduleCourse(memId, courseCode, scheduleDate)
        if sc.searchParticipant(memId) is False:    
            sc.addParticipant(m)
            return True
        else:   
            print("Member is exsiting in participant list!!")
            return False
                      
    def cancelEnrollment(self, memId, courseCode, scheduleDate, cancelDate): 
        m, c, sc = self.getMemberCourseAndScheduleCourse(memId, courseCode, scheduleDate)
        if sc.searchParticipant(memId) is True:    
            sc.removeParticipant(m)
            numOfCancelDays = (scheduleDate - cancelDate).days
            penalty = sc.course.cancellationPenalty(m.monIncome, m.ageCalculation(scheduleDate), numOfCancelDays)
            return penalty  
        else:   
            #print("no participant found")
            return -1
        
    def memberStr(self):
        temp="-------------------------Member list-----------------------------------\n"
        for k, v in self._members.items():
            temp += str(v) + '\n'
        return temp + "\n"
        
    def courseStr(self):
        temp="-------------------------Course list-----------------------------------\n"
        for k, v in self._courses.items():
            temp += str(v) + '\n\n'
        return temp       
    
    def scheduleCourseStr(self):
        temp = "-------------------------schedule course list-----------------------------------\n"
        for k, v in self._scheduledCourses.items():
            temp +=  str(v) + '\n'
        return temp       




def menuSelect():  
    '''create a menu with option 0-8'''
    print ("Menu")
    print ("1. List Members")
    print ("2. List Courses")
    print ("3. List Schedules")
    print ("4. Add Member")
    print ("5. Add Course")
    print ("6. Add Schedule")
    print ("7. Enroll Member")
    print ("8. Cancel Enrollment")
    print ("0. Exit")
    menuChoice = int(input("Enter choice: ")) 
    return menuChoice  
              

def getValidDate():
    ''' The method is to check the date format, raise error if datetime format is wrong'''
    while True:
        try:
           dt = datetime.strptime( input("Enter date of birth in d/m/yyyy: "), "%d/%m/%Y")
           return dt
        except:
            #catch the invalid format of birth date
            print('Invalid date format. Try again')


def getValidScheduleDate():
    '''For Option6, 7, 8 - check the date format, raise error if datetime format is wrong'''
    while True:
        try:
           scheduleDate = datetime.strptime( input("Enter schedule date in d/m/yyyy format: "), "%d/%m/%Y")
           return scheduleDate
        except:
            #catch the invalid format of schedule date
            print('Please enter date in d/m/yyyy format')            


def getValidCancelScheduleDate():
    '''Only Option 8 cancel enroll - check the date format, raise error if datetime format is wrong'''
    while True:
        try:
           cancelDate = datetime.strptime( input("Enter cancel date in d/m/yyyy format: "), "%d/%m/%Y")
           return cancelDate
        except:
            #catch the invalid format of schedule date
            print('Please enter date in d/m/yyyy format') 
  
                
def getValidCodeInput():
    ''' This method is to check course code input, raise Handling exception if input is empty string'''
    while True:
        try:
            codeInput = input("Enter Course Code: ")
            if codeInput != '':
                return codeInput
            else: #throw exception if input is empty
                raise Exception("Please enter course code!!") 
        except Exception as ex:
            #catch the Exception and print particular message here. 
            print(ex) 
            
      
def getValidCourseType():
    '''Only for Option5CourseAdding-raise handling exception if user input is: 
    1. not capital "V" or "N"
    2. Empty string''' 
    while True: 
        try:
            voOrNonCourse = input("Enter V to add vocational Course and N to add non-vocational Course: ")
            if (voOrNonCourse == 'N' or voOrNonCourse == 'V'): 
                return voOrNonCourse
            else: #throw exception if input is empty or wrong type
                raise Exception("Type of course should be N or V!!")
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)
        
                    
def getValidDescripCourse():
    '''Only for option5CourseAdding-raise handling exception if description input is empty string'''
    while True: 
        try:
            descripCourse = input("Enter description: ")
            if descripCourse == '':
               raise Exception("Description cannot be empty!!") 
            else:#throw exception if input is empty
                return descripCourse 
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)


def getValidTitleCourse():
    '''Only for option5CourseAdding-raise handling exception if title input is empty string'''
    while True: 
        try:
            titleCourse = input("Enter title: ")
            if titleCourse == '':
                raise Exception("Please enter title!!")
            else:#throw exception if input is empty
                return titleCourse
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)
  
    
def getValidFeeCourse():
    '''Only for option5CourseAdding-check the fee of course format, 
    raise handling exception if user input is:
       1. not whole number 
       2.not positive number 
       3. empty string
       4. 0 amount'''       
    while True:
        try:
            feeCourse = input("Enter fees: ")
            if feeCourse.find(".") != -1 and feeCourse.find("-") != -1: 
                #throw exception if input found "." and "-".
                #which means fees must be whole number and no negative value 
                raise Exception("Course fee cannot be negative and must be whole number!!") 
            elif feeCourse.find("-") != -1:
                #throw exception if input found "-".
                #which means fees must be non negative value 
                raise Exception("Course fee cannot be negative!!") 
            elif feeCourse.find(".") != -1:
                #throw exception if input found ".".
                #which means fees must be whole number
                raise Exception("Please enter whole number!!")  
            elif feeCourse == '':
                #throw exception if input is empty string
                raise Exception("Please enter course fee!!") 
            elif int(feeCourse) == 0:
                #throw exception if input is 0
                raise Exception("Course fee cannot be 0!!")    
            else:
                return feeCourse 
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)


def getValidIndustry():
    '''Only for option5CourseAdding-To check industry input.
     raise handling exception if input is empty string'''
    while True:
        try:
            industryVoCourse = input("Enter industry: ")
            if industryVoCourse == '':
                #throw exception if input is empty string.
                raise Exception("Please enter industry!!") 
            else:
                return industryVoCourse
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)    
            

def getValidNameInput():
    '''Only for option4MemberAdding- To check the name input, 
    raise handling exception if input is empty string'''
    while True:
        try: 
            nameInput = input("Enter name: ")
            if nameInput == '':
                #throw exception if input is empty string.
               raise Exception("Please enter name!!")
            else:
                return nameInput
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)
    
            
def getValidContactInput():
    '''Only for option4MemberAdding- To check the name input, 
    raise handling exception if input is empty string'''
    while True:
        try:
            contactInput = input("Enter contact: ")
            if contactInput == '':
                #throw exception if input is empty string.
                raise Exception("Please enter contact!!")    
            else:
                return contactInput
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)
             

def getValidMemIdInput():
    '''For option7EnrollMember and option8EnrollCancel- To check id input.
     raise handling exception if input is empty string''' 
    while True:
        try:
            memIdInput = input("Enter Member id: ")  
            if memIdInput == '':
                #throw exception if input is empty string.
                raise Exception("Please enter Id!!") 
            elif not memIdInput.isdigit():
                #throw exception if input is non digit.
                raise Exception("Id must be number!!")
            else:
                return memIdInput
        except Exception as ex: 
            #catch the Exception and print particular message here.
            print(ex)  


def option4MemberAdding(coop):
    '''Option4- To adding member into dictionary by enter member detail,
    raise exception if date format, contact, income format are wrong.''' 
    try:
        '''Option 4 - add member method'''
        nameInput = getValidNameInput() #enter repeatly if empty string
        contactInput = getValidContactInput() #enter repeatly if empty string
        #cust contact from str to int, it will raise Valueerror if non digit or whole number.
        c = int(contactInput)    
        memDob = getValidDate() #enter repeatly if date format wrong
        monIncome = input("Enter monthly income to nearest whole number or <ENTER> if not disclosing: ")    
        if monIncome == '': #income set to undisclose if user enter empty string.
            coop.addMember(Member(nameInput, contactInput, memDob))
        elif monIncome != '': 
            #income set if user enter value.
            #ini(monincome) auto check the value is it digit or not. raise Valueerror is not whole number or digit.
            coop.addMember(Member(nameInput, contactInput, memDob, int(monIncome))) 
        print("Add Member operation is successful\n")   
    except ValueError: 
        print("The operation is unsuccessful. Contact or monthly income is not a whole number\n")
    except CooperativeException as e: 
        print(e) #catch Cooperative error and print error here.
    except Exception as ex: 
        #catch the getValidContactInput() exception and print error message here.
        print(ex)
    
                     
def option5CourseAdding(coop):
    '''The Option 5 is allows user to adding course by key in:
    1.Code Type
    2. course code
    3. course tittle
    4. course description
    5.course fee
    6.industry(if code type is "V"'''
    try:
        vOrNCourse = getValidCourseType()
        codeInput = getValidCodeInput()
        titleCourse = getValidTitleCourse() 
        descripCourse = getValidDescripCourse()
        feeCourse = getValidFeeCourse()   
        if vOrNCourse == 'V':
            industryVoCourse = getValidIndustry()
            coop.addCourse(VocationalCourse(codeInput, titleCourse, descripCourse, int(feeCourse), industryVoCourse))
        elif vOrNCourse == 'N': 
            coop.addCourse(NonVocationalCourse(codeInput, titleCourse, descripCourse, int(feeCourse)))
        print("Add Course operation is successful\n")
    except CooperativeException as e: 
        #catch the CooperativeException print the Cooperative class and print out error message here.
        print(e)
    
                      
def option6ScheduleAdding(coop):
    '''Adding the schedule course and raise CooperativeException if:
    1. Course code not found inside course list.
    2. Course code and schedule date is found in schedule course.'''  
    try:
        codeInput = getValidCodeInput()
        scheduleDate = getValidScheduleDate()
        c = coop.getCourse(codeInput) 
        s = ScheduledCourse(c,scheduleDate)
        if c is None:
            raise Exception(f"No course with code {codeInput} \n") 
        coop.addScheduledCourse(s)
        print("Add Schedule operation is successful\n")
    except CooperativeException as e: 
        #catch the CooperativeException print the Cooperative class
        #print out error message here.
        print(e)
    except Exception as ex: 
        #catch the Exception and print particular message here.
        print(ex)
   

def option7EnrollMember(coop):
    try:
        memIdInput = getValidMemIdInput()
        codeInput = getValidCodeInput()
        scheduleDate = getValidScheduleDate()
    
        IdInput = int(memIdInput) #cust the memIdInput to integer and pass to coop.enroll()
        if coop.enroll(IdInput,codeInput,scheduleDate):
            fee = coop.getCourse(codeInput).fees
            income = coop.getMember(IdInput).monIncome
            age = coop.getMember(IdInput).ageCalculation(scheduleDate)
            afterSubsidy = coop.getCourse(codeInput).getSubsidy(income, age)
            totalPay = fee - afterSubsidy
            print(coop.getMember(IdInput).__str__()) 
            print(f"Course Fee: ${fee:.2f}\tSubsidy: ${afterSubsidy:.2f}\tPayment: ${totalPay:.2f}\nEnroll Operation is successful\n") 
        else:
            print("Enroll Operation is un-successful\n")
    except CooperativeException as e: 
        #catch the CooperativeException print the Cooperative class
        #print out error message here.
        print(e)


def option8EnrollCancel(coop):
    try:
        memIdInput = getValidMemIdInput()
        codeInput = getValidCodeInput()
        scheduleDate = getValidScheduleDate()
    
        #check existing of memIdInput,codeInput, scheduleDate, allows user key in cancel date if value is exist. 
        m,c,sc = coop.getMemberCourseAndScheduleCourse(int(memIdInput),codeInput, scheduleDate)
    
        #if coop.getMemberCourseAndScheduleCourse(memIdInput,codeInput, scheduleDate) checking is ok then enter cancel schedule date
        cancelScheduleDate = getValidCancelScheduleDate()
    
        if cancelScheduleDate <  scheduleDate:
            numOfCancelDays = (scheduleDate - cancelScheduleDate).days #calculate number of days 
            totalPay = c.fees - c.getSubsidy(m.monIncome,m.ageCalculation(scheduleDate)) #calculate total payment from getSubsidy()  
        
            #call cancellationPenaltyRate to compute the penalty rate based on days
            penaltyRate = c.cancellationPenaltyRate(numOfCancelDays) 
            
            #call cancelEnrollment to compute the cancel penalty amount and remove member if member in the list
            cancelPenalty = coop.cancelEnrollment(m.memberId, c.courseCode, sc.scheduleDate, cancelScheduleDate)
        
            if cancelPenalty != -1: #print detail if cancelEnrollment successful. 
                print(f"Cancellation rate for {numOfCancelDays} days {penaltyRate}" )
                print(m.__str__()) 
                print(f"Age: {m.ageCalculation(scheduleDate)}\tCourse Fee: ${c.fees:.2f}\tSubsidy: ${c.getSubsidy(m.monIncome,m.ageCalculation(scheduleDate)):.2f}\tPayment: ${totalPay:.2f}")
                print(f"Penalty Rate: {penaltyRate}%\tPenalty Amount: ${cancelPenalty:.2f}")
                print("Cancel Enrollment operation is successful\n")    
            else:
                raise Exception("Member no found in participant list!!\nCancel Enrollment operation is unsuccessful\n")    
        else: raise Exception(f"****The cancel date:{cancelScheduleDate:%d/%m/%Y} cannot over the schedule date:{scheduleDate:%d/%m/%Y}****\n")
    except CooperativeException as e: 
        #catch the CooperativeException print the Cooperative class
        #print out error message here.
        print(e)
    except Exception as ex: 
        #catch the Exception and print particular error message here.
        print(ex)
    
                
def main():
    '''The main function to run the program, raise handling exception if option is invalid'''
    co = Cooperative()
    while True:
        try:
            menuChoice = menuSelect()
            if menuChoice == 1:
                print(co.memberStr())
            elif menuChoice == 2:
                print(co.courseStr())
            elif menuChoice == 3:
                print(co.scheduleCourseStr())
            elif menuChoice == 4:
                option4MemberAdding(co)      
            elif menuChoice == 5:
                option5CourseAdding(co)
            elif menuChoice == 6:
                option6ScheduleAdding(co)
            elif menuChoice == 7:
                option7EnrollMember(co)
            elif menuChoice == 8:
                option8EnrollCancel(co)
            elif menuChoice == 0:
                sys.exit()
            else:
                raise CooperativeException("Invalid option!!Please enter option between 0-8\n")
        except ValueError as e:
            print("Invalid input\n")
        except CooperativeException as e:
            print(e)               
main()
        

        
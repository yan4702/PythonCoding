from _datetime import datetime, timedelta

class Hotel:
    '''The hotel class with hotel name and hotel address'''
    def __init__(self, hotelName, hotelAddress):
        self._hotelName = hotelName
        self._hotelAddress = hotelAddress
        
    @property
    def hotelName(self):
        return self._hotelName
    
    @property
    def hotelAddress(self):
        return self._hotelAddress
    
    def __str__(self):
        return f"Hotel Name: {self._hotelName:<7} Address: {self._hotelAddress}"
    
    
class Driver:
    '''The Driver class with driver name and vehicle number'''
    def __init__(self, driverName, vehNumber):
        self._driverName = driverName
        self._vehNumber = vehNumber
        
    @property
    def driverName(self):
        return self._driverName
    
    @property
    def vehNumber(self):
        return self._vehNumber
    
    @vehNumber.setter
    def vehNumber(self,vehNumber):
        self._vehNumber = vehNumber
        
    def __str__(self):
        return f"Driver Name: {self._driverName:<7} Vehicle Number: {self._vehNumber}"
 
   
    
class Booking:
    '''The Booking class with pickupdate, fromAirport, hotel, numOfpax'''
    def __init__(self, pickUpDateTime, fromAirport, hotel, numOfPax):
        self._pickUpDateTime = pickUpDateTime 
        self._fromAirport = fromAirport
        self._hotel = hotel
        self._numOfPax = numOfPax
        self._withDriver = None #There are no driver assign for new booking yet. Thus,set to None.
            
    @property
    def pickUpDateTime(self):
        return self._pickUpDateTime
       
    @property
    def fromAirport(self):
        return self._fromAirport
        
    @property
    def hotel(self):
        return self._hotel
    
    @property
    def numOfPax(self):
        return self._numOfPax
    
    @property
    def withDriver(self):  
        return self._withDriver
    
    @pickUpDateTime.setter
    def pickUpDateTime(self, pickUpDateTime):
        self._pickUpDateTime = pickUpDateTime
    
    @numOfPax.setter
    def numOfPax(self, numOfPax):
        self._numOfPax = numOfPax
    
    @withDriver.setter
    def withDriver(self, withDriver): 
        self._withDriver = withDriver
        
    def __str__(self):
        #if no drive, set to "No" #otherwise set to self._withDriver 
        hasDriver = "No" if self._withDriver is None else f"{self._withDriver}"
 
        if self.fromAirport == True: #if fromAirport is True then return date, time of booking with TO Hotel, hotel information and driver
            return "Date/Time: {:%d %b %Y %I:%M %p}  TO Hotel\n   {}  Number of Pax: {}\n   Assigned: {}"\
                .format(self._pickUpDateTime,self._hotel, self._numOfPax,hasDriver)
        else: #if fromAirport is False then return date, time of booking with TO Airport, hotel information and driver
            return "Date/Time: {:%d %b %Y %I:%M %p} TO Airport\n   {}  Number of Pax: {}\n   Assigned: {}"\
                .format(self._pickUpDateTime,self._hotel, self._numOfPax,hasDriver)
             
       
class TransportService:
    '''TransportService class consists of 
    1. search hotel, driver, booking method
    2. add hotel,driver, booking method
    3. assign driver method
    4. string method for otel,driver, booking collection
    5.3 empty list for driver, hotel, booking'''
    
    def __init__(self):
        #3 empty list to collect information of hotel, driver, booking
        self._drivers =[]
        self._hotels =[]
        self._bookings =[]
      
        
    def searchHotel(self, hotelName):
        #to check hotel name. Return hotel if exists else return None.
        for h in self._hotels:
            if h.hotelName == hotelName:
                return h
        return None
        
            
    def searchDriver(self, driverName, vehNumber):
        #to check driver name, vehicle no. Return driver if exists else return None.
        for d in self._drivers:
            if (d.driverName == driverName) and (d.vehNumber == vehNumber): 
                return d
        return None
    
    def searchBooking(self, pickUpDateTime, fromAirport, hotelName):
        #to check bookings. Return bookings if exists else return None.
        hotelSearch = self.searchHotel(hotelName)
        for b in self._bookings:
            if (b.pickUpDateTime == pickUpDateTime and bool(b.fromAirport) == fromAirport and hotelSearch):   
                return b 
        return None 

    def addDriver(self, driver):
        #Add driver into driver list if driver is not exist else return False
        if driver not in self._drivers:
            self._drivers.append(driver)
            print("Driver added!!")
            return True
        else:
            print("Existing driver!!")
            return False  
                 
    def addHotel(self, hotel):
        #Add hotel into hotel list if hotel is not exist else return False
        if hotel not in self._hotels:
            self._hotels.append(hotel)
            print("Hotel added!!")
            return True
        else:
            print("Existing hotel!!")
            return False
            
    def addBooking(self, booking):
        #Add driver into driver list driver is not exist else return False
        if booking not in self._bookings:
            self._bookings.append(booking)
            print("Booking added!!")
            return True
        else:
            print("Existing booking!!")
            return False
        
    def removeDriver(self, driveName, vehNo):
        #Remove driver from driver list if driver is exist else return False
        d = self.searchDriver(driveName, vehNo)
        if d is None:
            return False
        else:
            self._drivers.remove(d)
            return True
            
    def removeBooking(self, pickUpDateTime, fromAirport, hotel):
        #Remove bookings from bookings list if bookings is exist else return False
        b = self.searchBooking(pickUpDateTime, fromAirport, hotel) 
        if b is None:
            return False
        else:
            self._bookings.remove(b)
            return True

    def hotelsStr(self):
        #String method to list out hotel detail
        stringList = "\n**********Hotel Collection List***********************\n"
        for hotelInfor in self._hotels:
            stringList += str(hotelInfor) + '\n'
        return stringList
    
    def driversStr(self):
        #String method to list out driver detail
        stringList = "\n**********Driver Collection List***********************\n"
        for driverInfor in self._drivers:
            stringList += str(driverInfor) + '\n'
        return stringList
    
    def bookingsStr(self):
        #String method to list out booking detail
        stringList = "\n******************Booking Collection List***********************\n"
        for bookingsInfor in self._bookings:
            stringList += str(bookingsInfor) +'\n\n'
        return stringList   
        

    def assignDriver(self, pickUpDate, fromAirport, hotel, driveName, vehNo):
        #To check driver and booking. Assign the driver if exists in list else return False
        driver = self.searchDriver(driveName, vehNo) #to check driver is exists or not
        booking = self.searchBooking(pickUpDate, fromAirport, hotel) #to check booking is exists or not
       
        if (booking is not None and driver is not None) and (booking.withDriver is None):
            booking.withDriver = driver
            return True
        return False


def main():    
    '''Hotel class Testing'''
    #Q1.a.create hotel = Zenite and print out string format.
    hotelNum1 = Hotel("Zenite", "1, One Road P111")
    #print(hotelNum1)
    print()
    
    
    '''Driver class Testing'''
    #Q1.b.create driver = Alan and print out the string format.
    driverNum1 = Driver("Alan", "A1110")
    #print(driverNum1)
    print()
    
    #Q1.b.change the vehicle number for Alan to A1111.
    driverNum1.vehNumber = "A1111"
    #print(driverNum1)
    print()
    
    
    '''Booking class testing'''
    #Q1.c.create a bookingNum1 with date: 01 Dec 2019 12:45pm, to hotel(True), hotelNum1 = Zenite , 4 pax  
    #timedelta is to deduct 1 hour before the booking
    #print out the result of booking
    bookingNum1 = Booking(datetime.strptime("01 Dec 2019 12:45 PM","%d %b %Y %I:%M %p")- timedelta(hours=1), True, hotelNum1, 4)
    #print(bookingNum1)
    print()
    
    
    '''Transport Service class Testing'''
    #Q1.d.create a bookingNum2 with date: 02 Dec 2019 10:45am, to airport(False), hotelNum1 = Zenite , 1 pax  
    #timedelta is to deduct 1 hour before the booking
    bookingNum2 = Booking(datetime.strptime("02 Dec 2019 10:45 AM","%d %b %Y %I:%M %p")- timedelta(hours=1), False, hotelNum1, 1)
    
    #Q1.d.create hotelNum2 = Young Lodge 
    hotelNum2 = Hotel("Young Lodge", "2, Two Road P222") 
    
    #Q1.d.create driverNum2, driverNum3
    driverNum2 = Driver("Betty", "B2222")
    driverNum3 = Driver("Charlie", "C3333")
      
    #Q1.d.adding all drivers, hotels and bookings to 3 empty list in Transport Service class
    transService = TransportService()
    transService.addHotel(hotelNum1)
    transService.addHotel(hotelNum2)
    transService.addHotel(hotelNum1) #existing hotelNum1 found when add again
    print()
     
    transService.addDriver(driverNum1)
    transService.addDriver(driverNum2)
    transService.addDriver(driverNum3)
    transService.addDriver(driverNum2) #existing driverNum2 found when add again. 
    print() 
     
    transService.addBooking(bookingNum1)
    transService.addBooking(bookingNum2)
    transService.addBooking(bookingNum1) #existing bookingNum1 found when add again. 
    print()
    
    #Q1.d print out the information from driver, hotel and booking list
    print(transService.hotelsStr() + '\n')
    print(transService.driversStr() +'\n')
    print(transService.bookingsStr() + '\n')
    
    #Q1.d.Apply searchHotel to search hotel = "Zenite" and "Zenites" and print "hotel" found if in list
    print("No hotel found" if transService.searchHotel("Zenite") is None else "Hotel found")
    print("No hotel found" if transService.searchHotel("Zenites") is None else "Hotel found") 
    print()
    
    #Q1.d.Apply removeDriver to remove driver if driver = Charlie, veh = B2222 found and print its detail.
    #Display no driver found!! if driver = Charlie, veh = C3333 no found.
    print("No driver or vehicle found" if transService.removeDriver("Charlie", "B2222") is False else "Driver found and removed!!")
    print("No driver or vehicle found" if transService.removeDriver("Charlie", "C3333") is False else "Driver found and removed!!") 
    print()
    
    #print the driver list after remove 
    print(transService.driversStr() +'\n')
    
    print("Driver found in this bookings" if transService.assignDriver(datetime.strptime("01 Dec 2019 12:45 PM","%d %b %Y %I:%M %p")- timedelta(hours=1), True, "Zenite","Alan", "A1111")\
          is False else "Drivers assign into bookings")
    print(transService.bookingsStr() + '\n')
    
    print("Driver already assign in this bookings/or no booking/or no driver found" if transService.assignDriver(datetime.strptime("01 Dec 2019 12:45 PM","%d %b %Y %I:%M %p")- timedelta(hours=1), True, "Zenite","Charlie", "A1111")\
         is False else "Drivers assign into bookings")
    #print(transService.bookingsStr() + '\n') 
    
main()    
    
    
    
    

   
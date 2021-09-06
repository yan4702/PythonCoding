#A client wishes to keep track of his investment in shares.
#Write a program to help him manage his stock portfolio. You are to record both the shares that
#he is holding as well as shares that he has sold. 

def stockDictList():
    '''convert the nested list to dictionary'''
    stockListDetail = [['3AB', "Telcom", "12/07/2018", 1.55, 3000],
                ['S12', "S&P", "12/08/2018", 3.25, 2000], 
                ['AE1', "A ENG", "04/03/2018", 1.45, 5000]]
    stockDictList = {}
    for n, stockName, lastDateBuy, priceBought, volumeBought in stockListDetail:
        stockDictList[n] = [stockName, lastDateBuy, priceBought, volumeBought]
    
    return stockDictList


def menuOption():
    '''create a menu with option 0-5'''
    
    print ("Menu")
    print ("1. List Holding and Sold details for a Stock")
    print ("2. Buy Stock")
    print ("3. Sell Stock")
    print ("4. List Holdings")
    print ("5. List Sold Stocks")
    print ("0. Exit")
    menuEnter = int(input("Enter choice: ")) 
    return menuEnter 

def printHeldStockDetails(clientStockCode, clientStockName, dateOfBought, priceOfBought, volumeOfBought, investCost):
    '''print held stock details, based on the information passed into the function'''
    
    print ("")
    print ("Held Stock Details:")
    print (f"Code: {clientStockCode}")
    print (f"Name: {clientStockName}")
    print (f"Last Purchase Date: {dateOfBought}")
    print (f"Average Price: $: {priceOfBought:.2f}")
    print (f"Volume: {volumeOfBought}")
    print (f"Investment Cost ($): {investCost:.2f}")
    print ("---------------------------------------")
    print ("")
    
    
def printSoldStockDetails(clientStockCode, clientStockName, dateOfSales, volumeOfSales, profitGainLoss):
    '''print sold stock details, based on the information passed into the function'''
    
    print ("Sold Stock Details:")
    print (f"Code: {clientStockCode}")
    print (f"Name: {clientStockName}")
    print (f"Last Sold Date: {dateOfSales}")
    print (f"Volume: {volumeOfSales}")
    print (f"Profit/Loss ($):{profitGainLoss:.2f}")
    print ("---------------------------------------")  


def holdSoldStock(stockHoldDict,stockSoldDict):
    '''display holdings and selling info based on a single stock code'''
    
    clientStockCode = input("Enter stock code: ")
    
    if (clientStockCode not in stockHoldDict) and (clientStockCode not in stockSoldDict):
        print ("Stock is not in portfolio!")
        print ("---------------------------------------" )
           
    if clientStockCode in stockHoldDict:
        # calculate investment value
        investmentCost = stockHoldDict[clientStockCode][2] * stockHoldDict[clientStockCode][3] 
        # print stock code holding details using function
        printHeldStockDetails(clientStockCode, stockHoldDict[clientStockCode][0],\
        stockHoldDict[clientStockCode][1], stockHoldDict[clientStockCode][2], \
        stockHoldDict[clientStockCode][3], investmentCost)
        
    if clientStockCode in stockSoldDict: 
        printSoldStockDetails(clientStockCode, stockSoldDict[clientStockCode][0], \
        stockSoldDict[clientStockCode][1], stockSoldDict[clientStockCode][2], stockSoldDict[clientStockCode][3])
          

def stockPurchasing(stockHoldDict):
    '''user desire to buy a stock by enter a new code for a stock name or existing code '''
    
    clientStockCode = input("Enter stock code: ")
    # if user already has the stock in his holding portfolio
    if clientStockCode in stockHoldDict:
        print ("You are buying existing stock -", stockHoldDict[clientStockCode][0])
        newStockPrice = float(input("Enter current price per unit: "))
        # looping condition - ask user to key in stock price until it is positive in value
        while newStockPrice < 0:
            newStockPrice = float(input("Enter current price per unit: "))
        volumeOfBought = int(input("Enter number of stocks: "))
        # looping condition - ask user to key in number of stocks until it is positive in value
        while volumeOfBought < 0:
            volumeOfBought = int(input("Enter number of stocks: "))
        dateOfBought = input("Enter date of purchase (dd/mm/yyyy): ")

        # update new volume by adding it to existing volume in dictionary
        newVolume = volumeOfBought + stockHoldDict[clientStockCode][3]
        # update new average price by averaging it with existing price and volume in dictionary
        newAveragePrice = ((stockHoldDict[clientStockCode][2] * stockHoldDict[clientStockCode][3]) + (volumeOfBought * newStockPrice)) / newVolume
        # calculate investment value
        investCost = newVolume * newAveragePrice

        printHeldStockDetails(clientStockCode, stockHoldDict[clientStockCode][0], dateOfBought, newAveragePrice, newVolume, investCost)
        stockHoldDict[clientStockCode] = [stockHoldDict[clientStockCode][0], dateOfBought, newAveragePrice, newVolume]
        
    else: #for stock code doesn't exit in stock
        print ("You are buying new stock")
        clientStockName = input("Enter name: ")
        stockPrice = float(input("Enter current price per unit: "))
        while stockPrice < 0:
            stockPrice = float(input("Enter current price per unit: "))
        volumeOfBought = int(input("Enter number of stocks: "))
        while volumeOfBought < 0:
            volumeOfBought = int(input("Enter number of stocks: "))
        dateOfBought = input("Enter date of purchase (dd/mm/yyyy): ")
        investCost = volumeOfBought * stockPrice

        printHeldStockDetails(clientStockCode, clientStockName, dateOfBought, stockPrice, volumeOfBought, investCost)
        stockHoldDict[clientStockCode] = [clientStockName, dateOfBought, stockPrice, volumeOfBought]


def stockSelling(stockHoldDict, stockSoldDict):
    '''existing stock selling by user'''
    
    clientStockCode = input("Enter stock code: ")
    if clientStockCode in stockHoldDict:
        print ("You are selling this stock: ", stockHoldDict[clientStockCode][0])
        stockPrice = float(input("Enter current price per unit: "))
        while stockPrice < 0: 
            stockPrice = float(input("Enter current price per unit: "))
        volumeOfSales = int(input("Enter number of stocks: "))
        while volumeOfSales < 0:
            volumeOfSales = int(input("Enter number of stocks: "))
          
        if stockHoldDict[clientStockCode][3] < volumeOfSales:
            print ("You do not have sufficient stocks to sell!")
        else:
            dateOfSale = input("Enter date (dd/mm/yyyy): ")
            # profit is given by (price sold - price bought) * volumeOfSales
            profitGainLoss = 0.0
            profitGainLoss += (stockPrice -stockHoldDict[clientStockCode][2]) * volumeOfSales
            # update the number of stocks left, by deducting sold stocks from existing holding
            noOfStocksLeft = stockHoldDict[clientStockCode][3] - volumeOfSales
            # new investment value
            investment_value = noOfStocksLeft * stockHoldDict[clientStockCode][2]

            # check if stock has been sold before
            # if stock has been sold before, update the sold dictionary with new PnL, as well as update total number of stocks sold
            if clientStockCode in stockSoldDict:
                noOfStockSold = volumeOfSales + stockSoldDict[clientStockCode][2] #calculate total sold volume 
                accumProfit = profitGainLoss  + stockSoldDict[clientStockCode][3] #calculate the previous profit with new enter profit
            else:
                accumProfit = profitGainLoss
                noOfStockSold = volumeOfSales

            # if profit is more than zero, print profit, otherwise print loss
            if profitGainLoss >= 0:
                print (f"You made a profit of ${profitGainLoss:.2f} in this transaction.")
            else:
                print (f"You made a loss of ${profitGainLoss:.2f} in this transaction.")
            print (f"You have a remaining volume of {str(noOfStocksLeft)} in your holdings.")

            printHeldStockDetails(clientStockCode, stockHoldDict[clientStockCode][0], stockHoldDict[clientStockCode][1], stockHoldDict[clientStockCode][2], noOfStocksLeft, investment_value)
            printSoldStockDetails(clientStockCode, stockHoldDict[clientStockCode][0], dateOfSale, noOfStockSold, accumProfit)

            stockSoldDict[clientStockCode] = [stockHoldDict[clientStockCode][0], dateOfSale, noOfStockSold, round(accumProfit)]

            if noOfStocksLeft == 0: #remove stock if volume 0.
                stockHoldDict.pop(clientStockCode)
            else:
                stockHoldDict[clientStockCode] = [stockHoldDict[clientStockCode][0], stockHoldDict[clientStockCode][1], stockHoldDict[clientStockCode][2], noOfStocksLeft]            
    else: 
        print ("Error: code not found!")
    

def stockHoldingList(stockHoldDict):
    '''Display details of all stocks the client is holding'''
    
    print ("Code  Name     Last Buy Date    Price-$    Volume      Investment Cost-$")
    accum_investment_value = 0.0
    for key in stockHoldDict: 
        # calculate investment value   
        investment_value = stockHoldDict[key][2] * stockHoldDict[key][3]  
        # add to accum_investment_value  
        accum_investment_value += investment_value         
        print(f"{key:5} {stockHoldDict[key][0]:<8} {stockHoldDict[key][1]:<10} {stockHoldDict[key][2]:10} {stockHoldDict[key][3]:10} {investment_value:16.2f}")
    print (f"Total investment cost is ${accum_investment_value:.2f}")
    print ("---------------------------------------")



def stockSoldList(stockSoldDict):
    '''Display details of stocks the client has sold'''
  
    print ("Code  Name     Last Sell Date   Volume     Profit/Loss-$")
    accum_profit = 0.0
    for key in stockSoldDict: 
        accum_profit += stockSoldDict[key][3]
        print(f"{key:5} {stockSoldDict[key][0]:<8} {stockSoldDict[key][1]:<10} {stockSoldDict[key][2]:10} {stockSoldDict[key][3]:12.2f}")
        
    # if profit is positive, make the statement that client has profited. Otherwise, make statement that client has lost.
    if accum_profit >= 0:
        print (f"To date, you have made a profit of ${accum_profit:.2f}")
    else:
        print (f"To date, you have made a loss of ${accum_profit:.2f}")
    print ("---------------------------------------")

           
def main():
    '''main running program'''
     
    import sys
    
    #hold dict call function
    stockHoldDict = stockDictList()
    
    #create a new sold dict
    stockSoldDict= {}
     
    menuEnter = 0    
    while True: 
        print()
        
        #menu option call function
        menuEnter = menuOption()
        if menuEnter == 0:
            print("Holding Dict Detail")
            for k,v in stockHoldDict.items():
                print(k,v)
            print("-------------------------------------------\n")
          
            print("Sold Dict Detail")    
            for k,v in stockSoldDict.items():
                print(k,v)
            print("-------------------------------------------\n")
            sys.exit()
        elif menuEnter == 1:
            holdSoldStock(stockHoldDict,stockSoldDict)
        elif menuEnter == 2:
            stockPurchasing(stockHoldDict)
        elif menuEnter == 3:
            stockSelling(stockHoldDict, stockSoldDict)
        elif menuEnter == 4:
            stockHoldingList(stockHoldDict)
        elif menuEnter == 5:
            stockSoldList(stockSoldDict)
        else:
            print("invalid option")      
main()        
         

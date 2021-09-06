#Write a Python program to implement a spelling game that a player can play
repeatedly.


import random
import sys

listWord = "meringue albumen foulard eudaemonic narcolepsy elucubrate vivisepulture \
        popocurante cymotrichous malfeasance"
 
splitList = listWord.split()

while True: 
    
    choiceWord = random.choice(splitList)
    numWord =  "-" * len(choiceWord)
    listConvert = list(numWord)
    wrongGuess = 0
    spellWholeWord = False
    newWordSpell = False
    spellNow = False
    print(choiceWord)
    
    print (f'The word {numWord} has {len(choiceWord)} letters. Spell it in 5 tries')
        
    for n in range (0, 5):  
        enterGuess = input(f"Try {n+1} - Current: {''.join(listConvert)}. Your guess? ")
        wrongGuess += 1
     
        for i in range(0, len(choiceWord)):
            if enterGuess == choiceWord[i]:
                listConvert[i] = enterGuess 
                spellNow = True      
            elif enterGuess != choiceWord[i]:
                if wrongGuess == 5:
                    spellWholeWord =True      
        print("Outcome: ", ''.join(listConvert))
         
        
        if spellNow:
            inputSpellNow = input(f"Do you want spell the word now? (y/n) ")
            if inputSpellNow == "y":
                spellWholeWord = True 
            else:
                pass
                 
        if spellWholeWord:
            inputCompleteWord = input("Spell the complete word: ")
            if inputCompleteWord == choiceWord:
                print(f"You are correct! \nThe correct word is {choiceWord}")
                splitList.remove(choiceWord) 
            else:
                print(f"You are incorrect! \nThe correct word is {choiceWord}")
            newWordSpell = True 
        
           
        if newWordSpell:
            wishSpellNew = input("Spell another word? (y/n): ")
            print()
            if wishSpellNew == "y":
                break
            else:
                print(f"{len(splitList)} remaining words: ")
                for w in splitList:
                    print (w)
                print("Thank you for playing Spell The Word!")
                sys.exit()
                     
                 

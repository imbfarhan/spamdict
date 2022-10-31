'''
SpamDict
A Spam Word Detector And Filterer
Author: Farhan Bukhari
Version:1.7
'''

import json
import string
from string import punctuation
import re

dict = {"subscribe" : "SPAM",
        "asshole" : "*******",
        "noob" : "beginner",
}
spc_chars= { "!":"i","@":'a',"$":"s","&":"n","0":"o","#":"h","&":"n","3":"e",}
link_re="^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
allow_link_filtering=0
allow_strong_filtering=0

def loaddict(test):
    global dict #automatically loads the spamdict upon execution
    with open("SpamDict.txt") as f:
        importeddict=f.read()
    dict=json.loads(importeddict)

#Default words in the dictionary
def dictnewword():
    inp=str(input("\nEnter a word to be added to the dictionary:"))
    print("Enter the type of word:\n1.Spam\n2.Censored\n3.Custom")
    wordtype=int(input())
    if(wordtype==1):
        dict.update({inp:"SPAM"})

    elif(wordtype==2):
        censoredword='*'*len(inp)
        dict.update({inp:censoredword})

    elif(wordtype==3):
        customword=input(f"Enter the word to be replaced with {inp}:")
        dict.update({inp:customword})
    print(f"{inp} has been added successfully!")

def showwords():
    print("\nThe words present in SpamDict are:")
    spamwords=list(dict.keys())
    print("Total words present:",len(spamwords))
    for i in range(0,len(spamwords)):
        print(spamwords[i] , ", ", end = " ")
   
    print("\n")

def wordlookup():
    inp=input("\nEnter a word to lookup in SpamDict:")
    wordget=dict.get(inp,-1)  #find a word and its type in the dictionary
    if(wordget==-1):
        print("The word is not present in SpamDict")
    else:
        print("Word:",inp,"\nType:",dict[inp])

def spamchecker():
    count=0
    #Filtering spam from a file
    wordslist=list(dict.keys())  
    spl_chr_list=list(spc_chars.keys())
    content=True
    with open("spam.txt","r") as f:
        with open("spam_clear.txt","w") as f2:
            while content:
            
                content=f.readline() #read each line
                contentlist=content.split() #convert the line to a list
                for i in range (0,len(contentlist)):  # spam converter
                #iterate through every item of the string(each line) converted to list
                #an element in list is a word seperated by space.
                    flag=0  #reset the flag in every iteration.flag is used to check if word has been converted or not
                    value=contentlist[i]
                    already_checked=0
#ver 1.5 start
                    new=""  #to remove spam words like $#!T   
                    for p in value:
                        if(p in spl_chr_list):
                            new=new+spc_chars[p]
                        else:
                            new=new+p
                    new=new.lower()
                    if(allow_strong_filtering==1):
                        for z in dict:
                            substring_check=re.search(f"([A-Za-z0-9])*{z}([A-Za-z0-9])*",new)
                            if(substring_check):
                                    flag=1
                                    count+=1
                                    already_checked=1
                                    contentlist[i]=dict[z]

                    if(new in wordslist):
                        flag=1 #means the word has already been converted to prevent duplication of count
                        if(already_checked==0):
                            count+=1
                        contentlist[i]=dict[new]
                    already_checked=0
#ver 1.5 end
                    convertedvalue=""
#ver 1.2 start
                    for j in value:
                        if j not in punctuation:
                            convertedvalue+=j  #remove special characters from file
#ver 1.2 end 
                    convertedvalue=convertedvalue.lower()
                    if(convertedvalue in wordslist):
                        if(flag==0):
                            count+=1
                            already_checked=1
                        contentlist[i]=dict[convertedvalue]
#ver 1.6 start
                    link_check=re.search(link_re,contentlist[i])   #Link Checker  
                    if(link_check):
                        if(allow_link_filtering==1):
                            count+=1
                            contentlist[i]="SPAM_LINK"
#ver 1.6 end
                    if(allow_strong_filtering==1):
                        for z in dict:
                            substring_check=re.search(f"([A-Za-z0-9])*{z}([A-Za-z0-9])*",contentlist[i])
                            if(substring_check):
                                if(flag==0 and already_checked==0):
                                    count+=1
                                contentlist[i]=dict[z]
                                

                filteredline=' ' #convert list back to string
                filteredline=filteredline.join(contentlist)
                f2.write(filteredline) #write the filtered string back to the file
                f2.write("\n")
    print("\nFile has been filtered successfully!")
    print(f"Total words filtered:{count}")

def savedict():
    with open ("SpamDict.txt","w") as converted_file:  #save the dictionary
        converted_file.write(json.dumps(dict))
    print("SpamDict has been saved and updated successfully!\n")


def dictworddelete():
    inp=input("\nEnter the word to be deleted:")  #remove a word from the dictionary
    dict.pop(inp)
    print(f"{inp} has been deleted successfully!")

def settings():
#ver 1.6 start
    global allow_link_filtering
    global allow_strong_filtering
    settings_ch=0
    #Settings Sub-Menu
    while(settings_ch!=3):
        print("\n\t|SETTINGS|")
        print("1.Toggle link filtering")
        print("2.Toggle strong filtering (BETA)")
        print("3.Go Back")

        settings_ch=int(input("Enter your choice:"))
        if(settings_ch==1):
            if(allow_link_filtering==0):
                allow_link_filtering=1
                print("Link Filtering has been enabled.")
            elif(allow_link_filtering==1):
                allow_link_filtering=0
                print("Link filtering has been disabled.")
        elif(settings_ch==2):
            if(allow_strong_filtering==0):
                allow_strong_filtering=1
                print("Strong filtering has been enabled.")
            elif(allow_strong_filtering==1):
                allow_strong_filtering=0
                print("Strong filtering has been disabled.")
        elif(settings_ch==3):
            return
        else:
            print("Please enter a valid choice!")
#ver 1.6 end


#MAIN BODY
ch=0
loaddict(1)
print("\nNOTE:Save the file to be checked for spam as spam.txt")  
while(ch!=8):
    print("\n\t\t<-|SPAMDICT MENU|->")
    print("1.Add a new word into SpamDict")
    print("2.Check the words present in SpamDict")
    print("3.Delete a word from SpamDict")
    print("4.Lookup a word in the SpamDict")
    print("5.Filter spam from a file")
    print("6.Save the SpamDict")
    print("7.Settings")
    print("8.Exit")
    ch=input("Enter your choice:")
    ch=int(ch)
    if(ch==1):
        dictnewword()
    elif(ch==2):
        showwords()
    elif(ch==3):
        dictworddelete()
    elif(ch==4):
        wordlookup()
    elif(ch==5):
        spamchecker()
    elif(ch==6):
        savedict()
    elif(ch==7):
        settings()
    elif(ch==8):
        print("\n\nThanks for using SpamDict!")
        break
    else:
        print("Enter a valid choice!")
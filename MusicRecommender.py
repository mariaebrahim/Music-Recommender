########################################### THE BASICS

newFile = open("musicrecplus.txt", "a")
newFile.close()
x = open("musicrecplus.txt" , "r")
dic = {}


def read4(filename):
    '''helper function for store thats splits up the file'''
    x = []
    with open(filename, "r") as f:
        for line in f:
            x += [(line.split(":"))]
            
    return x

def store(filename):
    ''' stores file into dictionary sorted captilized and no duplicates'''
    x = read4(filename)

    for i in range(len(x)):
        artists = x[i][1].split(",")
        artists[-1] = artists[-1][:-1]
        dic[x[i][0]] = artists
                
    return dic

usernames = store("musicrecplus.txt")
#usernames = store("musicrecplus_ex2_a.txt")

""" Adding Initial Preferences and asking User for their name """
name = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ")
PRIVATE = False

if name[-1] == "$":
    PRIVATE = True
    
p = []
if name not in usernames:
    pref = input("Enter initial preferences: (Press Enter to Quit) ")
    if pref == "":
        p = []
    else:
        p += [str(pref)]
    
    pref = input("Enter initial preferences: (Press Enter to Quit) ")
    while True:
        if pref == "":
            break
        elif not pref in p: 
            p += [str(pref)]
        pref = input("Enter initial preferences: (Press Enter to Quit) ")
        
    dic[name] = p[0:len(p)-1] + [p[len(p)-1]]

    for value in dic.values():
        for i in range(len(value)):
            value[i] = value[i].title()

    for value in dic.values():
        value = value.sort()


########################################### MENU AND FUNCTIONALITY

text = "Enter a letter to choose an option:\ne - Enter preferences\nr - Get recomendations\np - Show most popular artists\nh - How popular is the most popular\nm - Which user has the most likes\nq - Save and quit\n"

"""Menu and while loop that contains all the functionality"""
menu = input(text)
options = ['e', 'r', 'p', 'h', 'm', 'q']

while True:
    
    while menu not in options:
        menu = input(text)

    # SAVE AND QUIT
    ''' When q is pressed the file is saved with the respective preferences by the user'''
    if menu == 'q':
        outputStr = ''

        for user in dic:
            outputStr += user + ':'
            for artist in dic[user]:
                outputStr += artist + ","

            outputStr = outputStr[0:len(outputStr)-1]

            if outputStr[-2:len(outputStr)] != '\n':
                outputStr += '\n'


        myfile = open("musicrecplus.txt", "w")
        myfile.write(outputStr)
        myfile.close()
	
        break

    # ENTER PREFERENCES
    ''' When e is presed, user is prompted to enter intial preferences'''
    newArtists = []
    while menu == 'e':
        pref = input("Enter an artist that you like (Enter to finish): ")
        if pref == "":
            break
        elif not pref in newArtists: 
            newArtists += [str(pref)]
            
        dic[name] = newArtists[0:len(newArtists)]
            
        for value in dic.values():
            for i in range(len(value)):
                value[i] = value[i].title()

        for value in dic.values():
            value = value.sort()

    # GET RECOMMENDATIONS
    '''Prints the recommendations from the user that has the most similar artists'''
    if menu == 'r':

        if PRIVATE:
            break
        
        count = {}
        for user in dic:
            ct = 0
            if not user == name and user[-1] != '$':
                for value in dic[user]:
                    if value in dic[name]:
                        ct +=1
                        
                count[user] = ct
 
        while True:
            mostSim = max(count.values())
            if mostSim == 0:
                print("No recommendations available at this time.")
                break
        
            keyList = list(count.keys())
            valList = list(count.values())

            pos = valList.index(mostSim)
            user = keyList[pos]
            
            if not (sorted(dic[name]) == sorted(dic[user])):
                for value in dic[user]:
                    if not value in dic[name]:
                        print(value)
                break
            
            count.pop(user)

    #SHOW MOST POPULAR ARTIST
    ''' Prints the artists that are liked by the most users'''  
    if menu=='p':
        matches = [[None, 0],[None, 0], [None, 0]]
        for user in dic:
            if user[-1] != '$':
                for artist in dic[user]:
                    count = 0
                    for user1 in dic:
                        if user1[-1] != '$':
                            for artist1 in dic[user1]:
                                if artist==artist1:
                                    count += 1
                        if count>matches[0][-1]:
                            matches = [[artist, count],matches[0], matches[1]]
                        if count>matches[1][-1] and count<matches[0][-1]:
                            matches = [matches[0], [artist, count], matches[1]]
                        if count>matches[2][-1] and count<matches[0][-1] and count<matches[1][-1]:
                            matches = [matches[0], matches[1], [artist, count]]

        if matches[0][-1]<2 and matches[1][-1]<2 and matches[2][-1]<2:
            print("Sorry, no artists found.")
        elif matches[2][-1]<2:
            print(matches[0][0])
            print(matches[1][0])
        elif matches[1][-1]<2 and matches[2][-1]<2:
            print(matches[0][0])
        else:
            print(matches[0][0])
            print(matches[1][0])
            print(matches[2][0])

                              
    #HOW POPULAR IS THE MOST POPULAR ARTIST
    ''' Prints the number of likes the most popular artist received'''
    if menu == 'h':
        match = [None, 0]
        for user in dic:
            if user[-1] != '$':
                for artist in dic[user]:
                    count = 0
                    for user1 in dic:
                        if user1[-1] != '$':
                            for artist1 in dic[user1]:
                                if artist==artist1:
                                    count += 1
                        if count>match[-1]:
                            match = [artist, count]
        if match[-1]<1:
            print("Sorry, no artists found.")
        else:
            print(match[-1])
                                
    # Which User Likes the Most Artists
    ''' Prints the full name of the users who likes the most artists'''
    if menu == 'm':

        maxLikes = 0
        nm = "Sorry no user found."
        
        for user in dic:
            if user[-1] != '$' and len(dic[user]) > maxLikes:
                maxLikes = len(dic[user])
                nm = user

        print(user)

    
            
    menu = input(text)

from getpass import getpass
from colorama import Fore
from instagram import Instagram
from password import username, password

print(Fore.GREEN + """\n
                               /'                                                             /'                /'
                           --/'--                                                           /'              --/'--
     O  ,____     ____     /' ____     ____      ____     ____     ,__________            /'__     ____     /'    
   /'  /'    )  /'    )--/' /'    )  /'    )   )'    )--/'    )   /'    )     )         /'    )  /'    )--/'      
 /'  /'    /'  '---,   /' /'    /' /'    /'  /'       /'    /'  /'    /'    /'        /'    /' /'    /' /'        
(__/'    /(__(___,/   (__(___,/(__(___,/(__/'        (___,/(__/'    /'    /(__       (___,/(__(___,/'  (__        
                                     /'                                       -------                             
                             /     /'                                                                             
                            (___,/'                                                            twitter alii76tt                   
""")
    

print("Please Login!")
print("\nPlease Wait. Log in...")

instagram = Instagram(username=username, password=password)
instagram.signIn()
while True:
    try:
        choice = int(input("""
                Menu\n
                1- Get Followers\n
                2- Get Following\n
                3- Images Download\n
                4- Videos Download\n
                5- Whatch Story\n
                9- Exit\n
                Choice: """))
        if choice == 1:
            input_search_username = input("Username: ")
            instagram.getFollowers(input_search_username)
        elif choice == 2:
            instagram.getFollowing()
        elif choice == 3:
            input_search_username = input("Username: ")
            instagram.images_load(username=input_search_username)
        elif choice == 4:
            input_search_username = input("Username: ")
            instagram.reels_load(username=input_search_username)
        elif choice == 5:
            search_username = input("Username: ")
            instagram.whatchStory(username = search_username)
        elif choice == 9:
            break
        else:
            "Enter correct choice!"
    except KeyboardInterrupt:
        print("\n" + "Time to leave!")
        quit()
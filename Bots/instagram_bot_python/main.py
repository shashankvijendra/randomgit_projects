from getpass import getpass
from colorama import Fore
from instagram import Instagram

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
username = "random___poster"
password =  "Vs724071997$"
search_list = ["thecliffyvibe", "ananyaraj.official", "ranju.k_raj",
               "nishtharoy007", "sakshimalikk", "yaminijoshi_25"]
search_username = search_list[4]
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
                4- Whatch Story\n
                9- Exit\n
                Choice: """))
        choice = 3
        if choice == 1:
            instagram.getFollowers(search_username)
        elif choice == 2:
            instagram.getFollowing()
        elif choice == 3:
            instagram.images_load(username=search_username)
        elif choice == 4:
            user = input("Username: ")
            instagram.whatchStory(username = user)
        elif choice == 9:
            break
        else:
            "You entered incorrectly!"
    except KeyboardInterrupt:
        print("\n" + "Goodbye, Friend!")
        quit()
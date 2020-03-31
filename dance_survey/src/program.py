from colorama import Fore
import program_dancers
import program_studios
import data.mongo_setup as mongo_setup


def main():

    # Setup MongoDB
    mongo_setup.global_init()

    print_header()

    try:
        while True:
            intent = find_user_intent()
            if intent == "dancer":
                program_dancers.run()
            elif intent == "studio":
                program_studios.run()
    except KeyboardInterrupt:
        return


def print_header():
    fwd_ascii_art = \
        """
           ...ZOOOOOOOOZ$...            
        ..$ZOOOOOOOOOOOOOOOZ7..         
      ..OOOOOOOOOOOOOOOOOOOOOOO..       
    ..ZOOOOOOOOOOOOOOOOOOOOOOOOOZ..     
   .,ZOOOOOOOOOOOOOOOOOOOOOOOOOOOZ..    
  .,OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO..   
 .,ZOOOOO..OOOOOOOOO .OOOOOOOOOOOOOO,.  
 .OOOOOOO   .+OOOOOO   ..ZOOOOOOOOOOO.  
.,OOOOOOO  .   .OOOO  ..  .IOOOOOOOOO,. 
.ZOOOOOOO  OOO . .=O  .OZ.. ..OOOOOOOO. 
,ZOOOOOOO  OOOOZ..    .OOOZO.  .7ZOOOO, 
,OOOOOOOO  OOOOOOZO.  .OOOOOOO.   .ZOO, 
,OOOOOOOO  OOOOOZ.    .OOOOO.   .OOOOO,.
,ZOOOOOOO  OOO.. ..O  .OOI.  .OOOOOOOO,.
.:OOOOOOO  Z.  .OOOO  ..  ..OOOOOOOOO+..
.:OOOOOOO   ..OOOOOO    .OOOOOOOOOOOO:. 
..=OOOOOO  ZOOOOOOOO ..ZOOOOOOOOOOOO=.  
 .,~OOOOOZOOOOOOOOOOOZOOOOOOOOOOOOO+,.  
  .,=OOOOOOOOOOOOOOOOOOOOOOOOOOOOO=,.   
   .,=OOOOOOOOOOOOOOOOOOOOOOOOOOO=,.    
    ..:=OOOOOOOOOOOOOOOOOOOOOOO=:..     
      ..:+ZOOOOOOOOOOOOOOOOOZ+~...      
        ..,~+$OOOOOOOOOOO$+~,...        
          ...,,:~=====~:,,...           
                  ...  .                
        Hosted by www.fwd.dance
                     """

    print(Fore.WHITE + '************  DanceSurvey  ************')
    print(Fore.GREEN + fwd_ascii_art)
    print(Fore.WHITE + '***************************************')
    print()
    print("Welcome to our Dance Survey!")
    print("Which option best describes you?")
    print("\n")


def find_user_intent():
    print("[1] Dancer - I want to book classes, and connect with dancers")
    print("[2] Studio - I want to rent studio space for dance teachers")
    print("\n")

    while True:
        try:
            value = int(input("Enter a number: "))
            if 0 < value <= 2:
                choice = value
                break
            else:
                print("Invalid Number. Try Again.")
                continue
        except ValueError:
            print("Please use a number and try again.")
            continue
    if choice == 1:
        return 'dancer'
    elif choice == 2:
        return 'studio'


if __name__ == '__main__':
    main()

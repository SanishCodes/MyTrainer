from app.models import BicepCurlCounter, SquatsCounter, PushupCounter, CrunchCounter, OverheadTricepsCounter, DeadliftCounter, LateralRaiseCounter, BarbellRowCounter, LungesCounter



def main():
   
    print("Choose exercise: 1) Bicep Curl  2) Squats 3) Pushup 4) Crunch 5) Overhead Triceps")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        biceps_counter = BicepCurlCounter()
        
    elif choice == '2':
        squats_counter = SquatsCounter()
    
    elif choice == '3':
        PushupCounter()
    
    elif choice == '4':
        CrunchCounter()

    elif choice == '5':
        OverheadTricepsCounter()
    
    
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
   
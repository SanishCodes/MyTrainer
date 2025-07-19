from app.models import BicepCurlCounter, SquatsCounter, PushupCounter, CrunchCounter, OverheadTricepsCounter, DeadliftCounter, LateralRaiseCounter, BarbellRowCounter, LungesCounter



def main():
   
    print("Choose exercise: 1) Bicep Curl  2) Squats 3) Pushup 4) Crunch 5) Overhead Triceps 6) Deadlift 7) Lateral Raise 8) Barbell Row 9) Lunges Counter")
    choice = input("Enter your choice (1-8): ")

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
    
    elif choice == '6':
        DeadliftCounter()

    elif choice == '7':
        LateralRaiseCounter()

    elif choice == '8':
        BarbellRowCounter()
    
    elif choice == '9':
        LungesCounter()
    
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
   
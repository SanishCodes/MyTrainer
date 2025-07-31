from biceps_curl_counter import BicepCurlCounter
from squats_counter import SquatsCounter
from pushup_counter import PushupCounter
from crunch_counter import CrunchCounter
from overhead_triceps_counter import OverheadTricepsCounter
from deadlift_counter import DeadliftCounter
from lateral_raise_counter import LateralRaiseCounter
from barbell_row_counter import BarbellRowCounter
from lunges_counter import LungesCounter

def main():
   
    print("Choose exercise: 1) Bicep Curl  2) Squats 3) Pushup 4) Crunch 5) Overhead Triceps 6) Deadlift 7) Lateral Raise 8) Barbell Row 9) Lunges Counter")
    choice = input("Enter your choice (1-9): ")

    if choice == '1':
        BicepCurlCounter()
        
    elif choice == '2':
        SquatsCounter()
    
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
   
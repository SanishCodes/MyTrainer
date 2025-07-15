from app.models.biceps_curl_counter import BicepCurlCounter
from app.models.squats_counter import SquatsCounter

def main():
   
    print("Choose exercise: 1) Bicep Curl  2) Squats")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        biceps_counter = BicepCurlCounter()
        
    elif choice == '2':
        squats_counter = SquatsCounter()
        
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
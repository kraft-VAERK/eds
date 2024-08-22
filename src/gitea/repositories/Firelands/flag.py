import sys
import hashlib

def hash_input(input_string):
    # Hash the input string using SHA256 algorithm
    hashed_input = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed_input

def main():
    if len(sys.argv) < 2:
        print("Usage: python program_name.py <input_string>")
        return
    
    # Input string from command-line argument
    input_string = sys.argv[1].upper()

    # Hash the input string
    hashed_input = hash_input(input_string)

    # Print the hashed input
    print("Hashed input:", hashed_input)

    # Provide the hashed string for comparison
    hashed_string = hash_input("HKN{W3LC0M3_T0_3DS_3MP0W3R1NG_D3V0PS_S3CUR1TY}")
    
    # Check if the hashed input matches the provided hashed string
    if hashed_input == hashed_string:
        print("The hashed input matches the provided hashed string.")
        print("Flag: HKN{W3LC0M3_T0_3DS_3MP0W3R1NG_D3V0PS_S3CUR1TY}")
    else:
        print("The hashed input does not match the provided hashed string.")

if __name__ == "__main__":
    main()

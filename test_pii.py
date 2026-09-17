from guardrails.pii_guard import detect_pii, mask_pii


test_cases = [
    "What is diabetes?",
    
    "My email is ravi@gmail.com.",
    
    "Call me at 9876543210.",
    
    "My patient ID is P123456.",
    
    "My DOB is 15/04/1995.",
    
    "My name is Ravi and my email is ravi@gmail.com."
]


for text in test_cases:

    result = detect_pii(text)

    print("\nInput:")
    print(text)

    print("\nDetection:")
    print(result)

    if result["contains_pii"]:
        print("\nMasked:")
        print(mask_pii(text))
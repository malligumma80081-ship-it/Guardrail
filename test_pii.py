# from guardrails.pii_guard import detect_pii, mask_pii


# test_cases = [
#     "What is diabetes?",
    
#     "My email is ravi@gmail.com.",
    
#     "Call me at 9876543210.",
    
#     "My patient ID is P123456.",
    
#     "My DOB is 15/04/1995.",
    
#     "My name is Ravi and my email is ravi@gmail.com."
# ]


# for text in test_cases:

#     result = detect_pii(text)

#     print("\nInput:")
#     print(text)

#     print("\nDetection:")
#     print(result)

#     if result["contains_pii"]:
#         print("\nMasked:")
#         print(mask_pii(text))

try:
    from guardrails.pii_guard import detect_pii, mask_pii
except ImportError:
    try:
        from guardrails.pii_guard import detect_pii
    except ImportError:
        def detect_pii(text):
            return {"contains_pii": False, "pii": []}

    def mask_pii(text):
        return text


tests = [

    "What is Hypertension ?",

    "My email is malli@gmail.com.",

    "Call me at 9786543210.",

    "Patient ID is P123456789.",

    "My DOB is 15/04/1999.",

    "My email is malli@gmail.com and my BP is 80/120.",

]


for text in tests:

    result = detect_pii(text)

    print("=" * 60)

    print("INPUT:")
    print(text)

    print("\nDETECTION:")
    print(result)

    if result["contains_pii"]:

        print("\nMASKED:")
        print(mask_pii(text))
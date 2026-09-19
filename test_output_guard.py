from guardrails.output_guard import validate_output


test_cases = [

    "Diabetes is a condition that affects blood glucose.",

    "You should increase your dose to 20 mg.",

    "You definitely have diabetes.",

    "A CBC is a blood test used to evaluate blood cells.",

    "Double your medication dose tomorrow."

]


for text in test_cases:

    result = validate_output(text)

    print("=" * 60)

    print("OUTPUT:")
    print(text)

    print("\nVALIDATION:")
    print(result)
#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
    sys.exit(
        "Please insert your height in centimeters (cm) and weight in kilograms (kg)")

elif len(sys.argv) < 3:
    sys.exit('You forgot to insert your weight!')

height = float(sys.argv[1])
weight = float(sys.argv[2])
bmi = weight / ((height*0.01)**2)

if bmi < 18.5:
    print(f'You are underweight with BMI of {bmi}')

elif bmi > 25:
    print(f'You are overweight with BMI of {bmi}')

else:
    print(f'You are normal or healthy weight with BMI of {bmi}')

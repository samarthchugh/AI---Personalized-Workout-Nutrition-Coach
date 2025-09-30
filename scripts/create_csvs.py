# scripts/create_csvs.py

import os
from src.contants import (
    RAW_DATA_DIR_NAME,
    WORKOUTS_CSV_FILE_NAME,
    NUTRITION_CSV_FILE_NAME,
    FAQ_CSV_FILE_NAME
)

# Ensure raw data folder exists
raw_data_path = os.path.join("data", RAW_DATA_DIR_NAME)
os.makedirs(raw_data_path, exist_ok=True)

# 1️⃣ Workouts CSV text
workouts_csv = """id,name,duration_min,intensity,muscle_group,age,gender,goal,bmi,fitness_level
1,Push Ups,10,Medium,Chest,25,Male,Build Muscle,24.5,Intermediate
2,Squats,15,High,Legs,30,Female,Weight Loss,22.1,Beginner
3,Plank,5,Low,Core,28,Male,Toning,23.4,Beginner
4,Burpees,12,High,Full Body,35,Female,Endurance,27.8,Intermediate
5,Lunges,10,Medium,Legs,22,Male,Build Muscle,21.9,Beginner
6,Pull Ups,8,High,Back,29,Female,Strength,25.2,Intermediate
7,Bench Press,15,Medium,Chest,32,Male,Strength,26.1,Advanced
8,Jumping Jacks,10,Low,Cardio,24,Female,Weight Loss,20.7,Beginner
9,Bicep Curls,12,Medium,Arms,27,Male,Toning,23.8,Intermediate
10,Mountain Climbers,8,High,Full Body,31,Female,Endurance,26.4,Intermediate
11,Deadlifts,15,High,Back,28,Male,Build Muscle,27.5,Advanced
12,Shoulder Press,10,Medium,Arms,35,Female,Strength,24.6,Intermediate
13,Crunches,5,Low,Core,23,Male,Toning,22.9,Beginner
14,Leg Press,15,High,Legs,30,Female,Build Muscle,25.1,Intermediate
15,Tricep Dips,8,Medium,Arms,26,Male,Toning,23.5,Intermediate
16,Push Ups,12,High,Chest,32,Female,Endurance,28.2,Advanced
17,Squats,10,Medium,Legs,24,Male,Weight Loss,22.8,Beginner
18,Plank,5,Low,Core,29,Female,Toning,23.7,Beginner
19,Burpees,15,High,Full Body,31,Male,Endurance,26.3,Intermediate
20,Lunges,12,Medium,Legs,27,Female,Build Muscle,24.1,Intermediate
21,Push Ups,12,Medium,Chest,26,Female,Toning,22.4,Beginner
22,Squats,15,High,Legs,29,Male,Build Muscle,25.9,Intermediate
23,Plank,6,Low,Core,31,Female,Toning,23.3,Beginner
24,Burpees,12,High,Full Body,33,Male,Endurance,26.7,Intermediate
25,Lunges,10,Medium,Legs,28,Female,Weight Loss,23.1,Beginner
26,Pull Ups,8,High,Back,32,Male,Strength,27.2,Intermediate
27,Bench Press,15,Medium,Chest,29,Female,Build Muscle,24.9,Advanced
28,Jumping Jacks,10,Low,Cardio,25,Male,Weight Loss,21.5,Beginner
29,Bicep Curls,12,Medium,Arms,27,Female,Toning,24.3,Intermediate
30,Mountain Climbers,9,High,Full Body,31,Male,Endurance,26.1,Intermediate
31,Deadlifts,16,High,Back,30,Female,Build Muscle,25.7,Advanced
32,Shoulder Press,11,Medium,Arms,34,Male,Strength,27.6,Intermediate
33,Crunches,6,Low,Core,24,Female,Toning,22.8,Beginner
34,Leg Press,14,High,Legs,29,Male,Build Muscle,26.2,Intermediate
35,Tricep Dips,8,Medium,Arms,28,Female,Toning,24.0,Intermediate
36,Push Ups,12,High,Chest,32,Male,Endurance,28.1,Advanced
37,Squats,10,Medium,Legs,26,Female,Weight Loss,22.7,Beginner
38,Plank,5,Low,Core,30,Male,Toning,23.6,Beginner
39,Burpees,15,High,Full Body,33,Female,Endurance,26.9,Intermediate
40,Lunges,12,Medium,Legs,27,Male,Build Muscle,24.2,Intermediate
41,Push Ups,11,Medium,Chest,25,Female,Toning,22.5,Beginner
42,Squats,16,High,Legs,28,Male,Build Muscle,26.0,Intermediate
43,Plank,6,Low,Core,32,Female,Toning,23.4,Beginner
44,Burpees,13,High,Full Body,34,Male,Endurance,27.0,Intermediate
45,Lunges,10,Medium,Legs,29,Female,Weight Loss,23.3,Beginner
46,Pull Ups,9,High,Back,31,Male,Strength,27.4,Intermediate
47,Bench Press,15,Medium,Chest,30,Female,Build Muscle,25.0,Advanced
48,Jumping Jacks,10,Low,Cardio,26,Male,Weight Loss,21.6,Beginner
49,Bicep Curls,12,Medium,Arms,28,Female,Toning,24.2,Intermediate
50,Mountain Climbers,9,High,Full Body,32,Male,Endurance,26.2,Intermediate
51,Deadlifts,15,High,Back,29,Female,Build Muscle,25.8,Advanced
52,Shoulder Press,11,Medium,Arms,33,Male,Strength,27.7,Intermediate
53,Crunches,5,Low,Core,24,Female,Toning,22.9,Beginner
54,Leg Press,14,High,Legs,30,Male,Build Muscle,26.3,Intermediate
55,Tricep Dips,8,Medium,Arms,27,Female,Toning,24.1,Intermediate
56,Push Ups,12,High,Chest,31,Male,Endurance,28.3,Advanced
57,Squats,10,Medium,Legs,26,Female,Weight Loss,22.9,Beginner
58,Plank,5,Low,Core,29,Male,Toning,23.5,Beginner
59,Burpees,15,High,Full Body,34,Female,Endurance,27.1,Intermediate
60,Lunges,12,Medium,Legs,28,Male,Build Muscle,24.3,Intermediate
61,Push Ups,12,Medium,Chest,25,Female,Toning,22.6,Beginner
62,Squats,15,High,Legs,29,Male,Build Muscle,26.1,Intermediate
63,Plank,6,Low,Core,31,Female,Toning,23.2,Beginner
64,Burpees,12,High,Full Body,33,Male,Endurance,26.8,Intermediate
65,Lunges,10,Medium,Legs,28,Female,Weight Loss,23.0,Beginner
66,Pull Ups,8,High,Back,32,Male,Strength,27.3,Intermediate
67,Bench Press,15,Medium,Chest,29,Female,Build Muscle,25.1,Advanced
68,Jumping Jacks,10,Low,Cardio,26,Male,Weight Loss,21.8,Beginner
69,Bicep Curls,12,Medium,Arms,28,Female,Toning,24.0,Intermediate
70,Mountain Climbers,9,High,Full Body,32,Male,Endurance,26.0,Intermediate
71,Deadlifts,15,High,Back,29,Female,Build Muscle,25.9,Advanced
72,Shoulder Press,11,Medium,Arms,33,Male,Strength,27.5,Intermediate
73,Crunches,5,Low,Core,24,Female,Toning,22.7,Beginner
74,Leg Press,14,High,Legs,30,Male,Build Muscle,26.1,Intermediate
75,Tricep Dips,8,Medium,Arms,27,Female,Toning,24.2,Intermediate
76,Push Ups,12,High,Chest,31,Male,Endurance,28.4,Advanced
77,Squats,10,Medium,Legs,26,Female,Weight Loss,22.8,Beginner
78,Plank,5,Low,Core,29,Male,Toning,23.3,Beginner
79,Burpees,15,High,Full Body,34,Female,Endurance,27.2,Intermediate
80,Lunges,12,Medium,Legs,28,Male,Build Muscle,24.4,Intermediate
81,Push Ups,12,Medium,Chest,25,Female,Toning,22.7,Beginner
82,Squats,15,High,Legs,29,Male,Build Muscle,26.2,Intermediate
83,Plank,6,Low,Core,31,Female,Toning,23.3,Beginner
84,Burpees,12,High,Full Body,33,Male,Endurance,26.9,Intermediate
85,Lunges,10,Medium,Legs,28,Female,Weight Loss,23.2,Beginner
86,Pull Ups,8,High,Back,32,Male,Strength,27.6,Intermediate
87,Bench Press,15,Medium,Chest,29,Female,Build Muscle,25.2,Advanced
88,Jumping Jacks,10,Low,Cardio,26,Male,Weight Loss,21.9,Beginner
89,Bicep Curls,12,Medium,Arms,28,Female,Toning,24.1,Intermediate
90,Mountain Climbers,9,High,Full Body,32,Male,Endurance,26.3,Intermediate
91,Deadlifts,15,High,Back,29,Female,Build Muscle,26.0,Advanced
92,Shoulder Press,11,Medium,Arms,33,Male,Strength,27.8,Intermediate
93,Crunches,5,Low,Core,24,Female,Toning,22.8,Beginner
94,Leg Press,14,High,Legs,30,Male,Build Muscle,26.2,Intermediate
95,Tricep Dips,8,Medium,Arms,27,Female,Toning,24.3,Intermediate
96,Push Ups,12,High,Chest,31,Male,Endurance,28.5,Advanced
97,Squats,10,Medium,Legs,26,Female,Weight Loss,22.9,Beginner
98,Plank,5,Low,Core,29,Male,Toning,23.4,Beginner
99,Burpees,15,High,Full Body,34,Female,Endurance,27.3,Intermediate
100,Lunges,12,Medium,Legs,28,Male,Build Muscle,24.5,Intermediate
"""  # You can paste all 100 rows here

# 2️⃣ Nutrition CSV text
nutrition_csv = """id,meal_name,calories,protein_g,carbs_g,fats_g,age,gender,bmi,goal,diet_type
1,Grilled Chicken Salad,350,30,20,10,25,Male,24.5,Build Muscle,High Protein
2,Oatmeal with Berries,250,8,40,5,30,Female,22.1,Weight Loss,Vegetarian
3,Protein Shake,200,25,10,5,28,Male,23.4,Toning,Keto
4,Avocado Toast,300,10,35,12,35,Female,27.8,Endurance,Vegan
5,Steamed Salmon with Rice,400,35,30,15,22,Male,21.9,Build Muscle,Pescatarian
6,Vegetable Stir Fry,280,12,40,10,29,Female,25.2,Strength,Vegan
7,Greek Yogurt with Honey,150,10,20,5,32,Male,26.1,Strength,Vegetarian
8,Turkey Sandwich,350,25,30,10,24,Female,20.7,Weight Loss,High Protein
9,Boiled Eggs,200,15,5,12,27,Male,23.8,Toning,Keto
10,Quinoa Salad,300,12,35,8,31,Female,26.4,Endurance,Vegan
11,Grilled Chicken Salad,350,30,20,10,28,Male,27.5,Build Muscle,High Protein
12,Oatmeal with Berries,250,8,40,5,35,Female,24.6,Weight Loss,Vegetarian
13,Protein Shake,200,25,10,5,23,Male,22.9,Toning,Keto
14,Avocado Toast,300,10,35,12,30,Female,25.1,Endurance,Vegan
15,Steamed Salmon with Rice,400,35,30,15,26,Male,23.5,Build Muscle,Pescatarian
16,Vegetable Stir Fry,280,12,40,10,32,Female,28.2,Strength,Vegan
17,Greek Yogurt with Honey,150,10,20,5,24,Male,22.8,Strength,Vegetarian
18,Turkey Sandwich,350,25,30,10,29,Female,23.7,Weight Loss,High Protein
19,Boiled Eggs,200,15,5,12,31,Male,26.3,Toning,Keto
20,Quinoa Salad,300,12,35,8,27,Female,24.1,Endurance,Vegan
21,Grilled Chicken Salad,360,32,22,11,26,Male,25.0,Build Muscle,High Protein
22,Oatmeal with Berries,260,9,42,6,31,Female,22.4,Weight Loss,Vegetarian
23,Protein Shake,210,26,12,6,29,Male,23.6,Toning,Keto
24,Avocado Toast,310,11,36,13,36,Female,28.0,Endurance,Vegan
25,Steamed Salmon with Rice,410,36,31,16,23,Male,22.0,Build Muscle,Pescatarian
26,Vegetable Stir Fry,290,13,42,11,30,Female,25.5,Strength,Vegan
27,Greek Yogurt with Honey,160,11,22,6,33,Male,26.3,Strength,Vegetarian
28,Turkey Sandwich,360,26,32,11,25,Female,21.0,Weight Loss,High Protein
29,Boiled Eggs,210,16,6,13,28,Male,24.0,Toning,Keto
30,Quinoa Salad,310,13,36,9,32,Female,26.5,Endurance,Vegan
31,Grilled Chicken Salad,355,31,21,11,27,Male,25.2,Build Muscle,High Protein
32,Oatmeal with Berries,255,8,41,5,34,Female,24.8,Weight Loss,Vegetarian
33,Protein Shake,205,25,11,6,24,Male,23.0,Toning,Keto
34,Avocado Toast,305,10,35,12,31,Female,25.2,Endurance,Vegan
35,Steamed Salmon with Rice,405,35,30,15,27,Male,23.6,Build Muscle,Pescatarian
36,Vegetable Stir Fry,285,12,41,10,33,Female,28.4,Strength,Vegan
37,Greek Yogurt with Honey,155,10,21,5,25,Male,23.0,Strength,Vegetarian
38,Turkey Sandwich,355,25,31,10,30,Female,23.8,Weight Loss,High Protein
39,Boiled Eggs,205,15,5,12,32,Male,26.1,Toning,Keto
40,Quinoa Salad,305,12,35,8,28,Female,24.2,Endurance,Vegan
41,Grilled Chicken Salad,350,30,20,10,26,Male,24.6,Build Muscle,High Protein
42,Oatmeal with Berries,250,8,40,5,31,Female,22.3,Weight Loss,Vegetarian
43,Protein Shake,200,25,10,5,29,Male,23.5,Toning,Keto
44,Avocado Toast,300,10,35,12,36,Female,27.2,Endurance,Vegan
45,Steamed Salmon with Rice,400,35,30,15,24,Male,22.2,Build Muscle,Pescatarian
46,Vegetable Stir Fry,280,12,40,10,31,Female,25.0,Strength,Vegan
47,Greek Yogurt with Honey,150,10,20,5,33,Male,26.5,Strength,Vegetarian
48,Turkey Sandwich,350,25,30,10,25,Female,21.2,Weight Loss,High Protein
49,Boiled Eggs,200,15,5,12,28,Male,23.9,Toning,Keto
50,Quinoa Salad,300,12,35,8,32,Female,26.0,Endurance,Vegan
51,Grilled Chicken Salad,360,32,22,11,27,Male,25.1,Build Muscle,High Protein
52,Oatmeal with Berries,260,9,42,6,34,Female,22.7,Weight Loss,Vegetarian
53,Protein Shake,210,26,12,6,24,Male,23.3,Toning,Keto
54,Avocado Toast,310,11,36,13,31,Female,25.4,Endurance,Vegan
55,Steamed Salmon with Rice,410,36,31,16,27,Male,23.7,Build Muscle,Pescatarian
56,Vegetable Stir Fry,290,13,42,11,33,Female,28.3,Strength,Vegan
57,Greek Yogurt with Honey,160,11,22,6,25,Male,23.1,Strength,Vegetarian
58,Turkey Sandwich,360,26,32,11,30,Female,23.9,Weight Loss,High Protein
59,Boiled Eggs,210,16,6,13,32,Male,26.2,Toning,Keto
60,Quinoa Salad,310,13,36,9,28,Female,24.3,Endurance,Vegan
61,Grilled Chicken Salad,355,31,21,11,27,Male,25.3,Build Muscle,High Protein
62,Oatmeal with Berries,255,8,41,5,34,Female,24.9,Weight Loss,Vegetarian
63,Protein Shake,205,25,11,6,24,Male,23.1,Toning,Keto
64,Avocado Toast,305,10,35,12,31,Female,25.3,Endurance,Vegan
65,Steamed Salmon with Rice,405,35,30,15,27,Male,23.8,Build Muscle,Pescatarian
66,Vegetable Stir Fry,285,12,41,10,33,Female,28.5,Strength,Vegan
67,Greek Yogurt with Honey,155,10,21,5,25,Male,23.2,Strength,Vegetarian
68,Turkey Sandwich,355,25,31,10,30,Female,23.7,Weight Loss,High Protein
69,Boiled Eggs,205,15,5,12,32,Male,26.0,Toning,Keto
70,Quinoa Salad,305,12,35,8,28,Female,24.4,Endurance,Vegan
71,Grilled Chicken Salad,350,30,20,10,26,Male,24.7,Build Muscle,High Protein
72,Oatmeal with Berries,250,8,40,5,31,Female,22.5,Weight Loss,Vegetarian
73,Protein Shake,200,25,10,5,29,Male,23.6,Toning,Keto
74,Avocado Toast,300,10,35,12,36,Female,27.3,Endurance,Vegan
75,Steamed Salmon with Rice,400,35,30,15,24,Male,22.3,Build Muscle,Pescatarian
76,Vegetable Stir Fry,280,12,40,10,31,Female,25.1,Strength,Vegan
77,Greek Yogurt with Honey,150,10,20,5,33,Male,26.6,Strength,Vegetarian
78,Turkey Sandwich,350,25,30,10,25,Female,21.3,Weight Loss,High Protein
79,Boiled Eggs,200,15,5,12,28,Male,24.0,Toning,Keto
80,Quinoa Salad,300,12,35,8,32,Female,26.1,Endurance,Vegan
81,Grilled Chicken Salad,360,32,22,11,27,Male,25.4,Build Muscle,High Protein
82,Oatmeal with Berries,260,9,42,6,34,Female,22.8,Weight Loss,Vegetarian
83,Protein Shake,210,26,12,6,24,Male,23.4,Toning,Keto
84,Avocado Toast,310,11,36,13,31,Female,25.5,Endurance,Vegan
85,Steamed Salmon with Rice,410,36,31,16,27,Male,23.9,Build Muscle,Pescatarian
86,Vegetable Stir Fry,290,13,42,11,33,Female,28.6,Strength,Vegan
87,Greek Yogurt with Honey,160,11,22,6,25,Male,23.3,Strength,Vegetarian
88,Turkey Sandwich,360,26,32,11,30,Female,24.0,Weight Loss,High Protein
89,Boiled Eggs,210,16,6,13,32,Male,26.3,Toning,Keto
90,Quinoa Salad,310,13,36,9,28,Female,24.5,Endurance,Vegan
91,Grilled Chicken Salad,355,31,21,11,27,Male,25.5,Build Muscle,High Protein
92,Oatmeal with Berries,255,8,41,5,34,Female,25.0,Weight Loss,Vegetarian
93,Protein Shake,205,25,11,6,24,Male,23.2,Toning,Keto
94,Avocado Toast,305,10,35,12,31,Female,25.6,Endurance,Vegan
95,Steamed Salmon with Rice,405,35,30,15,27,Male,24.0,Build Muscle,Pescatarian
96,Vegetable Stir Fry,285,12,41,10,33,Female,28.7,Strength,Vegan
97,Greek Yogurt with Honey,155,10,21,5,25,Male,23.4,Strength,Vegetarian
98,Turkey Sandwich,355,25,31,10,30,Female,24.1,Weight Loss,High Protein
99,Boiled Eggs,205,15,5,12,32,Male,26.1,Toning,Keto
100,Quinoa Salad,305,12,35,8,28,Female,24.6,Endurance,Vegan
"""  # You can paste all 100 rows here

# 3️⃣ FAQ CSV text
faq_csv = """id,question,answer
1,What is the best time to workout?,Morning workouts can boost energy and metabolism throughout the day.
2,How much protein do I need daily?,0.8–1g protein per kg body weight is recommended.
3,Can I lose weight without cardio?,Yes, strength training and calorie deficit can also support fat loss.
4,What foods help muscle growth?,Lean meats, fish, legumes, and protein-rich foods help muscle growth.
5,How often should I work out weekly?,3–5 times per week is effective for most people.
6,Are supplements necessary?,Not necessary, balanced diet can cover most needs.
7,What is a balanced meal?,Protein, carbs, healthy fats, and fiber make a balanced meal.
8,How much water should I drink daily?,2–3 liters depending on activity level and body size.
9,Is it okay to work out when sore?,Light activity can help recovery, but avoid overtraining.
10,How many hours of sleep do I need?,7–9 hours of sleep is essential for recovery.
11,What are the benefits of stretching?,Improves flexibility and reduces injury risk.
12,How do I stay consistent with fitness?,Set small goals and track progress regularly.
13,Can I gain muscle on a vegan diet?,Yes, with proper planning of protein intake.
14,How to track calorie intake effectively?,Apps or journals help track calories accurately.
15,What is progressive overload?,Gradually increase weight, reps, or sets over time.
16,Should I do cardio before or after weights?,Weights before cardio for strength focus; cardio first for stamina.
17,How important is rest day?,Rest days help muscles repair and grow.
18,How do I reduce belly fat?,Spot reduction isn’t possible; focus on overall fat loss.
19,Can I train twice a day?,Yes, if volume and recovery are managed properly.
20,What snacks are good post-workout?,Fruits, nuts, or protein shakes are ideal.
"""  # You can paste all 20 rows here

# Function to save CSV
def save_csv(filename, text):
    filepath = os.path.join(raw_data_path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{filename} created at {filepath}")

# Save all CSVs
save_csv(WORKOUTS_CSV_FILE_NAME, workouts_csv)
save_csv(NUTRITION_CSV_FILE_NAME, nutrition_csv)
save_csv(FAQ_CSV_FILE_NAME, faq_csv)

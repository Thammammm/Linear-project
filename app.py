from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# Define the 11 predefined skills
skills_list = [
    "Active Learning", "Analytical", "Communication", "Complex problem solving",
    "Creativity", "Digital quotience literacy", "Entrepreneurship", "Integrity",
    "Interpersonal Skills", "Leadership", "Resilience"
]

# Function to read the CSV and extract skill data
def read_csv(file_name):
    try:
        if not os.path.exists(file_name):
            print(f"Error: The file '{file_name}' was not found.")
            return None
        
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                programs_data = []
                for row in reader:
                    program_name = row[0]
                    skill_scores = list(map(int, row[1:12]))  # Read scores for 11 skills
                    programs_data.append((program_name, skill_scores))
                return programs_data
        except UnicodeDecodeError:
            print("UTF-8 encoding failed, trying ISO-8859-1 encoding...")
            with open(file_name, newline='', encoding='ISO-8859-1') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                programs_data = []
                for row in reader:
                    program_name = row[0]
                    skill_scores = list(map(int, row[1:12]))  # Read scores for 11 skills
                    programs_data.append((program_name, skill_scores))
                return programs_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to calculate dot product
def dot_product(vector1, vector2):
    return sum([vector1[i] * vector2[i] for i in range(len(vector1))])

# Function to calculate vector magnitude
def magnitude(vector):
    return sum([x * x for x in vector]) ** 0.5

# Function to calculate cosine similarity
def cosine_similarity(vector1, vector2):
    dot_prod = dot_product(vector1, vector2)
    magnitude1 = magnitude(vector1)
    magnitude2 = magnitude(vector2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_prod / (magnitude1 * magnitude2)

# Main route to handle the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user input for skills
            user_vector = [int(request.form.get(skill, 0)) for skill in skills_list]
            csv_file_name = 'skillmapping.csv'
            programs_data = read_csv(csv_file_name)

            if programs_data is None:
                return render_template('index.html', error="Skill mapping data not found.")

            # Calculate similarities
            similarities = []
            for program, skill_scores in programs_data:
                similarity = cosine_similarity(user_vector, skill_scores)
                similarities.append((program, similarity))

            # Sort and display the results
            sorted_programs = sorted(similarities, key=lambda x: x[1], reverse=True)
            return render_template('index.html', skills=skills_list, results=sorted_programs)

        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html', skills=skills_list)

if __name__ == '__main__':
    app.run(debug=True)

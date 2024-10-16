from flask import Flask, request, render_template
import os
import csv
import numpy as np

app = Flask(__name__)

skills_list = [
    "Active Learning", "Analytical", "Communication", "Complex problem solving",
    "Creativity", "Digital quotience literacy", "Entrepreneurship", "Integrity",
    "Interpersonal Skills", "Leadership", "Resilience"
]


def read_csv(file_name):
    try:
        if not os.path.exists(file_name):
            print(f"Error: The file '{file_name}' was not found.")
            return None
        
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                programs_data = []
                for row in reader:
                    program_name = row[0]
                    skill_scores = np.array(list(map(int, row[1:12]))) 
                    programs_data.append((program_name, skill_scores))
                return programs_data
        except UnicodeDecodeError:
            print("UTF-8 encoding failed, trying ISO-8859-1 encoding...")
            with open(file_name, newline='', encoding='ISO-8859-1') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                programs_data = []
                for row in reader:
                    program_name = row[0]
                    skill_scores = np.array(list(map(int, row[1:12])))  
                    programs_data.append((program_name, skill_scores))
                return programs_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def cosine_similarity(vector1, vector2):
    dot_prod = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_prod / (magnitude1 * magnitude2)

def get_similarity_results(user_vector):
    csv_file_name = 'skillmapping.csv'
    programs_data = read_csv(csv_file_name)
    
    if programs_data is None:
        return None

    similarities = []
    for program, skill_scores in programs_data:
        similarity = float(cosine_similarity(user_vector, skill_scores))
        similarities.append((program, similarity))

    return sorted(similarities, key=lambda x: x[1], reverse=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = [int(request.form.get(skill, 0)) for skill in skills_list]
        results = get_similarity_results(np.array(user_input))
        return render_template('index.html', skills=skills_list, results=results)
    
    return render_template('index.html', skills=skills_list)

if __name__ == '__main__':
    app.run(debug=True)

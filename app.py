from flask import Flask, request, render_template
import os
import csv
import numpy as np

app = Flask(__name__)


# ฟังก์ชันสำหรับอ่านไฟล์ CSV
def read_csv(file_name):
    try:
        if not os.path.exists(file_name):
            print(f"Error: The file '{file_name}' was not found.")
            return None
        
        programs_data = {}
        
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                program_name = row[0]
                skill_scores = np.array(list(map(int, row[1:12])))
                
                if program_name not in programs_data:
                    programs_data[program_name] = []
                programs_data[program_name].append(skill_scores)
                
        return programs_data
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# ฟังก์ชันสำหรับคำนวณ cosine similarity
def cosine_similarity(vector1, vector2):
    dot_prod = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    cosine = dot_prod / (magnitude1 * magnitude2)
    return cosine * (min(magnitude1, magnitude2) / max(magnitude1, magnitude2))

# ฟังก์ชันหลักในการคำนวณ
def get_similarity_results(user_vector):
    csv_file_name = 'skillmapping.csv'  # เส้นทางไปยังไฟล์ CSV ของคุณ
    programs_data = read_csv(csv_file_name)
    
    if programs_data is None:
        return None

    average_programs = {}
    for program, scores in programs_data.items():
        average_scores = np.mean(scores, axis=0)  
        average_programs[program] = average_scores

    similarities = []
    for program, avg_scores in average_programs.items():
        similarity = float(cosine_similarity(user_vector, avg_scores)) 
        similarities.append((program, similarity))
    
    return sorted(similarities, key=lambda x: x[1], reverse=True)

# Route สำหรับฟอร์มในหน้าเว็บ
@app.route('/', methods=['GET', 'POST'])
def index():
    skills_list = [
        "Active Learning - การเรียนรู้เชิงลึก", "Analytical - การวิเคราะห์", "Communication - การสื่อสาร", "Complex problem solving - การแก้ไขปัญหาที่ซับซ้อน",
        "Creativity - ความคิดสร้างสรรค์", "Digital quotience literacy - ความรู้ความสามารถด้านดิจิทัล", "Entrepreneurship - การเป็นผู้ประกอบการ", "Integrity - ความซื่อสัตย์",
        "Interpersonal Skills - ทักษะความสัมพันธืระหว่างบุคคล", "Leadership - การเป็นผู้นำ", "Resilience - การปรับตัว"
    ]
    
    if request.method == 'POST':
        user_input = [int(request.form.get(skill, 0)) for skill in skills_list]
        results = get_similarity_results(np.array(user_input))
        return render_template('index.html', skills=skills_list, results=results)
    
    return render_template('index.html', skills=skills_list)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import ratemyprofessor

app = Flask(__name__)

@app.route('/')
def get_professor_details():
    # Retrieve query parameters
    school_name = request.args.get('school_name')
    professor_name = request.args.get('professor_name')

    if not school_name or not professor_name:
        return jsonify({"error": "Missing school name or professor name"}), 400

    # Find school and professor
    school = ratemyprofessor.get_school_by_name(school_name)
    professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)

    if professor is not None:
        details = {
            "name": professor.name,
            "department": professor.department,
            "school": professor.school.name,
            "rating": professor.rating,
            "difficulty": professor.difficulty,
            "total_ratings": professor.num_ratings,
            "would_take_again": round(professor.would_take_again, 1) if professor.would_take_again is not None else "N/A"
        }
        return jsonify(details)
    else:
        return jsonify({"error": "Professor not found"}), 404

@app.route('/get_school_by_name')
def get_school_by_name():
    school_name = request.args.get('school_name')
    if not school_name:
        return jsonify({"error": "Missing school name"}), 400

    school = ratemyprofessor.get_school_by_name(school_name)
    if school is not None:
        print(dir(school))
        return jsonify({"school_name": school.name})
    else:
        return jsonify({"error": "School not found"}), 404

@app.route('/get_schools_by_name')
def get_schools_by_name():
    school_name = request.args.get('school_name')
    if not school_name:
        return jsonify({"error": "Missing school name"}), 400

    schools = ratemyprofessor.get_schools_by_name(school_name)
    if schools:
        return jsonify({"schools": [school.name for school in schools]})
    else:
        return jsonify({"error": "No schools found"}), 404

@app.route('/get_professor_by_school_and_name')
def get_professor_by_school_and_name():
    school_name = request.args.get('school_name')
    professor_name = request.args.get('professor_name')

    if not school_name or not professor_name:
        return jsonify({"error": "Missing school name or professor name"}), 400

    school = ratemyprofessor.get_school_by_name(school_name)
    professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)

    if professor is not None:
        professor_details = {
            "name": professor.name,
            "department": professor.department,
            "school": professor.school.name,
            "rating": professor.rating,
            "difficulty": professor.difficulty,
            "total_ratings": professor.num_ratings,
            "would_take_again": round(professor.would_take_again, 1) if professor.would_take_again is not None else "N/A"
        }
        return jsonify(professor_details)
    else:
        return jsonify({"error": "Professor not found"}), 404

@app.route('/get_professors_by_school_and_name')
def get_professors_by_school_and_name():
    school_name = request.args.get('school_name')
    professor_name = request.args.get('professor_name')

    if not school_name or not professor_name:
        return jsonify({"error": "Missing school name or professor name"}), 400

    school = ratemyprofessor.get_school_by_name(school_name)
    professors = ratemyprofessor.get_professors_by_school_and_name(school, professor_name)

    if professors:
        professors_details = [{"name": professor.name, "department": professor.department, "rating": professor.rating, "school": professor.school.name, "difficulty": professor.difficulty, "total_ratings": professor.num_ratings, "would_take_again": round(professor.would_take_again, 1) if professor.would_take_again is not None else "N/A"} for professor in professors]
        return jsonify({"professors": professors_details})
    else:
        return jsonify({"error": "No professors found"}), 404
if __name__ == '__main__':
    app.run(debug=True)

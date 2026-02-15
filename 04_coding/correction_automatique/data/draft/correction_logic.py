def auto_correct_exercise(exercise_answer, correct_answer):
    """
    Compares the student's answer to the correct answer and returns feedback.
    This function can be expanded with more complex logic as needed.
    """
    if exercise_answer.strip().lower() == correct_answer.strip().lower():
        return "Correct!"
    else:
        return f"Incorrect. The correct answer is: {correct_answer}"

def generate_correction_report(exercise, student_answer, correct_answer):
    """
    Generates a correction report for the given exercise.
    """
    feedback = auto_correct_exercise(student_answer, correct_answer)
    report = {
        "exercise": exercise,
        "student_answer": student_answer,
        "feedback": feedback
    }
    return report

def apply_correction_logic(exercise_data):
    """
    Applies correction logic to a given exercise data structure.
    The exercise_data should contain the exercise text, student's answer, and the correct answer.
    """
    exercise = exercise_data.get("exercise")
    student_answer = exercise_data.get("student_answer")
    correct_answer = exercise_data.get("correct_answer")

    return generate_correction_report(exercise, student_answer, correct_answer)
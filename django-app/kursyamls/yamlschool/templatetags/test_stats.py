from django import template

register = template.Library()

@register.filter
def total_attempts(students):
    """Calculate total number of attempts across all students."""
    total = 0
    for student_data in students.values():
        total += len(student_data['attempts'])
    return total

@register.filter
def average_grade(students):
    """Calculate average grade across all completed attempts."""
    total_grade = 0
    total_count = 0
    
    for student_data in students.values():
        for attempt in student_data['attempts']:
            if attempt['status'] == 'completed' and attempt.get('grade'):
                total_grade += float(attempt['grade'])
                total_count += 1
    
    return total_grade / total_count if total_count > 0 else 0

@register.filter
def successful_attempts(students):
    """Count number of successful attempts (grade >= 3)."""
    successful = 0
    
    for student_data in students.values():
        for attempt in student_data['attempts']:
            if attempt['status'] == 'completed' and attempt.get('grade'):
                if float(attempt['grade']) >= 3:
                    successful += 1
    
    return successful 
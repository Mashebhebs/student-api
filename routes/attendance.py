from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Attendance

attendance_blueprint = Blueprint('attendance', __name__)

# Mark attendance
@attendance_blueprint.route('/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')

    if not student_id or not status:
        return jsonify({"error": "Student ID and status are required"}), 400

    attendance = Attendance(student_id=student_id, status=status)
    db.session.add(attendance)
    db.session.commit()

    return jsonify({"message": "Attendance marked"}), 201

# Get attendance records
@attendance_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_attendance():
    records = Attendance.query.all()
    return jsonify([{"id": a.id, "student_id": a.student_id, "date": str(a.date), "status": a.status} for a in records])

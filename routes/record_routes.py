from flask import Blueprint, request,jsonify
from database import get_connection 
from config.auth import check_role

record_bp=Blueprint("record_bp",__name__)

@record_bp.route("/records",methods=["POST"])
def create_record():
    if not check_role(["admin"]):
        return jsonify({"error": "Access denied"}), 403
    
    data = request.json
    user_id=data["user_id"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User does not exist"}), 400
    
    cur.execute("""
        INSERT INTO records (user_id, amount, type, category, date, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["user_id"],
        data["amount"],
        data["type"],
        data["category"],
        data["date"],
        data.get("notes", "")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Record created"})


@record_bp.route("/records", methods=["GET"])
def get_records():
    if not check_role(["admin", "analyst"]):
        return jsonify({"error": "Access denied"}), 403
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            r.id,
            u.user_id,
            u.name,
            u.role,
            r.amount,
            r.type,
            r.category,
            r.date
        FROM records r
        JOIN users u ON r.user_id = u.user_id
    """)
    
    rows = cur.fetchall()
    result = []
    for r in rows:
        result.append({
            "record_id": r[0],
            "user_id": r[1],
            "name": r[2],
            "role": r[3],
            "amount": r[4],
            "type": r[5],
            "category": r[6],
            "date": str(r[7])
        })
    cur.close()
    conn.close()
    return jsonify(result)


@record_bp.route("/records",methods=["DELETE"])
def delete_records():
    if not check_role(["admin"]):
        return jsonify({"error": "Access denied"}), 403
    
    data = request.json
    if not data["user_id"] or not data["category"] or not data["date"]:
        return jsonify({"error": "Something is missing"}), 400
    user_id = data["user_id"]
    category = data["category"]
    date = data["date"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM records WHERE user_id = %s AND category = %s AND date = %s", (user_id,category,date))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    cur.execute("DELETE FROM records WHERE user_id = %s AND category = %s AND date = %s", (user_id,category,date))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"User's {category} record deleted successfully on {date}"}) 
    
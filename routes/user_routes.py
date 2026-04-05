from flask import Blueprint, request, jsonify
from database import get_connection
from config.auth import check_role
from config.prefix_id import generate_user_id

user_bp=Blueprint("user_bp",__name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
    if not check_role(["admin"]):
        return jsonify({"error": "Access denied"}), 403
    
    data = request.json
    if not data:
        return jsonify({"error": "No JSON"}), 400

    print("RAW-", request.data)
    print("JSON-", data)
    
    role = data["role"]
    name=data["name"]
    email=data["email"]
    passcode=data["passcode"]
    
    if not email or "@" not in email or "." not in email:
        return jsonify({"error":"Invalid Email"}), 400
    
    if not len(passcode)<5 or not passcode.isdigit():
        return jsonify({"error":"Invalid Passcode"}), 400
     
    user_id = generate_user_id(role)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = %s", (name,))
    user = cur.fetchone()
    if user:
        cur.close()
        conn.close()
        return jsonify({"error": "Name already exist ! Try for next."}), 400
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if user:
        cur.close()
        conn.close()
        return jsonify({"error": "Email already exist ! Try for next."}), 400
    
    cur.execute("""
        INSERT INTO users (user_id, name, email, passcode, role)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        user_id,
        name,
        email,
        passcode,
        role
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "message": "User created",
        "user_id": user_id
    })
    
@user_bp.route("/users", methods=["DELETE"])
def delete_user():
    if not check_role(["admin"]):
        return jsonify({"error": "Access denied"}), 403
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    user_id = data["user_id"]
    passcode=data["passcode"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s AND passcode = %s", (user_id,passcode))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted successfully"})    

from flask import Blueprint,jsonify,request
from database import get_connection
from config.auth import check_role

login_bp=Blueprint("login_bp",__name__)

@login_bp.route("/login",methods=["POST"])    
def login_credential():
    if not check_role(["admin", "analyst"]):
        return jsonify({"error": "Access denied"}), 403
    data=request.json
    conn=get_connection()
    cur=conn.cursor()
    email=data["email"]
    passcode=data["passcode"]
    cur.execute("""
        SELECT user_id, name, role FROM users
        WHERE email=%s AND passcode=%s
    """, (email,passcode))
    user=cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid Inputs"}), 401

    return jsonify({
        "user_id": user[0],
        "name": user[1],
        "role": user[2]
    })

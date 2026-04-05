from flask import Blueprint, jsonify, request
from database import get_connection
from config.auth import check_role

dashboard_bp=Blueprint("dashboard_bp",__name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    
    if not check_role(["admin", "analyst","viewer"]):
        return jsonify({"error": "Access denied"}), 403
    
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM records WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User does not exist"}), 400
    
    cur.execute("SELECT SUM(amount) FROM records WHERE type='income' AND user_id = %s",(user_id,))
    income = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM records WHERE type='expense'AND user_id = %s",(user_id,))
    expense = cur.fetchone()[0] or 0
    cur.close()
    conn.close()

    return jsonify({
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    })

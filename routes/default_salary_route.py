from flask import request,Blueprint,jsonify
from database import get_connection
from config.auth import check_role

df_sal_bp=Blueprint("df_sal_bp",__name__)

@df_sal_bp.route("/df_sal",methods=["POST"])
def default_increment():
    if not check_role(["admin"]):
        return jsonify({"error": "Access denied"}), 403
    
    data=request.json
    amount=data["amount"]
    date=data["date"]
    if not amount or not date or not amount.isdigit():
        return jsonify({"error": "Wrong Inputs"}), 400
    
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    
    for user in users:
        cur.execute("""
            INSERT INTO records (user_id, amount, type, category, date, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user[0],
            amount,
            "income",
            "salary",
            date,
            "Default salary"
        ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": f"Salary added for {len(users)} users"})
    


#Simple Code for test all the functions only!


# from flask import Flask,request,jsonify
# import random
# from database import get_connection
# import json

# app=Flask(__name__)

# def check_role(allowed_role):
#     role=request.headers.get("role") #postman 
#     if role not in allowed_role:
#         return False
#     return True

# def generate_user_id(role):
#     prefix_name={
#         "admin":"AD",
#         "analyst":"AN",
#         "viewer":"VI"      
#     }
#     prefix=prefix_name.get(role.lower())
#     number = random.randint(10000, 99999)   
#     return f"{prefix}{number}"
    
    
# @app.route("/users", methods=["POST"])
# def create_user():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No JSON"}), 400

#     print("RAW:", request.data)
#     print("JSON:", data)
    
#     role = data.get("role")
#     user_id = generate_user_id(role)
    
#     conn = get_connection()
#     cur = conn.cursor()
    
#     cur.execute("SELECT * FROM users WHERE name = %s", (data["name"],))
#     user = cur.fetchone()
#     if user:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "User already exist ! Try for next."}), 400
    
    
#     cur.execute("""
#         INSERT INTO users (user_id, name, email, passcode, role)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (
#         user_id,
#         data.get("name"),
#         data.get("email"),
#         data.get("passcode"),
#         role
#     ))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return jsonify({
#         "message": "User created",
#         "user_id": user_id
#     })
# @app.route("/users", methods=["DELETE"])
# def delete_user():
#     if not check_role(["admin"]):
#         return jsonify({"error": "Access denied"}), 403
#     data = request.get_json()
#     if not data or "user_id" not in data:
#         return jsonify({"error": "user_id is required"}), 400
    
#     user_id = data["user_id"]
#     passcode=data["passcode"]
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users WHERE user_id = %s AND passcode = %s", (user_id,passcode))
#     user = cur.fetchone()
#     if not user:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "User not found"}), 404
#     cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return jsonify({"message": f"User {user_id} deleted successfully"})    


# @app.route("/login",methods=["POST"])    
# def login_credential():
#     data=request.json
#     conn=get_connection()
#     cur=conn.cursor()
    
#     cur.execute("""
#         SELECT user_id, name, role FROM users
#         WHERE email=%s AND passcode=%s
#     """, (data["email"], data["passcode"]))
#     user=cur.fetchone()
    
#     cur.close()
#     conn.close()

#     if not user:
#         return jsonify({"error": "Invalid credentials"}), 401

#     return jsonify({
#         "user_id": user[0],
#         "name": user[1],
#         "role": user[2]
#     })


# @app.route("/records", methods=["POST"])
# def create_record():
#     if not check_role(["admin"]):
#         return jsonify({"error": "Access denied"}), 403
#     data = request.json
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM users WHERE user_id = %s", (data["user_id"],))
#     user = cur.fetchone()
#     if not user:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "User does not exist"}), 400
    
#     cur.execute("""
#         INSERT INTO records (user_id, amount, type, category, date, notes)
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """, (
#         data["user_id"],
#         data["amount"],
#         data["type"],
#         data["category"],
#         data["date"],
#         data.get("notes", "")
#     ))

#     conn.commit()
#     cur.close()
#     conn.close()
    

#     return jsonify({"message": "Record created"})

# @app.route("/records", methods=["GET"])
# def get_records():
#     if not check_role(["admin", "analyst"]):
#         return jsonify({"error": "Access denied"}), 403
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT 
#             r.id,
#             u.user_id,
#             u.name,
#             u.role,
#             r.amount,
#             r.type,
#             r.category,
#             r.date
#         FROM records r
#         JOIN users u ON r.user_id = u.user_id
#     """)
#     rows = cur.fetchall()
#     result = []
#     for r in rows:
#         result.append({
#             "record_id": r[0],
#             "user_id": r[1],
#             "name": r[2],
#             "role": r[3],
#             "amount": r[4],
#             "type": r[5],
#             "category": r[6],
#             "date": str(r[7])
#         })

#     cur.close()
#     conn.close()
#     return jsonify(result)


# @app.route("/records",method=["DELETE"])
# def delete_records():
#     if not check_role(["admin"]):
#         return jsonify({"error": "Access denied"}), 403

#     data = request.get_json()
#     if not data["user_id"] or not data["category"] or not data["date"]:
#         return jsonify({"error": "Something is missing"}), 400
#     user_id = data.get("user_id")
#     category = data.get("category")
#     date = data.get("date")
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM records WHERE user_id = %s AND category = %s AND date = %s", (user_id,category,date))
#     user = cur.fetchone()
#     if not user:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "User not found"}), 404
#     cur.execute("DELETE FROM records WHERE user_id = %s AND category = %s AND date = %s", (user_id,category,date))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return jsonify({"message": f"User's {category} record deleted successfully on {date}"}) 
    
    

# @app.route("/dashboard", methods=["GET"])
# def dashboard():
    
#     if not check_role(["admin", "analyst","viewer"]):
#         return jsonify({"error": "Access denied"}), 403

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT SUM(amount) FROM records WHERE type='income'")
#     income = cur.fetchone()[0] or 0
#     cur.execute("SELECT SUM(amount) FROM records WHERE type='expense'")
#     expense = cur.fetchone()[0] or 0
#     cur.close()
#     conn.close()

#     return jsonify({
#         "total_income": income,
#         "total_expense": expense,
#         "net_balance": income - expense
#     })


# if __name__ == "__main__":
#     app.run(debug=True)
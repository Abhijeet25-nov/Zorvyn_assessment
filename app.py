from flask import Flask
from routes.user_routes import user_bp
from routes.record_routes import record_bp
from routes.dashboard_route import dashboard_bp
from routes.default_salary_route import df_sal_bp
from config.login import login_bp

app = Flask(__name__)


app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(record_bp)
app.register_blueprint(df_sal_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
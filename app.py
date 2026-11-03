import os, sqlite3, secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-deploying")
DB = os.path.join(os.path.dirname(__file__), "store.db")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "GantiPassword123!")

GAMES = {
    "Mobile Legends": [("86 Diamonds", 20000), ("172 Diamonds", 39000), ("257 Diamonds", 58000), ("344 Diamonds", 77000)],
    "Free Fire": [("70 Diamonds", 10000), ("140 Diamonds", 20000), ("355 Diamonds", 49000), ("720 Diamonds", 97000)],
    "PUBG Mobile": [("60 UC", 16000), ("325 UC", 79000), ("660 UC", 158000)],
    "Genshin Impact": [("60 Genesis Crystals", 16000), ("300 + 30 Crystals", 79000)],
    "Roblox": [("80 Robux", 16000), ("400 Robux", 79000), ("800 Robux", 159000)]
}

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, customer TEXT,
            game TEXT, item TEXT, player_id TEXT, server_id TEXT, amount INTEGER,
            payment TEXT, status TEXT DEFAULT 'Menunggu pembayaran', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html", games=GAMES)

@app.route("/buat-pesanan", methods=["POST"])
def create_order():
    customer = request.form.get("customer", "").strip()
    game = request.form.get("game", "")
    item = request.form.get("item", "")
    player_id = request.form.get("player_id", "").strip()
    server_id = request.form.get("server_id", "").strip()
    payment = request.form.get("payment", "QRIS")
    valid = next((price for name, price in GAMES.get(game, []) if name == item), None)
    if not customer or not player_id or valid is None:
        flash("Periksa nama, ID pemain, game, dan nominal.", "error")
        return redirect(url_for("index"))
    code = "PIZA-" + secrets.token_hex(4).upper()
    with db() as con:
        con.execute("INSERT INTO orders(code,customer,game,item,player_id,server_id,amount,payment) VALUES(?,?,?,?,?,?,?,?)",
                    (code, customer, game, item, player_id, server_id, valid, payment))
    return redirect(url_for("order_detail", code=code))

@app.route("/pesanan/<code>")
def order_detail(code):
    with db() as con:
        order = con.execute("SELECT * FROM orders WHERE code=?", (code,)).fetchone()
    if not order: abort(404)
    return render_template("order.html", order=order)

@app.route("/cek-pesanan", methods=["GET", "POST"])
def check_order():
    order = None
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        with db() as con:
            order = con.execute("SELECT * FROM orders WHERE code=?", (code,)).fetchone()
        if not order: flash("Kode pesanan tidak ditemukan.", "error")
    return render_template("check.html", order=order)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and secrets.compare_digest(request.form.get("password", ""), ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Username atau password salah.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin():
    with db() as con:
        orders = con.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    return render_template("admin.html", orders=orders)

@app.route("/admin/status/<int:order_id>", methods=["POST"])
@admin_required
def update_status(order_id):
    status = request.form.get("status")
    allowed = ["Menunggu pembayaran", "Pembayaran diterima", "Diproses", "Selesai", "Dibatalkan"]
    if status not in allowed: abort(400)
    with db() as con:
        con.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    flash("Status pesanan diperbarui.", "success")
    return redirect(url_for("admin"))

@app.template_filter("rupiah")
def rupiah(value):
    return "Rp" + f"{value:,.0f}".replace(",", ".")

# Ensure the database exists for both local runs and production WSGI servers.
init_db()

if __name__ == "__main__":
    app.run(debug=False)

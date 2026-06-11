from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    shipment = None

    if request.method == "POST":

        tracking_number = request.form["tracking_number"]

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT tracking_number, status, location
            FROM shipments
            WHERE tracking_number = ?
            """,
            (tracking_number,)
        )

        shipment = cursor.fetchone()

        conn.close()

    return render_template(
        "index.html",
        shipment=shipment
    )


@app.route("/dispatcher", methods=["GET", "POST"])
def dispatcher():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    if request.method == "POST":

        shipment_id = request.form["shipment_id"]

        new_status = request.form["status"]

        cursor.execute(
            """
            UPDATE shipments
            SET status = ?
            WHERE id = ?
            """,
            (new_status, shipment_id)
        )

        conn.commit()

        conn.close()

        return redirect("/dispatcher")

    cursor.execute(
        """
        SELECT id, tracking_number, status, location
        FROM shipments
        """
    )

    shipments = cursor.fetchall()

    conn.close()

    return render_template(
        "dispatcher.html",
        shipments=shipments
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
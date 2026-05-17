from flask import Flask, render_template, request, redirect
import sqlite3
from geopy.distance import geodesic
from model import predict_time

app = Flask(__name__)

hospitals = [
    {"name":"AIIMS Delhi","location":(28.5672,77.2100)},
    {"name":"Apollo Chennai","location":(13.0674,80.2376)},
    {"name":"Kokilaben Hospital Mumbai","location":(19.1370,72.8258)},
    {"name":"Fortis Bangalore","location":(12.9345,77.6113)},
    {"name":"Medanta Gurgaon","location":(28.4380,77.0400)},
    {"name":"Narayana Health Bangalore","location":(12.8452,77.6602)},
    {"name":"AMRI Hospital Kolkata","location":(22.5383,88.3656)},
    {"name":"Care Hospital Hyderabad","location":(17.4241,78.4486)},
    {"name":"Ruby Hall Clinic Pune","location":(18.5308,73.8777)},
    {"name":"KIMS Hospital Trivandrum","location":(8.5241,76.9366)},
    {"name":"Manipal Hospital Delhi","location":(28.5665,77.2433)},
    {"name":"Apollo Ahmedabad","location":(23.0225,72.5714)},
    {"name":"Fortis Mohali","location":(30.7046,76.7179)},
    {"name":"AIIMS Bhopal","location":(23.2599,77.4126)},
    {"name":"SMS Hospital Jaipur","location":(26.9124,75.8200)},
    {"name":"PGI Chandigarh","location":(30.7612,76.7750)},
    {"name":"Apollo Bhubaneswar","location":(20.2961,85.8245)},
    {"name":"Lilavati Hospital Mumbai","location":(19.0515,72.8295)},
    {"name":"Yashoda Hospital Hyderabad","location":(17.4399,78.4983)},
    {"name":"Max Hospital Delhi","location":(28.5666,77.2430)}
]

def nearest_hospital(user_loc):
    nearest = hospitals[0]
    min_dist = geodesic(user_loc, hospitals[0]["location"]).km
    for h in hospitals:
        dist = geodesic(user_loc, h["location"]).km
        if dist < min_dist:
            min_dist = dist
            nearest = h
    return nearest, min_dist

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/save_user", methods=["POST"])
def save_user():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?)", (name, email, password))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    # User coordinates from form
    user_lat = float(request.form["lat"])
    user_lon = float(request.form["lon"])
    user_loc = (user_lat, user_lon)

    # Find nearest hospital
    hospital, distance = nearest_hospital(user_loc)
    hospital_lat, hospital_lon = hospital["location"]

    # Optional: predicted travel time using ML model
    time_of_day = request.form["time"]
    weather = request.form["weather"]
    traffic = request.form["traffic"]
    travel_time = predict_time(distance, time_of_day, weather, traffic)

    return render_template(
        "dashboard.html",
        user_lat=user_lat,
        user_lon=user_lon,
        hosp_lat=hospital_lat,
        hosp_lon=hospital_lon,
        hospital_name=hospital["name"],
        distance=round(distance, 2),
        travel_time=round(travel_time, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import sqlite3
import os
from geopy.distance import geodesic
from model import predict_time

app = Flask(__name__)

# DB init
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

hospitals = [
    {"name":"PGI Multispeciality Hospital Amritsar","location":(31.7698,74.9184)},
    {"name":"Global Multispeciality Hospital Kochi","location":(9.9096,76.1769)},
    {"name":"Fortis Medical Centre Dehradun","location":(30.0882,78.141)},
    {"name":"MIOT Super Speciality Hospital Ludhiana","location":(30.7409,75.6917)},
    {"name":"Columbia Asia Heart Institute Nagpur","location":(21.106,78.9756)},
    {"name":"SMS General Hospital Srinagar","location":(34.058,74.9326)},
    {"name":"Kauvery Multispeciality Hospital Bangalore","location":(13.0602,77.5652)},
    {"name":"Max Hospital Vadodara","location":(22.5328,73.3342)},
    {"name":"Hinduja Heart Institute Ahmedabad","location":(22.8854,72.4405)},
    {"name":"Metro Heart Institute Pune","location":(18.6866,73.6867)},
    {"name": "AIIMS Hospital Delhi", "location": (28.6139, 77.2090)},
    {"name": "Apollo Hospital Chennai", "location": (13.0674, 80.2376)},
    {"name": "Fortis Hospital Bangalore", "location": (12.9345, 77.6113)},
    hospitals = [
    {"name": "PGI Multispeciality Hospital Amritsar", "location": (31.7698, 74.9184)},
    {"name": "Global Multispeciality Hospital Kochi", "location": (9.9096, 76.1769)},
    {"name": "Fortis Medical Centre Dehradun", "location": (30.0882, 78.141)},
    {"name": "MIOT Super Speciality Hospital Ludhiana", "location": (30.7409, 75.6917)},
    {"name": "Columbia Asia Heart Institute Nagpur", "location": (21.106, 78.9756)},
    {"name": "SMS General Hospital Srinagar", "location": (34.058, 74.9326)},
    {"name": "Kauvery Multispeciality Hospital Bangalore", "location": (13.0602, 77.5652)},
    {"name": "Max Hospital Vadodara", "location": (22.5328, 73.3342)},
    {"name": "Hinduja Heart Institute Ahmedabad", "location": (22.8854, 72.4405)},
    {"name": "Metro Heart Institute Pune", "location": (18.6866, 73.6867)},
    {"name": "Star Super Speciality Hospital Surat", "location": (21.2513, 72.7359)},
    {"name": "BLK City Hospital Hyderabad", "location": (17.2224, 78.7148)},
    {"name": "Metro Super Speciality Hospital Ranchi", "location": (23.2876, 85.5133)},
    {"name": "Vikram General Hospital Varanasi", "location": (25.1042, 82.818)},
    {"name": "SMS Heart Institute Trivandrum", "location": (8.4057, 77.0944)},
    {"name": "Wockhardt City Hospital Ranchi", "location": (23.3935, 85.188)},
    {"name": "PGI Heart Institute Amritsar", "location": (31.4173, 75.1134)},
    {"name": "AIIMS City Hospital Dehradun", "location": (30.2067, 77.787)},
    {"name": "KIMS Multispeciality Hospital Surat", "location": (21.3151, 72.883)},
    {"name": "Care Hospital Srinagar", "location": (34.1416, 74.7054)},
    {"name": "Sunshine Heart Institute Guwahati", "location": (26.2548, 91.7988)},
    {"name": "AIG Hospital Jammu", "location": (32.6615, 75.0859)},
    {"name": "AIIMS Heart Institute Bangalore", "location": (13.0006, 77.7255)},
    {"name": "Manipal General Hospital Jammu", "location": (32.6838, 74.6127)},
    {"name": "Hiranandani General Hospital Indore", "location": (22.6977, 75.8816)},
    {"name": "Breach Candy Heart Institute Chennai", "location": (12.9546, 80.2252)},
    {"name": "Star Heart Institute Amritsar", "location": (31.4185, 74.7649)},
    {"name": "Bombay Super Speciality Hospital Bhubaneswar", "location": (20.3522, 85.7178)},
    {"name": "Bombay City Hospital Hyderabad", "location": (17.2392, 78.4383)},
    {"name": "Bombay Hospital Kanpur", "location": (26.349, 80.135)},
    {"name": "Ruby Hall Hospital Jammu", "location": (32.6224, 74.6823)},
    {"name": "Manipal Medical Centre Jammu", "location": (32.5811, 74.6599)},
    {"name": "PGI Multispeciality Hospital Dehradun", "location": (30.2216, 78.0394)},
    {"name": "SRM Super Speciality Hospital Nagpur", "location": (21.2461, 78.904)},
    {"name": "Sparsh Super Speciality Hospital Surat", "location": (21.1713, 72.6057)},
    {"name": "Medicover Hospital Nashik", "location": (19.8598, 73.6024)},
    {"name": "Hiranandani Medical Centre Ranchi", "location": (23.211, 85.3861)},
    {"name": "KEM General Hospital Kanpur", "location": (26.5916, 80.3152)},
    {"name": "Narayana Medical Centre Mysore", "location": (12.3079, 76.4251)},
    {"name": "Manipal City Hospital Rajkot", "location": (22.3041, 70.8979)},
    {"name": "CMC City Hospital Bangalore", "location": (13.0588, 77.3483)},
    {"name": "Sir Ganga Ram City Hospital Bangalore", "location": (13.0426, 77.4272)},
    {"name": "SIMS General Hospital Rajkot", "location": (22.5184, 70.6188)},
    {"name": "Wockhardt Super Speciality Hospital Srinagar", "location": (34.2923, 74.9787)},
    {"name": "Care City Hospital Agra", "location": (27.0075, 78.2811)},
    {"name": "AIIMS Medical Centre Mumbai", "location": (19.2686, 73.0702)},
    {"name": "PSG Multispeciality Hospital Ahmedabad", "location": (23.1202, 72.7433)},
    {"name": "Sunshine Medical Centre Coimbatore", "location": (11.1499, 77.021)},
    {"name": "Sparsh City Hospital Kanpur", "location": (26.6393, 80.3832)},
    {"name": "Vikram Medical Centre Agra", "location": (27.3901, 78.2768)},
    {"name": "Sharda Super Speciality Hospital Vadodara", "location": (22.2928, 73.1542)},
        {"name": "Sharda Super Speciality Hospital Vadodara", "location": (22.2928, 73.1542)},
    {"name": "Medicover City Hospital Meerut", "location": (28.8486, 77.6127)},
    {"name": "KIMS General Hospital Coimbatore", "location": (11.1205, 76.854)},
    {"name": "Columbia Asia General Hospital Nagpur", "location": (21.0152, 79.1249)},
    {"name": "Jaslok Multispeciality Hospital Jaipur", "location": (27.0574, 75.7813)},
    {"name": "Amrita Hospital Srinagar", "location": (33.9276, 74.9012)},
    {"name": "Max Multispeciality Hospital Kochi", "location": (10.0643, 76.0318)},
    {"name": "Breach Candy Heart Institute Srinagar", "location": (33.9698, 74.9817)},
    {"name": "Sahyadri Hospital Dehradun", "location": (30.3364, 78.0661)},
    {"name": "Aster General Hospital Rajkot", "location": (22.1842, 70.7926)},
    {"name": "Wockhardt Super Speciality Hospital Vadodara", "location": (22.5181, 73.278)},
    {"name": "Sagar General Hospital Dehradun", "location": (30.555, 77.85)},
    {"name": "BLK Super Speciality Hospital Jammu", "location": (32.6313, 75.0243)},
    {"name": "Artemis Medical Centre Ahmedabad", "location": (22.9497, 72.4668)},
    {"name": "AIG Super Speciality Hospital Ranchi", "location": (23.5235, 85.5066)},
    {"name": "Star Heart Institute Pune", "location": (18.3671, 73.6355)},
    {"name": "AMRI City Hospital Chandigarh", "location": (30.9233, 76.5338)},
    {"name": "Apollo General Hospital Mysore", "location": (12.376, 76.5441)},
    {"name": "Columbia Asia Hospital Bhubaneswar", "location": (20.0587, 85.9813)},
    {"name": "KIMS Heart Institute Rajkot", "location": (22.1858, 71.0326)},
    {"name": "Narayana Heart Institute Chennai", "location": (12.9272, 80.2257)},
    {"name": "SIMS City Hospital Agra 72", "location": (26.9864, 78.2748)},
    {"name": "Sir Ganga Ram Hospital Ludhiana 73", "location": (30.8494, 75.8168)},
    {"name": "Kauvery Super Speciality Hospital Ranchi 74", "location": (23.5713, 85.468)},
    {"name": "Kokilaben Heart Institute Ahmedabad 75", "location": (22.7991, 72.7776)},
    {"name": "Hiranandani Medical Centre Mysore 76", "location": (12.0869, 76.4714)},
    {"name": "SMS Heart Institute Delhi 77", "location": (28.7289, 77.2572)},
    {"name": "Sahyadri General Hospital Bhubaneswar 78", "location": (20.0639, 85.853)},
    {"name": "Sahyadri Medical Centre Bhubaneswar 79", "location": (20.0859, 85.6171)},
    {"name": "Sharda Medical Centre Ludhiana 80", "location": (31.0018, 75.8371)},
    {"name": "Hinduja Heart Institute Ranchi 81", "location": (23.3267, 85.1366)},
    {"name": "Kauvery General Hospital Ludhiana 82", "location": (30.674, 76.0746)},
    {"name": "Continental City Hospital Meerut 83", "location": (28.9173, 77.7629)},
    {"name": "AIIMS Heart Institute Nashik 84", "location": (20.082, 73.8379)},
    {"name": "Apollo Hospital Chandigarh 85", "location": (30.9136, 76.8382)},
    {"name": "Sunshine City Hospital Coimbatore 86", "location": (10.9541, 77.0216)},
    {"name": "Artemis Heart Institute Rajkot 87", "location": (22.363, 70.9602)},
    {"name": "Artemis City Hospital Lucknow 88", "location": (26.727, 80.7973)},
    {"name": "Sagar Multispeciality Hospital Mumbai 89", "location": (18.9883, 72.9479)},
    {"name": "Hinduja Super Speciality Hospital Amritsar 90", "location": (31.3916, 75.0272)},
    {"name": "Max Super Speciality Hospital Pune 91", "location": (18.6184, 73.9145)},
    {"name": "Star Hospital Amritsar 92", "location": (31.7817, 74.761)},
    {"name": "Kauvery Hospital Lucknow 93", "location": (26.8743, 80.978)},
    {"name": "Vikram City Hospital Agra 94", "location": (27.106, 78.1782)},
    {"name": "Global Medical Centre Dehradun 95", "location": (30.3409, 77.8993)},
    {"name": "Global Hospital Indore 96", "location": (22.5791, 75.7889)},
    {"name": "Vikram Hospital Coimbatore 97", "location": (10.92, 77.1478)},
    {"name": "Kokilaben Heart Institute Meerut 98", "location": (29.1827, 77.4956)},
    {"name": "Bombay Medical Centre Pune 99", "location": (18.6084, 73.8413)},
    {"name": "Medanta Multispeciality Hospital Chandigarh 100", "location": (30.7812, 76.7969)},
]
   
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

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user_lat = float(request.form["lat"])
    user_lon = float(request.form["lon"])
    user_loc = (user_lat, user_lon)
    hospital, distance = nearest_hospital(user_loc)
    hospital_lat, hospital_lon = hospital["location"]
    time_of_day = request.form["time"]
    weather = request.form["weather"]
    traffic = request.form["traffic"]
    travel_time = predict_time(distance, time_of_day, weather, traffic)
    return render_template(
        "dashboard.html",
        user_lat=user_lat, user_lon=user_lon,
        hosp_lat=hospital_lat, hosp_lon=hospital_lon,
        hospital_name=hospital["name"],
        distance=round(distance, 2),
        travel_time=round(travel_time, 2)
    )

if __name__ == "__main__":
    app.run()

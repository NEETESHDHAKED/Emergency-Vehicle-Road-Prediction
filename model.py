import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("traffic_dataset_5000.csv")

le_time = LabelEncoder()
le_weather = LabelEncoder()
le_traffic = LabelEncoder()

data["time_of_day"] = le_time.fit_transform(data["time_of_day"])
data["weather"] = le_weather.fit_transform(data["weather"])
data["traffic_level"] = le_traffic.fit_transform(data["traffic_level"])

x = data[["distance","time_of_day","weather","traffic_level"]]
y = data["travel_time"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(x,y)

def predict_time(distance,time,weather,traffic):

    speed = 50  # km per hour

    # Traffic effect
    if traffic == "high":
        speed -= 20
    elif traffic == "medium":
        speed -= 10

    # Weather effect
    if weather == "rain":
        speed -= 10
    elif weather == "fog":
        speed -= 15

    # Time of day effect
    if time == "night":
        speed += 5
    elif time == "evening":
        speed -= 5

    if speed < 10:
        speed = 10

    travel_time = distance / speed   # HOURS

    return travel_time


print(predict_time(5,"morning","rain","high"))

print(data["distance"].min())
print(data["distance"].max())

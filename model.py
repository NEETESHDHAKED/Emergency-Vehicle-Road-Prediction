import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


# ---------------- LOAD DATASET ----------------

data = pd.read_csv("traffic_dataset_5000.csv")

required_columns = [
    "distance",
    "time_of_day",
    "weather",
    "traffic_level",
    "travel_time"
]

missing = set(required_columns) - set(data.columns)

if missing:
    raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

data = data[required_columns].dropna().copy()

# Standardize category text
for column in ["time_of_day", "weather", "traffic_level"]:
    data[column] = data[column].astype(str).str.strip().str.lower()

# travel_time (minutes) = distance (km) x pace (min/km).
# Pace sirf time/weather/traffic par depend karta hai, distance par nahi.
# Isliye model pace seekhta hai, taaki 15 km se lambi trips bhi sahi scale hon.
data["pace"] = data["travel_time"] / data["distance"]
TRAINED_MAX_KM = float(data["distance"].max())

# ---------------- ENCODE CATEGORIES ----------------

le_time = LabelEncoder()
le_weather = LabelEncoder()
le_traffic = LabelEncoder()

data["time_of_day"] = le_time.fit_transform(data["time_of_day"])
data["weather"] = le_weather.fit_transform(data["weather"])
data["traffic_level"] = le_traffic.fit_transform(data["traffic_level"])

# ---------------- TRAIN MODEL ----------------

X = data[["time_of_day", "weather", "traffic_level"]]

y = data["pace"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# ---------------- PREDICT TRAVEL TIME ----------------

def predict_time(distance, time, weather, traffic):
    """Return predicted travel time in MINUTES for a distance in km."""
    time = str(time).strip().lower()
    weather = str(weather).strip().lower()
    traffic = str(traffic).strip().lower()

    try:
        encoded_time = le_time.transform([time])[0]
        encoded_weather = le_weather.transform([weather])[0]
        encoded_traffic = le_traffic.transform([traffic])[0]

    except ValueError as exc:
        raise ValueError(
            "Time, weather, or traffic value dataset ke categories "
            "se match nahi karta. Form values aur dataset check karo."
        ) from exc

    features = pd.DataFrame(
        [[encoded_time, encoded_weather, encoded_traffic]],
        columns=["time_of_day", "weather", "traffic_level"]
    )

    pace = float(model.predict(features)[0])  # minutes per km

    return max(0.0, pace * float(distance))


# ---------------- CHECK MODEL ----------------

if __name__ == "__main__":
    print("Dataset distance range:")
    print(data["distance"].min(), "to", data["distance"].max())

    print("\nAccepted time values:", list(le_time.classes_))
    print("Accepted weather values:", list(le_weather.classes_))
    print("Accepted traffic values:", list(le_traffic.classes_))

    print("\nExample prediction:")
    print(predict_time(5, "morning", "rain", "high"), "min")
    print(predict_time(39.26, "morning", "clear", "low"), "min (39.26 km)")

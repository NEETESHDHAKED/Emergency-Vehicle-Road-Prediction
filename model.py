
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

X = data[
    ["distance", "time_of_day", "weather", "traffic_level"]
]

y = data["travel_time"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# ---------------- PREDICT TRAVEL TIME ----------------

def predict_time(distance, time, weather, traffic):
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
        [[
            float(distance),
            encoded_time,
            encoded_weather,
            encoded_traffic
        ]],
        columns=[
            "distance",
            "time_of_day",
            "weather",
            "traffic_level"
        ]
    )

    prediction = model.predict(features)[0]

    return max(0.0, float(prediction))


# ---------------- CHECK MODEL ----------------

if __name__ == "__main__":
    print("Dataset distance range:")
    print(data["distance"].min(), "to", data["distance"].max())

    print("\nAccepted time values:", list(le_time.classes_))
    print("Accepted weather values:", list(le_weather.classes_))
    print("Accepted traffic values:", list(le_traffic.classes_))

    print("\nExample prediction:")
    print(predict_time(5, "morning", "rain", "high"))

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


# =========================
# 1️⃣ Load Data
# =========================
DATA_PATH = "data/AgriQ_Final_Tulkarm_Data.csv"

df = pd.read_csv(DATA_PATH)

# توحيد اسم عمود المحصول
if "label" in df.columns:
    df = df.rename(columns={"label": "crop"})


# =========================
# 2️⃣ Encode Target
# =========================
label_encoder = LabelEncoder()
df["crop_encoded"] = label_encoder.fit_transform(df["crop"])


# =========================
# 3️⃣ Feature Selection
# =========================
FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "water_access",
    "market_demand",
    "farming_type"
]

X = df[FEATURES]
y = df["crop_encoded"]


# =========================
# 4️⃣ Scaling
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# =========================
# 5️⃣ Train / Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)


# =========================
# 6️⃣ Train Model
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# 7️⃣ Crop Statistics (for water & cost)
# =========================
crop_stats = df.groupby("crop").agg({
    "water_access": "mean",
    "production_cost": "mean"
}).reset_index()

max_cost = crop_stats["production_cost"].max()


# =========================
# 8️⃣ Recommendation Function
# =========================
def recommend_crops(farmer_input, top_k=2):
    """
    Returns top crop recommendations with:
    score, water proxy, and relative profit
    """

    # Input → DataFrame
    input_df = pd.DataFrame([farmer_input])

    # Scaling
    input_scaled = scaler.transform(input_df)

    # Probabilities
    probabilities = model.predict_proba(input_scaled)[0]
    top_indices = np.argsort(probabilities)[::-1][:top_k]

    recommendations = []

    for idx in top_indices:
        crop_name = label_encoder.inverse_transform([idx])[0]
        score = float(probabilities[idx])

        crop_row = crop_stats[crop_stats["crop"] == crop_name]

        if not crop_row.empty:
            water_access = float(crop_row["water_access"].values[0])
            water = round((1 - water_access) * 100, 1)
            cost = float(crop_row["production_cost"].values[0])
        else:
            water = 0.0
            cost = 0.0

        # Relative profit score (for optimization)
        profit = (score * 100) - (cost / max_cost) * 40
        profit = round(float(profit), 1)

        recommendations.append({
            "crop": crop_name,
            "score": round(score, 3),
            "water": water,
            "profit": profit
        })

    # Domain constraints (local realism)
    UNSUITABLE_CROPS = ["mango", "banana", "papaya"]
    recommendations = [
        r for r in recommendations
        if r["crop"] not in UNSUITABLE_CROPS
    ]

    return recommendations

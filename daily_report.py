import pandas as pd
import datetime
import json
import os

# Charger le fichier CSV
csv_path = "/home/ubuntu/eth-project/prices.csv"
output_path = "/home/ubuntu/eth-project/daily_report.json"

try:
    df = pd.read_csv(csv_path, names=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Filtrer les données du jour
    today = datetime.datetime.now().date()
    df_today = df[df["timestamp"].dt.date == today]

    if df_today.empty:
        report = {
            "status": "aucune donnée trouvée pour aujourd’hui",
            "date": today.strftime("%Y-%m-%d")
        }
    else:
        open_price = df_today.iloc[0]["price"]
        close_price = df_today.iloc[-1]["price"]
        variation_abs = close_price - open_price
        variation_pct = (variation_abs / open_price) * 100
        volatility = df_today["price"].std()

        report = {
            "status": "ok",
            "date": today.strftime("%Y-%m-%d"),
            "open_price": round(open_price, 2),
            "close_price": round(close_price, 2),
            "variation_abs": round(variation_abs, 2),
            "variation_pct": round(variation_pct, 2),
            "volatility": round(volatility, 4)
        }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"✅ Rapport généré : {output_path}")

except Exception as e:
    print(f"❌ Erreur : {e}")

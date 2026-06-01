import sqlite3

DB_NAME = "smart_city.db"


# -------------------------------
# 1. Create Table
# -------------------------------
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone TEXT,
            hour INTEGER,
            day INTEGER,
            traffic INTEGER,
            aqi INTEGER,
            weather TEXT,
            fuel REAL,
            power INTEGER
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# 2. Save Prediction
# -------------------------------
def save_prediction(zone, hour, day, traffic, aqi, weather, fuel, power):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (zone, hour, day, traffic, aqi, weather, fuel, power)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (zone, hour, day, traffic, aqi, weather, fuel, power))

    conn.commit()
    conn.close()


# -------------------------------
# 3. Get Last Predictions
# -------------------------------
def get_history(limit=20):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT zone, hour, day, traffic, aqi, weather, fuel, power
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "zone": row[0],
            "hour": row[1],
            "day": row[2],
            "traffic": row[3],
            "aqi": row[4],
            "weather": row[5],
            "fuel": row[6],
            "power": row[7]
        })

    return history


# -------------------------------
# 4. Run File Directly
# -------------------------------
if __name__ == "__main__":
    create_table()
    print("✅ Database & Table Created Successfully")
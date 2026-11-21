import os
import aiosqlite
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "harvestiq.db")

async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop TEXT NOT NULL,
                variety TEXT NOT NULL,
                district TEXT NOT NULL,
                market_name TEXT NOT NULL,
                min_price REAL NOT NULL,
                max_price REAL NOT NULL,
                modal_price REAL NOT NULL,
                arrival_tonnes REAL NOT NULL,
                date TEXT NOT NULL,
                source TEXT NOT NULL
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS soil_cards (
                card_number TEXT PRIMARY KEY,
                farmer_name TEXT NOT NULL,
                village TEXT NOT NULL,
                district TEXT NOT NULL,
                nitrogen REAL NOT NULL,
                phosphorus REAL NOT NULL,
                potassium REAL NOT NULL,
                ph REAL NOT NULL,
                ec REAL NOT NULL,
                organic_carbon REAL NOT NULL
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS district_gov (
                district_code TEXT PRIMARY KEY,
                district_name TEXT NOT NULL,
                zone TEXT NOT NULL,
                cropped_area_ha REAL NOT NULL,
                predicted_yield_mt REAL NOT NULL,
                godown_capacity_mt REAL NOT NULL,
                current_stock_mt REAL NOT NULL,
                procurement_budget_cr REAL NOT NULL
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_type TEXT NOT NULL,
                useful INTEGER NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def refresh_prices() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM prices")
        sample_prices = [
            ("Rice", "ADT 37 / Medium", "Thanjavur", "Thanjavur Regulated Market", 2080.0, 2250.0, 2180.0, 142.5, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Rice", "BPT 5204 (Samba)", "Thanjavur", "Kumbakonam Mandi", 2150.0, 2380.0, 2290.0, 95.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Rice", "Co 51", "Madurai", "Madurai Central Market", 2020.0, 2210.0, 2140.0, 110.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Rice", "CR 1009 Sub 1", "Tiruchirappalli", "Trichy Gandhi Market", 2050.0, 2240.0, 2160.0, 125.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Groundnut", "TMV 7 (Pod)", "Erode", "Erode Regulated Market", 7400.0, 8100.0, 7850.0, 78.4, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Groundnut", "VRI 2", "Salem", "Salem Market Yard", 7200.0, 7950.0, 7700.0, 62.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Groundnut", "JL 24", "Villupuram", "Tindivanam Regulated Market", 7350.0, 8020.0, 7800.0, 84.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Sugarcane", "Co 86032", "Madurai", "Alanganallur Sugar Mill Gate", 3350.0, 3600.0, 3500.0, 410.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Sugarcane", "Co 0212", "Erode", "Appakudal Mill Collection Yard", 3300.0, 3550.0, 3480.0, 380.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Sugarcane", "CoC 671", "Cuddalore", "Pennadam Regulated Yard", 3280.0, 3500.0, 3440.0, 290.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Cotton", "MCU 5 (Long Staple)", "Thanjavur", "Thiruvaiyaru Market Yard", 7100.0, 7650.0, 7420.0, 45.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Cotton", "Bunny Bt", "Salem", "Attur Regulated Market", 6950.0, 7550.0, 7340.0, 68.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Cotton", "Suvin", "Coimbatore", "Pollachi Market Yard", 7500.0, 8200.0, 7920.0, 52.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Maize", "Hybrid Yellow", "Dindigul", "Oddanchatram Market", 2150.0, 2350.0, 2280.0, 160.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Turmeric", "Finger (Erode Local)", "Erode", "Perundurai Turmeric Complex", 13800.0, 15400.0, 14650.0, 115.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Black Gram", "VBN 8 (Urad)", "Thanjavur", "Papanasam Regulated Market", 7900.0, 8600.0, 8350.0, 35.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Banana", "Grand Naine (Robusta)", "Tiruchirappalli", "Thottiyam Banana Yard", 1800.0, 2300.0, 2100.0, 210.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection"),
            ("Small Onion", "Shallots (CO 4)", "Dindigul", "Dindigul Daily Mandi", 4200.0, 5600.0, 5100.0, 140.0, "2026-11-21", "Agmarknet, Dte of Mktg & Inspection")
        ]
        for item in sample_prices:
            await db.execute("""
                INSERT INTO prices (crop, variety, district, market_name, min_price, max_price, modal_price, arrival_tonnes, date, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, item)

        await db.execute("DELETE FROM soil_cards")
        sample_cards = [
            ("TN-THJ-2026-8812", "M. Ramanathan", "Ammapettai", "Thanjavur", 240.0, 18.5, 290.0, 6.8, 0.42, 0.65),
            ("TN-ERD-2026-4401", "K. Sengottaiyan", "Modakkurichi", "Erode", 180.0, 24.0, 195.0, 7.4, 0.38, 0.52),
            ("TN-MDU-2026-9032", "P. Muthuramalingam", "Usilampatti", "Madurai", 210.0, 14.0, 320.0, 8.1, 0.65, 0.45),
            ("TN-CBE-2026-5519", "S. Velusamy", "Sulur", "Coimbatore", 290.0, 28.0, 340.0, 6.5, 0.35, 0.72),
            ("TN-TRZ-2026-1190", "A. Soundarapandian", "Lalgudi", "Tiruchirappalli", 260.0, 22.0, 270.0, 7.1, 0.40, 0.58)
        ]
        for card in sample_cards:
            await db.execute("""
                INSERT INTO soil_cards (card_number, farmer_name, village, district, nitrogen, phosphorus, potassium, ph, ec, organic_carbon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, card)

        await db.execute("DELETE FROM district_gov")
        districts_data = [
            ("THJ", "Thanjavur", "Cauvery Delta", 185000, 740000, 480000, 412000, 1480.0),
            ("TVR", "Tiruvarur", "Cauvery Delta", 162000, 630000, 390000, 345000, 1260.0),
            ("NAG", "Nagapattinam", "Cauvery Delta", 125000, 480000, 310000, 268000, 960.0),
            ("MYL", "Mayiladuthurai", "Cauvery Delta", 98000, 390000, 250000, 218000, 780.0),
            ("ERD", "Erode", "Western Zone", 142000, 520000, 320000, 215000, 840.0),
            ("MDU", "Madurai", "Southern Zone", 138000, 460000, 280000, 192000, 720.0),
            ("CBE", "Coimbatore", "Western Zone", 115000, 380000, 260000, 175000, 610.0),
            ("TRZ", "Tiruchirappalli", "Cauvery Delta", 155000, 580000, 360000, 298000, 1120.0),
            ("SLM", "Salem", "Western Zone", 168000, 590000, 340000, 238000, 890.0),
            ("CUD", "Cuddalore", "Cauvery Delta", 178000, 680000, 420000, 360000, 1340.0),
            ("VLR", "Vellore", "Northern Zone", 92000, 310000, 220000, 145000, 480.0),
            ("DPI", "Dharmapuri", "North Western Zone", 135000, 440000, 270000, 180000, 650.0),
            ("DGL", "Dindigul", "Southern Zone", 148000, 490000, 290000, 201000, 740.0),
            ("KRI", "Krishnagiri", "North Western Zone", 128000, 410000, 240000, 158000, 590.0),
            ("NMK", "Namakkal", "Western Zone", 122000, 430000, 260000, 172000, 630.0),
            ("TUP", "Tiruppur", "Western Zone", 145000, 470000, 300000, 198000, 710.0),
            ("VPM", "Villupuram", "North Eastern Zone", 172000, 610000, 370000, 282000, 980.0),
            ("KLL", "Kallakurichi", "North Eastern Zone", 144000, 510000, 310000, 235000, 820.0),
            ("TNM", "Tiruvannamalai", "North Eastern Zone", 189000, 650000, 390000, 295000, 1050.0),
            ("PUD", "Pudukkottai", "Cauvery Delta", 134000, 470000, 290000, 225000, 750.0),
            ("SIV", "Sivaganga", "Southern Zone", 118000, 360000, 230000, 150000, 540.0),
            ("RAM", "Ramanathapuram", "Southern Zone", 126000, 340000, 220000, 138000, 510.0),
            ("VRD", "Virudhunagar", "Southern Zone", 132000, 390000, 250000, 165000, 580.0),
            ("TNI", "Theni", "Southern Zone", 88000, 320000, 200000, 132000, 470.0),
            ("TEN", "Tenkasi", "Southern Zone", 96000, 350000, 210000, 142000, 530.0),
            ("TIN", "Tirunelveli", "Southern Zone", 112000, 410000, 260000, 185000, 620.0),
            ("THO", "Thoothukudi", "Southern Zone", 129000, 370000, 240000, 160000, 550.0),
            ("KAN", "Kanniyakumari", "High Rainfall Zone", 45000, 180000, 120000, 72000, 280.0),
            ("ARI", "Ariyalur", "Cauvery Delta", 95000, 360000, 230000, 178000, 560.0),
            ("PER", "Perambalur", "Cauvery Delta", 88000, 330000, 210000, 155000, 510.0),
            ("KRR", "Karur", "Western Zone", 94000, 340000, 220000, 148000, 520.0),
            ("TPT", "Tirupathur", "Northern Zone", 78000, 260000, 180000, 115000, 390.0),
            ("RNP", "Ranipet", "Northern Zone", 82000, 280000, 190000, 122000, 420.0),
            ("KCH", "Kanchipuram", "North Eastern Zone", 98000, 350000, 230000, 152000, 540.0),
            ("CGL", "Chengalpattu", "North Eastern Zone", 89000, 310000, 200000, 130000, 460.0),
            ("TLR", "Tiruvallur", "North Eastern Zone", 105000, 380000, 250000, 168000, 580.0),
            ("NIL", "Nilgiris", "Hilly Zone", 32000, 110000, 80000, 44000, 180.0),
            ("CHE", "Chennai", "Coastal Urban", 2000, 5000, 150000, 95000, 40.0)
        ]
        for dist in districts_data:
            await db.execute("""
                INSERT INTO district_gov (district_code, district_name, zone, cropped_area_ha, predicted_yield_mt, godown_capacity_mt, current_stock_mt, procurement_budget_cr)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, dist)

        await db.commit()

async def get_all_prices():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM prices ORDER BY district, crop")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_soil_card(card_no: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM soil_cards WHERE card_number = ?", (card_no,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def get_district_gov_data():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM district_gov ORDER BY current_stock_mt * 100.0 / godown_capacity_mt DESC")
        rows = await cursor.fetchall()
        results = []
        for r in rows:
            d = dict(r)
            util = round((d["current_stock_mt"] / d["godown_capacity_mt"]) * 100, 1)
            d["utilization_pct"] = util
            d["overflow_risk"] = util >= 85.0
            results.append(d)
        return results

async def save_feedback(rec_type: str, useful: bool, comment: Optional[str] = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO feedback (recommendation_type, useful, comment) VALUES (?, ?, ?)",
                         (rec_type, 1 if useful else 0, comment))
        await db.commit()
        return {"status": "success"}

#!/usr/bin/env python3
"""Script to clear existing data and re-ingest with proper vector format"""

import sys
sys.path.insert(0, 'src')

from services.database import DatabaseManager

def clear_data():
    """Clear all existing player stats data"""
    db = DatabaseManager()
    db.connect()
    cursor = db.connection.cursor()

    print("Clearing existing data from player_stats_documents table...")
    cursor.execute("TRUNCATE TABLE player_stats_documents;")
    db.connection.commit()
    cursor.close()
    db.disconnect()
    print("Data cleared successfully!")
    print("\nNow run: python src/embed_stats.py")
    print("This will re-ingest all data with proper vector formatting.")

if __name__ == "__main__":
    clear_data()

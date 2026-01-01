#!/usr/bin/env python3
"""
Add UTC offset column and CET work hours column to timezone geopackage.
This script adds:
1. An integer column 'UTC' with offset values relative to UTC
2. A text column 'work_hours_CET' showing equivalent local time when it's 09:00-17:00 in CET
"""

import sqlite3
from datetime import datetime
import pytz

def get_utc_offset(tzid):
    """
    Get the current UTC offset for a timezone in hours.
    Returns integer offset (e.g., 0 for UTC, 1 for UTC+1, -5 for UTC-5)
    """
    try:
        tz = pytz.timezone(tzid)
        # Use current date to get the offset
        dt = datetime(2025, 12, 31, 12, 0, 0)
        offset = tz.utcoffset(dt)
        if offset is None:
            return 0
        # Convert to hours (as integer)
        hours = int(offset.total_seconds() / 3600)
        return hours
    except Exception as e:
        print(f"Error processing {tzid}: {e}")
        return None

def get_cet_work_hours(tzid):
    """
    Calculate equivalent local work hours when it's 09:00-17:00 in CET.
    Returns string in format "HH:MM-HH:MM"
    """
    try:
        # Get CET timezone and the target timezone
        cet_tz = pytz.timezone('Europe/Paris')  # CET/CEST
        local_tz = pytz.timezone(tzid)
        
        # Create datetime objects for 09:00 and 17:00 CET on Dec 31, 2025
        dt_start_cet = cet_tz.localize(datetime(2025, 12, 31, 9, 0, 0))
        dt_end_cet = cet_tz.localize(datetime(2025, 12, 31, 17, 0, 0))
        
        # Convert to target timezone
        dt_start_local = dt_start_cet.astimezone(local_tz)
        dt_end_local = dt_end_cet.astimezone(local_tz)
        
        # Format as HH:MM-HH:MM
        start_time = dt_start_local.strftime("%H:%M")
        end_time = dt_end_local.strftime("%H:%M")
        
        return f"{start_time}-{end_time}"
    except Exception as e:
        print(f"Error processing work hours for {tzid}: {e}")
        return None

def add_utc_column(gpkg_path):
    """
    Add UTC offset column to the geopackage and populate it.
    """
    # Connect to the geopackage (it's a SQLite database)
    conn = sqlite3.connect(gpkg_path)
    # Load spatialite extension to support GeoPackage functions
    conn.enable_load_extension(True)
    try:
        conn.load_extension("mod_spatialite")
    except:
        try:
            conn.load_extension("libspatialite")
        except:
            print("Warning: Could not load spatialite extension, continuing anyway...")
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(combinedshapefilenow)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'UTC' in columns:
        print("UTC column already exists. Dropping it to recreate...")
        cursor.execute("ALTER TABLE combinedshapefilenow DROP COLUMN UTC")
        conn.commit()
    
    if 'work_hours_CET' in columns:
        print("work_hours_CET column already exists. Dropping it to recreate...")
        cursor.execute("ALTER TABLE combinedshapefilenow DROP COLUMN work_hours_CET")
        conn.commit()
    
    # Add the columns
    print("Adding UTC column...")
    cursor.execute("ALTER TABLE combinedshapefilenow ADD COLUMN UTC INTEGER")
    conn.commit()
    
    print("Adding work_hours_CET column...")
    cursor.execute("ALTER TABLE combinedshapefilenow ADD COLUMN work_hours_CET TEXT")
    conn.commit()
    
    # Get all timezone IDs
    cursor.execute("SELECT fid, tzid FROM combinedshapefilenow")
    rows = cursor.fetchall()
    
    print(f"Processing {len(rows)} timezones...")
    
    # Update each row with the UTC offset and work hours
    utc_updates = []
    work_hours_updates = []
    
    for fid, tzid in rows:
        offset = get_utc_offset(tzid)
        work_hours = get_cet_work_hours(tzid)
        
        if offset is not None:
            utc_updates.append((offset, fid))
        
        if work_hours is not None:
            work_hours_updates.append((work_hours, fid))
        
        # Display the info
        offset_str = f"UTC{offset:+d}" if offset is not None else "UTC?"
        work_str = work_hours if work_hours else "?"
        print(f"  {tzid}: {offset_str}, Work hours: {work_str}")
    
    # Batch updates
    print("\nUpdating UTC offsets...")
    cursor.executemany("UPDATE combinedshapefilenow SET UTC = ? WHERE fid = ?", utc_updates)
    conn.commit()
    
    print("Updating work hours...")
    cursor.executemany("UPDATE combinedshapefilenow SET work_hours_CET = ? WHERE fid = ?", work_hours_updates)
    conn.commit()
    
    print(f"\nSuccessfully updated {len(utc_updates)} records.")
    
    # Show summary
    cursor.execute("SELECT DISTINCT UTC FROM combinedshapefilenow ORDER BY UTC")
    offsets = [row[0] for row in cursor.fetchall()]
    print(f"\nUnique UTC offsets in the data: {offsets}")
    
    conn.close()

if __name__ == "__main__":
    gpkg_path = "/home/ngavish/Projects/timezone-map/geodata/timezones_now.gpkg"
    add_utc_column(gpkg_path)
    print("\nDone! The UTC and work_hours_CET columns have been added to the geopackage.")
    print("\nwork_hours_CET shows the equivalent local time when it's 09:00-17:00 in CET (Europe/Paris).")

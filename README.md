# Timezone Map

Interactive map displaying world timezones with color-coded work hours relative to Central European Time (CET).

## Project Structure

```
timezone-map/
├── data/
│   └── tzdata2025c/          # IANA timezone database
├── geodata/
│   ├── timezones_now.gpkg    # Source geopackage with UTC & work_hours_CET fields
│   ├── timezones_v*.geojson  # Processed timezone GeoJSON exports
│   ├── countries_v*.geojson  # Country boundaries GeoJSON
│   ├── world_v*.mbtiles      # MBTiles vector tiles
│   └── world_v*.pmtiles      # PMTiles vector tiles (deployed)
├── webpage/
│   ├── index.html            # Interactive map interface
│   ├── server.py             # HTTP server with Range request support
│   └── world_v*.pmtiles      # Deployed PMTiles file
└── add_utc_offset.py         # Script to add UTC & work_hours_CET columns
```

## Processing Pipeline

### 1. Add UTC Offset and Work Hours Columns

Run the Python script to add `UTC` and `work_hours_CET` columns to the geopackage:

```bash
python3 add_utc_offset.py
```

This adds:
- `UTC` (Integer): UTC offset (-11 to +14)
- `work_hours_CET` (String): Equivalent local time when it's 09:00-17:00 in CET

### 2. Process in QGIS

For timezones:
- Dissolve by 'UTC' field
- Reproject to EPSG:3857 (Web Mercator)
- Simplify geometry (Visvalingam algorithm, 10,000 meters)
- Export as GeoJSON → `timezones_v*.geojson`

Repeat for countries → `countries_v*.geojson`

### 3. Create Vector Tiles

Generate MBTiles with two layers:

```bash
tippecanoe \
  -o world_v3.mbtiles \
  -Z0 -z6 \
  --layer=timezones timezones_v*.geojson \
  --layer=countries countries_v*.geojson \
  --drop-densest-as-needed \
  --force
```

### 4. Convert to PMTiles

Convert MBTiles to PMTiles format for web deployment:

```bash
pmtiles convert world_v3.mbtiles world_v3.pmtiles
cp world_v3.pmtiles webpage/
```

## Testing / Development

### Start the Development Server

The webpage requires a server with HTTP Range request support for PMTiles:

```bash
cd webpage
python3 server.py
```

Server runs at: `http://localhost:8000`

### View the Map

Open your browser to `http://localhost:8000`

Features:
- **Color-coded timezones**: Each timezone colored by its work hours start time
- **Hover highlighting**: White border on hover (fast, uses feature-state)
- **Click for details**: Popup shows timezone name, UTC offset, CET work hours, and country
- **Persistent popups**: Click to open, click X or elsewhere to close

### Configuration

Edit [webpage/index.html](webpage/index.html) line 42 to change the PMTiles file:

```javascript
const PMTILES_URL = 'world_v3.pmtiles';  // Change filename here
```

## Data Sources

**Timezone Shapes (based on OSM):**
https://github.com/evansiroky/timezone-boundary-builder

## Requirements

- Python 3.x with `pytz` library
- QGIS (for geometry processing)
- Tippecanoe (vector tile generation)
- PMTiles CLI (format conversion)
- GDAL/OGR (optional, for inspection)

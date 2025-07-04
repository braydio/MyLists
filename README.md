# MappyMapper

This script generates an interactive HTML map of points of interest around a
specified address using data from OpenStreetMap's Overpass API. Results are
cached locally to avoid unnecessary requests. Geocoding is performed with the
public Nominatim API.

## APIs

- **Nominatim** is used to turn the configured address into latitude and
  longitude coordinates. No key is required.
- **Overpass API** supplies points of interest and natural features from
  OpenStreetMap.

## Usage

Activate a Python environment with the dependencies from `requirements.txt`
and run `python mapper.py`. The generated map will be saved to
`output/map.html`.

### Environment variables

- `DISPLAY_NATURE=true` enables natural points of interest like parks, rivers,
  outdoor activities, hiking trails, trailheads and parking lots.
- `SKIP_GEO=true` skips geocoding when running tests or offline.

Both APIs are public and do not require access tokens, but you must have
internet access enabled when running the script.

## Testing

Run the unit tests without making network requests by setting `SKIP_GEO=true`:

```bash
SKIP_GEO=true python -m unittest discover tests
```


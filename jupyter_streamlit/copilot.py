
import json
import unicodedata
import urllib.request

import pydeck as pdk
import streamlit as st


st.set_page_config(page_title="Mexico population map", layout="wide")
st.title("Mexico — population map")
st.caption("Hover a state marker to see its population (Census 2020).")

# 2020 state populations (INEGI 2020 census; values also commonly mirrored on Wikipedia).
# Keyed by *normalized* state name.
STATE_POPULATION_2020 = {
	"aguascalientes": 1_425_607,
	"baja california": 3_769_020,
	"baja california sur": 798_447,
	"campeche": 928_363,
	"chiapas": 5_543_828,
	"chihuahua": 3_741_869,
	"ciudad de mexico": 9_209_944,
	"coahuila": 3_146_771,
	"coahuila de zaragoza": 3_146_771,
	"colima": 731_391,
	"durango": 1_832_650,
	"guanajuato": 6_166_934,
	"guerrero": 3_540_685,
	"hidalgo": 3_082_841,
	"jalisco": 8_348_151,
	"mexico": 16_992_418,
	"michoacan": 4_748_846,
	"michoacan de ocampo": 4_748_846,
	"morelos": 1_971_520,
	"nayarit": 1_235_456,
	"nuevo leon": 5_784_442,
	"oaxaca": 4_132_148,
	"puebla": 6_583_278,
	"queretaro": 2_368_467,
	"queretaro de arteaga": 2_368_467,
	"quintana roo": 1_857_985,
	"san luis potosi": 2_822_255,
	"sinaloa": 3_026_943,
	"sonora": 2_944_840,
	"tabasco": 2_402_598,
	"tamaulipas": 3_527_735,
	"tlaxcala": 1_342_977,
	"veracruz": 8_062_579,
	"yucatan": 2_320_898,
	"zacatecas": 1_622_138,
}

MEXICO_TOTAL_POPULATION_2020 = 126_014_024

# Rough geographic center of Mexico for initial view.
MEXICO_CENTER_LAT = 23.6345
MEXICO_CENTER_LON = -102.5528

MEXICO_STATES_GEOJSON_URL = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"


def _normalize_name(text: str) -> str:
	text = (text or "").strip().lower()
	text = (
		unicodedata.normalize("NFKD", text)
		.encode("ascii", "ignore")
		.decode("ascii")
	)
	text = " ".join(text.split())
	return text


def _polygon_centroid_and_area(lon_lat_ring: list[list[float]]) -> tuple[tuple[float, float], float]:
	if not lon_lat_ring or len(lon_lat_ring) < 3:
		return (0.0, 0.0), 0.0

	# Ensure ring is closed.
	if lon_lat_ring[0] != lon_lat_ring[-1]:
		points = lon_lat_ring + [lon_lat_ring[0]]
	else:
		points = lon_lat_ring

	area2 = 0.0
	cx = 0.0
	cy = 0.0
	for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
		cross = x0 * y1 - x1 * y0
		area2 += cross
		cx += (x0 + x1) * cross
		cy += (y0 + y1) * cross

	if area2 == 0.0:
		avg_lon = sum(p[0] for p in lon_lat_ring) / len(lon_lat_ring)
		avg_lat = sum(p[1] for p in lon_lat_ring) / len(lon_lat_ring)
		return (avg_lon, avg_lat), 0.0

	area = area2 / 2.0
	cx = cx / (3.0 * area2)
	cy = cy / (3.0 * area2)
	return (cx, cy), abs(area)


def _geometry_centroid(geometry: dict) -> tuple[float, float] | None:
	if not geometry or "type" not in geometry:
		return None

	geom_type = geometry.get("type")
	coords = geometry.get("coordinates")

	if geom_type == "Polygon":
		# coords: [outer_ring, hole1, hole2, ...]
		if not coords or not coords[0]:
			return None
		(lon, lat), _ = _polygon_centroid_and_area(coords[0])
		return lat, lon

	if geom_type == "MultiPolygon":
		# coords: [[poly1_rings], [poly2_rings], ...]
		best_area = -1.0
		best_centroid = None
		for poly in coords or []:
			if not poly or not poly[0]:
				continue
			(lon, lat), area = _polygon_centroid_and_area(poly[0])
			if area > best_area:
				best_area = area
				best_centroid = (lat, lon)
		return best_centroid

	return None


@st.cache_data(show_spinner=False)
def _load_geojson(url: str) -> dict:
	with urllib.request.urlopen(url, timeout=30) as response:
		return json.loads(response.read().decode("utf-8"))


try:
	geojson = _load_geojson(MEXICO_STATES_GEOJSON_URL)
except Exception as exc:
	st.error(
		"Could not load Mexico states GeoJSON. "
		"Check your internet connection and try again.\n\n"
		f"Details: {exc}"
	)
	st.stop()


states = []
for feature in geojson.get("features", []):
	props = feature.get("properties", {})
	state_name = props.get("name", "")
	state_id = props.get("id", "")

	centroid = _geometry_centroid(feature.get("geometry"))
	if centroid is None:
		continue
	lat, lon = centroid

	normalized = _normalize_name(state_name)
	population = STATE_POPULATION_2020.get(normalized)
	if population is None:
		# Try a couple of common name variants.
		population = STATE_POPULATION_2020.get(normalized.replace("estado de ", ""))

	if population is None:
		continue

	abbr = state_id.replace("MX-", "") if isinstance(state_id, str) else ""
	radius_m = 20

	states.append(
		{
			"name": state_name,
			"abbr": abbr,
			"lat": float(lat),
			"lon": float(lon),
			"population": int(population),
			"population_fmt": f"{int(population):,}",
			"radius_m": radius_m,
		}
	)

if len(states) < 32:
	st.warning(
		f"Loaded {len(states)} state markers. "
		"If any are missing, it’s likely due to a name mismatch in the GeoJSON source."
	)

view_state = pdk.ViewState(
	latitude=MEXICO_CENTER_LAT,
	longitude=MEXICO_CENTER_LON,
	zoom=4.2,
	pitch=0,
)

layers = [
	pdk.Layer(
		"GeoJsonLayer",
		data=geojson,
		stroked=True,
		filled=True,
		get_line_color=[90, 90, 90, 180],
		get_fill_color=[200, 200, 200, 40],
		line_width_min_pixels=1,
		pickable=False,
	),
	pdk.Layer(
		"ScatterplotLayer",
		data=states,
		get_position="[lon, lat]",
		get_radius="radius_m",
		radius_units="meters",
		get_fill_color=[20, 108, 204, 170],
		get_line_color=[20, 108, 204, 220],
		line_width_min_pixels=1,
		pickable=True,
	),
	pdk.Layer(
		"TextLayer",
		data=states,
		get_position="[lon, lat]",
		get_text="abbr",
		get_size=12,
		get_color=[20, 20, 20, 220],
		get_text_anchor="middle",
		get_alignment_baseline="top",
	),
]

tooltip = {
	"html": "<b>{name}</b><br/>Population (2020): {population_fmt}",
	"style": {"backgroundColor": "white", "color": "black"},
}

deck = pdk.Deck(
	map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
	initial_view_state=view_state,
	layers=layers,
	tooltip=tooltip,
)

st.pydeck_chart(deck, use_container_width=True)
st.metric("Mexico population (total, 2020)", f"{MEXICO_TOTAL_POPULATION_2020:,}")

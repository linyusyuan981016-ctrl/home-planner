"""Shared application constants."""

DEFAULT_ROOM_WIDTH_CM = 400
DEFAULT_ROOM_LENGTH_CM = 300
DEFAULT_ROOM_HEIGHT_CM = 250

DEFAULT_FURNITURE_WIDTH_CM = 200
DEFAULT_FURNITURE_DEPTH_CM = 90

ROOM_TYPES = {
	"Living room": "Living Room",
	"Bedroom": "Bedroom",
	"Kitchen": "Kitchen",
	"Bathroom": "Bathroom",
	"Other": "Room",
}

FURNITURE_TYPES = {
	"Sofa": (200, 90),
	"Bed": (200, 160),
	"Dining table": (180, 90),
	"Chair": (50, 50),
	"Desk": (120, 60),
	"Cabinet": (100, 45),
	"Rug": (200, 140),
	"Other": (DEFAULT_FURNITURE_WIDTH_CM, DEFAULT_FURNITURE_DEPTH_CM),
}

ROOM_GAP_CM = 50

MIN_ROOM_DIMENSION_CM = 50
MAX_ROOM_DIMENSION_CM = 2000
MIN_ROOM_HEIGHT_CM = 200
MAX_ROOM_HEIGHT_CM = 500

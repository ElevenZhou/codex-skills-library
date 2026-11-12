## GameState.gd - runtime game state + versioned save/load (Autoload "GameState").
## Pure data and rules, no node lookups, so it can be tested headless.
extends Node

const SAVE_VERSION := 2
const SAVE_PATH := "user://save.json"
const TAPS_PER_LEVEL := 10

var score: int = 0
var taps: int = 0
var level: int = 1


func reset() -> void:
	score = 0
	taps = 0
	level = 1


## Register one tap worth `points`. Returns true if the player leveled up.
func register_tap(points: int = 1) -> bool:
	taps += 1
	score += points * level
	var leveled := false
	var new_level := 1 + floori(float(taps) / TAPS_PER_LEVEL)
	if new_level > level:
		level = new_level
		leveled = true
	return leveled


func to_dict() -> Dictionary:
	return {"version": SAVE_VERSION, "score": score, "taps": taps, "level": level}


## Migrate old save dictionaries to the current version. Never crashes on bad input.
func migrate(data: Dictionary) -> Dictionary:
	var d := data.duplicate()
	var v := int(d.get("version", 1))
	if v < 2:
		# v1 had no "level"; derive it from taps.
		d["level"] = 1 + floori(float(d.get("taps", 0)) / TAPS_PER_LEVEL)
		v = 2
	d["version"] = v
	return d


func from_dict(data: Dictionary) -> void:
	var d := migrate(data)
	score = int(d.get("score", 0))
	taps = int(d.get("taps", 0))
	level = maxi(1, int(d.get("level", 1)))


func save_game(path: String = SAVE_PATH) -> bool:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		push_warning("GameState: cannot open %s for writing" % path)
		return false
	f.store_string(JSON.stringify(to_dict()))
	return true


## Returns true if a valid save was loaded; otherwise keeps defaults.
func load_game(path: String = SAVE_PATH) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return false
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("GameState: corrupt save, starting fresh")
		return false
	from_dict(parsed)
	return true

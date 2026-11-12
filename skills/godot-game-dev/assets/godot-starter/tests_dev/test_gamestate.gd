## test_gamestate.gd - headless test for the GameState autoload.
## Run from the project root:  godot --headless -s tests_dev/test_gamestate.gd
## Exit code 0 = all pass, 1 = failure.
##
## A script run with -s is a SceneTree script, and autoloads are instantiated
## before _initialize(), so GameState is reachable as a child of root.
extends SceneTree

var _failures: int = 0
var _checks: int = 0
var _gs: Node


func _initialize() -> void:
	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		printerr("FAIL: GameState autoload not found (is project.godot [autoload] set?)")
		quit(1)
		return

	_test_initial_state()
	_test_tap_scoring_and_level_up()
	_test_reset()
	_test_migration_v1()
	_test_roundtrip_save_load()
	_test_corrupt_save_is_safe()

	print("%d checks, %d failures" % [_checks, _failures])
	quit(1 if _failures > 0 else 0)


func _check(cond: bool, label: String) -> void:
	_checks += 1
	if cond:
		print("  ok   " + label)
	else:
		_failures += 1
		printerr("  FAIL " + label)


func _fresh() -> void:
	# Always reset singleton state first so tests cannot pollute each other.
	_gs.reset()


func _test_initial_state() -> void:
	_fresh()
	_check(_gs.score == 0 and _gs.taps == 0 and _gs.level == 1, "initial state is zeroed")


func _test_tap_scoring_and_level_up() -> void:
	_fresh()
	var leveled := false
	for i in range(_gs.TAPS_PER_LEVEL - 1):
		leveled = _gs.register_tap()
	_check(not leveled and _gs.level == 1, "no level up before threshold")
	_check(_gs.score == _gs.TAPS_PER_LEVEL - 1, "score = taps at level 1")
	leveled = _gs.register_tap()
	_check(leveled and _gs.level == 2, "level up exactly at threshold")
	var before: int = _gs.score
	_gs.register_tap()
	_check(_gs.score == before + 2, "points scale with level")


func _test_reset() -> void:
	_gs.register_tap()
	_gs.reset()
	_check(_gs.score == 0 and _gs.taps == 0 and _gs.level == 1, "reset clears state")


func _test_migration_v1() -> void:
	_fresh()
	var old := {"version": 1, "score": 50, "taps": 25}
	_gs.from_dict(old)
	_check(_gs.score == 50 and _gs.taps == 25, "v1 save keeps score and taps")
	_check(_gs.level == 3, "v1 save derives level from taps (25 taps -> level 3)")


func _test_roundtrip_save_load() -> void:
	_fresh()
	for i in range(12):
		_gs.register_tap()
	var snap: Dictionary = _gs.to_dict()
	var path := "user://test_save.json"
	_check(_gs.save_game(path), "save_game writes file")
	_gs.reset()
	_check(_gs.load_game(path), "load_game reads file")
	_check(_gs.to_dict() == snap, "round trip equals snapshot")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _test_corrupt_save_is_safe() -> void:
	_fresh()
	var path := "user://test_corrupt.json"
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string("{not json")
	f = null  # close
	_check(not _gs.load_game(path), "corrupt save returns false")
	_check(_gs.level == 1, "corrupt save leaves defaults")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

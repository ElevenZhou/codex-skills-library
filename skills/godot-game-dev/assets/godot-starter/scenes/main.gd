## main.gd - tiny tap loop: tap the button, score grows, level goes up every N taps.
## Talks to the world only through the Events bus and the GameState autoload.
extends Control

@onready var score_label: Label = $VBox/ScoreLabel
@onready var level_label: Label = $VBox/LevelLabel
@onready var tap_button: Button = $VBox/TapButton
@onready var reset_button: Button = $VBox/ResetButton

var _tween: Tween


func _ready() -> void:
	GameState.load_game()
	Events.score_changed.connect(_on_score_changed)
	Events.level_up.connect(_on_level_up)
	Events.game_reset.connect(_refresh)
	tap_button.pressed.connect(_on_tap_pressed)
	reset_button.pressed.connect(_on_reset_pressed)
	_refresh()


func _on_tap_pressed() -> void:
	var leveled := GameState.register_tap()
	Events.tap_registered.emit(GameState.taps)
	Events.score_changed.emit(GameState.score)
	if leveled:
		Events.level_up.emit(GameState.level)
	_pop()


func _on_reset_pressed() -> void:
	GameState.reset()
	Events.game_reset.emit()


func _on_score_changed(_new_score: int) -> void:
	_refresh()


func _on_level_up(_new_level: int) -> void:
	_refresh()


func _refresh() -> void:
	score_label.text = "Score: %d" % GameState.score
	level_label.text = "Level %d  (%d/%d taps)" % [
		GameState.level,
		GameState.taps % GameState.TAPS_PER_LEVEL,
		GameState.TAPS_PER_LEVEL,
	]


## Kill the previous tween before starting a new one so rapid taps never stack tweens.
func _pop() -> void:
	if _tween != null and _tween.is_valid():
		_tween.kill()
	tap_button.pivot_offset = tap_button.size / 2.0
	tap_button.scale = Vector2(0.94, 0.94)
	_tween = create_tween()
	_tween.tween_property(tap_button, "scale", Vector2.ONE, 0.12)


func _notification(what: int) -> void:
	# Mobile: the OS may kill the app right after pause, so save here.
	if what == NOTIFICATION_APPLICATION_PAUSED or what == NOTIFICATION_WM_CLOSE_REQUEST:
		GameState.save_game()

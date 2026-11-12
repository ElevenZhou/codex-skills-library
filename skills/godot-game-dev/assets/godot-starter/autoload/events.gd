## Events.gd - global signal bus (Autoload "Events").
## Rule: signals only; no state, no logic. Emitters and listeners never reference each other.
extends Node

signal score_changed(new_score: int)
signal tap_registered(total_taps: int)
signal level_up(new_level: int)
signal game_reset()
signal save_requested()

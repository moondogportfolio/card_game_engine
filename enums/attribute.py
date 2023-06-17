from enum import Enum, auto


class AttrEnum(Enum):
	ATTACHMENT = auto()
	CAPTURED_UNITS = auto()
	#flags
	SILENCED = auto()
	VOID_KEYWORD = auto()
	#etc
	REVEALED = auto()
	INDEX = auto()
	LOCATION = auto()
	COUNTDOWN = auto()
	ENLIGHTENED = auto()
	STUNNED = auto()
	ATTACK = auto()
	HEALTH = auto()
	COST = auto()
	KEYWORDS = auto()
	POSITIVE_KEYWORDS = auto()
	IMPACT = auto()
	# CARDCODE = 'cardcode'
	# NAME = 'name'
	OWNER = auto()
	CREATOR = auto()
	SPELL_DAMAGE = auto()
	IMPRISONED_REFS = auto()
	OPPONENT = auto()
	# REGIONS = Region_
	# TYPE = Types_
	SUBTYPES = auto()
	SUPERTYPE = auto()
	BEARER = auto()
	#player
	SPELL_MANA = auto()
	RALLY = auto()
	MANA = auto()
	MANA_GEM = auto()
	#spell
	SPELL_SPEED = auto()
	#effect
	INTERNAL_VALUE = auto()
	HALLOW_VALUE = auto()
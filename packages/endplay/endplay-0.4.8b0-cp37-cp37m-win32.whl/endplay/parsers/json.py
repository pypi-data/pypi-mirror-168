"Parser for endplay formatted JSON files"

from __future__ import annotations

__all__ = ["JSONEncoder", "JSONDecoder", "dump", "dumps", "load", "loads"]

import json as _json
from enum import IntEnum
from collections.abc import Collection, Mapping
from endplay.types import ContractBid, PenaltyBid, Denom, Penalty, \
	Card, Rank, Contract, Player, Deal, Vul, Board, Hand, SuitHolding

def _check_keys(keys: set, mandatory: set, optional: set = set()):
	if not mandatory.issubset(keys):
		return False
	return (keys - mandatory).issubset(optional)

def _object_hook(d: dict):
	keys = set(d.keys())
	if _check_keys(keys, 
		set(["level", "denom"]), 
		set(["alertable", "announcement"])):
		return ContractBid(
			d.get("level"), Denom.find(d.get("denom")), 
			d.get("alertable", False), d.get("announcement"))
	elif _check_keys(keys, 
		set(["penalty"]), 
		set(["alertable", "announcement"])):
		return PenaltyBid(
			Penalty.find(d.get("penalty")), 
			d.get("alertable", False), d.get("announcement"))
	elif _check_keys(keys, set(["suit", "rank"])):
		return Card(
			suit=Denom.find(d.get("suit")), 
			rank=Rank.find(d.get("rank")))
	elif _check_keys(keys, 
		set(["level", "denom", "declarer"]), 
		set(["penalty", "result"])):
		return Contract(
			level=d.get("level"),
			denom=Denom.find(d.get("denom")),
			declarer=Player.find(d.get("declarer")),
			penalty=Penalty.find(d.get("penalty", "pass")),
			result=d.get("result", 0))
	elif _check_keys(keys,
		set(["north", "south", "east", "west"]),
		set(["first", "trump", "curtrick"])):
		deal = Deal(
			first=Player.find(d.get("first", "north")),
			trump=Denom.find(d.get("trump", "nt")))
		for hand in ["north", "south", "east", "west"]:
			for card in d.get(hand, []):
				deal[Player.find(hand)].add(card)
		for card in d.get("curtrick", []):
			deal.play(card)
		return deal
	elif _check_keys(keys,
		set(["deal", "auction", "play", "board_num"]),
		set(["vul", "dealer", "contract", "claimed", "info"])):
		board = Board(
			deal=d.get("deal"),
			auction=d.get("auction"),
			play=d.get("play"),
			board_num=d.get("board_num"),)
		if "vul" in d:
			board.vul = Vul.find(d.get("vul"))
		if "dealer" in d:
			board.dealer = Player.find(d.get("dealer"))
		if "contract" in d:
			board.contract = d.get("contract")
		if "claimed" in d:
			board.claimed = d.get("claimed")
		if "info" in d:
			for key, val in d.get("info").items():
				board.info[key] = val
		return board
	else:
		return d 

class JSONDecoder(_json.JSONDecoder):
	"""
	Class providing functionality for reading the JSON file format
	"""
	def __init__(self, 
		*, object_hook=None, parse_float=None, parse_int=None,
		parse_constant=None, strict=True, object_pairs_hook=None):
		if object_hook is not None or object_pairs_hook is not None:
			raise RuntimeError("object_hook and object_pairs_hook currently not supported")
		super().__init__(
			object_hook = _object_hook,
			parse_float = parse_float,
			parse_int = parse_int,
			parse_constant = parse_constant,
			strict = strict
		)

def _preprocess_intenum(o):
    if isinstance(o, IntEnum):
        return {'__class__': o.__class__.__name__,
                '__value__': (o.value,)}
    if isinstance(o, dict):
        return {k: _preprocess_intenum(v) for k, v in o.iteritems()}
    if isinstance(o, (list, tuple)):
        return [_preprocess_intenum(v) for v in o]
    return o

class JSONEncoder(_json.JSONEncoder):
	"""
	Class providing functionality for writing to the JSON file format
	"""
	def iterencode(self, o, _one_shot=False):
		return super().iterencode(_preprocess_intenum(o), _one_shot)

	def default(self, o):
		if isinstance(o, ContractBid):
			res = {
				"level": o.level,
				"denom": o.denom.name,
				"alertable": o.alertable,
			}
			if o.announcement:
				res["announcement"] = o.announcement
			return res
		elif isinstance(o, PenaltyBid):
			res = {
				"penalty": "pass" if o.penalty is Penalty.passed else o.penalty.name[:-1],
				"alertable": o.alertable
			}
			if o.announcement:
				res["announcement"] = o.announcement
			return res
		elif isinstance(o, Board):
			res = {
				"deal": o.deal,
				"auction": o.auction,
				"play": o.play,
				"board_num": o.board_num,
				"info": dict(o.info)
			}
			if o.vul is not None:
				res["vul"] = o.vul.name
			if o.dealer is not None:
				res["dealer"] = o.dealer.name
			if o.contract is not None:
				res["contract"] = o.contract
			if o.claimed is not None:
				res["claimed"] = o.claimed
			return res
		elif isinstance(o, Card):
			return {
				"suit": o.suit.name,
				"rank": o.rank.name[1]
			}
		elif isinstance(o, Contract):
			return {
				"level": o.level,
				"denom": o.denom.name,
				"declarer": o.declarer.name,
				"penalty": o.penalty.abbr,
				"result": o.result
			}
		elif isinstance(o, Deal):
			return {
				"north": list(o.north),
				"east": list(o.east),
				"south": list(o.south),
				"west": list(o.west),
				"first": o.first.name,
				"trump": o.trump.name,
				"curtrick": list(o.curtrick)
			}
		elif isinstance(o, Hand):
			return list(o)
		elif isinstance(o, SuitHolding):
			return [r.name for r in o] 
		else:
			return super().default(self, o)

def dump(obj, fp, 
	*, skipkeys=False, ensure_ascii=True, check_circular=True, 
	allow_nan=True, indent=None, separators=None, default=None, 
	sort_keys=False, **kw):
	return _json.dump(obj, fp,
		skipkeys=skipkeys,
		ensure_ascii=ensure_ascii,
		check_circular=check_circular,
		allow_nan=allow_nan,
		cls=JSONEncoder,
		indent=indent,
		separators=separators,
		default=default,
		sort_keys=sort_keys,
		**kw)

def dumps(obj, 
	*, skipkeys=False, ensure_ascii=True, check_circular=True, 
	allow_nan=True, indent=None, separators=None, default=None, 
	sort_keys=False, **kw):
	return _json.dumps(obj,
		skipkeys=skipkeys,
		ensure_ascii=ensure_ascii,
		check_circular=check_circular,
		allow_nan=allow_nan,
		cls=JSONEncoder,
		indent=indent,
		separators=separators,
		default=default,
		sort_keys=sort_keys,
		**kw)

def load(fp, *, 
	object_hook=None, parse_float=None, parse_int=None, 
	parse_constant=None, object_pairs_hook=None, **kw):
	return _json.load(fp,
		cls=JSONDecoder,
		object_hook=object_hook,
		parse_float=parse_float,
		parse_int=parse_int,
		parse_constant=parse_constant,
		object_pairs_hook=object_pairs_hook,
		**kw
	)

def loads(s, *, 
	object_hook=None, parse_float=None, parse_int=None, 
	parse_constant=None, object_pairs_hook=None, **kw):
	return _json.loads(s, 
		cls=JSONDecoder,
		object_hook=object_hook,
		parse_float=parse_float,
		parse_int=parse_int,
		parse_constant=parse_constant,
		object_pairs_hook=object_pairs_hook,
		**kw)
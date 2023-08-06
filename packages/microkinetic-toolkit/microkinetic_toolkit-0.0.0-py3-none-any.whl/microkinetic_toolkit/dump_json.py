#!/usr/bin/env python3

import json
import numpy as np
from typing import List

DUMP_ATTR_NAMES = ["reaction_symbols",
                   "deltaGs_eV",
                   "TdeltaSs_eV",
                   "dEas_eV",
                   "dEs_eV",
                   "_kfor",
                   "_krev",
                   "_Kc",
                   "Ncstr",
                   "_bep_param",
                   "_sden",
                   "_v0",
                   "_wcat",
                   "_area",
                   "_phi",
                   "_rho_b",
                   "_Vr",
                   "_tau",
                   "_total_tau",
                   "_sens_matrix",
                   "_converion_info",
                   "_gas_flow_info",
                   "_reduced_discarded_rxns_info",
                   "_reduced_rxns_info"]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {"np.array": obj.tolist()}
        elif isinstance(obj, np.float_):
            return float(obj)
        elif isinstance(obj, np.int_):
            return int(obj)
        else:
            json.JSONEncoder.default(self, obj)


def numpy_decodehook(d: dict):
    if "np.array" in d:
        return np.array(d["np.array"])
    else:
        return d


def loads(s, *args, cls=None,
          parse_float=None,
          parse_int=None, parse_constant=None,
          object_pairs_hook=None, **kw):
    """
    extended json.loads loads np.ndarray from json.
    """
    return json.loads(s, *args, cls=cls,
                      object_hook=numpy_decodehook,
                      parse_float=parse_float,
                      parse_int=parse_int,
                      parse_constant=parse_constant,
                      object_pairs_hook=object_pairs_hook,
                      **kw)


def load(fp, *args, cls=None, parse_float=None,
         parse_int=None, parse_constant=None,
         object_pairs_hook=None, **kw):
    return json.load(fp, *args, cls=cls,
                     object_hook=numpy_decodehook,
                     parse_float=parse_float,
                     parse_int=parse_int,
                     parse_constant=parse_constant,
                     object_pairs_hook=object_pairs_hook,
                     **kw)


def dumps(obj, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=NumpyEncoder, indent=4, separators=None,
          default=None, sort_keys=False, **kw):
    return json.dumps(obj, *args, skipkeys=skipkeys,
                      ensure_ascii=ensure_ascii,
                      check_circular=check_circular,
                      allow_nan=allow_nan,
                      cls=cls,
                      indent=indent,
                      separators=separators,
                      default=default,
                      sort_keys=sort_keys, **kw)


def dump(obj, fp, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
         allow_nan=True, indent=4, separators=None, default=None, sort_keys=False, **kw):
    return json.dump(obj, fp, *args,
                     skipkeys=skipkeys,
                     ensure_ascii=ensure_ascii,
                     check_circular=check_circular,
                     allow_nan=allow_nan,
                     cls=NumpyEncoder, indent=indent,
                     separators=separators,
                     default=default,
                     sort_keys=sort_keys, **kw)


class PropertyDumpMixin(object):
    def set_attribute_names(self, attr_names=None, default=None):
        if attr_names is None:
            attr_names = DUMP_ATTR_NAMES
        self._attr_names = attr_names
        self._default = default

    def dump(self, dump_json):
        assert ".json" in dump_json
        if not hasattr(self, "_attr_names"):
            self._attr_names = DUMP_ATTR_NAMES
        dump_dict = {}
        if not hasattr(self, "_default"):
            self._default = None
        for attr_nm in self._attr_names:
            dump_dict[attr_nm] = getattr(self, attr_nm, self._default)
        with open(dump_json, "w") as write:
            dump(dump_dict, write)

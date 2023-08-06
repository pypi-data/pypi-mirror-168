import dataclasses
import hashlib
import json
import pickle
import torch


class HashGenerator:
    """Calculate hash for the given object.

    Note that we cannot simply hashlib.sha1(pickle.dumps(obj)) since some of the contents might be cached on remote. For nested objects, we calculate hash for each child element recursively.
    """
    @classmethod
    def calculate_hash(cls, value, context=None):
        def get_hash(value):
            from .variable import Variable
            if isinstance(value, dict):
                value = json.dumps({k: get_hash(v) for k, v in sorted(value.items())})
            elif isinstance(value, (list, tuple)):
                value = json.dumps([get_hash(v) for v in value])
            elif dataclasses.is_dataclass(value):
                value = json.dumps({k: get_hash(v) for k, v in sorted(dataclasses.asdict(value).items())})
            elif isinstance(value, Variable):
                return value.get_hash(context)
            elif isinstance(value, (str, bytes)):
                pass
            elif isinstance(value, torch.Tensor):
                value = value.cpu().detach().numpy().tobytes()
            elif hasattr(value, '__getstate__'):
                return get_hash(value.__getstate__())
            elif hasattr(value, '__reduce__'):
                try:
                    states = value.__reduce__()
                    value = json.dumps([str(value.__class__), get_hash((states[1:3]))])
                except TypeError:
                    pass

            if isinstance(value, str):
                value = value.encode('utf-8')

            if not isinstance(value, bytes):
                # Fall back to pickle.
                value = pickle.dumps(value)

            return hashlib.sha1(value).hexdigest()

        return get_hash(value)

import torch
import numpy


def magic_print(obj, n_indent: int = 0, prefix: str = ""):
    prefix = str("  " * n_indent) + prefix
    if isinstance(obj, torch.Tensor):
        print(prefix, "Tensor of shape:", obj.shape)
        return None
    if isinstance(obj, numpy.ndarray):
        print(prefix, "Tensor of shape:", obj.shape)
        return None
    if obj is None:
        print(prefix, obj)
        return None

    # Nested types
    print(prefix, type(obj))
    n_indent += 1

    if isinstance(obj, dict):
        for k, v in obj.items():
            magic_print(v, n_indent, k)

    elif isinstance(obj, tuple):
        for i, v in enumerate(obj):
            magic_print(v, n_indent, str(i))
    else:
        try:
            for k, v in obj.__dict__.items():
                if not callable(obj):
                    magic_print(v, n_indent, k)
        except:
            print(prefix, "Unknown type:", type(obj))

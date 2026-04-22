"""Phase H: Dense Constraint Tests — All 59 agents with 15-30+ checkpoints each."""
from .tests import PHASE_H_TESTS as _BATCH1
from .batch2 import PHASE_H_BATCH2 as _BATCH2
from .batch3 import PHASE_H_BATCH3 as _BATCH3
from .batch4 import PHASE_H_BATCH4 as _BATCH4
from .batch5 import PHASE_H_BATCH5 as _BATCH5
from .batch6 import PHASE_H_BATCH6 as _BATCH6
from .batch7 import PHASE_H_BATCH7 as _BATCH7

PHASE_H_TESTS = _BATCH1 + _BATCH2 + _BATCH3 + _BATCH4 + _BATCH5 + _BATCH6 + _BATCH7

__all__ = ["PHASE_H_TESTS"]

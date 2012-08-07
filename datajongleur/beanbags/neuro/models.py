import sqlalchemy as sa
import sqlalchemy.orm as orm
import numpy as np
import json
import uuid
from datajongleur import Base
from datajongleur.utils.sa import NumpyType
from datajongleur.beanbags.nwu import NumericWithUnits
import datajongleur.beanbags.interfaces as i
from datajongleur.beanbags.models import *
import datajongleur.beanbags.neuro.nwu as nwu

PREFIX = 'dj_neuro_'


class SpikeTimes(nwu.SpikeTimes, Identity):
    __tablename__ = PREFIX + 'spike_times'
    __mapper_args__ = {'polymorphic_identity': 'SpikeTimes'}
    uuid = sa.Column(
        sa.ForeignKey(Identity.uuid),
        primary_key=True)
    _signal_base_amount = sa.Column('signal_base_amount', NumpyType)
    _signal_base_units = sa.Column('signal_base_units', sa.String)

    def __init__(self, times, units):
        NumericWithUnits.__init__(self, np.ones(len(times)), "")
        self.signal_base = NumericWithUnits(times, units)
        self._signal_base_amount = self.signal_base._amount
        self._signal_base_units = self.signal_base._units

    @orm.reconstructor
    def init_on_load(self):
        NumericWithUnits.__init__(
                self, np.ones(len(self._signal_base_amount)), "")
        self.signal_base = NumericWithUnits(
            self._signal_base_amount, self._signal_base_units)


class BinnedSpikes(nwu.BinnedSpikes, Identity):
    """
    ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
    integer values for ``signals`` and bin-times as ``signal_base``.
    """
    __tablename__ = PREFIX + 'binned_spikes'
    __mapper_args__ = {'polymorphic_identity': 'BinnedSpikes'}
    uuid = sa.Column(
        sa.ForeignKey(Identity.uuid),
        primary_key=True)
    _amount = sa.Column('amount', NumpyType)
    _units = sa.Column('units', sa.String)
    _start = sa.Column('start', sa.Float)
    _stop = sa.Column('stop', sa.Float)

    def __init__(self, amount, period_amount, period_units):
        nwu.BinnedSpikes.__init__(self, amount, period_amount, period_units)
        self._amount = self.amount
        self._start = self.start
        self._stop = self.stop
        self._units = self.units

    def checksum_json(self):
        return checksum_json(self)

    @orm.reconstructor
    def init_on_load(self):
        nwu.BinnedSpikes.__init__(
                self,
                self._amount,
                [self._start, self._stop],
                self._units)

if __name__ == "__main__":
    from datajongleur.utils.sa import get_test_session
    session = get_test_session(Base)

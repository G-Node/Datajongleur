import numpy as np
from datajongleur.beanbags.nwu import NumericWithUnits,\
        SimpleSampledSignal, RegularlySimpleSampledSignal

class SpikeTimes(SimpleSampledSignal):
    """
    ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
    ``signals`` and spike times as ``signal_base``, respectively.
    """

    def __init__(self, times, units):
        SimpleSampledSignal.__init__(self,
            np.ones(len(times)),
            "",
            times,
            signal_base_units)

    # ----- Implementing Interval ------
    @property
    def start(self):
        return self.info['signal_base'].min()

    @property
    def stop(self):
        return self.info['signal_base'].max()

    @property
    def length(self):
        return self.stop - self.start

    def checksum_json(self):
        return checksum_json(self)
     
    @property
    def info(self):
        return {
            'signal_base': self.signal_base}


class BinnedSpikes(RegularlySimpleSampledSignal):
    """
    ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
    integer values for ``signals`` and bin-times as ``signal_base``.
    """
    def __init__(self, amount, period_amount, period_units):
        RegularlySimpleSampledSignal.__init__(
                self,
                np.array(amount, 'int'),
                "",
                period_amount,
                period_units)

    @property
    def units(self):
        return self.period.units

    @property
    def info(self):
        return {"period": self.period}

    def checksum_json(self):
        return checksum_json(self)
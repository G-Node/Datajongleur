def assert_interval(iq, start, stop):
  assert iq.start == start
  assert iq.stop == stop
  assert iq.length == stop - start
  return True

def assert_sampled_signal(iq):
  assert len(iq) == len(iq.signal)
  assert len(iq) == len(iq.base)
  assert len(iq) == iq.n_sampling_points
  return True

def assert_regularly_sampled_signal(iq):
  assert assert_sampled_signal(iq)
  assert assert_interval(iq)
  assert iq.sampling_rate == iq.n_sampling_points/iq.length
  assert iq.step_size == 1 / iq.sampling_rate
  return True


import asyncio
import logging
import random

from datalogd import DataSource

class RandomWalkDataSource(DataSource):
    """
    Generate test or demonstration data using a random walk algorithm.

    For each iteration of the algorithm, the output value will either be
    unchanged, increase, or decrease by a fixed increment. The options are
    chosen randomly with equal probability.

    Multiple walkers can be initialised to produce several sources of random
    data. The ``walkers`` parameter is a list, the length of which determines
    the number of walkers to use. Each item in the list must be a list/tuple of
    two items: the walker's initial value and increment.

    :param seed: Seed used to initialise the random number generator.
    :param interval: How often to run an iteration of the algorithm, in seconds.
    :param walkers: List defining number of walkers and their parameters in the
        form ``[[init, increment], ...]``.
    """
    def __init__(self, sinks=[], seed=None, interval=1.0, walkers=[[0.0, 1.0], [0.0, 2.0]]):
        super().__init__(sinks=sinks)
        self.log = logging.getLogger("RandomWalkDataSource")
        random.seed(seed)
        self.interval = interval
        self.walkers = []
        for w in walkers:
            try:
                self.walkers.append([float(w[0]), float(w[1])])
            except Exception as ex:
                self.log.warning(f"Invalid parameters for walker: {w} {ex}")
        # Queue first call of update routine
        asyncio.get_event_loop().call_soon(self.generate_data)

    def generate_data(self):
        """
        Run one iteration of the random walk algorithm and send the value to any
        connected sinks.
        """
        loop = asyncio.get_event_loop()
        # Update walker values and notify sinks
        data = []
        for w_i, w in enumerate(self.walkers):
            w[0] += random.choice([-w[1], 0.0, w[1]])
            data.append({"type": "analog", "id": f"randomwalk{w_i}", "value": w[0]})
        self.send(data)
        # Reschedule next update
        loop.call_later(self.interval, self.generate_data)

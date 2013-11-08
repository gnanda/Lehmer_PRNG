#!/usr/bin/python

import time
import sys

MODULUS = 2147483647L     # DON'T CHANGE THIS VALUE
MULTIPLIER = 48271L       # use 16807 for the "minimal standard"
CHECK = 399268537L        # use 1043616065 for the "minimal standard"
STREAMS = 256             # # of streams, DON'T CHANGE THIS VALUE
A256 = 22925              # jump multiplier, DON'T CHANGE THIS VALUE
DEFAULT = 123456789L      # initial seed, use 0 < DEFAULT < MODULUS
MAX_DRAWS = 8367782       # The number of calls to random separating each stream

Q_random = MODULUS / MULTIPLIER
R_random = MODULUS % MULTIPLIER
Q_seed = MODULUS / A256
R_seed = MODULUS % A256


class LehmerRNG(object):
    """
    A Lehmer random number generator supporting 265 streams of random numbers.
    The seed is modified using the seed property. ex. rng.seed = 123456789.
    Setting the seed is done in the following way:
        "if x > 0 then x is the state
        if x < 0 then the state is obtained from the system clock
        if x = 0 then the state is to be supplied interactively."
    The stream is chosen using the stream property. ex. rng.stream = 5
    Random numbers are retrieved using the random method. rng.random()
        "The generator used in this library is a so-called 'Lehmer random number
        generator' which returns a pseudo-random number uniformly distributed
        0.0 and 1.0.  The period is (m - 1) where m = 2,147,483,647 and the
        smallest and largest possible values are (1 / m) and 1 - (1 / m)
        respectively."
    """

    def __init__(self, initial_seed=DEFAULT, initial_stream=0):
        """
        Creates an RNG object that generates pseudo-random numbers, with options to initialize the seed and the stream.

        @param initial_seed: The initial seed for the RNG
        @type initial_seed: int
        @param initial_stream: The initial stream for the RNG
        @type initial_stream: int
        """
        self.__stream = 0
        self.__seeds = [0] * STREAMS      # The current seeds of all the streams
        self.__num_draws = [0] * STREAMS  # For determining overflow
        self.stream = initial_stream      # The current stream
        self.seed = initial_seed
        self.plant_seeds(initial_seed)

    def __del__(self):
        """At the end of the program, when the destructor is called, determine whether any of the streams overlapped"""
        for k in xrange(len(self.__num_draws)):
            if self.__num_draws[k] > MODULUS:
                print >> sys.stderr, "Error: Stream %d completely cycled" % k
            j = 1
            while self.__num_draws[k] > MAX_DRAWS:
                print >> sys.stderr, "Error: Stream %d overlapped stream %d" % (k, (k+j) % STREAMS)
                self.__num_draws[k] -= MAX_DRAWS
                j += 1

    def random(self):
        """
        Returns a pseudo-random real valued float, uniformly distributed between 0.0 and 1.0, using the current stream
        of the Lehmer generator.

        @return: A pseudo-random float, uniformly distributed between 0.0 and 1.0
        @rtype : float
        """
        self.__num_draws[self.stream] += 1

        t = MULTIPLIER * (self.__seeds[self.stream] % Q_random) - R_random * (self.__seeds[self.stream] / Q_random)
        if t > 0:
            self.__seeds[self.stream] = t
        else:
            self.__seeds[self.stream] = t + MODULUS

        return float(self.__seeds[self.stream]) / MODULUS

    @property
    def seed(self):
        """The seed for the current stream"""
        return self.__seeds[self.stream]

    @seed.setter
    def seed(self, new_seed):
        if new_seed > 0:
            new_seed %= MODULUS
        if new_seed < 0:
            new_seed = int(time.time()) % MODULUS
        if new_seed == 0:
            while new_seed <= 0 or new_seed >= MODULUS:
                new_seed = input("Enter a positive integer seed (9 digits or less) >> ")
        self.__seeds[self.stream] = new_seed

    def plant_seeds(self, x):
        """
        "Use this function to set the state of all the random number generator
        streams by "planting" a sequence of states (seeds), one per stream,
        with all states dictated by the state of the default stream.
        The sequence of planted states is separated one from the next by
        8,367,782 calls to Random()."

        @param x: The seed to use to begin setting the streams' seeds
        @type x: int
        """
        s = self.stream                          # remember the current stream
        self.stream = 0                          # change to stream 0
        self.seed = x                            # set seed[0]
        self.stream = s                          # reset the current stream

        for j in xrange(1, STREAMS):
            x = A256 * (self.__seeds[j - 1] % Q_seed) - R_seed * (self.__seeds[j - 1] / Q_seed)
            if x > 0:
                self.__seeds[j] = x
            else:
                self.__seeds[j] = x + MODULUS

    @property
    def stream(self):
        """The current stream index"""
        return self.__stream

    @stream.setter
    def stream(self, index):
        self.__stream = index % STREAMS

    def test_random(self):
        """Checks for a correct implementation."""
        self.stream = 0
        self.seed = 1
        for n in range(10000):
            self.random()
        x = self.seed

        self.stream = 1
        self.plant_seeds(1)
        y = self.seed

        if x == CHECK and y == A256:
            print "The implementation is correct"
        else:
            print "Error: the implementation is not correct"


if __name__ == '__main__':
    rng = LehmerRNG()
    rng.test_random()
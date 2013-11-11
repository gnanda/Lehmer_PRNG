Lehmer_PRNG
===========

An implementation for a Lehmer pseudo-random number generator.  Ported from the C implementation to python, with some
 syntactic sugar.

Example usage:

    Creating a PRNG object:
    Using the default seed and the initial stream 0:
        my_rng = LehmerRNG()
    Specifying the seed and the initial stream:
        my_rng = LehmerRNG(123456789, 0)

    Retrieving a random float:
        a = my_rng.random()

    Choosing the stream:
        my_rng.stream = 4

    Changing the seed of the current stream:
        my_rng.seed = 123456789

    Initialize the seeds for all the streams, beginning with a specified seed:
        my_rng.plant_seeds(123456789)

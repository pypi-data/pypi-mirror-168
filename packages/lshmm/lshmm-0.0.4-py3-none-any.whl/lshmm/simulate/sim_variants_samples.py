"""Collection of functions to simulate haplotype and phased genotype data, where the data is structured as variants x samples."""
import msprime
import numpy as np

EQUAL_BOTH_HOM = 4
UNEQUAL_BOTH_HOM = 0
BOTH_HET = 7
REF_HOM_OBS_HET = 1
REF_HET_OBS_HOM = 2

# Haploid


def rand_for_testing_hap(n, m, mean_r=1e-5, mean_mu=1e-5, seed=42):
    """
    Simulate a haplotype matrix, sequence, and parameters for testing.

    Here we run a naive simulation of a haplotype matrix with no LD, a random haplotype vector to use as an observation, set a recombination probability vector, and random mutation vector for the emissions.
    """
    np.random.seed(seed)
    # sites x samples
    H = np.random.randint(2, size=(m, n))

    # Recombination probability
    r = mean_r * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)
    r[0] = 0

    # Error probability
    mu = mean_mu * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)

    # New sequence
    s = np.random.randint(2, size=(1, m))

    # Define the emission probability matrix
    e = np.zeros((m, 2))
    e[:, 0] = mu
    e[:, 1] = 1 - mu

    return H, s, r, mu, e


def rand_for_testing_hap_better(n, length=100000, mean_r=1e-5, mean_mu=1e-5, seed=42):
    """
    Simulate a haplotype matrix, sequence, and parameters for testing using msprime.

    Create a simulated haplotype matrix using msprime, by passing a genome length, mutation rate, and recombination rate across the region. We then generate a set of recombination probabilities and mutation rates for emitted sequences based on this haplotype matrix.
    """
    # Simulate
    ts = msprime.simulate(
        n + 1,
        length=length,
        mutation_rate=mean_mu,
        recombination_rate=mean_r,
        random_seed=seed,
    )
    m = ts.get_num_sites()
    H = ts.genotype_matrix()
    s = H[:, 0].reshape(1, H.shape[0])
    H = H[:, 1:]

    np.random.seed(seed)
    # Recombination probability
    r = mean_r * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)
    r[0] = 0

    # Error probability
    mu = mean_mu * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)

    # Define the emission probability matrix
    e = np.zeros((m, 2))
    e[:, 0] = mu
    e[:, 1] = 1 - mu

    return H, s, r, mu, e, m


# Diploid


def rand_for_testing_dip(n, m, mean_r=1e-5, mean_mu=1e-5, seed=42):
    """
    Simulate a phased-genotype matrix, sequence, and parameters for testing.

    Here we run a naive simulation of a haplotype matrix with no LD, a random haplotype vector to use as an observation, set a recombination probability vector, and random mutation vector for the emissions.
    """
    np.random.seed(seed)
    # Set up random genetic data
    H = np.random.randint(2, size=(m, n))
    G = np.zeros((m, n, n))
    for i in range(m):
        G[i, :, :] = np.add.outer(H[i, :], H[i, :])

    # Recombination probability
    r = mean_r * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)
    r[0] = 0

    # Error probability
    mu = mean_mu * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)

    # New sequence
    s = np.random.randint(2, size=(1, m)) + np.random.randint(2, size=(1, m))

    e = np.zeros((m, 8))
    e[:, EQUAL_BOTH_HOM] = (1 - mu) ** 2
    e[:, UNEQUAL_BOTH_HOM] = mu ** 2
    e[:, BOTH_HET] = 1 - mu
    e[:, REF_HOM_OBS_HET] = 2 * mu * (1 - mu)
    e[:, REF_HET_OBS_HOM] = mu * (1 - mu)

    return H, G, s, r, mu, e


def rand_for_testing_dip_better(n, length=100000, mean_r=1e-5, mean_mu=1e-5, seed=42):
    """
    Simulate a phased genotype matrix, sequence, and parameters for testing using msprime.

    Create a simulated phased haplotype matrix using msprime, by passing a genome length, mutation rate, and recombination rate across the region. We then generate a set of recombination probabilities and mutation rates for emitted sequences based on this phased haplotype matrix.
    """
    # Simulate
    ts = msprime.simulate(
        n + 2,
        length=length,
        mutation_rate=mean_mu,
        recombination_rate=mean_r,
        random_seed=seed,
    )
    m = ts.get_num_sites()
    H = ts.genotype_matrix()
    # New sequence
    s = H[:, 0].reshape(1, H.shape[0]) + H[:, 1].reshape(1, H.shape[0])
    H = H[:, 2:]

    G = np.zeros((m, n, n))
    for i in range(m):
        G[i, :, :] = np.add.outer(H[i, :], H[i, :])

    np.random.seed(seed)
    # Recombination probability
    r = mean_r * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)
    r[0] = 0

    # Error probability
    mu = mean_mu * np.ones(m) * ((np.random.rand(m) + 0.5) / 2)

    # Define the emission probability matrix
    e = np.zeros((m, 8))
    e[:, EQUAL_BOTH_HOM] = (1 - mu) ** 2
    e[:, UNEQUAL_BOTH_HOM] = mu ** 2
    e[:, BOTH_HET] = 1 - mu
    e[:, REF_HOM_OBS_HET] = 2 * mu * (1 - mu)
    e[:, REF_HET_OBS_HOM] = mu * (1 - mu)

    return H, G, s, r, mu, e, m

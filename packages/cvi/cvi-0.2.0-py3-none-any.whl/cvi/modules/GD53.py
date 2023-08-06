"""
The Generalized Dunn's Index 53 (GD53) Cluster Validity Index.
"""

# Custom imports
import numpy as np

# Local imports
from . import _base


# GD53 object definition
class GD53(_base.CVI):
    """
    The stateful information of the Generalized Dunn's Index 53 (GD53) Cluster Validity Index.

    References
    ----------
    1. A. Ibrahim, J. M. Keller, and J. C. Bezdek, "Evaluating Evolving Structure in Streaming Data With Modified Dunn's Indices," IEEE Transactions on Emerging Topics in Computational Intelligence, pp. 1-12, 2019.
    2. M. Moshtaghi, J. C. Bezdek, S. M. Erfani, C. Leckie, and J. Bailey, "Online Cluster Validity Indices for Streaming Data," ArXiv e-prints, 2018, arXiv:1801.02937v1 [stat.ML].
    3. M. Moshtaghi, J. C. Bezdek, S. M. Erfani, C. Leckie, J. Bailey, "Online cluster validity indices for performance monitoring of streaming data clustering," Int. J. Intell. Syst., pp. 1-23, 2018.
    4. J. C. Dunn, "A fuzzy relative of the ISODATA process and its use in detecting compact well-separated clusters," J. Cybern., vol. 3, no. 3 , pp. 32-57, 1973.
    5. J. C. Bezdek and N. R. Pal, "Some new indexes of cluster validity," IEEE Trans. Syst., Man, and Cybern., vol. 28, no. 3, pp. 301-315, Jun. 1998.
    """

    def __init__(self):
        """
        Generalized Dunn's Index 53 (GD53) initialization routine.
        """

        # Run the base initialization
        super().__init__()

        # CH-specific initialization
        self.mu = np.zeros([0])     # dim
        self.D = np.zeros([0, 0])   # n_clusters x n_clusters
        self.inter = 0.0
        self.intra = 0.0

    @_base._add_docs(_base._setup_doc)
    def _setup(self, sample: np.ndarray):
        """
        Generalized Dunn's Index 53 (GD53) setup routine.
        """

        # Run the generic setup routine
        super()._setup(sample)

        # GD53-specific setup
        self.mu = sample

    @_base._add_docs(_base._param_inc_doc)
    def _param_inc(self, sample: np.ndarray, label: int):
        """
        Incremental parameter update for the Generalized Dunn's Index 53 (GD53) CVI.
        """

        # Get the internal label corresponding to the provided label
        i_label = self.label_map.get_internal_label(label)

        # Increment the local number of samples count
        n_samples_new = self.n_samples + 1

        # Check if the module has been setup, then set the mu accordingly
        if self.n_samples == 0:
            self._setup(sample)
        else:
            self.mu = (
                (1 - 1/n_samples_new) * self.mu
                + (1/n_samples_new) * sample
            )

        # IF NEW CLUSTER LABEL
        # Correct for python 0-indexing
        if i_label > self.n_clusters - 1:
            n_new = 1
            v_new = sample
            CP_new = 0.0
            G_new = np.zeros(self.dim)
            if self.n_clusters == 0:
                D_new = np.zeros((1, 1))
            else:
                D_new = np.zeros((self.n_clusters + 1, self.n_clusters + 1))
                D_new[0:self.n_clusters, 0:self.n_clusters] = self.D
                d_column_new = np.zeros(self.n_clusters + 1)
                for jx in range(self.n_clusters):
                    d_column_new[jx] = (
                        np.sum((v_new - self.v[jx, :]) ** 2)
                    )
                D_new[i_label, :] = d_column_new
                D_new[:, i_label] = d_column_new

            # Update 1-D parameters with list appends
            self.n_clusters += 1
            self.n.append(n_new)
            self.CP.append(CP_new)

            # Update 2-D parameters with numpy vstacks
            self.v = np.vstack([self.v, v_new])
            self.G = np.vstack([self.G, G_new])
            self.D = D_new

        # ELSE OLD CLUSTER LABEL
        else:
            n_new = self.n[i_label] + 1
            v_new = (
                (1 - 1 / n_new) * self.v[i_label, :]
                + (1 / n_new) * sample
            )
            delta_v = self.v[i_label, :] - v_new
            diff_x_v = sample - v_new
            CP_new = (
                self.CP[i_label]
                + np.inner(diff_x_v, diff_x_v)
                + self.n[i_label] * np.inner(delta_v, delta_v)
                + 2 * np.inner(delta_v, self.G[i_label, :])
            )
            G_new = (
                self.G[i_label, :]
                + diff_x_v
                + self.n[i_label] * delta_v
            )
            d_column_new = np.zeros(self.n_clusters)
            for jx in range(self.n_clusters):
                # Skip the current i_label index
                if jx == i_label:
                    continue
                d_column_new[jx] = (
                    # np.sqrt(np.sum((v_new - self.v[jx, :]) ** 2))
                    (CP_new + self.CP[jx]) / (n_new + self.n[jx])
                )

            # Update parameters
            self.n[i_label] = n_new
            self.v[i_label, :] = v_new
            self.CP[i_label] = CP_new
            self.G[i_label, :] = G_new
            self.D[i_label, :] = d_column_new
            self.D[:, i_label] = d_column_new

        # Update the parameters that do not depend on label novelty
        self.n_samples = n_samples_new

    @_base._add_docs(_base._param_batch_doc)
    def _param_batch(self, data: np.ndarray, labels: np.ndarray):
        """
        Batch parameter update for the Generalized Dunn's Index 53 (GD53) CVI.
        """

        # Setup the CVI for batch mode
        super()._setup_batch(data)

        # Take the average across all samples, but cast to 1-D vector
        self.mu = np.mean(data, axis=0)
        u = np.unique(labels)
        self.n_clusters = u.size
        self.n = [0 for _ in range(self.n_clusters)]
        self.v = np.zeros((self.n_clusters, self.dim))
        self.CP = [0.0 for _ in range(self.n_clusters)]
        self.G = np.zeros((self.n_clusters, self.dim))
        self.D = np.zeros((self.n_clusters, self.n_clusters))

        for ix in range(self.n_clusters):
            # subset_indices = lambda x: labels[x] == ix
            subset_indices = (
                [x for x in range(len(labels)) if labels[x] == ix]
            )
            subset = data[subset_indices, :]
            self.n[ix] = subset.shape[0]
            self.v[ix, :] = np.mean(subset, axis=0)
            diff_x_v = subset - self.v[ix, :] * np.ones((self.n[ix], 1))
            self.CP[ix] = np.sum(diff_x_v ** 2)

        for ix in range(self.n_clusters - 1):
            for jx in range(ix + 1, self.n_clusters):
                self.D[ix, jx] = (
                    # np.sqrt(np.sum((self.v[ix, :] - self.v[jx, :]) ** 2))
                    (self.CP[ix] + self.CP[jx]) / (self.n[ix] + self.n[jx])
                )

        self.D = self.D + np.transpose(self.D)

    @_base._add_docs(_base._evaluate_doc)
    def _evaluate(self):
        """
        Criterion value evaluation method for the Generalized Dunn's Index 53 (GD53) CVI.
        """

        if self.n_clusters > 1:
            self.intra = 2 * np.max(np.divide(self.CP, self.n))
            # Between-group measure of separation/isolation
            self.inter = (
                np.min(self.D[
                    np.triu(
                        np.ones((self.n_clusters, self.n_clusters), bool), 1
                    ),
                ])
            )
            # GD53 index value
            self.criterion_value = self.inter / self.intra
        else:
            self.criterion_value = 0.0

# rail_gpz_v1
RAIL interface to Peter Hatfield's python 3 port of the GPz v1 algorithm.  A slight modification of Peter's code found here: <br>
[https://github.com/pwhatfield/GPz_py3](https://github.com/pwhatfield/GPz_py3)<br>
which is itself adapted from Ibrahim Almosallam's original implementation here:<br>
[https://github.com/OxfordML/GPz](https://github.com/OxfordML/GPz) (in Matlab).<br>
If subsequent versions of GPz with either improved features or faster performance are made available then they may replace this version.

Any use of `rail_gpz_v1` in a paper or report should cite [Almosallam et al. 2016](https://ui.adsabs.harvard.edu/abs/2016MNRAS.462..726A/abstract)

There are several free parameters that can be set via the `config_params` in `Inform_GPz_v1` that will be described in brief below, See [Almosallam et al. 2016](https://ui.adsabs.harvard.edu/abs/2016MNRAS.462..726A/abstract) for more details on the parameters, their meanings, and their effects :<br>
`gpz_method` (str): this parameter takes a str argument that sets how the length scale and covariance of the radial basis functions behave in the Gaussian process.  Valid options are `GL`, `VL`, `GD`, `VD`, `GC`, and `VC`, and give the following behavior:<br>
- `GL`: "global length scale", all basis functions share a single length scale.<br>
- `VL`: "variable length scale", each basis function has its own length scale.<br>
- `GD`: "global diagonal covariance", all basis functions share a signle diagonal covariance.<br>
- `VD`: "variable diagonal`, each basis function has its own (diagonal) covariance.<br>
- `GC`: "global covariance`, all basis functions share a single (non-diagonal) covariance.<br>
- `VC`(default): "variable covariance", each basis function has a unique non-diagonal covariance.<br>

`trainfrac` (float): this parameter sets the fraction of the training set to be used to train the GP, the remainder is used as validation data when determining the parameter SIGMA.<br>

`n_basis` (int): this parameter sets the number of radial basis functions to use in the GPz model.<br>

`learn_jointly` (bool): this parameter sets whether to jointly learn the prior linear mean function.<br>

`hetero_noise` (bool): this parameter, if set to True, learns heterscedastic noise process.<br>

`csl_method` (str): this parameter sets the "cost sensitive learning" method, valid arguments are "normal", "balanced", and "normalized".  This refers to a weight vector applied to the training data that can attempt to "balance" the training set. If "normal" is chosen (the default), then no weights are applied.  If "balanced" is chosen then rare samples are upweighted during training.  If "normalized" is chosen the a a weight inversely proportional to redshift is applied to each galaxy: w=1/(1+z).<br>

`csl_binwidth` (float): this parameter sets the bandwidth for the cost sensitive learning if csl_method is set to True.<br>

`pca_decorrelate` (bool): if True, this parameter decorrelates the data using PCA in a preprocessing stage.<br>

`max_iter` (int): the maximum number of iterations to perform during training.<br>

`max_attempt` (int): sets the maximum iterations if no progress made during validation.<br>

`log_errors` (bool): if True, takes the log of magnitude errors before feeding into the algorithm.<br>



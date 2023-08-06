import os
import torch
from botorch.acquisition.multi_objective.monte_carlo import qExpectedHypervolumeImprovement, qNoisyExpectedHypervolumeImprovement
from botorch.optim.optimize import optimize_acqf
from botorch.models.gp_regression import FixedNoiseGP
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from botorch.exceptions import BadInitialCandidatesWarning
from botorch.utils.multi_objective.box_decompositions.dominated import DominatedPartitioning
from botorch.sampling.samplers import SobolQMCNormalSampler
from botorch.utils.transforms import unnormalize, normalize
from botorch.utils.sampling import draw_sobol_samples
import pandas as pd
import numpy as np
from .sample_space import generate_sample_space
import warnings
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


tkwargs = {
    "dtype": torch.double,
    "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
}
SMOKE_TEST = os.environ.get("SMOKE_TEST")


class Active_Learning_Loop:
    def __init__(self, filename, label_x, label_y, target, scaling = None):
        self.hypervolumes =[0]
        self.label_x = label_x
        self.label_y = label_y
        if scaling is None:
            scaling = ['lin']*len(label_y)
        self.train_x, self.train_y, self.train_yvar, self.ref_point = self.read_data(filename, target, scale = scaling)
        self.model = None

    def run_Loop(self):
        warnings.filterwarnings('ignore', category=BadInitialCandidatesWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)

        N_BATCH = 20 if not SMOKE_TEST else 10
        MC_SAMPLES = 512  if not SMOKE_TEST else 16

        hvs_qnehvi = []
        self.y_bounds= torch.stack([self.train_y.min(axis = 0)[0], self.train_y.max(axis = 0)[0]])

        self.train_y_norm = normalize(self.train_y, bounds = self.y_bounds)
        self.train_yvar_norm = normalize(self.train_yvar + self.train_y.min(axis = 0)[0], bounds = self.y_bounds)

        mll, self.model = self.initialize_model()
        
        # compute hypervolume
        bd = DominatedPartitioning(ref_point= self.ref_point, Y=self.train_y)
        volume = bd.compute_hypervolume().item()
        print(volume)
        self.hypervolumes.append(volume)
        hvs_qnehvi.append(volume)

        qnehvi_sampler = SobolQMCNormalSampler(num_samples=MC_SAMPLES)
            
            # optimize acquisition functions and get new observations

        new_x_qnehvi = self.optimize_qnehvi_and_get_observation(qnehvi_sampler)
        self.predictions_OG = self.get_prediction(new_x_qnehvi)
        self.predictions_clean = self.get_prediction(self.clean_predictions(new_x_qnehvi),  save = True)

        return self.predictions_OG, self.predictions_clean


    def clean_predictions(self, X):
        X = (X > 0.04).float()*X
        X = X / X.sum(dim=-1).unsqueeze(-1)
        X = torch.round(X, decimals = 3)
        return X

    def optimize_qnehvi_and_get_observation(self, sampler):
        """Optimizes the qEHVI acquisition function, and returns a new candidate and observation."""
        # partition non-dominated space into disjoint rectangles
        acq_func = qNoisyExpectedHypervolumeImprovement(
            model=self.model,
            ref_point=[0.,0.,0.,0.],#normalize(self.ref_point, self.y_bounds),  # use known reference point 
            X_baseline=self.train_x,
            prune_baseline=True,  # prune baseline points that have estimated zero probability of being Pareto optimal
            sampler=sampler,
        )
        # optimize

        #samp_space = generate_initial_space()
        #print(samp_space.shape)
        standard_bounds = torch.zeros(2, 3, **tkwargs)
        standard_bounds[1] = 1
        standard_bounds[1][-1] = 0.4

        candidates, _ = optimize_acqf(
            acq_function=acq_func,
            bounds=standard_bounds,
            q=5,
            num_restarts=10,
            raw_samples= 512,  #used for intialization heuristic
            options= {"batch_limit": 5, "maxiter": 200, "disp":True},
            #batch_initial_conditions= samp_space,
            equality_constraints = [(torch.tensor([0,1,2], **{"dtype": torch.int64,"device": torch.device("cuda" if torch.cuda.is_available() else "cpu")}),torch.tensor(np.array([1,1,1]), **tkwargs), float(1.0))],
            sequential=False,
        )
        #torch.tensor(np.array([0,1,2,3,4]), **{"dtype": torch.int,"device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),})
        # observe new values 
        #new_x =  unnormalize(candidates.detach(), bounds=BOUNDS)
        new_x = candidates.detach()
        #new_obj_true = problem(new_x)
        #new_obj = new_obj_true + torch.randn_like(new_obj_true)
        return new_x

    def read_data(self, filename, targets, scale):
        data_frame = pd.read_excel(filename)
        data_frame = data_frame.dropna(0)
        print(data_frame)
        #data_frame = data_frame.loc[data_frame[['HEMA']].sum(axis=1) == 0,:]
        #data_frame = data_frame.loc[data_frame[['monomer 6']].sum(axis=1) == 0,:].fillna(0)
        data_frame_x = data_frame[self.label_x]
        data_frame_y = data_frame[self.label_y]
        data_frame_yvar = data_frame[[p+'_stdev' for p in self.label_y]]
        self.train_y_OG = torch.tensor(np.array(data_frame_y), **tkwargs)
        self.targets = {}
        self.scales = {}
        i = 0
        for c in data_frame_y.columns:
            if scale[i] == 'log10':
                print(c, data_frame_y[c].max() - data_frame_y[c].min())
                y_upper_sc = np.log10(data_frame_y[c] + data_frame_yvar[c+'_stdev'], dtype = np.float64)
                data_frame_y[c] = np.log10(data_frame_y[c])
                data_frame_yvar[c+'_stdev'] = y_upper_sc - data_frame_y[c]
            self.scales[c] = scale[i]
            self.targets[c] = targets[i]
            i += 1
        train_x = torch.tensor(np.array(data_frame_x), **tkwargs)
        train_y = torch.tensor(np.array(data_frame_y), **tkwargs)

        train_yvar = torch.tensor(np.array(data_frame_yvar), **tkwargs)
        if 'min' in targets:
            min_prop = targets.index('min')
            train_y[:,min_prop] = -train_y[:,min_prop]
        ref_point = train_y.min(axis = 0)[0]
        print(train_y)
        print(ref_point)
        return train_x, train_y, train_yvar, ref_point

    def generate_initial_space():
        samps = generate_sample_space(monomers= ['HEA','IDA','t-BA', 'IBOA'], cross = ['cross-linker A'])
        return torch.tensor(np.array(samps))

    def initialize_model(self):
        # define models for objective and constraint
        #BOUNDS = torch.cat([torch.tensor([[0,0,0]], **tkwargs), torch.tensor([[1,1,1]], **tkwargs)])
        #train_x = normalize(self.train_x, BOUNDS)
        models = []
        for i in range(self.train_y.shape[-1]):
            train_y = self.train_y_norm[..., i:i+1]
            train_yvar = self.train_yvar_norm[..., i:i+1]
            models.append(FixedNoiseGP(self.train_x, train_y, train_yvar, outcome_transform=Standardize(m=1)))
        model = ModelListGP(*models)
        mll = SumMarginalLogLikelihood(model.likelihood, model)
        return mll, model

    def get_prediction(self, X, save = False):
        if type(X) == pd.core.frame.DataFrame:
            X = X[self.label_x].dropna(0)
            X = torch.tensor(X, **tkwargs)
        
        out = self.model.posterior(X)

        if save:
            self.predictions_out = out.mean
        comps = pd.DataFrame(X.cpu().detach().numpy(), columns = self.label_x)
        props = pd.DataFrame(unnormalize(out.mean, self.y_bounds).cpu().detach().numpy(), columns = self.label_y)
        prop_var = pd.DataFrame((unnormalize(out.variance, self.y_bounds) - self.y_bounds[0]).cpu().detach().numpy(), columns = [p+'_stdev' for p in self.label_y])
        out = pd.concat([comps, props, prop_var], axis = 1)[self.label_x + sorted(self.label_y + [p+'_stdev' for p in self.label_y])]

        for k in self.scales:
            if self.targets[k] == 'min':
                out[k] = -out[k]
            
            if self.scales[k] == 'log10':
                print(out[k+'_stdev'])
                yvar_unsc = np.power(10, out[k+'_stdev'] + out[k])
                out[k] = np.power(10, out[k])
                out[k + '_stdev'] = yvar_unsc - out[k]
        
        return out

    def calculate_hypervolume(self, data_type = 'original', norm = True):
        if norm: 
            rf = normalize(self.ref_point, self.y_bounds)
            y = self.train_y_norm
            if data_type == 'recs':
                y = torch.concat([y, self.predictions_out])
        else:
            rf = self.ref_point
            y = self.train_y
            if data_type == 'recs':
                y = torch.concat([y, unnormalize(self.predictions_out, self.y_bounds)])
        
        if data_type == 'original':
            bd = DominatedPartitioning(ref_point= rf, Y=y)
            volume = bd.compute_hypervolume().item()
            return volume
        
        if data_type == 'recs':
            bd = DominatedPartitioning(ref_point= rf, Y=y)
            volume = bd.compute_hypervolume().item()
            return volume

    
    def visualize_prop_space(self, data_type = 'original', props = [0,1], ref = None):
        if ref is None:
            ref = self.predictions_clean
        X = self.train_y_OG.cpu().detach().numpy()
        
        #pca = PCA(n_components=2)
        #pca = pca.fit(X)
        #X = pca.transform(X)
        plt.scatter(X[:,props[0]], X[:,props[1]], label = 'Original Data')
        plt.xlabel(self.label_y[props[0]])
        plt.ylabel(self.label_y[props[1]])
        if data_type == 'recs':
            X2 = np.array(ref[[self.label_y[props[0]], self.label_y[props[1]]]])
            #X2 = pca.transform(X2)
            #print(X2[:,0].shape)
            print(np.array(ref[self.label_y[props[0]]+'_stdev']))
            plt.errorbar(X2[:,0], X2[:,1], xerr = np.array(ref[self.label_y[props[0]]+'_stdev']), yerr = np.array(ref[self.label_y[props[1]]+'_stdev']), marker = 'o',ls='none',color = 'r', label = 'New Sample Predictions')
            #plt.errorbar(X2[:,0], X2[:,1] ,color = 'r', label = 'New Sample Predictions')

        plt.legend()
        plt.show()
        
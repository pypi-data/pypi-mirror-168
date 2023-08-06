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
from data_tools.sample_space import generate_sample_space
import warnings


tkwargs = {
    "dtype": torch.double,
    "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
}
SMOKE_TEST = os.environ.get("SMOKE_TEST")


class Active_Learning_Loop:
    def __init__(self, filename, label_x, label_y, target):
        self.hypervolumes =[0]
        self.label_x = label_x
        self.label_y = label_y
        self.train_x, self.train_y, self.train_yvar, self.ref_point = self.read_data(filename, target)
        self.model = None

    def run_Loop(self):
        warnings.filterwarnings('ignore', category=BadInitialCandidatesWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)

        N_BATCH = 20 if not SMOKE_TEST else 10
        MC_SAMPLES = 128  if not SMOKE_TEST else 16

        hvs_qnehvi = []
        # call helper functions to generate initial training data and initialize model

    
        y_bounds = torch.cat([torch.tensor([[0]*4], **tkwargs), torch.tensor(self.train_y.max(axis = 0)[0].clone().detach(), **tkwargs).view(1,-1)])
        y_bounds_unnorm = torch.stack([self.train_y.min(axis = 0)[0], self.train_y.max(axis = 0)[0]])
        print(y_bounds_unnorm)
        #print(torch.tensor(train_y.max(axis = 0)[0], **tkwargs))
        self.train_y_norm = normalize(self.train_y, bounds = y_bounds)
        self.train_yvar_norm = normalize(self.train_yvar, bounds = y_bounds)
        #print(train_y_norm)
        #print(train_y_norm.max(axis = 0))
        mll, self.model = self.initialize_model()
        
        # compute hypervolume
        bd = DominatedPartitioning(ref_point= self.ref_point, Y= self.train_y)
        volume = bd.compute_hypervolume().item()
        print(volume)
        self.hypervolumes.append(volume)
        hvs_qnehvi.append(volume)

        qnehvi_sampler = SobolQMCNormalSampler(num_samples=MC_SAMPLES)
            
            # optimize acquisition functions and get new observations

        new_x_qnehvi = self.optimize_qnehvi_and_get_observation(qnehvi_sampler)
        out = self.model.posterior(new_x_qnehvi)
        comps = pd.DataFrame(new_x_qnehvi.cpu().detach().numpy(), columns = self.label_x)
        props = pd.DataFrame(unnormalize(out.mean, y_bounds_unnorm).cpu().detach().numpy(), columns = self.label_y)
        prop_var = pd.DataFrame(unnormalize(out.variance, y_bounds_unnorm).cpu().detach().numpy(), columns = [p+'_stdev' for p in self.label_y])
        self.predictions = pd.concat([comps, props, prop_var], axis = 1)[self.label_x + sorted(self.label_y + [p+'_stdev' for p in self.label_y])]

        
        new_x_qnehvi = self.clean_predictions(new_x_qnehvi)
        out = self.model.posterior(new_x_qnehvi)
        comps = pd.DataFrame(new_x_qnehvi.cpu().detach().numpy(), columns = self.label_x)
        props = pd.DataFrame(unnormalize(out.mean, y_bounds_unnorm).cpu().detach().numpy(), columns = self.label_y)
        prop_var = pd.DataFrame(unnormalize(out.variance, y_bounds_unnorm).cpu().detach().numpy(), columns = [p+'_stdev' for p in self.label_y])
        self.predictions2 = pd.concat([comps, props, prop_var], axis = 1)[self.label_x + sorted(self.label_y + [p+'_stdev' for p in self.label_y])]

        return self.predictions, self.predictions2


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
            ref_point=self.ref_point,  # use known reference point 
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
            equality_constraints = [(torch.tensor(np.array([0,1,2]), **{"dtype": torch.int64,"device": torch.device("cuda" if torch.cuda.is_available() else "cpu")}),torch.tensor(np.array([1,1,1]), **tkwargs), float(1.0))],
            sequential=False,
        )
        #torch.tensor(np.array([0,1,2,3,4]), **{"dtype": torch.int,"device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),})
        # observe new values 
        #new_x =  unnormalize(candidates.detach(), bounds=BOUNDS)
        new_x = candidates.detach()
        #new_obj_true = problem(new_x)
        #new_obj = new_obj_true + torch.randn_like(new_obj_true)
        return new_x



    def read_data(self, filename, targets):
        data_frame = pd.read_excel(filename)
        data_frame = data_frame.dropna(0)
        #data_frame = data_frame.loc[data_frame[['HEMA']].sum(axis=1) == 0,:]
        #data_frame = data_frame.loc[data_frame[['monomer 6']].sum(axis=1) == 0,:].fillna(0)
        data_frame_x = data_frame[self.label_x]
        data_frame_y = data_frame[self.label_y]
        data_frame_yvar = data_frame[[p+'_stdev' for p in self.label_y]]
        train_x = torch.tensor(np.array(data_frame_x), **tkwargs)
        train_y = torch.tensor(np.array(data_frame_y), **tkwargs)
        train_yvar = torch.tensor(np.array(data_frame_yvar), **tkwargs)
        ref_point = train_y.min(axis = 0)[0]
        if 'min' in targets:
            min_prop = targets.index('min')
            ref_point[min_prop] = train_y[:,min_prop].max().item()
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
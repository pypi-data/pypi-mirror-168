import pandas as pd
from itertools import combinations, product
import numpy as np
from scipy.stats import norm
from .gpr import model_building


def generate_sample_space(monomers, cross, num_comb = 2, cross_content = [0, 0.01, 0.02, 0.03, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4], get_excel = False, comp_tens = False):
    res = list(combinations(monomers, num_comb))
    final = []
    for i in res:
        for c in cross:
            i = list(i)
            final.append(i + [c])

    sample_df = pd.DataFrame(columns = monomers + cross)
    ratios = monomer_ratios(5)
    i = 0
    
    # for r in range(len(final)):
    #     for rat in ratios:
    #         for m in cross_content:
    #             mon_cont = 1 - m
    #             sample_df.loc[i, final[r][2]] = m
    #             for mon in range(len(final[r])-1):
    #                 sample_df.loc[i, final[r][mon]] = rat[mon]*mon_cont/sum(rat)
    #                 sample_df.loc[i, final[r][mon]] = rat[mon]*mon_cont/sum(rat)
    #             i += 1
    sample_df = pd.DataFrame(ratios, columns = monomers + cross)
    sample_df = sample_df.fillna(0).drop_duplicates().reset_index(drop = True)
    
    if comp_tens:
        sample_df['type'] = 0
        dup_df = sample_df.copy()
        dup_df['type'] = 1
        sample_df = sample_df.append(dup_df, ignore_index=True)

    if get_excel: sample_df.to_excel('data_space.xlsx')
    return sample_df

def monomer_ratios(num):
    res = np.array([i for i in product(np.linspace(0, 1, 21), repeat=num) if sum(i) == 1 and i[4] <= 0.4])
    return res

def predict_sample_uncertainty(models, sample_space, targets, dual_props = []):
    """
    For each model, makes predictions for a given space space.
    returns the combined variance of each predicted sample
    """
    properties = models.keys()
    y_pred = {}
    var = {}
    var_sc = {}
    key = {0:'compressive', 1:'tensile'}
    X_pred = np.array(sample_space.loc[sample_space['type'] == 0])
    i = 0
    for prop in properties:
        if prop in dual_props:
            for k in key:
                t = key[k]
                X_pred_temp = np.array(sample_space.loc[sample_space['type'] == k])
                y_pred[t + ' ' + prop], var[t + ' ' + prop] = models[prop].predict(X_pred_temp, return_std = True)
                var_sc[t + ' ' + prop] = np.power(var[t + ' ' + prop] / y_pred[t + ' ' + prop],2)
                targets[t + ' ' + prop] = targets[prop]
        else:
            y_pred[prop], var[prop] = models[prop].predict(X_pred, return_std = True)
            var[prop] = var[prop].reshape(-1)
            y_pred[prop] = y_pred[prop].reshape(-1)
            var_sc[prop] = np.power(var[prop] / y_pred[prop],2)
     #   print(var_sc[prop])

    #print(var_sc)
    hyper_var = np.sum([var[prop] for prop in var.keys()], axis = 0)
    #print(hyper_var.shape)
    hyper_var = np.sqrt(hyper_var)
    #print(hyper_var)
    #hyper_pred = np.prod(np.concatenate([y_pred[prop] for prop in properties], axis = -1), axis = -1)
    hyper_pred = calculate_hypervol(y_pred, targets)
    return hyper_pred, hyper_var, y_pred, var

def calculate_hypervol(Y, targets):
    prop_space = []
    props = list(Y.keys())
    for K in props:
        prop_space.append(Y[K])
    prop_space = np.array(prop_space).T
    ref_point = []
    for i in range(len(props)):
        t = targets[props[i]]
        if t == 'max':
            ref_point.append(0)
        elif t == 'min':
            ref_point.append(np.amax(prop_space, axis = 0)[0])
            prop_space[:,[i]] = ref_point[i] - prop_space[:,[i]]
        elif isinstance(t, float()):
            ref_point.append(0)
            prop_space[:,[i]] = np.power((prop_space[:,[i]] - t), 2)
    
    hyper_vol = np.prod(prop_space, axis = -1)
    return hyper_vol


def experiment_recommendation(sample_space, hyper_pred, uncertainty, known_space, predicted_samps, rec_type = 'High_Variance', targets = None):
    if rec_type == 'High_Variance':
        ind = np.argpartition(uncertainty, -5)[-5:]
        benchmark = max(uncertainty[ind])
        high_var = np.where(np.logical_and(uncertainty >= benchmark*0.99, uncertainty <= benchmark*1.01))[0]
        print(high_var)
        if ind.shape[0] > high_var.shape[0]: high_var = ind
        print(ind.shape)
        
    elif rec_type == 'Predictive_Variance':
        prop_list = []
        if not targets:
            raise Exception('Target needs to be specified for Predictive Variance recommendations.')
        ind = []
        var = uncertainty
        for i in range(5):
            #print(var)
            highest_var = sample_space.loc[np.argmax(var)] #highest var = sample combination with the highest variance
            ind.append(np.argmax(var))
            highest_var['type'] = 0
            for prop in [p for p in list(predicted_samps.keys()) if 'tensile' not in p]:
                p = [c for c in known_space.columns if str(c) in prop][0]
                prop_list.append(p)
                print(highest_var)
                highest_var.loc[p] = np.array(predicted_samps[prop][ind[-1]])
                highest_var.loc[p + '_stdev'] = 0
            known_space = known_space.append(highest_var, ignore_index = True)
            highest_var = sample_space.loc[np.argmax(var)]
            highest_var['type'] = 1
            for prop in [p for p in list(predicted_samps.keys()) if 'compressive' not in p]:
                p = [c for c in known_space.columns if str(c) in prop][0]
                print(highest_var)
                highest_var.loc[p] = np.array(predicted_samps[prop][ind[-1]])
                highest_var.loc[p + '_stdev'] = 0
            known_space = known_space.append(highest_var, ignore_index = True)
            print(known_space)
            models = update_models(known_space, list(sample_space.keys()),prop_list)
            _, var, _, _ = predict_sample_uncertainty(models, sample_space, targets)
    elif rec_type == 'EI1':
        print(hyper_pred)
        Exp_Imp = EI_1(hyper_pred, uncertainty, max(hyper_pred))
        ind = np.argpartition(Exp_Imp, -5)[-5:]
        print(Exp_Imp[ind])
    return ind, sample_space.loc[ind]

def EI_1(pred, std, best, ep = 0.01):
    #print(std)
    sigma = std
    imp = pred - best - ep
    print(imp)
    Z = imp / std
    ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
    print(norm.cdf(Z))
    ei[sigma == 0.0] = 0.0
    return ei

def EI_2(pred, std):
    pass

def update_models(known_space: pd.DataFrame, vars, props):
    surr, __ = model_building(known_space, vars ,props, std = True)
    return surr

def best_sample(samples, targets):
    samples = samples[[col for col in samples.columns if ('hardness' in col or 'strength' in col or 'modulus' in col or 'yield strength' in col) and 'stdev' not in col]]
    samples = samples.divide(samples.max(axis = 0))
    hypervols = calculate_hypervol(samples, targets)
    print(hypervols)
    best_id = np.argmax(np.nan_to_num(hypervols, nan = 0))
    return best_id



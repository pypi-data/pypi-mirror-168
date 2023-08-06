from email.mime import base
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from itertools import combinations

def R_sq(y,  y_pred):
    y = np.array(y) #reshape(-1,1)
    mean_y = np.mean(y)
    sq_error = np.sum(np.power(y - y_pred, 2))

    print(sq_error)
    mean_diff_sq = np.sum(np.power(mean_y- y, 2))

    print(mean_diff_sq)
    return 1 - (sq_error / mean_diff_sq)


def uncertainty_parity(model, train_df, test_df, prop_num = 4):
    X_train = np.array(train_df.iloc[:, :-prop_num]).astype(float)
    X_test = np.array(test_df.iloc[:, :-prop_num]).astype(float)
    properties = train_df.columns[-prop_num:]
    for prop in properties:
        y_train = train_df[prop]
        y_test = test_df[prop]
        yy_train, train_var = model[prop].predict(X_train,  return_std = True)
        yy_test, test_var = model[prop].predict(X_test, return_std = True)
        plt.figure()

        plt.errorbar(y_train, yy_train, yerr = train_var, c = 'orange', fmt = 'o', zorder = 20)
        plt.errorbar(y_test , yy_test, yerr= test_var, fmt =  'o')

        plt.plot(np.linspace((min(y_test)), (max(y_test)), num = 2),np.linspace((min(y_test)), (max(y_test)), num = 2),'k-')
        plt.ylabel('Prediction')
        plt.xlabel('Truth')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend(['Truth = Prediction','Train','Test'])
        plt.title(prop + ' GPR Parity Plot: R^2 Test = ' + str(r2_score(y_test, yy_test)))    

def single_prop_comparison(models, prop, mon, cross, prop_space, data_mon, scalers, std_list = None):
    test_data = pd.DataFrame(columns = data_mon.columns)
    m = models[prop]
    data_mon = data_mon.loc[prop_space[prop][prop_space[prop][prop] >= 0].index]
    test_data[mon] = np.linspace(0.6, 1, 60)
    test_data[cross] = 1 - test_data[mon]
    test_data = test_data.fillna(0)

    y_pred, std = m.predict(np.array(test_data),return_std = True)
    y_pred = scalers[prop].inverse_transform(y_pred)
    std = std*(scalers[prop].data_max_ - scalers[prop].data_min_)

    
    #data_mon[mon]>0
    #Plot #########################
    plt.plot(test_data[cross], y_pred, '--', label = 'ML Prediction')
    plt.fill_between(test_data[cross], (y_pred - std.reshape(-1,1)).reshape(-1,), (y_pred + std.reshape(-1,1)).reshape(-1,), alpha = 0.35, label = 'Uncertainty')
    if std_list is not None:
        plt.errorbar(data_mon.loc[data_mon[mon]>0,cross], scalers[prop].inverse_transform(np.array(prop_space[prop].loc[data_mon[mon]>0,prop]).reshape(-1,1)), yerr = np.array(std_list).reshape(-1,), fmt = 'o', label = 'Experimental Points')
    else:
        plt.scatter(data_mon.loc[data_mon[mon]>0,cross], scalers[prop].inverse_transform(np.array(prop_space[prop].loc[data_mon[mon]>0,prop]).reshape(-1,1)), label = 'Experimental Points')
    plt.ylabel(prop)
    plt.xlabel(cross + '% with ' + mon)
    plt.legend()

def property_space_viz(prop_space, pred_space, pred_var, models, data, scalers, selection = np.array([None]), new_exp = False):
    props = list(pred_space.keys())
    p_combs = combinations(props, 2)
    plt.style.use('seaborn')
    
    for p in p_combs:
        plt.figure()
        plt.title(f'Data Space Visualization: {p[1]} vs. {p[0]}')
        plt.xlabel(p[0])
        plt.ylabel(p[1])
        #Points where we know both properties exp values
        joint_space = prop_space[p[0]].merge(prop_space[p[1]], on = 'ID')
        print(joint_space)
        #prop2 predictions for points with just prop1
        #X = np.array(data.loc[prop_space[p[0]][prop_space[p[0]][p[0]] >= 0].index])
        y_pred_2, std_2 = pred_space[p[1]], pred_var[p[1]]
        #y_pred_2, std_2 = models[p[1]].predict(X, return_std = True)
        
        #prop1 predictions for points with just prop2
        #X = np.array(data.loc[prop_space[p[1]][prop_space[p[1]][p[1]] >= 0].index])
        y_pred_1, std_1 = pred_space[p[0]], pred_var[p[0]]
        #y_pred_1, std_1 = models[p[0]].predict(X, return_std = True)
        if "tensile" in p[0] or "compressive" in p[0]:
            base_prop_0 = ' '.join(p[0].split(" ")[1:])
            print(base_prop_0)
        else:
            base_prop_0 = p[0]
        
        if "tensile" in p[1] or "compressive" in p[1]:
            base_prop_1 = ' '.join(p[1].split(" ")[1:])
            print(base_prop_1)
        else:
            base_prop_1 = p[1]

        if base_prop_0 == base_prop_1:
            j_0 = base_prop_0 + "_x"
            j_1 = base_prop_1 + "_y"
            print(joint_space)
        else:
            j_0 = base_prop_0 
            j_1 = base_prop_1 

        #Plot
        #plt.errorbar(scalers[base_prop_0].inverse_transform(np.array(joint_space[base_prop_0]).reshape(-1, 1)), scalers[base_prop_1].inverse_transform(np.array(joint_space[base_prop_1]).reshape(-1, 1)), color = 'blue', fmt = 'o', zorder = 5, label = f'{p[0]} Experimental')
        #plt.errorbar(scalers[base_prop_0].inverse_transform(y_pred_1.reshape(-1, 1)), scalers[base_prop_1].inverse_transform(np.array(prop_space[p[1]]).reshape(-1, 1)), color = 'green', fmt = 'o', zorder = 5, label = f'{p[1]} Experimental')
        
        try:
            #plot known points
            plt.errorbar(scalers[base_prop_0].inverse_transform(np.array(joint_space[j_0]).reshape(-1, 1)), 
            scalers[base_prop_1].inverse_transform(np.array(joint_space[j_1]).reshape(-1, 1)), color = 'red', fmt = 'o', zorder = 10, label = f'{p[0]} and {p[1]} Experiments')
        except:
            print(f'Error in plotting joint points for {p[1]} vs {p[0]}')

        x = np.array([float(a) for a in scalers[base_prop_0].inverse_transform(pred_space[p[0]].reshape(-1,1)).reshape(-1,1)])
        y = np.array([float(a) for a in scalers[base_prop_1].inverse_transform(pred_space[p[1]].reshape(-1,1)).reshape(-1,1)])
        x_err = np.array([float(a) for a in (pred_var[p[1]]*(scalers[base_prop_0].data_max_ - scalers[base_prop_0].data_min_)).reshape(-1,1)])
        y_err = np.array([float(a) for a in (pred_var[p[0]]*(scalers[base_prop_1].data_max_ - scalers[base_prop_1].data_min_)).reshape(-1,1)])

        print(x.shape, y.shape, x_err.shape, y_err.shape)
        _,_,bars = plt.errorbar(x, y, yerr = y_err, xerr = x_err, color = 'orange', fmt='o')
        [b.set_alpha(0.05) for b in bars]
        if new_exp:
            x = []
            y = []
            selection = list(selection)
            for s in selection:
                x.append(scalers[base_prop_0].inverse_transform(pred_space[p[0]][s].reshape(-1,1))) 
                y.append(scalers[base_prop_1].inverse_transform(pred_space[p[1]][s].reshape(-1,1)))
            print(x,y)
            plt.scatter(x, y, color='blue', zorder = 20, label = 'Proposed Next Experiments')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4))
        plt.show()
    
    # plt.errorbar(pred_space[p[0]], pred_space[props[1]], yerr = np.array([i[0] for i in np.array(pred_var[props[1]])]), xerr = np.array([i[0] for i in np.array(pred_var[p[0]])]), color = 'orange', fmt='o')

def AL_summary():
    data = pd.read_excel('AM-designchart-CA (3).xlsx')
    max_round = max(data['Round'])
    props = ['compressive modulus',	'compressive strength',	'compressive yield strain',	'hardness',	'tensile modulus',	'tensile strength',	'tensile yield strain']
    
    max_df = pd.DataFrame(columns = props)
    
    #Create figure
    fig = plt.figure()
    

    for rnd in list(range(max_round+1)):
        subset = data.loc[data['Round'] <= rnd,:]
        max_dict = {'Round':rnd}
        for prop in props:
            max_dict[prop] = max(subset[prop])
        
        max_df = max_df.append(max_dict, ignore_index = True)
    
    print(max_df)
    max_df = max_df.divide(max_df.loc[0])
    print(max_df)
    for prop in props:
        print(max_df[prop])
        plt.plot(list(range(max_round + 1)), max_df[prop], label = prop)

    plt.legend()
    plt.show()

    
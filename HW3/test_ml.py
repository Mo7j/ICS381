if __name__ == "__main__":
    import numpy as np
    from machine_learning import *
    import warnings
    warnings.filterwarnings('ignore')

    np.random.seed(35171)
    
    # setup stroke dataset
    cv_df = pd.read_csv('stroke_cv.csv')
    heldout_test_df = pd.read_csv('stroke_heldout_test.csv')
    
    disc_features = ['gender', 'hypertension', 'heart_disease', 'ever_married',
                  'work_type', 'Residence_type', 'smoking_status']
    cont_features = ['age', 'avg_glucose_level', 'bmi']
    label_col = 'stroke'
    
    # testing out preprocessing function
    X_train, y_train, X_test, y_test = preprocess_dataset(cv_df, heldout_test_df, discrete_columns=disc_features, 
                                                          continuous_columns=cont_features, 
                                                          label_column=label_col)
                                                          
    print(f'(X_train={X_train.shape}, y_train={y_train.shape})')
    print(f'(X_test={X_test.shape}, y_test={y_test.shape})')
    print(X_train[:5,:])
    print(y_train[:5])
    print(X_test[:5,:])
    print(y_test[:5])
    print('\n_______________________________________________________________________\n\n')
    
    # do model selection us k-fold cv
    print('Performing 3-fold cv...')
    
    cv_results_df = k_fold_cv(cv_df, discrete_columns=disc_features, 
                              continuous_columns=cont_features, 
                              label_column=label_col, k=3)
    
    print(cv_results_df.sort_values(['model name', 'fold id']))
    print('\n_______________________________________________________________________\n\n')
    
    # determine best model using the cv_results_df
    best_model_rocauc = determine_best_model(results_df=cv_results_df, metric_col='roc-auc')
    best_model_prauc = determine_best_model(results_df=cv_results_df, metric_col='pr-auc')
    
    print(f'based on roc-auc. best_model_name={best_model_rocauc}')
    print(f'based on pr-auc. best_model_name={best_model_prauc}')
    print('_______________________________________________________________________\n')
    
    # evaluate best model on test set
    roc_auc_test, pr_auc_test = evaluate_best_model(best_model_name=best_model_prauc, 
                                                     train_df=cv_df, test_df=heldout_test_df, 
                                                     discrete_columns=disc_features, 
                                                     continuous_columns=cont_features, 
                                                     label_column=label_col)
    print(f'held-out test results using {best_model_prauc}')
    print(f'roc_auc_test={roc_auc_test}')
    print(f'pr_auc_test={pr_auc_test}')
    print('_______________________________________________________________________\n')
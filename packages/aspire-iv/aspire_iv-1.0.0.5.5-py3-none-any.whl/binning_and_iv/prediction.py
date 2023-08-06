import pandas as pd
import numpy as np
from functools import reduce
from pymysql import connect
# from binning_and_iv.prediction import iv_pred

# iv_result_df=iv_pred.segmented_iv(feature_df=contactiblity_ftr, cred=cred)
class iv_pred():
    def data_fetch(cred,query:str,**kwargs)->pd.DataFrame:
        """
        Fetches data for the given query from the database.
        """
        while True:
            try:
                db_connection = connect(**cred, database='aspiredb', host='13.126.97.63')
                break
            except Exception as e:
                print(f'connection error  {e}')
        try:
            with db_connection.cursor() as cursor:
                chunks=[]

                for chunk in pd.read_sql(query, db_connection, chunksize = 10000, **kwargs):
                    chunks.append(chunk)
                if len(chunks) == 0:
                    return False,None
                else:
                    df_in = pd.concat(chunks, ignore_index=True)
                    return True, df_in
        except Exception as e:
            print(f"{type(e).__name__}\n{e}")
            False, None
        finally:
            db_connection.close()

        return False, None 
    #using Decision tree doing binning
    def binning(df_binning, df_bins, columns, max_depth_,min_samples_split_, min_samples_leaf_,max_leaf_nodes_):
        from sklearn.tree import DecisionTreeClassifier
        feature = []
        feature_bin = []
        for i in range(0,len(columns)):
            column = columns[i] 
            model = DecisionTreeClassifier(max_depth=max_depth_,min_samples_split=min_samples_split_, min_samples_leaf=min_samples_leaf_, max_leaf_nodes =max_leaf_nodes_)
            model.fit(df_binning[column].to_frame(), df_binning.target)
            #print(model.predict_proba(df_binning[columns[i]].to_frame()))
            # taking probability of bad rate as value
            df_binning[column]=model.predict_proba(df_binning[columns[i]].to_frame())[:,1]
            df_bins[column+'_bin'] = df_binning[column]
            feature.append(column)
            feature_bin.append(column+'_bin')
        return df_binning, df_bins, feature, feature_bin
    #bucket distribution
    def num_bucket(df_bins, feature, feature_bin):
        lst = []
        for i in range(len(feature)):
            sorted_data = df_bins.sort_values([feature[i]], ascending = True)
            for j in range(sorted_data[feature_bin[i]].nunique()):
                value = list(sorted_data[feature_bin[i]].unique())[j]
                data = sorted_data[(sorted_data[feature_bin[i]]==value)]
                lst.append({
                    'feature': feature_bin[i],
                    'bin_val' : value,
                    'val':(f'{data[feature[i]].min()} - {data[feature[i]].max()}'),
                    'good':data[data['target']==0].count()[feature[i]],
                    'bad':data[data['target']==1].count()[feature[i]],
                    'bad_rate' : round(((data[data['target']==1].count()[feature[i]])/(data['target'].count()))*100,2)
                })
        d = pd.DataFrame(lst)
        return d
    def cat_bucket(df, feature):
        lst = []
        for i in range(len(feature)):
            for j in range(df[feature[i]].nunique()):
                value = list(df[feature[i]].unique())[j]
                data = df[(df[feature[i]]==value)]
                lst.append({
                    'feature': feature[i],
                    'bin_val' : value,
                    'good':data[data['target']==0].count()[feature[i]],
                    'bad':data[data['target']==1].count()[feature[i]],
                    'bad_rate' : round(((data[data['target']==1].count()[feature[i]])/(data['target'].count()))*100,2)
                })
        d = pd.DataFrame(lst)
        return d
    def calculate_woe_iv(dataset, feature, target):
        lst = []
        for i in range(dataset[feature].nunique()):
            val = list(dataset[feature].unique())[i]
            lst.append({
                'Value': val,
                'All': dataset[dataset[feature] == val].count()[feature],
                'Good': dataset[(dataset[feature] == val) & (dataset[target] == 0)].count()[feature],
                'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 1)].count()[feature]
            })
        dset = pd.DataFrame(lst)
        dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()

        dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
        dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
        dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
        dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
        iv = dset['IV'].sum()
        
        dset = dset.sort_values(by='WoE')
        
        #return dset if needed
        return iv
    def calculate_woe_iv(dataset, feature, target):
        lst = []
        for i in range(dataset[feature].nunique()):
            val = list(dataset[feature].unique())[i]
            lst.append({
                'Value': val,
                'All': dataset[dataset[feature] == val].count()[feature],
                'Good': dataset[(dataset[feature] == val) & (dataset[target] == 0)].count()[feature],
                'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 1)].count()[feature]
            })
        dset = pd.DataFrame(lst)
        dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()

        dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
        dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
        dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
        dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
        iv = dset['IV'].sum()
        
        dset = dset.sort_values(by='WoE')
        
        #return dset if needed
        return iv
    # columns = numerical_var
    def DT_binning(dataframe, max_depth_=3,min_samples_split_=200, min_samples_leaf_=200,max_leaf_nodes_ = 4, num_feature= [],cat_feature=[]):
        """
        Input :
        dataframe -> Feature dataframe.
        num_feature = [] -> set to empty, select if you have numerical features :- List[features].
        cat_feature = [] -> set to empty, select if you have categorical features :- List[features].

        Output :
        dataframe with ['var_name','Information_Value']

        __return__:
                    tuple(cal_bad_num,cal_bad_cat,iv_score)

        """
        df = dataframe.copy()
        df_bins = dataframe.copy()
        df_binning = dataframe.copy()
        if num_feature != []:
            df_binning, df_bins, feature, feature_bin = iv_pred.binning(df_binning,df_bins, num_feature, max_depth_,min_samples_split_, min_samples_leaf_,max_leaf_nodes_)
            cal_bad_num = iv_pred.num_bucket(df_bins, feature, feature_bin)
            cal_bad_num = cal_bad_num.set_index(['feature','bin_val'])
        else:
            cal_bad_num = np.nan
        if cat_feature != []:
            cal_bad_cat = iv.cat_bucket(df, cat_feature)
        else:
            cal_bad_cat = np.nan
        
        var = []
        iv=[]
        for i in range (1,len(df_binning.columns)):
            k=iv_pred.calculate_woe_iv(df_binning,df_binning.iloc[:,i].name,'target')
            var.append(df_binning.iloc[:,i].name)
            iv.append(k)
        
        dx=pd.DataFrame()
        dx['var_name'] = var
        dx['Information_Value']=iv
        iv_score = dx.sort_values(['Information_Value'], ascending = False)

        return cal_bad_num,cal_bad_cat,iv_score
    def target_extracter(feature_df:pd.DataFrame,cred:dict)->pd.DataFrame:
        user_id = feature_df['user_id'].unique()
        user_tuple = "('" + "','".join(np.array(user_id)) + "')"

        Query = f"""SELECT user_id,Bureau_credit_score,transacted_user_fl,thick_thin_ntc,target 
                    FROM asp_playground.DS_final_traget_variable
                    WHERE user_id in {user_tuple}"""
        Query2 = f"""SELECT user_id,transacted_user_fl,credit_score,target
                    FROM ds_master.Target_var_nov_feb
                    WHERE user_id in {user_tuple};"""
        flag, db_data = iv_pred.data_fetch(cred,query=Query)
        if (db_data.shape[0]==0):
            flag, db_data = iv_pred.data_fetch(cred,query=Query2)
            if (db_data.shape[0]!=0):
                db_data['thick_thin_ntc']=np.where((db_data['credit_score']==0), "NTC",
                                                np.where((db_data['credit_score']>=0)&(db_data['credit_score']<=20)), 
                                               "Thin", "Thick")
            if (db_data.shape[0]==0):
                print("Error in Extracting Target data for the given user_id")

        ftr_df=feature_df.merge(db_data, on="user_id",how='left')

        return ftr_df
    def segment_extractor(df_feature:pd.DataFrame, num_features=[], cat_features=[])->pd.DataFrame:
        import warnings
        warnings.filterwarnings('ignore')
        ftr_df=df_feature.copy()

        df_iv=[]
        for segment in ['Thick',"Thin","NTC"]:
            ftr_df.fillna(value=0, inplace =True)
            ftr_df.replace([np.inf, -np.inf], 0, inplace = True)
            ftr_df_ext=ftr_df.loc[ftr_df['thick_thin_ntc']==f"{segment}"]
            dataframe=ftr_df_ext.drop(columns=['transacted_user_fl','Bureau_credit_score','thick_thin_ntc']).copy()
            # num=dataframe.drop(columns=['user_id']).columns.to_list()
            
            cal_bad_num,cal_bad_cat,iv_score=iv_pred.DT_binning(dataframe=dataframe, num_feature=num_features,cat_feature=cat_features)
            if not isinstance(cal_bad_cat, pd.DataFrame):
                cal_bad_cat=pd.DataFrame()
                cal_bad_cat['var_name']=dataframe.columns.to_list()
            cal_bad_num.reset_index(inplace=True)
            cal_bad_num["var_name"]=cal_bad_num["feature"].apply(lambda x:x.replace("_bin",""))
            df=reduce(lambda left,right: pd.merge(left,right,on=['var_name'],
                                                how='outer'),[iv_score,cal_bad_cat,cal_bad_num])
            df.drop(columns=['var_name'], inplace=True)
            df['segment']=f"{segment}"
            df_iv.append(df)

        df_result=pd.concat(df_iv, ignore_index=True)
        
        return df_result
    def segmented_iv(feature_df:pd.DataFrame,cred:dict,num_features, cat_features)->pd.DataFrame:
        feature_df=iv_pred.target_extracter(feature_df,cred)
        tr_df_chunk=[]
        for i in [1,0]:
            tr_df=feature_df.loc[feature_df['transacted_user_fl']==i]
            iv_final=iv_pred.segment_extractor(tr_df,num_features, cat_features)
            iv_final['transacting']=i   
            tr_df_chunk.append(iv_final)
        
        df_result=pd.concat(tr_df_chunk, ignore_index=True)
        df_result.set_index(['feature','Information_Value','bin_val'], inplace=True)
        df_result.dropna(inplace=True)
        return df_result
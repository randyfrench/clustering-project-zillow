import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import os
import env


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans

sql_query = """
       SELECT prop.*,
       pred.logerror,
       pred.transactiondate,
       air.airconditioningdesc,
       arch.architecturalstyledesc,
       build.buildingclassdesc,
       heat.heatingorsystemdesc,
       landuse.propertylandusedesc,
       story.storydesc,
       construct.typeconstructiondesc
       FROM   properties_2017 prop
       INNER JOIN (SELECT parcelid,
                   Max(transactiondate) transactiondate
        FROM   predictions_2017
        GROUP  BY parcelid) pred
        USING (parcelid)
       JOIN predictions_2017 as pred USING (parcelid, transactiondate)
       LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
       LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
       LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
       LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid)
       LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid)
       LEFT JOIN storytype story USING (storytypeid)
       LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid)
       WHERE  prop.latitude IS NOT NULL
       AND prop.longitude IS NOT NULL
"""

def get_db_url(db):
    from env import host, user, password
    url = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    return url


# acquire zillow data using the query
def get_zillow():
    url = get_db_url('zillow')
    zillow_df = pd.read_sql(sql_query, url, index_col='id')
    
    return zillow_df


def handle_missing_values(df, prop_required_column = .5, prop_required_row = .70):
    # function that will drop rows or columns based on the percent of values that are missing:\
    # handle_missing_values(df, prop_required_column, prop_required_row
    threshold = int(round(prop_required_column*len(df.index),0))
    df = df.dropna(axis=1, thresh=threshold)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    
    return df


def remove_columns(df, cols_to_remove):
    # remove columns not needed
    df = df.drop(columns=cols_to_remove)
    
    return df

def train_validate_test_split(df):
    train_and_validate, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train_and_validate, train_size=0.75, random_state=123)
    
    # Have function print datasets shape
    print(f'train -> {train.shape}')
    print(f'validate -> {validate.shape}')
    print(f'test -> {test.shape}')
    
    return train, validate, test

# Zillow Split to X & Y

def zillow_split(df, target):
    '''
    This function take in get_zillow  from aquire.py and performs a train, validate, test split
    Returns train, validate, test, X_train, y_train, X_validate, y_validate, X_test, y_test as partitions
    and prints out the shape of train, validate, test
    '''
    # create train and validate and test datasets
    train_and_validate, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train_and_validate, train_size=0.75, random_state=123)

    # Split into X and y
    X_train = train.drop(columns=[target])
    y_train = train[target]

    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]

    X_test = test.drop(columns=[target])
    y_test = test[target]
   
    return X_train, X_validate, X_test, y_train, y_validate, y_test

def wrangle_zillow():
    if os.path.isfile('zillow_cached.csv') == False:
        df = get_zillow()
        df.to_csv('zillow_cached.csv',index = False)
    else:
        df = pd.read_csv('zillow_cached.csv')

    # Restrict df to only properties that meet single use criteria
    single_use = [261, 262, 263, 264, 266, 268, 273, 276, 279]
    df = df[df.propertylandusetypeid.isin(single_use)]

    # Restrict df to only those properties with at least 1 bath & bed and 350 sqft area
    df = df[(df.bedroomcnt > 0) & (df.bathroomcnt > 0) & ((df.unitcnt<=1)|df.unitcnt.isnull())\
            & (df.calculatedfinishedsquarefeet>350)]

    # Handle missing values i.e. drop columns and rows based on a threshold
    df = handle_missing_values(df)

    # Add column for counties
    df['county'] = df['fips'].apply(
        lambda x: 'Los Angeles' if x == 6037\
        else 'Orange' if x == 6059\
        else 'Ventura')

    # drop unnecessary columns
    dropcols = ['parcelid',
         'calculatedbathnbr',
         'finishedsquarefeet12',
         'fullbathcnt',
         'heatingorsystemtypeid',
         'propertycountylandusecode',
         'propertylandusetypeid',
         'propertyzoningdesc',
         'censustractandblock',
         'propertylandusedesc']

    df = remove_columns(df, dropcols)

    # replace nulls in unitcnt with 1
    df.unitcnt.fillna(1, inplace = True)

    # assume that since this is Southern CA, null means 'None' for heating system
    df.heatingorsystemdesc.fillna('None', inplace = True)

    # replace nulls with median values for select columns
    df.lotsizesquarefeet.fillna(7313, inplace = True)
    df.buildingqualitytypeid.fillna(6.0, inplace = True)

    # Columns to look for outliers
    df = df[df.taxvaluedollarcnt < 5_000_000]
    df = df[df.calculatedfinishedsquarefeet < 8000]

    # Just to be sure we caught all nulls, drop them here
    df = df.dropna()

    return df


# MIN MAX SCALER 


def min_max_scaler(X_train, X_validate, X_test, numeric_cols):
    """
    this function takes in 3 dataframes with the same columns,
    a list of numeric column names (because the scaler can only work with numeric columns),
    and fits a min-max scaler to the first dataframe and transforms all
    3 dataframes using that scaler.
    it returns 3 dataframes with the same column names and scaled values.
    """
    # create the scaler object and fit it to X_train (i.e. identify min and max)
    # if copy = false, inplace row normalization happens and avoids a copy (if the input is already a numpy array).
    scaler = MinMaxScaler(copy=True).fit(X_train[numeric_cols])
    # scale X_train, X_validate, X_test using the mins and maxes stored in the scaler derived from X_train.
    X_train_scaled_array = scaler.transform(X_train[numeric_cols])
    X_validate_scaled_array = scaler.transform(X_validate[numeric_cols])
    X_test_scaled_array = scaler.transform(X_test[numeric_cols])
    # convert arrays to dataframes
    X_train_scaled = pd.DataFrame(X_train_scaled_array, columns=numeric_cols).set_index(
        [X_train.index.values]
    )
    X_validate_scaled = pd.DataFrame(
        X_validate_scaled_array, columns=numeric_cols
    ).set_index([X_validate.index.values])
    X_test_scaled = pd.DataFrame(X_test_scaled_array, columns=numeric_cols).set_index(
        [X_test.index.values]
    )
    # Overwriting columns in our input dataframes for simplicity
    for i in numeric_cols:
        X_train[i] = X_train_scaled[i]
        X_validate[i] = X_validate_scaled[i]
        X_test[i] = X_test_scaled[i]
        
    return X_train, X_validate, X_test

# CREATE CLUSTERS

def create_cluster(df, X, k, col_name = None):
    
    ''' 
    This function takes in df, X (dataframe with variables you want to cluster on) and k
    It scales the X, calcuates the clusters and return train (with clusters), the Scaled dataframe,
    the scaler and kmeans object and scaled centroids as a dataframe
    '''
    scaler = StandardScaler(copy=True).fit(X)
    X_scaled = pd.DataFrame(scaler.transform(X), columns=X.columns.values).set_index([X.index.values])
    kmeans = KMeans(n_clusters = k, random_state = 123)
    kmeans.fit(X_scaled)
    centroids_scaled = pd.DataFrame(kmeans.cluster_centers_, columns = list(X))
    
    if col_name == None:
        #clusters on dataframe 
        df[f'clusters_{k}'] = kmeans.predict(X_scaled)
    else:
        df[col_name] = kmeans.predict(X_scaled)
    
    
    return df, X_scaled, scaler, kmeans, centroids_scaled

# GROUP SCATTERPLOT

def scatter_plots(X_scaled, col_name= 'column_one', col_name_two= 'column_two'):
    '''
    This function takes in two columns and 
    creates a range of scatter plots based on varying k values
    '''
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)
    for ax, k in zip(axs.ravel(), range(2, 6)):
        clusters = KMeans(k).fit(X_scaled).predict(X_scaled)
        ax.scatter(X_scaled[col_name], X_scaled[col_name_two], c=clusters)
        ax.set(title='k = {}'.format(k), xlabel=col_name, ylabel=col_name_two)

def outlier_function(df, cols, k):
    # function to detect and handle oulier using IQR rule
    for col in df[cols]:
        q1 = df.annual_income.quantile(0.25)
        q3 = df.annual_income.quantile(0.75)
        iqr = q3 - q1
        upper_bound =  q3 + k * iqr
        lower_bound =  q1 - k * iqr
        df = df[(df[col] < upper_bound) & (df[col] > lower_bound)]
        
    return df

def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    prcnt_miss = num_missing / rows * 100
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'percent_rows_missing': prcnt_miss})
    
    return cols_missing

def nulls_by_row(df):
    num_missing = df.isnull().sum(axis=1)
    prcnt_miss = num_missing / df.shape[1] * 100
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': prcnt_miss})\
    .reset_index()\
    .groupby(['num_cols_missing', 'percent_cols_missing']).count()\
    .rename(index=str, columns={'customer_id': 'num_rows'}).reset_index()
    
    return rows_missing

def summarize(df):
    '''
    summarize will take in a single argument (a pandas dataframe)
    and output to console various statistics on said dataframe, including:
    # .head()
    # .info()
    # .describe()
    # value_counts()
    # observation of nulls in the dataframe
    '''
    print(f'There are total of {df.isna().sum().sum()} missing values in the entire dataframe.')
    print('')
    print('-------------------')
    print('=====================================================\n\n')
    print('Dataframe head: ')
    print(df.head(3).to_markdown())
    print('=====================================================\n\n')
    print('Dataframe info: ')
    print(df.info())
    print('=====================================================\n\n')
    print('Dataframe Description: ')
    print(df.describe().to_markdown())
    num_cols = [col for col in df.columns if df[col].dtype != 'O']
    cat_cols = [col for col in df.columns if col not in num_cols]
    print('=====================================================')
    print('DataFrame value counts: ')
    for col in df.columns:
        if col in cat_cols:
            print(df[col].value_counts())
        else:
            print(df[col].value_counts(bins=10, sort=False))
    print('=====================================================')
    print('nulls in dataframe by column: ')
    print(nulls_by_col(df))
    print('=====================================================')
    print('nulls in dataframe by row: ')
    print(nulls_by_row(df))
    print('============================================')
    
 
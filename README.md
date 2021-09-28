# Finding Drivers of Zestimate Errors

### Table of Contents
---

I.   [Project Overview             ](#i-project-overview)
1.   [Description                  ](#1-description)
2.   [Deliverables                 ](#2-deliverables)

II.  [Executive Summary  ](#ii-executive-summary)
1.   [Goals:                        ](#1-goals)
2.   [Key Findings:                 ](#2-key-findings)
3.   [Recommendations:              ](#1-recommendations)

III. [Project                      ](#iii-project)
1.   [Questions & Hypothesis       ](#1-questions--hypothesis)
2.   [Findings                     ](#2-findings)

IV. [Data Context                 ](#iv-data-context)
1.   [Data Dictionary              ](#1-data-dictionary)

V.  [Process                      ](#v-process)
1.   [Project Planning             ](#1-project-planning)
2.   [Data Acquisition             ](#2-data-acquisition)
3.   [Data Preparation             ](#3-data-preparation)
4.   [Data Exploration             ](#4-data-exploration)
5.   [Modeling & Evaluation        ](#5-modeling--evaluation)
6.   [Product Delivery             ](#6-product-delivery)

VI.   [Modules                      ](#vi-modules)

VII.  [Project Reproduction         ](#vii-project-reproduction)

<br>

<br>

### I. Project Overview
---

#### 1. Description

The primary focus of the project was to incorporate clustering methodologies and discover potential drivers of the log_error of the Zillow® Zestimate focusing on single unit / single-family homes, using the 2017 properties and predictions data. In this context, log_error is equal to 𝑙𝑜𝑔(𝑍𝑒𝑠𝑡𝑖𝑚𝑎𝑡𝑒) − 𝑙𝑜𝑔(𝑆𝑎𝑙𝑒𝑃𝑟𝑖𝑐𝑒). I will present my findings and drivers of the log error through a notebook walkthough to my datascience team.

- What is driving the errors in the Zestimates?
- This notebook will be a continuation of my regression modeling. I am adding clustering methodologies to see what kind of improvements we can make.

#### 2. Deliverables

- Final Report Notebook detailing all of my findings and methodologies.
- Sections indicated with markdown headings in my final notebook with a good title and the documentation is sufficiently explanatory and of high quality
- A Python module or modules that automate the data acquisistion and preparation process, imported and used in final notebook
- README file that details the project specs, planning, key findings, and steps to reproduce



### II. Executive Summary
---

#### 1. Goals:

- Incorporate clustering methodologies and discover potential drivers of the log_error of the Zillow® Zestimate for single-unit properties sold during 2017. In this context, log_error is equal to 𝑙𝑜𝑔(𝑍𝑒𝑠𝑡𝑖𝑚𝑎𝑡𝑒) − 𝑙𝑜𝑔(𝑆𝑎𝑙𝑒𝑃𝑟𝑖𝑐𝑒). 
- Create modules storing functions of each step of the data pipeline
- Thoroughly document each step
- Construct at least 4 models
- Make sure project is reproduceable

#### 2. Key findings:
- The tests rejected all four Null Hypothesis
- There is a relationship between these features and logerror
- The 2nd Degree Ploynomial regression model performed the best

#### 3. Recommendations:
- I would like to continue to look into other features to use for clusters (such as age vs sqft)
- I would like to perform more testing to find better models to use to determine logerror

---

### III. Project

#### 1. Questions & Hypothesis

- Is there a correlation between logerror and bathroom count
- Is there a correlation between logerror and lot size square feet
- Is there a correlation between logerror and calculated finished square feet
- Is there a relationship between logerror and bedroom count


## Hypothesis 1: Correlation Test (Logerror vs Bathroomcnt)
- $H_o$: There is no correlation between logerror and taxamount
- $H_a$: There ia a correlation between logerror and taxamount

## Hypothesis 2: Correlation Test (Logerror vs Lot size squarefeet)
- $H_o$: There is no correlation between logerror and lotsizesquarefeet
- $H_a$: There is a correlation between logerror and lotsizesquarefeet

## Hypothesis 3: Correlation Test ( Logerror vs Calculated finished square feet)
- $H_o$: There is no correlation between logerror and calculatedfinishedsquarefeet
- $H_a$: There is a correlation between logerror and calculatedfinishedsquarefeet

## Hypothesis 4: T-Test (Logerror vs Bedroomcnt)
- $H_o$: There is no relationship between logerror and bedroomcnt
- $H_a$: There is a relationship between logerror and bedroomcnt



### 2. Findings
#### My findings are:
- The tests rejected all four Null Hypothesis
- There is a relationship between these features and logerror
- The 2nd Degree Ploynomial regression model performed the best

| Model                            | rmse_train  | rmse_validate |
|----------------------------------|:-----------:|---------------|
|mean_baseline                     | 0.16828     | 0.15740       |
|1. OLS                            | 0.16813     | 0.15738       |
|2. LassoLars (alpha 2)            | 0.16828     | 0.15740       |
|3. Polynomial Regression(degree=2)| 0.16806     | 0.15743       |
|4. OLS (Unscaled Data)            | 0.16813     | 0.15738       |

- RMSE for Polynomial Model, degrees=2
  - Training/In-Sample:  0.16812589644110204 
  - Validation/Out-of-Sample:  0.16581584996771273


### IV. Data Context
---

#### 1. Data Dictionary

Following acquisition and preparation of the initial SQL database, the DataFrames used in this project contain the following variables. Contained values are defined along with their respective data types.

| Variable                     | Definition                                         | Data Type  |
|:----------------------------:|:--------------------------------------------------:|:----------:|     
| bathroomcnt                  | count of bathrooms                                 | float64    |
| bedroomcnt                   | count of bedrooms                                  | float64    |
| buildingqualitytypeid        | the building struture quality                      | float64    |
| calculatedfinishedsquarefeet | finished structure_square_feet                     | float64    |
| fips.                        | Federal Information Processing Standards,          |            |
|                              | unique county code                                 | float64    |
| latitude                     | Property latitudinal location                      | float64    |
| longitude                    | Property longitudinal locatio                      | float64    |
| lotsizesquarefeet            | size of the lot in square feet                     | float64    |
| rawcensustractandblock       | statistical subdivisions of a county               | float64    |
| regionidcity                 | metropolitan area id for a city                    | float64    |
| log_error *                  | difference of log(Zestimate) and log(SalePrice)    | float64    |
| regionidcounty               | metropolitan area id for a county                  | float64    |
| regionidzip                  | metropolitan area id for a zipcode                 | float64    |
| roomcnt                      | total number of rooms                              | float64    |
| unitcnt                      | how many single family units                       | float64    |
| yearbuilt                    | year the property was built.                       | float64    |
| structuretaxvaluedollarcnt   | vaule of the structure by taxing district          | float64    |
| taxvaluedollarcnt            | value of property in entirety in U.S. dollars      | float64    |
| assessmentyear               | year the tax was assessed                          | float64    |
| landtaxvaluedollarcnt        | value of the land                                  | float64    |
| taxamount                    | most recent tax payment from property owner        | float64    |
| transactiondate              | most recent date of property sale                  | object     |
| heatingorsystemdesc          | type of heating system used                        | object     |
| county                       | the county the property is in                      | object     |    

* Target variable

### V. Process
---
- See my Trello board [Clustering with Zillow](https://trello.com/b/4xTXow9H/clustering-with-zillow)

#### 1. Project Planning
✓ 🟢 **Plan** ➜ ☐ _Acquire_ ➜ ☐ _Prepare_ ➜ ☐ _Explore_ ➜ ☐ _Model_ ➜ ☐ _Deliver_

- [x] Build this README containing:
    - Project overview
    - Initial thoughts and hypotheses
    - Project summary
    - Instructions to reproduce
- [x] Plan stages of project and consider needs versus desires

#### 2. Data Acquisition
✓ _Plan_ ➜ 🟢 **Acquire** ➜ ☐ _Prepare_ ➜ ☐ _Explore_ ➜ ☐ _Model_ ➜ ☐ _Deliver_

- [x] Obtain initial data and understand its structure
    - Obtain data from Codeup database with appropriate SQL query
- [x] Remedy any inconsistencies, duplicates, or structural problems within data
- [x] Perform data summation

#### 3. Data Preparation
✓ _Plan_ ➜ ✓ _Acquire_ ➜ 🟢 **Prepare** ➜ ☐ _Explore_ ➜ ☐ _Model_ ➜ ☐ _Deliver_

- [x] Address missing or inappropriate values, including outliers
- [x] Plot distributions of variables
- [x] Consider and create new features as needed
- [x] Split data into `train`, `validate`, and `test`

#### 4. Data Exploration
✓ _Plan_ ➜ ✓ _Acquire_ ➜ ✓ _Prepare_ ➜ 🟢 **Explore** ➜ ☐ _Model_ ➜ ☐ _Deliver_

- [x] Visualize relationships of variables
- [x] Formulate hypotheses
- [x] Use clustering methodology in exploration of data
    - Perform statistical testing and visualization
    - Use at least 3 combinations of features
    - Document takeaways of each clustering venture
    - Create new features with clusters if applicable
- [x] Perform statistical tests
- [x] Decide upon features and models to be used

#### 5. Modeling & Evaluation
✓ _Plan_ ➜ ✓ _Acquire_ ➜ ✓ _Prepare_ ➜ ✓ _Explore_ ➜ 🟢 **Model** ➜ ☐ _Deliver_

- [x] Establish baseline prediction
- [x] Create, fit, and predict with models
    - Create at least four different models
    - Use different configurations of algorithms, hyper parameters, and/or features
- [x] Evaluate models with out-of-sample data
- [x] Utilize best performing model on `test` data
- [x] Summarize, visualize, and interpret findings

#### 6. Product Delivery
✓ _Plan_ ➜ ✓ _Acquire_ ➜ ✓ _Prepare_ ➜ ✓ _Explore_ ➜ ✓ _Model_ ➜ 🟢 **Deliver**
- [x] Prepare Jupyter Notebook of project details through data science pipeline
    - Python code clearly commented when necessary
    - Sufficiently utilize markdown
    - Appropriately title notebook and sections
- [x] With additional time, continue with exploration beyond MVP
- [x] Proof read and complete README and project repository

### VI. Modules
---

The created modules used in this project below contain full comments an docstrings to better understand their operation. Where applicable, all functions used `random_state=123` at all times. Use of functions requires access credentials to the Codeup database and an additional module named `env.py`. See project reproduction for more detail.

- [`acquire`](https://raw.githubusercontent.com/randyfrench/clustering-project-zillow/main/acquire.py): contains functions used in initial data acquisition leading into the prepare phase
- [`wrangle_zillow`](https://raw.githubusercontent.com/randyfrench/clustering-project-zillow/main/wrangle_zillow.py): contains functions to prepare data in the manner needed for this specific project needs

### VII. Project Reproduction
---

To recreate and reproduce results of this project, you will need to create a module named `env.py`. This file will need to contain login credentials for the Codeup database server stored in their respective variables named `host`, `username`, and `password`. You will also need to create the following function within. This is used in all functions that acquire data from the SQL server to create the URL for connecting. `db` needs to be passed as a string that matches exactly with the name of a database on the server.

```py
def get_connection(db_name):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'
```

After its creation, ensure this file is not uploaded or leaked by ensuring git does not interact with it by using gitignore. When using any function housed in the created modules above, ensure full reading of comments and docstrings to understand its proper use and passed arguments or parameters.

[[Return to Top]](#finding-drivers-of-zestimate-errors)


# Finding Drivers of Zestimate Errors

### Table of Contents
---

I.   [Project Overview             ](#i-project-overview)
1.   [Description                  ](#1-description)
2.   [Deliverables                 ](#2-deliverables)

II.  [Project Summary              ](#ii-project-summary)
1.   [Goals                        ](#1-goals)
2.   [Questions & Hypothesis       ](#2-questions--hypothesis)
3.   [Findings                     ](#3-findings)

III. [Data Context                 ](#iii-data-context)
1.   [Data Dictionary              ](#1-data-dictionary)

IV.  [Process                      ](#iv-process)
1.   [Project Planning             ](#1-project-planning)
2.   [Data Acquisition             ](#2-data-acquisition)
3.   [Data Preparation             ](#3-data-preparation)
4.   [Data Exploration             ](#4-data-exploration)
5.   [Modeling & Evaluation        ](#5-modeling--evaluation)
6.   [Product Delivery             ](#6-product-delivery)

V.   [Modules                      ](#v-modules)

VI.  [Project Reproduction         ](#vi-project-reproduction)

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



### II. Project Summary
---

#### 1. Goals

- The primary focus of the project was to incorporate clustering methodologies and discover potential drivers of the log_error of the Zillow® Zestimate for single-unit properties sold during 2017. In this context, log_error is equal to 𝑙𝑜𝑔(𝑍𝑒𝑠𝑡𝑖𝑚𝑎𝑡𝑒) − 𝑙𝑜𝑔(𝑆𝑎𝑙𝑒𝑃𝑟𝑖𝑐𝑒). 
- Create modules storing functions of each step of the data pipeline
- Thoroughly document each step
- Construct at least 4 models
- Make sure project is reproduceable

#### 2. Questions & Hypothesis

- Is there a correlation between logerror and bathroom count
- Is there a correlation between logerror and lot size square feet
- Is there a correlation between logerror and calculated finished square feet
- Is there a relationship between logerror and bedroom count


## Hypothesis 1: Correlation Test (Logerror vs Bathroomcnt)
- $H_0$: There is no correlation between logerror and taxamount
- $H_a$: There ia a correlation between logerror and taxamount

## Hypothesis 2: Correlation Test (Logerror vs Lot size squarefeet)
- $H_0$: There is no correlation between logerror and lotsizesquarefeet
- $H_a$: There is a correlation between logerror and lotsizesquarefeet

## Hypothesis 3: Correlation Test ( Logerror vs Calculated finished square feet)
- $H_0$: There is no correlation between logerror and calculatedfinishedsquarefeet
- $H_a$: There is a correlation between logerror and calculatedfinishedsquarefeet

## Hypothesis 4: T-Test (Logerror vs Bedroomcnt)
- $H_0$: There is no relationship between logerror and bedroomcnt
- $H_a$: There is a relationship between logerror and bedroomcnt



### 3. Findings
#### My findings are:
- The tests rejected all four Null Hypothesis
- There is a relationship between these features and logerror
- The 2nd Degree Ploynomial regression model performed the best

model	rmse_train	rmse_validate
0	mean_baseline	0.16828	0.15740
1	Model 1: OLS	0.16813	0.15738
2	Model 2: LassoLars (alpha 2)	0.16828	0.15740
3	Model 3: Polynomial Regression (degree=2)	0.16806	0.15743
4	Model 4: OLS (Unscaled Data)	0.16813	0.15738


### III. Data Context
---

#### 1. Data Dictionary

Following acquisition and preparation of the initial SQL database, the DataFrames used in this project contain the following variables. Contained values are defined along with their respective data types.

| Variable               | Definition                                         | Data Type  |
|:----------------------:|:--------------------------------------------------:|:----------:|     |
| bathrooms              | count of full- and half-bathrooms                  | float64    |
| bed_sqft_age_clstr_#   | boolean for five clusters of bed_sqft_age          | uint8      |
| bedrooms               | count of bedrooms                                  | int64      |
| bedrooms_per_sqft      | ratio of bedrooms to structure_square_feet         | float64    |
| census_tractcode       | US census tract codes for non-precise location     | float64    |
| full_bathrooms         | count of only full-bathrooms                       | int64      |
| la_county              | boolean for if county is within Los Angeles County | int64      |
| land_value_usd         | value of land in U.S. dollars                      | float64    |
| lat_long_clstr_#       | boolean for five clusters of lat_long              | uint8      |
| latitude               | latitudinal geographic coordinate of property      | float64    |
| log_error *            | difference of log(Zestimate) and log(SalePrice)    | float64    |
| longitude              | longitudinal geographic coordinate of property     | float64    |
| lot_rooms_clstr_#      | boolean for five clusters of lot_rooms             | uint8      |
| lot_square_feet        | size of lot(land) in square feet                   | float64    |
| orange_county          | boolean for if county is within Orange County      | int64      |
| parcel_id              | unique identifier of property                      | int64      |
| property_id            | unique identifier of property                      | int64      |
| property_value_usd     | value of property in entirety in U.S. dollars      | float64    |
| room_count             | count of bedrooms and full- and half-bathrooms     | float64    |
| structure_square_feet  | dimensions of structure on property in square feet | float64    |
| structure_value_usd    | value of structure on property in U.S. dollars     | float64    |
| tax_amount_usd         | most recent tax payment from property owner        | float64    |
| tract_size_age_clstr_# | boolean for five clusters of tract_size_age        | uint8      |
| transaction_date       | most recent date of property sale                  | datetime64 |
| year_built             | year structure was originally built                | int64      |

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  * Target variable

### IV. Process
---
- See my Trello board [Clustering with Zillow](https://trello.com/b/4xTXow9H/clustering-with-zillow)

#### 1. Project Planning
🟢 **Plan** ➜ ☐ _Acquire_ ➜ ☐ _Prepare_ ➜ ☐ _Explore_ ➜ ☐ _Model_ ➜ ☐ _Deliver_

- [] Build this README containing:
    - Project overview
    - Initial thoughts and hypotheses
    - Project summary
    - Instructions to reproduce
- [] Plan stages of project and consider needs versus desires

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
- [] Prepare Jupyter Notebook of project details through data science pipeline
    - Python code clearly commented when necessary
    - Sufficiently utilize markdown
    - Appropriately title notebook and sections
- [] With additional time, continue with exploration beyond MVP
- [] Proof read and complete README and project repository

### V. Modules
---

The created modules used in this project below contain full comments an docstrings to better understand their operation. Where applicable, all functions used `random_state=` at all times. Use of functions requires access credentials to the Codeup database and an additional module named `env.py`. See project reproduction for more detail.

- [`acquire`](): contains functions used in initial data acquisition leading into the prepare phase
- [`prepare`](): contains functions used to prepare data for exploration and visualization
- [`explore`](): contains functions to visualize the prepared data and estimate the best drivers of property value
- [`wrangle`](): contains functions to prepare data in the manner needed for specific project needs
- [`model`  ](): contains functions to create, test models and visualize their performance

### VI. Project Reproduction
---

To recreate and reproduce results of this project, you will need to create a module named `env.py`. This file will need to contain login credentials for the Codeup database server stored in their respective variables named `host`, `username`, and `password`. You will also need to create the following function within. This is used in all functions that acquire data from the SQL server to create the URL for connecting. `db` needs to be passed as a string that matches exactly with the name of a database on the server.

```py
def get_connection(db_name):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'
```

After its creation, ensure this file is not uploaded or leaked by ensuring git does not interact with it by using gitignore. When using any function housed in the created modules above, ensure full reading of comments and docstrings to understand its proper use and passed arguments or parameters.

[[Return to Top]](#finding-drivers-of-zestimate-errors)


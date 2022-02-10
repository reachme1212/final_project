# University of Arizona Data analytics Boot-camp - Final_project
## Capstone Analysis

# Analyzing concentration of occupation based on location in USA

**Overview of the analysis: **

In this final project our team has decided to analyze occupation based on demographic information, we are trying to understand if there is a trend or correlation in a certain type of occupation vs location (for example: which city or state offers more technical jobs). Question we hope to answer “is there a relationship between demography and Job type”. 

Reason we choose this topic is our curiosity to find which city or state has most tech/data jobs, now most tech jobs can be performed remotely, applying in multiple states which offers more jobs increases our probability of getting the job we desire faster.
Overall outline of this analysis is getting employment and demographic data, Merge and clean the data, upload the final clean data to database and create a machine model and dashboard to add some interactive elements.


**Developers**
- Ken Paulson
- Khanh Ngo
- Sangeetha Venu Gopalan

**Git-hub and general communication:**

Team members are assigned specific roles every week in this project, we all work together on each part of the project. we meet via zoom twice a week on Tuesdays and Thursdays (6 or 6.30pm) to discuss ideas and responsibilities. We use slack every day to communicate ideas and changes made to repository.In our team to avoid git issues we work on our separate branch after we merge to main we delete the branch from the repository.

**Understanding the dataset:** 

After we cleaned and merged the two data frames (employment and demographic information), we spent some time to explore the data and to decide what we can predict from this dataset.

![data_frame](images/final_data.PNG)

**Data Source:**

We have downloaded employment data from bls.gov, we used the demographic data from a private database link given below.

https://www.bls.gov/oes/tables.htm

https://www.cubitplanning.com

**Machine Learning:** 

We have tried linear regression and quantifying linear regression , both did not perform well for our data set , so we have built a random regressor model.

![Regressor](images/ml_r2.PNG)

**Database:** 

We have set up the database that will connect to AWS with our sample data. We have created tables in postgres to load different dataframes we will join using SQL and create a new combined data that can be used to train and test the machine model.

**Dashboard** 

We are building a google slides, to create an initial dashboard , we have to decide whether we are going to use tableau or other dashboard options for our final dashboard.

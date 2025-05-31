# Multi-Class-Prediction-of-Obesity-Risk

#### This project is an extension of improving the models, productionizing the project with best practices previously developed for Kaggle Competition "Multi Class Prediction of Obesity Risk"where we placed within the top 5%. The project aims at redoing the project with added production using best practices learned from class MGSC-695-076. For the sake of security, no access keys were shared. 

Tech Stack: Apache Kafka, MLflow, Azure ML, VS Code, Poetry, AutoGluon, H2O, PyCaret, FLAML, PandasAI, Docker, Streamlit, Postman, FastAPI, SHAP

## Project Overview

#### 1. Data Preparation and Simulation

- **Data Source:** Original Kaggle CSV data split into Model Development and Hold-Off datasets.
- **Live Data Simulation:** Used Apache Kafka for simulating real-time data feeds.



<!-- Slide 6 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide6.png">
</p>

<!-- Slide 7 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide7.png">
</p>

<!-- Slide 8 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide8.png">
</p>

#### 2. Azure Machine Learning Setup

- **Workspace Configuration:** Established Azure ML Workspace with RBAC.
- **Team Roles:** Assigned roles for Data Science, Data Engineering, ML Engineering, and Governance.

#### 3. Exploratory Data Analysis (EDA)

- **Comprehensive Analysis:**
  - **Univariate Analysis:** Leveraged PandasAI for detailed insights.
  - **Bivariate Analysis:** Used pairplots and interaction plots.
  - **Dimensionality Reduction:** Applied PCA with KMediansClustering.

<!-- Slide 9 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide9.png">
</p>

<!-- Slide 10 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide10.png">
</p>

<!-- Slide 11 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide11.png">
</p>

<!-- Slide 12 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide12.png">
</p>


<!-- Slide 13 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide13.png">
</p>

#### 4. Data Preprocessing

- **Feature Engineering:** Enhanced performance based on EDA insights.
- **Normalization and Scaling:** Ensured optimal feature scaling.
- **Missing Data Handling:** Applied appropriate strategies for missing data.

#### Step 9: EDA [Owner to Update Step]
<!-- Slide 14 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide14.png">
</p>



#### 5. Dependency Management

- **Poetry Integration:** Managed dependencies for reproducibility.


<!-- Slide 15 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide15.png">
</p>



#### 6. Model Development and Optimization

- **State-of-the-Art Models:**
  - Custom models like XGBoost, LightGBM, CatBoost.
  - **Hyperparameter Tuning:** Used Optuna for optimization.

- **AutoML Exploration:**
  - Explored Pycaret, AutoGluon, H2O for benchmarking.
  - **Advanced Techniques:** Stacked models, Isolation Forest, custom loss functions.

#### 7. Experiment Tracking and Management

- **MLflow & Azure MLFlow Integration:**
  - Tracked global and local metrics, target distribution.
  - **SHAP Analysis:** Utilized SHAP values for explainability and error analysis.


<!-- Slide 16 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide16.png">
</p>



<!-- Slide 17 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide17.png">
</p>



<!-- Slide 18 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide18.png">
</p>



<!-- Slide 19 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide19.png">
</p>



<!-- Slide 20 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide20.png">
</p>



<!-- Slide 21 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide21.png">
</p>


#### 8. Deployment Strategies

- **Containerization:** Used FastAPI and Docker.
- **Azure Deployment:** Azure Container Instances, planned Kubernetes.

- **Conversion to Azure Scripts:**
  - Converted Jupyter notebooks to Python scripts for Azure jobs.
  - **Azure Pipelines:** CI/CD with GitHub Actions and Azure Container Registry.

#### 9. User Interface and Interaction

- **Streamlit Application:** User-friendly interface integrated with APIs.

#### 10. Model Monitoring and Drift Management

- **Monitoring Strategy:** Drift detection, automated endpoint management.

#### 11. Azure ML Designer Integration

- **UI-Based Experiments:** Used Azure ML Designer for experiments additionally for learning purposes using SDK v2, and UI.


<!-- Slide 22 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide22.png">
</p>



<!-- Slide 23 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide23.png">
</p>



<!-- Slide 24 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide24.png">
</p>



<!-- Slide 25 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide25.png">
</p>



<!-- Slide 26 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide26.png">
</p>



<!-- Slide 27 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide27.png">
</p>



<!-- Slide 28 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide28.png">
</p>



<!-- Slide 29 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide29.png">
</p>



<!-- Slide 30 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide30.png">
</p>



<!-- Slide 31 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide31.png">
</p>



<!-- Slide 32 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide32.png">
</p>



<!-- Slide 33 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide33.png">
</p>



<!-- Slide 34 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide34.png">
</p>



<!-- Slide 35 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide35.png">
</p>



#### 12. Additional Expert Considerations

- **Cross-Validation:** Ensured model generalizability.
- **Model Governance:** Versioning, lineage tracking, compliance.
- **Scalability and Optimization:** Performance tests, scalability checks.
- **Feedback Loop:** Integrated feedback for continuous improvement.

   
### Technologies Used

- **Data Analysis/Model Training:** Python, Jupyter Notebooks
- **Experiment Tracking:** MLFlow
- **Model Building:** PyCaret, LightGBM, XGBoost, CatBoost
- **Hyperparameter Optimization:** Optuna
- **Containerization:** Docker
- **Realtime Data Streaming:** Kafka
- **Version Control and CI/CD:** Git, GitHub Actions
- **Cloud Deployment:** Azure Machine Learning, Azure Blob Storage
- **User Interface:** Streamlit
- **Dependency and Environment Management:** Poetry

### Business Case

Our solution targets healthcare providers for early identification of at-risk patients, public health officials for data-driven policy making, and insurance companies for premium adjustment based on individual risk. The economic impact includes significant healthcare cost savings and revenue generation from tailored wellness programs.

### Acknowledgements

This project is an effort by the team to tackle the global health crisis of obesity by employing advanced data science and machine learning techniques, aiming to make a significant impact in the healthcare sector.


### Meet the Team 
Mahrukh, Aasna, Arham, Krishan, Yash, Nandani


----

<!-- Slide 36 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide36.png">
</p>



<!-- Slide 37 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide37.png">
</p>



<!-- Slide 38 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide38.png">
</p>




<!-- Slide 2 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide2.png">
</p>



<!-- Slide 3 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide3.png">
</p>



<!-- Slide 4 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide4.png">
</p>



<!-- Slide 5 -->
<p align="center">
  <img src="https://github.com/McGill-MMA-EnterpriseAnalytics/Multi-Class-Prediction-of-Obesity-Risk/blob/main/16-README-Support-Files/Slide5.png">
</p>

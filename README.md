# Bangkok Condominium Price Prediction

## Project Summay
---
Due to covid-19 situation, condominium prices decrease while condominium demands have been increasing since 2021. So, this is an opportunity to invest on Bangkok condominiums and machine learning models which can help investors find real value of condominiums.

This project aims to predict condominium prices in Bangkok by using scraped data from Hipflat via Selenium library. The final model of the project is Random Forest Regression.

The final model can perform well on condominiums that their prices are lower than 5 million baht and also on condominiums with 1-2 bedrooms.

## Problem Statement
---
- Opportunities:
    1. Prices decreased due to covid situation.
    2. Many campaigns and discounts are being used to reinforce market demand.
    3. Condominium prices are likely to increase in 2023 due to higher construction costs and also residential market recovery.

- Objectives:
    1. To conduct a model that could help investors to predict condominium prices.
    2. To be one of the tools that helps buyers find real condominium values.

## Conclusion
---
1. The final model is Random Forest with missing values replacement by the median.
2. Model performs better on lower price (< 5 MB) condominiums.
3. Currently, model performance based on data.
    - If we have a large and up-to-date dataset, model tends to perform well.
4. Outliers are one of the important areas of concern when working with price prediction data. 

## Future Works
---
1. Spend more time with feature selection and feature engineering processes.
2. Explore more hyperparameter tuning.
3. Add emotional features such as interior design.

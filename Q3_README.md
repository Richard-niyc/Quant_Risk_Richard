# Risk Factor Analysis for Crypto Assets

## Overview

This project is a Python-based framework designed for analyzing the risk associated with different crypto assets, as well as their relationships with macroeconomic factors, such as the S&P 500 index. It creates various risk factors including Volatility Clustering, Market Liquidity, Inter-Asset Correlation, Macro Sensitivity, and performs various analyses with models including multivariate regression, Principal Component Analysis (PCA) and stress testing. The project also generates visualizations to help understand these factors.

The goal of this project is to provide insights into crypto asset risks, focusing on macro sensitivity, asset correlations, and responses to extreme scenarios.

## Features

- Fetch crypto assets and S&P 500 data from CoinGecko and Yahoo Finance APIs
- Compute market liquidity and volatility clustering for crypto assets
- Analyze Macro Sensitivity for crypto assets
- Generate correlation matrices for different crypto assets
- Implement multivariate regression to identify risk factors
- Conduct Principal Component Analysis (PCA) for risk factor dimensionality reduction
- Perform stress tests to simulate extreme risk scenarios

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- The following Python packages are required:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `statsmodels`
  - `arch`
  - `scikit-learn`
  - `yfinance`
  - `requests`
  - `datetime`

To install the necessary packages, you can run:

```sh
pip install pandas numpy matplotlib statsmodels arch scikit-learn yfinance requests datetime
```

### Running the Project

1. **Clone the Repository**
   
   Clone the project repository from GitHub or download the source code manually:

   ```sh
   git clone <repository-url>
   cd crypto-risk-analysis
   ```

2. **Edit Assets and Dates (Optional)**

   You can modify the `assets`, `start_date`, and `end_date` variables to specify the crypto assets to analyze and the time period. The default assets are:

   ```python
   assets = ['bitcoin', 'ethereum', 'solana', 'chainlink']
   start_date = pd.Timestamp.now() - pd.Timedelta(days=365)
   end_date = pd.Timestamp.now()
   ```

3. **Run the Analysis**

   This will fetch the data, save it to CSV files, preprocess the data, and conduct a variety of risk analyses.

## Usage and Functions

### 1. Fetch Data (`fetch_data_to_csv()`)

This function fetches historical price and volume data for the specified crypto assets using CoinGecko's API and S&P 500 index from Yahoo Finance API. The data is saved to CSV files for later use.

### 2. Read Data (`read_csv_data()`)

Reads the data saved in CSV files and prepares it for analysis. It handles reindexing of data to ensure the index alignment of S&P 500 data with the crypto assets data.

### 3. Preprocess Data (`preprocess_data()`)

Handles data preprocessing for each crypto asset, including calculating daily returns, volatility and macroeconomic data (S&P 500 returns).

### 4. Compute Liquidity (`compute_liquidity()`)

Computes market liquidity for each crypto asset based on trading volume and price.

### 5. Compute Volatility Clustering (`compute_volatility_clustering()`)

Measures volatility clustering using a GARCH model for each crypto asset's returns.

### 6. Compute Correlations (`compute_correlations()`)

Calculates correlation matrices to assess dependencies among crypto assets.

### 7. Plot Macro Sensitivity (`plot_macro_sensitivity()`)

Generates plots showing the relationship between individual crypto asset returns and S&P 500 returns over time.

### 8. Plot Correlations (`plot_correlations()`)

Visualizes the correlation matrix among different crypto assets.

### 9. Factor Regression Model (`factor_regression_model()`)

Implements a multivariate regression model to analyze risk factors affecting each crypto asset's returns. The analysis includes macroeconomic factor (S&P 500 returns), liquidity, and volatility clustering.

### 10. PCA Analysis (`pca_analysis()`)

Performs Principal Component Analysis (PCA) to reduce dimensionality and identify main components of risk among crypto assets.

### 11. Stress Testing (`stress_testing()`)

Conducts a simple stress test to simulate how each crypto asset responds to extreme changes in risk factors, such as a significant drop in liquidity.

## Output

The program produces the following outputs:

- **CSV Files**: Data for each crypto assets and the S&P 500, saved in separate CSV files.
- **Plots**:
  - Macro Sensitivity of each crypto asset over time.
  - Correlation matrix of crypto assets.
  - Explained variance by principal components.
  - Stress test impact on crypto asset returns.
- **Regression Results**: Regression summary for each asset, printed to the console.

## Reproducibility Notes

- The program includes a retry mechanism with exponential backoff for data fetching, which helps to handle potential network or server issues.
- Time ranges are restricted to the last year due to API limitations or practical considerations for crypto assets volatility analysis.
- Dates can be adjusted to cover a wider or more specific time frame by modifying the `start_date` and `end_date` variables.

## Troubleshooting

- **Data Fetch Issues**: If the data fetch fails, it retries up to 3 times with exponential backoff. Ensure that you have a stable internet connection.
- **API Limitations**: If the API fails due to request limits, consider adding delay or spreading requests across time to avoid rate-limiting.

## Acknowledgments

- **CoinGecko API** for providing crypto assets data.
- **Yahoo Finance** for providing stock market data.

---


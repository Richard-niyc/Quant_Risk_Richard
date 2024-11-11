import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf
from arch import arch_model
from sklearn.decomposition import PCA
import time
import datetime
import yfinance as yf

class CryptoRiskAnalysis:
    def __init__(self, assets, start_date, end_date):
        self.assets = assets
        self.start_date = max(start_date, pd.Timestamp.now() - pd.Timedelta(days=365))
        self.end_date = min(end_date, pd.Timestamp.now())
        self.data = {}
        self.regression_coefficients = {}
        
    def fetch_data_to_csv(self):
        """
        Fetch historical price and volume data for the specified crypto assets using CoinGecko API.
        Fetch daily close price of S&P 500 index from Yahoo Finance API.
        Retry failed requests up to 3 times with exponential backoff.
        """
        base_url = "https://api.coingecko.com/api/v3/coins/"
        data = {}

        # Fetch crypto data
        for asset in self.assets:
            success = False
            attempts = 0
            while not success and attempts < 3:
                url = f"{base_url}{asset}/market_chart/range"
                params = {
                    'vs_currency': 'usd',
                    'from': int(self.start_date.timestamp()),
                    'to': int(self.end_date.timestamp())
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    self.data[asset] = pd.DataFrame(
                        {
                            'timestamp': [x[0] for x in data['prices']],
                            'price': [x[1] for x in data['prices']],
                            'volume': [x[1] for x in data['total_volumes']]
                        }
                    )
                    self.data[asset]['date'] = pd.to_datetime(self.data[asset]['timestamp'], unit='ms')
                    self.data[asset].set_index('date', inplace=True)
                    success = True
                    # Save the DataFrame to a CSV file
                    self.data[asset].to_csv(asset+".csv")

                else:
                    attempts += 1
                    print(f"Attempt {attempts} failed to fetch data for {asset}. Status Code: {response.status_code}. Response: {response.text}. Retrying...")
                    time.sleep(2 ** attempts)  # Exponential backoff

            if not success:
                print(f"Failed to fetch data for {asset} after 3 attempts.")
                self.data[asset] = None

        # Fetch S&P 500 data from Yahoo Finance API
        # Define the indices and the ticker symbol
        indices = {
            'S&P 500': '^GSPC'
        }
        
        # Create a DataFrame to store the closing prices
        df_index = pd.DataFrame()
        
        # Retrieve data for each index
        for index_name, ticker in indices.items():
            # Download the historical data
            data_index = yf.download(ticker, start=self.start_date, end=end_date)
            # Extract the 'Close' column and rename it to the index name
            df_index[index_name] = data_index['Close']
            df_index.index = [df_index.index[i].strftime('%Y-%m-%d') for i in range(len(df_index.index))]
            df_index.index.name = 'date'
        
        # Save the DataFrame to a CSV file
        df_index.to_csv('sp500.csv')

    def read_csv_data(self):
        assets_to_read = self.assets + ['sp500']
        for asset in assets_to_read:
            try:
                file_path = f"{asset}.csv"
                if asset != 'sp500':
                    self.data[asset] = pd.read_csv(file_path, index_col='date', parse_dates=True)
                    reindex_start = self.data[asset].index[0]
                    reindex_end = self.data[asset].index[-1]
                else:
                    self.data[asset] = pd.read_csv(file_path, index_col='date', parse_dates=True)
                    # Fill non-business day gaps with the previous business day's data
                    self.data[asset] = self.data[asset].reindex(pd.date_range(reindex_start, reindex_end, freq='D'), method='ffill')
            except FileNotFoundError:
                print(f"CSV file for {asset} not found at {file_path}.")
                self.data[asset] = None
        self.data['sp500'].index = self.data['bitcoin'].index
    
    def preprocess_data(self):
        """
        Preprocess the collected data, handle missing values, and calculate daily returns and volatility.
        """
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None:
                    df['return'] = df['price'].pct_change()
                    df['volatility'] = df['return'].rolling(window=30).std()
                    df['macro'] = self.data['sp500'].pct_change()
                    df.dropna(inplace=True)
            
    def compute_liquidity(self):
        """
        Compute market liquidity for each asset, based on trading volume.
        """
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None:
                    df['liquidity'] = df['volume'] / df['price']
                
    def compute_volatility_clustering(self):
        """
        Measure volatility clustering using GARCH model parameters for each asset.
        """
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None and 'return' in df.columns:
                returns = df['return'].dropna()
                if len(returns) > 1:
                    garch_model = arch_model(returns, vol='Garch', p=1, q=1)
                    garch_fit = garch_model.fit(disp='off')
                    df['volatility_clustering'] = garch_fit.conditional_volatility
                else:
                    df['volatility_clustering'] = np.nan
                
    def compute_correlations(self):
        """
        Compute correlation matrices to assess dependencies among assets.
        """
        valid_data = [df['return'] for asset, df in self.data.items() if asset != 'sp500' and df is not None and not df['return'].empty]
        if not valid_data:
            print("No valid data available for correlation computation.")
            return pd.DataFrame()
        combined_data = pd.concat(valid_data, axis=1)
        combined_data.columns = [asset for asset in self.assets if self.data[asset] is not None and not self.data[asset]['return'].empty]
        correlation_matrix = combined_data.corr()
        return correlation_matrix

    def plot_macro_sensitivity(self):
        """
        Plot the macro sensitivity of each asset over time.
        """
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None:
                plt.figure(figsize=(12, 8))
                plt.plot(df.index, df['return'], label=f'{asset} return')
                plt.plot(df.index, df['macro'], label=f'S&P 500 return')
                plt.xlabel('Date')
                plt.ylabel('Return')
                plt.title(f'Macro Sensitivity of {asset} Over Time')
                plt.savefig(f"Macro Sensitivity of {asset} Over Time.png")
                plt.legend()
                plt.show()
    
    def plot_correlations(self):
        """
        Visualize the correlation matrix of the crypto assets.
        """
        correlation_matrix = self.compute_correlations()
        if correlation_matrix.empty:
            print("No correlation data available to plot.")
            return
        plt.figure(figsize=(10, 8))
        plt.imshow(correlation_matrix, cmap='viridis', interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
        plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
        plt.title('Crypto Asset Correlations')
        plt.savefig("Crypto Asset Correlations.png")
        plt.show()

    def factor_regression_model(self):
        """
        Implement a multivariate regression model to analyze risk factors affecting asset returns.
        """ 
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None:
                # Prepare risk factors
                df = df.dropna(subset=['return', 'volatility_clustering', 'liquidity', 'macro'])
                if df.empty:
                    print(f"Not enough data for regression analysis for {asset}.")
                    continue
                X = df[['volatility_clustering', 'liquidity', 'macro']]
                X = sm.add_constant(X)  # Add constant to the model
                y = df['return']
                
                # Run regression model
                model = sm.OLS(y, X).fit()
                print(f"Regression Summary for {asset}:{model.summary()}")
                
                # Store the regression coefficients
                self.regression_coefficients[asset] = model.params

                # Calculate the proportion of variance explained by each factor
                r_squared = model.rsquared
                factor_contributions = (X * model.params).var() / y.var()
                print(f"R-squared: {r_squared}")
                print(f"Factor Contributions to Variance: {factor_contributions}")   

    def pca_analysis(self):
        """
        Perform Principal Component Analysis (PCA) to reduce dimensionality and identify main components of risk.
        """
        valid_data = [df[['volatility_clustering', 'liquidity', 'macro']].dropna() for asset, df in self.data.items() if asset != 'sp500' and df is not None]
        if not valid_data:
            print("No valid data available for PCA analysis.")
            return
        combined_data = pd.concat(valid_data, axis=0)
        pca = PCA(n_components=3)
        pca.fit(combined_data)
        explained_variance = pca.explained_variance_ratio_

        plt.figure(figsize=(10, 6))
        plt.bar(range(1, len(explained_variance) + 1), explained_variance, tick_label=[f'PC{i}' for i in range(1, len(explained_variance) + 1)])
        plt.xlabel('Principal Components')
        plt.ylabel('Explained Variance Ratio')
        plt.title('Explained Variance by Principal Components')
        plt.savefig("Explained Variance by Principal Components.png")
        plt.show()

        print(f"Explained Variance by Principal Components: {explained_variance}")

    def stress_testing(self):
        """
        Conduct a simple stress test to simulate how assets respond to extreme changes in risk factors.
        """
        stress_liquidity_drop = -0.5  # Simulate a 50% drop in liquidity
        for asset, df in self.data.items():
            if asset != 'sp500' and df is not None and not df.empty:
                stressed_returns = df['return'] + (df['liquidity'] * self.regression_coefficients[asset]['liquidity'] * stress_liquidity_drop)
                plt.figure(figsize=(10, 6))
                plt.plot(df.index, df['return'], label='Original Returns')
                plt.plot(df.index, stressed_returns, label='Stressed Returns', linestyle='--')
                plt.title(f'Stress Test for {asset} - Impact of Stressed Liquidity Drop')
                plt.xlabel('Date')
                plt.ylabel('Return')
                plt.legend()
                plt.savefig(f"Stress Test for {asset} - Impact of Stressed Liquidity Drop.png")
                plt.show()
                
    def run_analysis(self):
        self.fetch_data_to_csv()
        self.read_csv_data()
        self.preprocess_data()
        self.compute_liquidity()
        self.compute_volatility_clustering()
        self.plot_macro_sensitivity()
        self.plot_correlations()
        self.factor_regression_model()
        self.pca_analysis()
        self.stress_testing()

        
assets = ['bitcoin', 'ethereum', 'solana', 'chainlink']
start_date = pd.Timestamp.now() - pd.Timedelta(days=365)
end_date = pd.Timestamp.now()
analysis = CryptoRiskAnalysis(assets, start_date, end_date)
analysis.run_analysis()

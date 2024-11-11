# BTC Options Implied Volatility Surface Visualization

## 1. Overview
This project retrieves Bitcoin (BTC) options data from Deribit, extracts implied volatilities, and visualizes the implied volatility surface using a 3D graph. The results are saved for future reference, and the entire process can be automated with minimal manual intervention.

## 2. Requirements
- Python 3.x
- Libraries:
  - `requests`
  - `matplotlib`
  - `numpy`
  - `scipy`

## 3. Installation
1. Ensure Python is installed. You can download it from [python.org](https://www.python.org/downloads/).
2. Install the required libraries using the following command:
   ```sh
   pip install requests matplotlib numpy scipy
   ```

## 4. Usage
1. Clone this repository or download the Python script to your local machine:
   ```sh
   git clone <repository_url>
   ```
2. Run the script:

## 5. Explanation
### 5.1 Functions
- **`get_instruments(currency="BTC", kind="option")`**: Fetches all BTC option instruments from the Deribit API.
- **`get_order_book(instrument_name)`**: Retrieves the order book for a specific instrument to obtain its implied volatility.
- **`get_implied_volatilities(instruments)`**: Iterates over all instruments to fetch their implied volatilities and calculates the time to expiration.
- **`visualize_iv_surface(iv_data)`**: Visualizes the implied volatility surface using a 3D plot, including a smoothed version of the surface using a Gaussian filter.
- **`main()`**: Orchestrates the workflow—fetching instruments, retrieving implied volatilities, saving data to a JSON file, and visualizing the implied volatility surface.

## 6. Detailed Steps
### 6.1 Fetching Instruments
The `get_instruments` function fetches all available BTC option instruments from the Deribit API.

### 6.2 Getting Implied Volatilities
The `get_implied_volatilities` function calculates the implied volatility for each instrument along with the time to expiration in milliseconds.

### 6.3 Visualizing the Implied Volatility Surface
The `visualize_iv_surface` function generates a 3D plot of the implied volatility surface. It produces both the original and smoothed surfaces using a Gaussian filter.

### 6.4 Saving the Results
The script saves the implied volatility data and graphs locally for future reference.

## 7. Example Output
The script generates the following 3D plots:
- **Original Mark Implied Volatility Surface**
- **Smoothed Mark Implied Volatility Surface**

## 8. Automating Daily Runs
To run the script daily with minimal manual intervention:
- **Unix-based systems**: Set up a cron job.
- **Windows systems**: Use Task Scheduler.

---


# Avenir-Quant
1. Data Processing and Visualization

This project retrieves BTC option instruments from Deribit, obtains their implied volatilities, and visualizes the implied volatility surface on a 3D graph. The results are saved and can be run with minimal manual intervention.

1.1 Requirements
Python 3.x
requests library
matplotlib library
numpy library
scipy library

1.2 Installation
Ensure you have Python installed. You can download it from python.org.
Install the required libraries.

1.3 Usage
Clone this repository or download the Python script to your local machine.

1.4 Explanation
1.4.1 get_instruments(currency="BTC", kind="option"): Fetches all BTC option instruments from Deribit.
1.4.2 get_order_book(instrument_name): Retrieves the order book for a specific instrument to obtain its implied volatility.
1.4.3 get_implied_volatilities(instruments): Iterates over all instruments to fetch their implied volatilities and calculates the time to expiration.
1.4.4 visualize_iv_surface(iv_data): Visualizes the implied volatility surface using a 3D plot. Also smooths the surface using a Gaussian filter.
1.4.5 main(): The main function that fetches the instruments, retrieves their implied volatilities, saves the data to a JSON file, and visualizes the implied volatility surface.

1.5 Detailed Steps
1.5.1. Fetching Instruments
The get_instruments method fetches all available BTC option instruments from the Deribit API.
1.5.2. Getting Implied Volatilities
The get_implied_volatilities function calculates the implied volatility for each instrument and the time to expiration in milliseconds.
1.5.3. Visualizing the IV Surface
The visualize_iv_surface function generates a 3D plot of the implied volatility surface. It plots both the original and smoothed surfaces using a Gaussian filter.
1.5.4. Saving the Results
The implied volatility data and graphs are saved on your local drive for future reference.

1.6 Example Output
The script generates two 3D plots:
1.6.1. Original Mark Implied Volatility Surface
1.6.2. Smoothed Mark Implied Volatility Surface

Running the Script Daily
To run this script daily with minimal manual intervention, you can set up a cron job (Unix-based systems) or Task Scheduler (Windows) to execute the script.

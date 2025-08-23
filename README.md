# Stock Trading Signal Generator
This project is a Python-based command-line application that uses a LightGBM model to analyze historical stock price data and generate buy/sell signals for paper trading simulations. It processes a CSV file with stock prices and indicators, trains a model to predict buy signals, and produces a backtested output CSV with trade signals, stop-loss, and target prices.

## Installation
You can install the package using pip. It's recommended to do this in a virtual environment.
```bash
pip install -e .
```

## Usage
The application provides a command-line interface (CLI) to train the model and generate predictions.

**1. Train the Model**  
To train the model, use the train command and provide the path to your input CSV file and the path where the model should be saved.
```bash
signals train --input-file path/to/your/data.csv --model-file path/to/save/model.joblib
```
The input CSV file must contain at least the following columns: Date, Close, High. Other numeric columns will be used as features for the model.

***2. Generate Signals and Backtest***  
Once the model is trained, you can use the predict command to generate trading signals and run a backtest. You'll need to provide the input CSV, the trained model, and a path for the output CSV file.

```bash
signals predict --input-file path/to/your/data.csv --model-file path/to/your/model.joblib --output-file path/to/your/output.csv
```
- The output CSV will contain the original data along with the following columns:
- Buy_Signal: 1 if a buy signal is generated, 0 otherwise.
- StopLoss_Price: The calculated stop-loss price for the trade.
- Target_Price: The calculated target price for the trade.
- Sell_Signal: 1 if a sell signal is generated (due to target, stop-loss, or time-out), 0 otherwise.
- Trade_Result: The profit or loss from the trade.

#### Example Workflow  
```bash
# Step 1: Train the model
signals train --input-file historical_data.csv --model-file trading_model.joblib

# Step 2: Generate predictions and backtest
signals predict --input-file historical_data.csv --model-file trading_model.joblib --output-file backtest_results.csv
```
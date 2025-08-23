# signals/backtest.py

import pandas as pd
import numpy as np

def run_backtest(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs a simple backtest on the generated signals.

    Args:
        df: DataFrame with original data and 'Buy_Signal' column.

    Returns:
        DataFrame with backtesting results.
    """
    df['StopLoss_Price'] = 0.0
    df['Target_Price'] = 0.0
    df['Sell_Signal'] = 0
    df['Trade_Result'] = 0.0

    in_position = False
    position_entry_index = -1
    entry_price = 0.0
    stop_loss = 0.0
    target_price = 0.0

    for i in range(len(df)):
        # Entry condition
        if not in_position and df.at[i, 'Buy_Signal'] == 1:
            in_position = True
            position_entry_index = i
            entry_price = df.at[i, 'Close']
            stop_loss = entry_price * 0.99  # 1% stop loss
            target_price = entry_price * 1.03  # 3% target price

            df.at[i, 'StopLoss_Price'] = stop_loss
            df.at[i, 'Target_Price'] = target_price

        # Exit conditions
        if in_position:
            # Target price hit
            if df.at[i, 'High'] >= target_price:
                df.at[i, 'Sell_Signal'] = 1
                df.at[i, 'Trade_Result'] = target_price - entry_price
                in_position = False
            # Stop loss hit
            elif df.at[i, 'Close'] <= stop_loss:
                df.at[i, 'Sell_Signal'] = 1
                df.at[i, 'Trade_Result'] = stop_loss - entry_price
                in_position = False
            # Position timeout (2 days)
            elif i - position_entry_index >= 2:
                df.at[i, 'Sell_Signal'] = 1
                df.at[i, 'Trade_Result'] = df.at[i, 'Close'] - entry_price
                in_position = False

    # Calculate metrics
    trades = df[df['Sell_Signal'] == 1]
    if not trades.empty:
        win_rate = (trades['Trade_Result'] > 0).mean()
        total_profit = trades['Trade_Result'].sum()
        print("\n--- Backtest Results ---")
        print(f"Total Trades: {len(trades)}")
        print(f"Win Rate: {win_rate:.2%}")
        print(f"Total Profit/Loss: {total_profit:.2f}")
        print("------------------------")
    else:
        print("No trades were executed in the backtest.")


    return df

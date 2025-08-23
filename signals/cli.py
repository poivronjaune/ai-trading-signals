# signals/cli.py

import click
from joblib import load

from signals.data import load_data
from signals.model import train_model, predict_signals
from signals.backtest import run_backtest

@click.group()
def cli():
    """A CLI for training a trading model and generating signals."""
    pass

@cli.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the input CSV file.')
@click.option('--model-file', type=click.Path(), required=True, help='Path to save the trained model.')
def train(input_file, model_file):
    """Train the LightGBM model."""
    click.echo(f"Loading data from {input_file}...")
    df = load_data(input_file)
    click.echo("Training model...")
    train_model(df, model_file)
    click.echo("Training complete.")

@cli.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the input CSV file.')
@click.option('--model-file', type=click.Path(exists=True), required=True, help='Path to the trained model file.')
@click.option('--output-file', type=click.Path(), required=True, help='Path to save the output CSV file.')
def predict(input_file, model_file, output_file):
    """Generate signals and run a backtest."""
    click.echo(f"Loading data from {input_file}...")
    df = load_data(input_file)
    
    click.echo(f"Loading model from {model_file}...")
    model = load(model_file)
    
    click.echo("Generating predictions...")
    df['Buy_Signal'] = predict_signals(df, model)
    
    click.echo("Running backtest...")
    results_df = run_backtest(df)
    
    results_df.to_csv(output_file, index=False)
    click.echo(f"Backtest complete. Results saved to {output_file}")

if __name__ == '__main__':
    cli()

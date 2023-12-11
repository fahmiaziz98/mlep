# Training Pipeline
## Usage for Development
Run the scripts in the following order:

1. Start the hyperparameter tuning script:
`python -m training_pipeline.hyperparameter_tuning`
2. Upload the best config based on the previous hyperparameter tuning step:
`python -m training_pipeline.best_config`
3. Start the training script using the best configuration uploaded one step before:
`python -m training_pipeline.train`
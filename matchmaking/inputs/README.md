# Matchmaking inputs
To run matchmaking, the following inputs must be configured for your cohort:
- `somatic_variants`
- `copy_number_alterations`
- `fusions`
- `samples`
- `labeled samples`

A pairwise comparison must also be performed on samples and their labels. Please follow the following steps to configure your inputs to run matchmaking,
1. Follow instructions under [`formatted/`](formatted/) to format your samples and molecular features
2. Follow instructions under [`annotated/`](annotated/) to annotate molecular features after formatting
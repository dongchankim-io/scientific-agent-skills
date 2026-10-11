# Methodological Critique & Peer-Review Rubric

When evaluating or critiquing a scientific paper, systematically check the following dimensions:

## 1. Problem Formulation & Assumptions
- Are simplifying assumptions (e.g., i.i.d. data, noiseless observations, stationarity, specific priors) explicitly stated?
- Does the proxy metric optimized in the paper actually measure the real-world scientific phenomenon claimed in the introduction?

## 2. Baseline & Evaluation Fairness
- Are baselines tuned with comparable compute/hyperparameter budgets, or are they under-tuned strawmen?
- Are standard, strong domain baselines included?
- Is there any risk of data leakage, test-set contamination, or cherry-picked evaluation splits?

## 3. Statistical Rigor
- Are error bars, standard deviations, or confidence intervals reported across multiple random seeds or experimental replicates?
- Does the claimed improvement exceed the variance across runs?

## 4. Ablation Completeness
- If the proposed method combines $N$ components (e.g., new loss + new architecture + new data augmentation), does the ablation table isolate the contribution of each component individually?

## 5. Reproducibility & Resource Transparency
- Are compute requirements (GPU/CPU hours, memory footprint), hyperparameters, and dataset versions specified clearly enough to replicate the main table?

# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Complete documentation suite:
  - `START_HERE.md` - Project index and getting started guide
  - `QUICK_START.md` - Quick start guide for new experiments
  - `EDA_EXPLAINED.md` - Explanation of EDA and when to use it
  - `WORKFLOW_GUIDE.md` - Complete workflow guide
  - `FEATURE_ENGINEERING_EXAMPLE.md` - Examples of modifying features
  - `STRUCTURE.md` - Detailed project structure
- `requirements.txt` - Python package dependencies
- `.gitignore` - Git ignore file for ML projects
- `scripts/create_new_experiment.py` - Automated script to create new experiments
- `config.py` - Centralized configuration file

### Changed
- Improved project structure documentation
- Enhanced README.md with better organization

### Fixed
- Clarified EDA workflow (must be done BEFORE training)
- Explained how to modify feature engineering

## [2025-10-23] - Experiment 5

### Added
- Ensemble methods (Voting, Stacking, Blending, Weighted Average)
- Family survival feature

### Results
- XGBoost: 0.8664 (best)
- Ensemble models created

## [2025-10-22] - Experiment 4

### Added
- Submission files for all models

## [2025-10-21] - Experiment 3

### Added
- Model package save format
- Multiple model outputs

## [2025-10-20] - Experiment 2

### Added
- Model persistence with joblib
- Data preprocessing pipeline

## [2025-10-18] - Experiment 1

### Added
- Initial project setup
- Basic models (Logistic Regression, Random Forest, XGBoost)
- EDA notebook
- Training pipeline

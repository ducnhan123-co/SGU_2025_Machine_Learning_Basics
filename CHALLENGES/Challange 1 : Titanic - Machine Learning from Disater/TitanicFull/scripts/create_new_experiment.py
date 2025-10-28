#!/usr/bin/env python3
"""
Script to create a new experiment folder with template files.
Usage: python scripts/create_new_experiment.py [date]
Example: python scripts/create_new_experiment.py 24102025
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def create_experiment(date_str):
    """Create a new experiment folder with template files."""
    
    # Validate date format (DDMMYYYY)
    if len(date_str) != 8 or not date_str.isdigit():
        print("❌ Error: Date must be in DDMMYYYY format")
        print("Example: 24102025")
        return False
    
    # Parse date
    try:
        day = date_str[:2]
        month = date_str[2:4]
        year = date_str[4:]
        datetime(int(year), int(month), int(day))
    except ValueError:
        print("❌ Error: Invalid date")
        return False
    
    # Paths
    base_path = Path(__file__).parent.parent
    exp_name = f"test_{date_str}"
    exp_path = base_path / "process" / exp_name
    
    # Check if exists
    if exp_path.exists():
        print(f"❌ Error: Experiment {exp_name} already exists")
        return False
    
    # Create directories
    print(f"📁 Creating directories for {exp_name}...")
    (exp_path / "eda").mkdir(parents=True, exist_ok=True)
    (exp_path / "model").mkdir(parents=True, exist_ok=True)
    (exp_path / "runs").mkdir(parents=True, exist_ok=True)
    
    # Find latest experiment to copy from
    process_dir = base_path / "process"
    all_tests = sorted([d for d in process_dir.glob("test_*") if d.is_dir()])
    
    if all_tests:
        source = all_tests[-1]  # Latest experiment
        print(f"📋 Copying from latest experiment: {source.name}")
        
        # Copy train.ipynb
        if (source / "model" / "train.ipynb").exists():
            shutil.copy2(source / "model" / "train.ipynb", exp_path / "model" / "train.ipynb")
            print("  ✓ Copied train.ipynb")
        
        # Copy eda notebook (optional)
        if (source / "eda" / "eda01.ipynb").exists():
            shutil.copy2(source / "eda" / "eda01.ipynb", exp_path / "eda" / "eda01.ipynb")
            print("  ✓ Copied eda01.ipynb")
    else:
        print("⚠️  No previous experiments found, creating empty structure")
    
    # Create README template
    readme_content = f"""# Experiment {date_str}

## Date
{date_str[:2]}/{date_str[2:4]}/{date_str[4:]}

## Description
TODO: Describe this experiment

## Changes from previous experiment
TODO: List changes

## Results
TODO: Add results after training

### Models
- Logistic Regression:
- Random Forest:
- XGBoost:
- Kaggle Score:
"""
    
    (exp_path / "README.md").write_text(readme_content)
    print("  ✓ Created README.md")
    
    # Update train.ipynb config
    if (exp_path / "model" / "train.ipynb").exists():
        print("\n⚠️  Don't forget to update config in train.ipynb:")
        print(f"   exp_name: 'trainbase_{date_str}'")
        print(f"   exp_dir: '{base_path / 'process' / 'exps'}'")
    
    print(f"\n✅ Experiment {exp_name} created successfully!")
    print(f"📂 Path: {exp_path}")
    print(f"\nNext steps:")
    print(f"1. cd {exp_path}/model")
    print(f"2. jupyter notebook train.ipynb")
    print(f"3. Update exp_name in config")
    print(f"4. Modify preprocessing if needed")
    print(f"5. Run all cells")
    
    return True

def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        # Use today's date
        today = datetime.now()
        date_str = today.strftime("%d%m%Y")
        print(f"No date provided, using today: {date_str}")
    
    create_experiment(date_str)

if __name__ == "__main__":
    main()

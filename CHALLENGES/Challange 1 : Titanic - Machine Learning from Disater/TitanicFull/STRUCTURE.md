# 📐 Cấu trúc dự án chi tiết

## 🎯 Nguyên tắc thiết kế

Dự án được thiết kế theo nguyên tắc systems, in the sản khoa học:

1. **Tách biệt dữ liệu gốc** (`data/`) và dữ liệu đã xử lý (`exps/`)
2. **Versioning experiments** theo ngày tháng
3. **Tái sử dụng code** giữa các experiments
4. **Ghi chép kết quả** để so sánh

---

## 📁 Cấu trúc phân cấp

```
TitanicFull/
│
├── 📂 data/                          ─────┐
│   ├── train.csv                         │ DỮ LIỆU GỐC
│   ├── test.csv                          │ (chỉ đọc)
│   └── gender_submission.csv             └────────────
│
├── 📂 process/
│   │
│   ├── 📂 exps/                      ───┐
│   │   ├── record.xlsx                  │ KẾT QUẢ
│   │   └── trainbase_23102025/          │ EXPERIMENTS
│   │       ├── data.npz                 │
│   │       ├── *_model.pkl              │
│   │       ├── submission_*.csv         │
│   │       └── *_package.pkl            └────────────
│   │
│   └── 📂 test_23102025/             ───┐
│       ├── README.md                     │
│       ├── 📂 eda/                       │ NOTEBOOK
│       │   └── eda01.ipynb               │ WORKFLOW
│       ├── 📂 model/                     │
│       │   ├── train.ipynb  ⭐ CORE      │
│       │   └── train.html                │
│       └── 📂 runs/                      │
│           ├── main_23102025.ipynb      │
│           └── test_predictions.npy      └────────────
│
└── 📄 README.md
```

---

## 🔄 Luồng dữ liệu (Data Flow)

```
┌─────────────────────────────────────────────────────────────┐
│                     WORKFLOW EXPERIMENT                      │
└─────────────────────────────────────────────────────────────┘

1. DATA INGESTION
   ┌─────────────┐
   │  data/*.csv │ ────Read──> │ train.ipynb │
   └─────────────┘               └────────────┘

2. PREPROCESSING
   │ train.ipynb │ ──Preprocess─> │ df_output │
   └─────────────┘                  └──────────┘

3. SAVE PROCESSED DATA
   │ df_output │ ──np.savez──> │ exps/.../data.npz │
   └───────────┘                 └──────────────────┘

4. MODEL TRAINING
   │ exps/.../data.npz │ ──Load──> │ GridSearchCV │
   └───────────────────┘            └──────────────┘
                                    │
                                    v
                              │ best_model thumb │
                              └───────────────────┘

5. SAVE MODEL
   │ best_model │ ──joblib.dump──> │ exps/.../*_model.pkl │
   └────────────┘                   └──────────────────────┘

6. PREDICTION
   │ *_model.pkl │ ──Load──> │ model.predict(X_test) │
   └─────────────┘            └───────────────────────┘

7. SUBMISSION
   │ predictions │ ──to_csv──> │ exps/.../submission_*.csv │
   └─────────────┘               └───────────────────────────┘
```

---

## 📝 Trách nhiệm từng file

### Data Layer

| File | Nhiệm vụ | Ghi chú |
|------|----------|---------|
| `data/train.csv` | Dữ liệu training với nhãn | 891 samples, không thay đổi |
| `data/test.csv` | Dữ liệu test không nhãn | 418 samples, không thay đổi |
| `data/gender_submission.csv` | Mẫu format submission | Template cho Kaggle |

### Experiment Layer

| File | Nhiệm vụ | Cấu trúc |
|------|----------|----------|
| `exps/trainbase_YYYYMMDD/data.npz` | Dữ liệu đã preprocess | {train_data, test_data, columns} |
| `exps/trainbase_YYYYMMDD/*_model.pkl` | Model đã train | Pipeline với preprocessing + model |
| `exps/trainbase_YYYYMMDD/submission_*.csv` | File submission | {PassengerId, Survived} |
| `exps/trainbase_YYYYMMDD/*_package.pkl` | Package model + metadata | {model, features, scaler, date} |
| `exps/record.xlsx` | Tổng hợp kết quả | Excel so sánh experiments |

### Code Layer

| File | Nhiệm vụ | Chức năng chính |
|------|----------|-----------------|
| `test_*/README.md` | Documentation | Mô tả thay đổi, kết quả |
| `test_*/eda/eda01.ipynb` | Exploratory Data Analysis | Phân tích, visualization |
| `test_*/model/train.ipynb` | **Core logic** ⭐ | Preprocessing + Training |
| `test_*/model/train.html` | Exported notebook | View offline |
| `test_*/runs/main_YYYYMMDD.ipynb` | Orchestrator | Run toàn bộ workflow |
| `test_*/runs/test_predictions.npy` | Predictions cache | Numpy array |

---

## 🎬 Workflow Step by Step

### Phase 1: Setup
```python
# 1. Tạo thư mục
mkdir process/test_YYYYMMDD/{eda,model,runs}

# 2. Copy code từ experiment trước
cp process/test_OLD/model/train.ipynb process/test_NEW/model/

# 3. Cập nhật config trong train.ipynb
exp_name = 'trainbase_YYYYMMDD'
```

### Phase 2: Data Processing
```python
# Trong train.ipynb
df_train = pd.read_csv(f'{data_dir}/train.csv')
df_test = pd.read_csv(f'{data_dir}/test.csv')

# Preprocessing
df_output_train, _ = preprocessing_feature_01(df_train, is_train=True)
df_output_test, _ = preprocessing_feature_01(df_test, is_train=False)

# Save
np.savez(f'{save_dir}/data.npz', 
         train_data=df_output_train.values,
         test_data=df_output_test.values,
         train_columns=df_output_train.columns.values)
```

### Phase 3: Model Training
```python
# Load processed data
data = np.load('exps/trainbase_YYYYMMDD/data.npz', allow_pickle=True)
df_train = pd.DataFrame(data['train_data'], columns=data['train_columns'])

# Split features and target
X_train = df_train.drop(columns=['Output'])
y_train = df_train['Output']

# GridSearchCV
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Save best model
joblib.dump(grid_search.best_estimator_, 'exps/.../model.pkl')
```

### Phase 4: Prediction & Submission
```python
# Load model
model = joblib.load('exps/.../model.pkl')

# Predict
predictions = model.predict(X_test)

# Create submission
submission = pd.DataFrame({
    'PassengerId': test_data['PassengerId'],
    'Survived': predictions
})

submission.to_csv('exps/.../submission.csv', index=False)
```

---

## 🔗 Dependency Map

```
┌──────────────┐
│ main_*.ipynb │ ───run───> │ train.ipynb │
└──────────────┘            └─────────────┘
                                    │
                                    ├───read──> │ data/*.csv │
                                    │           └────────────┘
                                    │
                                    ├───write──> │ exps/.../data.npz │
                                    │            └───────────────────┘
                                    │
                                    ├───write──> │ exps/.../model.pkl │
                                    │            └────────────────────┘
                                    │
                                    └───write──> │ exps/.../submission.csv │
                                                 └───────────────────────────┘

┌──────────────┐
│ runs/*.ipynb │ ───load──> │ exps/.../data.npz │
└──────────────┘            │ exps/.../model.pkl │
                            └────────────────────┘
```

---

## 💾 File Format Notes

### .npz (Numpy Compressed)
```python
# Lưu
np.savez('data.npz', 
         train_data=X_train.values,
         train_columns=X_train.columns.values)

# Đọc
data = np.load('data.npz', allow_pickle=True)
df = pd.DataFrame(data['train_data'], columns=data['train_columns'])
```

### .pkl (Pickle)
```python
# Lưu
joblib.dump(model, 'model.pkl')
joblib.dump({'model': model, 'features': features}, 'package.pkl')

# Đọc
model = joblib.load('model.pkl')
pkg = joblib.load('package.pkl')
model = pkg['model']
```

### .csv (Submission)
```csv
PassengerId,Survived
892,0
893,1
...
```

---

## 🎯 Best Practices

### ✅ DO
- Lưu processed data để tái sử dụng
- Đặt tên experiment theo ngày
- Ghi README cho mỗi experiment
- Commit code vào git
- Backup model tốt nhất

### ❌ DON'T
- Sửa dữ liệu trong `data/`
- Ghi đè experiment cũ
- Bỏ qua documentation
- Hardcode paths
- Không track changes

---

## 🔧 Config Template

```python
params_cfg = {
    "action"   : "train_feat03",           # Action type
    "feat_path": "../../exps/.../data.npz", # Path to processed data
    "seed"     : 42,                        # Random seed
    "exp_dir"  : "process/exps",            # Experiments directory
    "exp_name" : "trainbase_YYYYMMDD",      # Experiment name
    "data_dir" : "data",                    # Raw data directory
    "verbose"  : True,                      # Print info
}

# Auto create save_dir
params_cfg.update(**{
    "save_dir": f'{params_cfg["exp_dir"]}/{params_cfg["exp_name"]}'
})
```

---

## 📊 Experiment Tracking

### Record File Structure (record.xlsx)

| Experiment | Date | Model | Features | Accuracy | Notes |
|------------|------|-------|----------|----------|-------|
| trainbase_23102025 | 23/10/2025 | XGBoost | feat03 | 0.8664 | Baseline |
| trainbase_24102025 | 24/10/2025 | XGBoost | feat04 | 0.8700 | +new_feature |

---

## 🎓 Lessons Learned

1. **Separate concerns**: Data, Processing, Models
2. **Version everything**: Experiments, Code, Results
3. **Automate**: Use notebooks orchestrator
4. **Document**: README for each experiment
5. **Compare**: Use record.xlsx to track progress

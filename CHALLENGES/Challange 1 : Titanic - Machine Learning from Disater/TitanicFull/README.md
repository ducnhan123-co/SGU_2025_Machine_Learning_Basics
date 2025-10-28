# Titanic Machine Learning Challenge - Template & Documentation

## 📌 Giới thiệu dự án

Dự án này được xây dựng để giải quyết bài toán **"Titanic - Machine Learning from Disaster"** trên Kaggle, đồng thời cung cấp một **template chuẩn** cho các dự án học máy (Machine Learning).

**Mục tiêu:** Dự đoán tỷ lệ sống sót của hành khách trên tàu Titanic dựa trên các thông tin như tuổi, giới tính, hạng vé, v.v.

**Link Challenge:** https://www.kaggle.com/competitions/titanic/overview

---

## 📁 Cấu trúc thư mục dự án

```
TitanicFull/
├── data/                          # Thư mục chứa dữ liệu gốc
│   ├── train.csv                  # Dữ liệu training
│   ├── test.csv                   # Dữ liệu test (không có nhãn)
│   └── gender_submission.csv      # Mẫu submission
│
├── process/                       # Thư mục xử lý và thực nghiệm
│   ├── exps/                      # Thư mục lưu kết quả experiment
│   │   ├── record.xlsx            # Excel ghi lại kết quả các experiment
│   │   ├── trainbase_18102025/    # Experiment 1: 18/10/2025
│   │   ├── trainbase_20102025/    # Experiment 2: 20/10/2025
│   │   ├── trainbase_21102025/    # Experiment 3: 21/10/2025
│   │   ├── trainbase_22102025/    # Experiment 4: 22/10/2025
│   │   └── trainbase_23102025/    # Experiment 5: 23/10/2025
│   │       ├── data.npz           # Dữ liệu đã preprocess (numpy compressed)
│   │       ├── *_model.pkl        # Các mô hình đã train (pickle)
│   │       ├── submission_*.csv   # Kết quả submission cho Kaggle
│   │       └── *_package.pkl      # Package chứa model + metadata
│   │
│   ├── test_18102025/             # Thư mục test của experiment 1
│   ├── test_20102025/             # Thư mục test của experiment 2
│   ├── test_21102025/             # Thư mục test của experiment 3
│   ├── test_22102025/             # Thư mục test của experiment 4
│   └── test_23102025/             # Thư mục test của experiment 5
│       ├── README.md              # Tài liệu mô tả experiment
│       ├── eda/                   # Thư mục Exploratory Data Analysis
│       │   └── eda01.ipynb        # Notebook phân tích dữ liệu
│       ├── model/                 # Thư mục training model
│       │   ├── train.ipynb        # Notebook train model (CORE)
│       │   └── train.html         # File HTML đãirtham khảo do train.ipynb
│       └── runs/                  # Thư mục chạy experiment
│           ├── main_23102025.ipynb # Notebook orchestrator chạy experiment
│           └── test_predictions.npy # Kết quả dự đoán
│
└── README.md                      # Tài liệu này
```

---

## 📋 Chi tiết từng thành phần

### 1. Thư mục `data/`

**Nhiệm vụ:** Lưu trữ dữ liệu gốc từ Kaggle, không được thay đổi.

**File trong thư mục:**
- `train.csv`: Dữ liệu training với 891 hành khách và có nhãn Survived
- `test.csv`: Dữ liệu test với 418 hành khách (không có nhãn)
- `gender_submission.csv`: Mẫu file submission theo format Kaggle yêu cầu

**Lưu ý:** Thư mục này chỉ đọc, không được chỉnh sửa dữ liệu gốc.

---

### 2. Thư mục `process/exps/`

**Nhiệm vụ:** Lưu trữ kết quả của các experiment theo thời gian.

**Đặc điểm:**
- Mỗi experiment có tên theo format `trainbase_<DDMMYYYY>/`
- Tách biệt kết quả các lần chạy để có thể theo dõi tiến trình
- Chứa các file kết quả đã được xử lý và model đã train

**File trong mỗi thử nghiệm:**
- `data.npz`: Dữ liệu đã được preprocess và lưu dưới dạng numpy compressed
- `*_model.pkl`: Các mô hình machine learning đã được train:
  - `logistic_regression_model.pkl`: Mô hình Logistic Regression
  - `random_forest_model.pkl`: Mô hình Random Forest
  - `xgboost_model.pkl`: Mô hình XGBoost
- `submission_*.csv`: Các file submission cho Kaggle với các phương pháp khác nhau:
  - `submission_logistic_regression.csv`
  - `submission_random_forest.csv`
  - `submission_xgboost.csv`
  - `submission_voting.csv`
  - `submission_stacking.csv`
  - `submission_blending.csv`
  - `submission_weighted.csv`
- `*_package.pkl`: Package chứa model + metadata (tên features, scaler, v.v.)
- `record.xlsx`: File Excel tổng hợp kết quả các experiment

**Workflow:**
1. Train model → lưu vào thư mục experiment
2. Tạo submission file
3. Submit lên Kaggle
4. Ghi kết quả vào `record.xlsx`

---

### 3. Thư mục `process/test_<DATE>/`

**Nhiệm vụ:** Tổ chức workflow và notebook cho mỗi experiment.

**Cấu trúc bên trong:**
```
test_<DATE>/
├── README.md          # Mô tả experiment, thay đổi, kết quả
├── eda/               # Phân tích dữ liệu
│   └──甚至   # Exploratory Data Analysis
├── model/             # Training model
│   ├── train.ipynb    # Notebook chứa code preprocessing + training
│   └── train.html     # Export HTML của train.ipynb
└── runs/              # Execution & Results
    ├── main_<DATE>.ipynb  # Notebook orchestrator
    └── test_predictions.npy # Predictions
```

#### 3.1. File `README.md`
- Mô tả experiment, mục tiêu, thay đổi so với lần trước
- Liệt kê nhật ký thay đổi (changelog)
- Ghi kết quả (accuracy, F1, ROC-AUC)
- Hướng dẫn cách chạy

#### 3.2. Thư mục `eda/`
- Lưu notebook phân tích dữ liệu (`eda01.ipynb`)
- Khám phá insights, missing values, distribution, correlation

#### 3.3. Thư mục `model/`
**File `train.ipynb` (CORE):**
- Load data từ `data/`
- Preprocessing và feature engineering
- Train các models (Logistic Regression, Random Forest, XGBoost)
- Hyperparameter tuning với GridSearchCV
- Lưu model vào `process/exps/`

**File `train.html`:** Export HTML để có thể xem mà không cần Jupyter

#### 3.4. Thư mục `runs/`
**File `main_<DATE>.ipynb`:**
- Orchestrator chạy toàn bộ workflow
- Chạy `%run ../model/train.ipynb`
- Export HTML, tạo submission file

**File `test_predictions.npy`:** Kết quả dự đoán trên test set

---

## 🔄 Workflow thực hiện experiment mới

### Bước 1: Tạo thư mục experiment
```bash
mkdir -p process/test_<DATE_NEW>
cd process/test_<DATE_NEW>
mkdir -p eda model runs
```

### Bước 2: Copy và chỉnh sửa notebook từ experiment trước
```bash
# Copy train.ipynb từ experiment trước
cp ../test_<DATE_OLD>/model/train.ipynb ./model/train.ipynb
# Copy eda01.ipynb nếu cần
cp ../test_<DATE_OLD>/eda/eda01.ipynb ./eda/eda01.ipynb
```

### Bước 3: Chỉnh sửa notebook
- Mở `model/train.ipynb` và cập nhật:
  - `exp_name`: Tên experiment mới
  - Preprocessing logic
  - Feature engineering
  - Hyperparameters

### Bước 4: Chạy experiment
```bash
# Mở Jupyter notebook
cd process/test_<DATE_NEW>/runs
jupyter notebook main_<DATE_NEW>.ipynb
```

### Bước 5: Ghi kết quả
- Cập nhật `README.md` với kết quả
- Ghi vào `process/exps/record.xlsx`

---

## 📊 Các mô hình đã implement

### 1. Logistic Regression
- Preprocessing: StandardScaler
- Hyperparameter tuning: GridSearchCV (C, penalty, solver)

### 2. Random Forest
- Preprocessing: StandardScaler (optional)
- Hyperparameter tuning: n_estimators, max_depth, min_samples_split, masamples_leaf, max_features

### 3. XGBoost
- Hyperparameter tuning: n_estimators, max_depth, learning_rate, subsample, colsample_bytree, regularization

###  Wohn tập Methods
- **Voting**: Soft voting của 3 model
- **Stacking**: Meta-learner với Logistic Regression
- **Blending**: Holdout-based blending
- **Weighted Average**: Trọng số dựa trên CV accuracy

---

## 🎯 Feature Engineering

Các features đã được tạo:

1. **Sex**: Encoding 'male'→1, 'female'→0
2. **Age**: KNN Imputer + binning (Babi, Teen, Young, Adult, Mid_Age, Old)
3. **Fare**: Binning (So_Cheap, Cheap, Medium, Expensive)
4. **Embarked**: Encoding立ち上げ→1, Q→2, S→3
5. **Name**: Trích xuất title (Mr, Miss, Mrs, Master, Dr, Others)
6. **Boy**: Flag cho nam < 16 tuổi
7. **WomanOrBoy**: Flag cho phụ nữ hoặc con trai
8. **Family_Size**: SibSp + Parch + 1
9. **IsAlone**: Flag đi một mình
10. **Family_Survival**: Dự đoán dựa trên họ và ticket

---

## 📈 Cách sử dụng

### Chạy experiment mới
```python
# 1. Mở notebook: process/test_<DATE>/runs/main_<DATE>.ipynb
# 2. Cập nhật params trong train.ipynb
# 3. Run all cells
```

### Load model đã train
```python
import joblib
import numpy as np

# Load dữ liệu đã preprocess
data = np.load('process/exps/trainbase_23102025/data.npz', allow_pickle=True)

# Load model
model = joblib.load('process/exps/trainbase_23102025/xgboost_model.pkl')

# Hoặc load package
pkg = joblib.load('process/exps/trainbase_23102025/model_package.pkl')
model = pkg['model']
```

### Tạo submission cho Kaggle
```python
# Load test data và model
predictions = model.predict(X_test)

submission = pd.DataFrame({
    'PassengerId': test_data['PassengerId'],
    'Survived': predictions
})

submission.to_csv('submission.csv', index=False)
```

---

## 🎓 Best Practices

1. ✅ Luôn lưu model và data vào thư mục `exps/` theo ngày
2. ✅ Ghi nhật ký thay đổi trong README của mỗi experiment
3. ✅ Tách notebook theo mục đích: EDA, Training, Runs
4. ✅ Use version control (git) cho code
5. ✅ Lưu dữ liệu đã preprocess để tái sử dụng
6. ✅ Tạo nhiều file submission để so sánh kết quả

---

## 📝 Ghi chú

- Mỗi experiment là độc lập, có thể chạy riêng biệt
- Có thể so sánh kết quả qua file `record.xlsx`
- Template này có thể áp dụng cho các dự án ML khác
- Cập nhật README thường xuyên để theo dõi tiến trình

---

## 👥 Thông tin nhóm

**Giảng viên:** Đỗ Như Tài  
**Sinh viên:** Trần Hồ Minh Hải, Trương Văn Thiện, Phan Đức Nhân, Võ Gia Kiệt  
**Trường:** Đại học Sài Gòn  
**Lớp:** Machine Learning 2025

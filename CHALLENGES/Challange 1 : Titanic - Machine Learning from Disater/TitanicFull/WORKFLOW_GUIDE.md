# 🚀 Hướng Dẫn Workflow Đầy Đủ

## 📋 Workflow Tổng Quan

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW TUẦN TỰ                          │
└─────────────────────────────────────────────────────────────┘

1️⃣  EXPLORATORY DATA ANALYSIS (EDA)
    ├─ File: process/test_YYYYMMDD/eda/eda01.ipynb
    ├─ Mục đích: Hiểu dữ liệu, tìm insights
    ├─ Output: Nhận xét, biểu đồ, quyết định FE
    └─ ⏱️ Thời gian: 30-60 phút (lần đầu)

2️⃣  FEATURE ENGINEERING (FE) 
    ├─ File: process/test_YYYYMMDD/model/train.ipynb
    │   └─ Function: preprocessing_feature_01()
    ├─ Mục đích: Xử lý dữ liệu dựa trên EDA
    ├─ Output: Dữ liệu đã clean và feature mới
    └─ ⏱️ Thời gian: 2-4 giờ (implement + test)

3️⃣  TRAINING & HYPERPARAMETER TUNING
    ├─ File: process/test_YYYYMMDD/model/train.ipynb
    ├─ Mục đích: Train model với GridSearchCV
    ├─ Output: Best model saved as *.pkl
    └─ ⏱️ Thời gian: 30 phút - 2 giờ (tùy model)

4️⃣  PREDICTION & SUBMISSION
    ├─ File: process/test_YYYYMMDD/runs/main_YYYYMMDD.ipynb
    ├─ Mục đích: Tạo file submission cho Kaggle
    ├─ Output: submission_*.csv
    └─ ⏱️ Thời gian: 5 phút

5️⃣  DOCUMENTATION
    ├─ File: process/test_YYYYMMDD/README.md
    ├─ Mục đích: Ghi lại thay đổi và kết quả
    └─ ⏱️ Thời gian: 10 phút
```

---

## 🎯 Chi Tiết Từng Bước

### Bước 1️⃣: EDA (Làm Đầu Tiên!)

**Câu hỏi:** Đây là lần đầu làm EDA hay copy từ trước?

#### Trường hợp A: Lần đầu làm EDA
```bash
# 1. Mở file
cd process/test_24102025/eda
jupyter notebook eda01.ipynb

# 2. Chạy các cells để khám phá:
# - Load data
# - Check missing values
# - Vẽ biểu đồ phân bố Age, Fare, ...
# - Tìm correlation
# - Đưa ra nhận xét
```

**Output:** Hiểu được:
- Age missing khoảng 20% và tương quan với Pclass
- Fare có nhiều outliers
- Sex là feature quan trọng nhất
- ...

#### Trường hợp B: Copy từ experiment trước (không cần đổi preprocessing)
```bash
# Copy EDA từ experiment cũ
cp ../test_23102025/eda/eda01.ipynb ./eda/
```

---

### Bước 2️⃣: Feature Engineering (CORE!)

**File:** `process/test_24102025/model/train.ipynb`

#### Scenario 1: Sửa Feature Cũ

**Bạn muốn:** Sửa cách binning Age từ `[-1,12,22,34,46,64,100]` sang `[-1,18,30,50,100]`

**Cách làm:**
```python
# 1. Mở train.ipynb, tìm function preprocessing_feature_01()

# 2. Tìm dòng:
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,12,22,34,46,64,100],  # ← DÒNG CŨ
                           labels=['Babi', 'Teen', 'Young', 'Adult', 'Mid_Age', 'Old'])

# 3. Sửa thành:
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,18,30,50,100],  # ← DÒNG MỚI
                           labels=['Child', 'Young', 'Adult', 'Old'])

# 4. ĐỒNG THỜI sửa biến cls_age:
cls_age = {'Child':0, 'Young':1, 'Adult':2, 'Old':3}  # ← Sửa để match labels mới
```

#### Scenario 2: Thêm Feature Mới

```python
# Thêm trong function preprocessing_feature_01()

# Thêm feature tương tác Age và Fare
df_output['Age_Fare'] = df_data['Age'] * df_data['Fare']

# Hoặc thêm feature khác
df_output['FarePerPerson'] = df_data['Fare'] / df_output['Family_Size']
```

#### Scenario 3: Xóa Feature Cũ (Comment code)

```python
# Trong preprocessing_feature_01():

# Comment dòng không muốn dùng nữa
# df_output['Boy'] = df_data.apply(is_boy_row, axis=1).astype(int)  # ← Comment

# Hoặc xóa hẳn
# df_output['WomanOrBoy'] = ((df_output["Sex"] == 0) | (df_output["Boy"])).astype(int)
```

**⚠️ QUAN TRỌNG:** Sau khi sửa, phải chạy lại TOÀN BỘ notebook!

---

### Bước 3️⃣: Training

**File:** `process/test_24102025/runs/main_24102025.ipynb`

```python
# Cell 1: Chạy train notebook
%run ../model/train.ipynb

# Cell 2: Load processed data
data = np.load('../../exps/trainbase_24102025/data.npz')

# Cell 3: Split data
X_train = df_train.drop(columns=['Output'])
y_train = df_train['Output']

# Cell 4-6: Train models (Logistic Regression, RF, XGBoost)
# ...

# Cell 7: Save best model
joblib.dump(best_model, '../../exps/trainbase_24102025/xgboost_model.pkl')
```

**Output:** Models saved trong `exps/trainbase_24102025/`

---

### Bước 4️⃣: Submission

```python
# Predict on test set
test_preds = best_model.predict(X_test)

# Create submission file
submission = pd.DataFrame({
    "PassengerId": test_data["PassengerId"],
    "Survived": test_preds
})

submission.to_csv('../../exps/trainbase_24102025/submission_xgboost.csv', 
                  index=False)
```

**Upload lên Kaggle để xem kết quả!**

---

### Bước 5️⃣: Ghi lại kết quả

**File:** `process/test_24102025/README.md`

```markdown
# Experiment ngày 24/10/2025

## Thay đổi:
- Sửa Age binning: [-1,12,22,34,46,64,100] → [-1,18,30,50,100]
- Thêm feature Age_Fare
- Loại bỏ Boy feature

## Kết quả:
- Logistic Regression: 0.8619 (baseline)
- Random Forest: 0.8664
- XGBoost: 0.8700 ⭐ Best
- Kaggle Score: 0.78468
```

---

## ⚡ Quick Reference

### "Tôi muốn sửa Feature Engineering, làm sao?"

1. Mở: `process/test_24102025/model/train.ipynb`
2. Tìm: Function `preprocessing_feature_01()`
3. Sửa: Code preprocessing
4. Desert: Chạy lại TOÀN BỘ notebook
5. Check: Kết quả trong `exps/trainbase_24102025/`

### "EDA là gì? Cần làm khi nào?"

- EDA = Exploratory Data Analysis
- Làm TRƯỚC khi train
- Mục đích: Hiểu dữ liệu để quyết định FE
- Nếu không đổi preprocessing → Copy từ experiment trước

### "Workflow thế nào?"

```
EDA → FE → Training → Submission → Documentation
```

### "Làm experiment mới như thế nào?"

```bash
# 1. Tạo thư mục
mkdir process/test_24102025/{eda,model,runs}

# 2. Copy train.ipynb từ experiment trước
cp process/test_23102025/model/train.ipynb process/test_24102025/model/

# 3. Sửa preprocessing trong train.ipynb

# 4. Chạy main notebook
cd process/test_24102025/runs
jupyter notebook main_24102025.ipynb
```

---

## 📝 Checklist Mỗi Experiment

- [ ] Tạo thư mục mới
- [ ] Copy code từ experiment trước
- [ ] Sửa config (exp_name, exp_dir)
- [ ] Sửa preprocessing nếu cần
- [ ] Chạy train notebook
- [ ] Train models (LR, RF, XGBoost)
- [ ] Tạo submission files
- [ ] Upload lên Kaggle
- [ ] Update README.md
- [ ] Update record.xlsx

---

## 🎓 Best Practices

✅ **DO:**
- Làm EDA kỹ lần đầu
- Sửa FE trong `preprocessing_feature_01()`
- Luôn chạy lại toàn bộ notebook sau khi sửa
- Ghi nhật ký trong README
- So sánh kết quả với experiment trước

❌ **DON'T:**
- Không sửa dữ liệu trong `data/` folder
- Không bỏ qua EDA lần đầu
- Không quên chạy lại sau khi sửa FE
- Không skip documentation

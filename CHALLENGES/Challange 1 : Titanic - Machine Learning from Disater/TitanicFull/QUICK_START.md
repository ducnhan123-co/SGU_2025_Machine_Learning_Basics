# 🚀 Quick Start Guide - Titanic ML Template

## Mục đích
Tạo một **experiment mới** để test thử preprocessing hoặc model mới.

## ⚡ Bước nhanh (5 phút)

### 1️⃣ Tạo thư mục mới
```bash
# Tạo thư mục ngày hôm nay (ví dụ: 24/10/2025)
mkdir -p process/test_24102025/{eda,model,runs}
```

### 2️⃣ Copy notebook từ experiment trước
```bash
# Copy từ experiment tốt nhất trước đó
cp process/test_23102025/model/train.ipynb process/test_24102025/model/
cp process/test_23102025/eda/eda01.ipynb process/test_24102025/eda/  # Tùy chọn
```

### 3️⃣ Tạo file orchestrator
```bash
# Tạo file main_24102025.ipynb trong thư mục runs
```

### 4️⃣ Chỉnh sửa config trong train.ipynb

Mở `process/test_24102025/model/train.ipynb` và tìm phần config (Cell 2):

```python
params_cfg = {
    "action"   : "train_feat03",  
    "feat_path": "../../exps/featbase_24102025/data.npz",  # ← Đổi tên
    "seed"     : 42,
    "exp_dir"  : os.path.abspath('../../exps'),
    'exp_name' : 'trainbase_24102025',  # ← Đổi tên
    "data_dir" : os.path.abspath("../../../data"),
    "verbose"  : True,
}
```

### 5️⃣ Chạy experiment
```bash
cd process/test_24102025/runs
jupyter notebook main_24102025.ipynb
```

---

## 📝 Template main_<DATE>.ipynb

Copy vào file `process/test_24102025/runs/main_24102025.ipynb`:

```python
# Cell 1: Import
from IPython import display

# Cell 2: Clear output (optional)
display.clear_output()

# Cell 3: Run train notebook
%run ../model/train.ipynb

# Cell 4: Export HTML (optional)
!jupyter nbconvert ../model/train.ipynb --to html

# Cell 5: Load data và train model
# (Copy code từ test_23102025/runs/main_23102025.ipynb)
```

---

## 🎯 Các thay đổi thường gặp

### Thay đổi preprocessing
Sửa function `preprocessing_feature_01()` trong `train.ipynb`:

```python
def preprocessing_feature_01(df_data, is_train=True, is_debug=True, **kwargs):
    df_output = pd.DataFrame()
    
    # Thêm features mới ở đây
    # Ví dụ: df_output['new_feature'] = ...
    
    return df_output, None
```

### Thay đổi hyperparameters
Tìm param_grid trong cell training và chỉnh sửa:

```python
param_grid = {
    'logreg__C': [0.1, 1, 10],  # Thêm/bớt values
    'logreg__penalty': ['l2'],   # Chỉ test l2
}
```

### Thay đổi model
Thêm/sửa model trong `train.ipynb`:

```python
from sklearn.ensemble import GradientBoostingClassifier

pipeline_gb = Pipeline([
    ('scaler', StandardScaler()),
    ('gb', GradientBoostingClassifier(random_state=42))
])
```

---

## 📊 Xem kết quả

### 1. Submission files
Kiểm tra trong: `process/exps/trainbase_24102025/`
- `submission_xgboost.csv`
- `submission_voting.csv`
- etc.

### 2. Model files
- `xgboost_model.pkl`: Model tốt nhất
- `data.npz`: Dữ liệu đã preprocess

### 3. So sánh với experiment trước
```bash
# Xem record
cat process/exps/record.xlsx

# Hoặc xem README của từng experiment
cat process/test_24102025/README.md
```

---

## 💡 Tips

1. **Tên experiment:**
   - Format: `trainbase_<DDMMYYYY>`
   - Ví dụ: `trainbase_24102025`

2. **Backup:**
   - Commit code vào git trước khi chạy
   - Giữ lại file notebook của experiment tốt nhất

3. **Debug:**
   - Set `"verbose": True` trong config để in thông tin
   - Set `is_debug=True` trong `preprocessing_feature_01()`

4. **Nhanh hơn:**
   - Giảm GridSearchCV param_grid khi test nhanh
   - Chỉ train 1 model khi test preprocessing

---

## 🐛 Troubleshooting

### Lỗi: File not found
```python
# Kiểm tra đường dẫn relative
print(os.getcwd())  # Current working directory
print(os.path.abspath('../../../data'))  # Check path
```

### Lỗi: Model chưa train
```python
# Kiểm tra xem model đã fit chưa
print(hasattr(model, 'feature_importances_'))
```

### Lỗi: Memory issue
- Giảm param_grid size
- Tăng `n_jobs` trong GridSearchCV
- Xóa output cells cũ trong notebook

---

## 📚 Next Steps

1. **Improve feature engineering** → Edit `preprocessing_feature_01()`
2. **Try different models** → Add new model cells
3. **Ensemble methods** → Implement voting/stacking/blending
4. **Submit to Kaggle** → Upload `submission_*.csv`
5. **Document results** → Update README.md

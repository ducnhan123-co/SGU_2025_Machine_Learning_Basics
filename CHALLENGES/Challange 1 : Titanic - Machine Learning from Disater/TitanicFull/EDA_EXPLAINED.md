# 🔍 EDA Là Gì? Và Làm Khi Nào?

## EDA = Exploratory Data Analysis (Phân tích khám phá dữ liệu)

### ❓ EDA làm gì?
- Khám phá dữ liệu để hiểu nó
- Tìm missing values, outliers
- Vẽ biểu đồ phân bố
- Tìm correlation giữa features
- Đưa ra nhận xét để quyết định **feature engineering**

### 📅 Khi nào làm EDA?
**LÀM TRƯỚC KHI TRAIN!** ⚠️

```
Workflow ĐÚNG:
1. EDA (eda01.ipynb) → Hiểu dữ liệu
2. Feature Engineering → Tạo features dựa trên EDA
3. Train model → Train với features đã xử lý
4. Submit → Nộp kết quả
```

---

## 🎯 Ví dụ cụ thể

### Bước 1: EDA - Khám phá
File: `eda/eda01.ipynb`

```python
# Ví dụ: EDA phát hiện ra:
# - Age có nhiều missing values
# - Age tương quan với Pclass
# → Quyết định: Dùng KNN Imputer với Pclass làm reference
```

### Bước 2: Feature Engineering
File: `model/train.ipynb` → Function `preprocessing_feature_01()`

```python
def preprocessing_feature_01(df_data, is_train=True, is_debug=True, **kwargs):
    # Implement các xử lý dựa trên EDA
    df_output["Age"] = impute_age_knn(df_data)["Age"]  # ← Logic từ EDA
    df_output['Age'] = pd.cut(df_output['Age'], bins=[-1,12,22,34,46,64,100], ...)
    # ...
    return df_output
```

---

## ❌ Làm Sai ❌

❌ Không làm EDA → Thiếu cơ sở để quyết định xử lý dữ liệu  
❌ EDA sau khi train → Vô nghĩa vì đã train rồi  
❌ Không hiểu EDA → Không biết vì sao làm preprocessing như vậy

---

## ✅ Workflow Đúng Cho Dự Án Này

### Experiment lần đầu (test_18102025):
```
1. Mở eda/eda01.ipynb → Load data, vẽ biểu đồ, phân tích
2. Từ EDA → Phát hiện insights
3. Tạo train.ipynb → Implement preprocessing dựa trên EDA
4. Train model → Kiểm tra kết quả
```

### Experiment tiếp theo (test_20102025):
```
1. Copy eda từ experiment trước (nếu muốn giữ insights cũ)
2. HOẶC tạo EDA mới nếu muốn test các phát hiện khác
3. Sửa train.ipynb → Thêm/sửa preprocessing
4. Train lại
```

---

## 💡 Câu hỏi hay của bạn

### Q: "Nếu đã làm EDA rồi, experiment sau có cần làm lại không?"
**A:** Tùy vào mục đích:
- Nếu không đổi cách xử lý dữ liệu → Không cần
- Nếu muốn thử cách xử lý khác → Nên làm EDA lại
- Copy eda01.ipynb từ experiment trước nếu không đổi

### Q: "Feature engineering nằm đâu? Sửa như thế nào?"
**A:** Trong `model/train.ipynb`, function `preprocessing_feature_01()`

**Cách sửa:**

```python
# Trong file train.ipynb, tìm function preprocessing_feature_01()

def preprocessing_feature_01(df_data, is_train=True, is_debug=True, **kwargs):
    df_output = pd.DataFrame()
    
    # 1. GIỮ NGUYÊN các feature cũ (nếu muốn)
    df_output["Sex"] = df_data["Sex"].apply(lambda x: cls_sex[x])
    
    # 2. SỬA feature cũ
    # THAY VÌ:
    # df_output['Age'] = pd.cut(..., bins=[-1,12,22,34,46,64,100], ...)
    # THÌ SỬA THÀNH:
    df_output['Age'] = pd.cut(..., bins=[-1,10,20,30,50,70,100], ...)
    
    # 3. THÊM feature mới
    df_output['Age_Fare'] = df_data['Age'] * df_data['Fare']  # ← Thêm mới
    
    return df_output
```

Sau đó chạy lại toàn bộ cell trong `train.ipynb`!

---

## 📖 Ví dụ: Sửa Feature Engineering

### Scenario: Muốn thử binning Age khác đi

**Trong train.ipynb, tìm đến cell chứa:**

```python
# CŨ - Cell này đã bị comment hoặc xóa
# df_output['Age'] = pd.cut(df_output['Age'], 
#                            bins=[-1,12,22,34,46,64,100], 
#                            labels=['Babi', 'Teen', 'Young', 'Adult', 'Mid_Age', 'Old'])
```

**Sửa thành:**

```python
# MỚI - Thử binning khác
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,18,30,50,100],  # ← Sửa bins
                           labels=['Child', 'Young', 'Adult', 'Old'])  # ← Sửa labels
```

**Sau đó chạy lại toàn bộ notebook từ đầu!**

---

## 🎓 Tips

1. **EDA đầu tiên** → Làm kỹ, tìm nhiều insights
2. **Experiment sau** → Copy EDA nếu không đổi gì
3. **Sửa FE** → Sửa trong `preprocessing_feature_01()`
4. **Luôn chạy lại** → Khi sửa preprocessing, phải run all cells
5. **Ghi nhận xét** → Trong README.md, viết "Đã sửa Age binning..."

---

## 📝 Template cho README.md

```markdown
## Experiment ngày 24/10/2025

### Thay đổi so với lần trước:
- Sửa Age binning: [12,22,34] → [18,30,50]
- Thêm feature: Age_Fare = Age * Fare
- Loại bỏ: Boy feature (không cải thiện)

### Kết quả:
- XGBoost: 0.8664 → 0.8700 (↑0.36%)
```

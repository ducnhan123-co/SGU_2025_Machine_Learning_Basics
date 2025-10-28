# 🔧 Ví dụ Cụ Thể: Sửa Feature Engineering

## ❓ Câu Hỏi Thường Gặp

### Q: "Làm sao để sửa lại khi xử lý cái mới? Comment lại rồi chạy lại model hay sao?"

**A:** Đúng rồi! Bạn comment hoặc sửa code, rồi chạy lại TOÀN BỘ notebook.

---

## 📝 Ví Dụ 1: Sửa Age Binning

### Mục đích:
Từ binning cũ `[-1,12,22,34,46,64,100]` thành `[-1,18,35,60,100]`

### Bước 1: Mở file train.ipynb
```bash
cd process/test_24102025/model
jupyter notebook train.ipynb
```

### Bước 2: Tìm function preprocessing_feature_01()

Scroll xuống đến dòng khoảng 2216-2217 (trong code hiện tại):

```python
# CŨ - Dòng này cần sửa:
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,12,22,34,46,64,100], 
                           labels=['Babi', 'Teen', 'Young', 'Adult', 'Mid_Age', 'Old'])
```

### Bước 3: Sửa code

**Option A: Comment và viết mới (Khuyên dùng)**
```python
# OLD - Comment để giữ lại reference
# df_output['Age'] = pd.cut(df_output['Age'], 
#                            bins=[-1,12,22,34,46,64,100], 
#                            labels=['Babi', 'Teen', 'Young', 'Adult', 'Mid_Age', 'Old'])

# NEW - Binning mới
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,18,35,60,100],  # ← Đổi bins
                           labels=['Young', 'Adult', 'Middle', 'Senior'])  # ← Đổi labels
```

**Option B: Sửa trực tiếp**
```python
# Sửa thành:
df_output['Age'] = pd.cut(df_output['Age'], 
                           bins=[-1,18,35,60,100],
                           labels=['Young', 'Adult', 'Middle', 'Senior'])
```

### Bước 4: Đồng thời sửa biến cls_age

Tìm đến khoảng dòng 26 (sau khi define cls_sex):

```python
# CŨ:
cls_age = {'Babi':0, 'Teen':1, 'Young':2, 'Adult':3, 'Mid_Age':4, 'Old':5}

# MỚI - Phải match với labels mới:
cls_age = {'Young':0, 'Adult':1, 'Middle':2, 'Senior':3}
```

### Bước 5: Chạy lại TOÀN BỘ notebook!

Trong Jupyter:
- Click **"Kernel"** → **"Restart & Run All"**
- HOẶC chạy từng cell từ đầu

### Bước 6: Kiểm tra kết quả

```python
# Trong notebook, check:
print("Columns:", df_output.columns.tolist())
print("Shape:", df_output.shape)

# Kiểm tra有沒有 các cột Age_Young, Age_Adult, Age_Middle, Age_Senior
```

---

## 📝 Ví Dụ 2: Thêm Feature Mới

### Mục đích:
Thêm feature `Age_Fare = Age * Fare`

### Bước 1-2: Như trên

### Bước 3: Thêm code trong preprocessing_feature_01()

Tìm cuối function, trước dòng `if is_train:`:

```python
# Thêm feature mới ở đây:
df_output['Age_Fare'] = df_data['Age'] * df_data['Fare']

# HOẶC thêm feature khác:
df_output['FarePerPerson'] = df_data['Fare'] / df_output['Family_Size']
df_output['IsRich'] = (df_data['Fare'] > 100).astype(int)
```

**Lưu ý:** Đảm bảo `df_data['Age']` đã được fillna() trước đó!

### Bước 4-6: Chạy lại và kiểm tra

---

## 📝 Ví Dụ 3: Loại Bỏ Feature

### Mục đích:
Bỏ feature `Boy` (không cải thiện accuracy)

### Bước 1-2: Như trên

### Bước 3: Comment hoặc xóa code

```python
# Trong preprocessing_feature_01(), tìm:

# COMMENT dòng này:
# df_output['Boy'] = df_data.apply(is_boy_row, axis=1).astype(int)

# VÀ comment feature WomanOrBoy cũng (vì phụ thuộc Boy):
# df_output['WomanOrBoy'] = ((df_output["Sex"] == 0) | (df_output["Boy"])).astype(int)

# NẾU vẫn muốn WomanOrBoy, sửa thành:
df_output['WomanOrBoy'] = (df_output["Sex"] == 0).astype(int)  # Chỉ phụ nữ
```

### Bước 4-6: Chạy lại và kiểm tra

---

## 📝 Ví Dụ 4: Kết Hợp Nhiều Thay Đổi

### Mục đích:
- Sửa Age binning
- Thêm feature mới
- Bỏ feature không quan trọng

### Code hoàn chỉnh:

```python
def preprocessing_feature_01(df_data, is_train=True, is_debug=True, **kwargs):
    df_output = pd.DataFrame()
    
    # 1. SEX - Không đổi
    df_output["Sex"] = df_data["Sex"].apply(lambda x: cls_sex[x])
    
    # 2. AGE - SỬA binning
    df_data["Age"] = impute_age_knn(df_data)["Age"]
    # CŨ: bins=[-1,12,22,34,46,64,100]
    # MỚI:
    df_output['Age'] = pd.cut(df_data['Age'], 
                               bins=[-1,18,35,60,100], 
                               labels=['Young', 'Adult', 'Middle', 'Senior']).apply(lambda x: cls_age[x])
    
    # 3. FARE - Giữ nguyên
    df_data['Fare'] = df_data['Fare'].fillna(df_data['Fare'].median())
    df_output['Fare'] = pd.cut(df_data['Fare'], bins=[-1,40,80,200,1000], labels=['So_Cheap', 'Cheap', 'Medium', 'Expensive']).apply(lambda x: cls_fare[x])
    
    # 4. PCLASS - Giữ nguyên
    for name in ['Pclass', 'SibSp', 'Parch', 'PassengerId']:
        df_output[name] = df_data[name]
    
    # 5. EMBARKED - Giữ nguyên
    cls_embarked = {'C':1, 'Q':2, 'S':3}
    df_output['Embarked'] = df_data['Embarked'].fillna(df_data['Embarked'].mode()[0]).apply(lambda x: cls_embarked[x])
    
    # 6. NAME - Giữ nguyên
    df_output['Name'] = df_data['Name'].apply(lambda x: cls_name[extract_name(x)] if extract_name(x) in top_5_title else cls_name['Others'])
    
    # 7. BOY - BỎ (comment)
    # df_output['Boy'] = df_data.apply(is_boy_row, axis=1).astype(int)
    
    # 8. WOMAN OR BOY - SỬA (chỉ còn phụ nữ)
    df_output['Woman'] = (df_output["Sex"] == 0).astype(int)  # Sửa tên thành Woman
    
    # 9. FAMILY SIZE - Giữ nguyên
    df_output['Family_Size'] = df_data['SibSp'] + df_data['Parch'] + 1
    
    # 10. IS ALONE - Giữ nguyên
    df_output['IsAlone'] = (df_output['Family_Size'] == 1).astype(int)
    
    # 11. FAMILY SURVIVAL - Giữ nguyên
    df_data["Last_Name"] = df_data["Name"].str.split(",").str[0]
    df_output['Family_Survival'] = df_data.apply(infer_family_survival, axis=1)
    
    # 12. THÊM FEATURES MỚI:
    df_output['Age_Fare'] = df_data['Age'] * df_data['Fare']
    df_output['FarePerPerson'] = df_data['Fare'] / df_output['Family_Size']
    df_output['IsRich'] = (df_data['Fare'] > 100).astype(int)
    
    # 13. Drop các cột không cần thiết
    drop_cols = ['SibSp', 'Parch', 'Embarked']
    for col in drop_cols:
        if col in df_output.columns:
            df_output = df_output.drop(col, axis=1)
    
    # 14. Dummies
    dummies_col = ['Name', 'Fare', 'Age']
    df_dummies = df_output.copy()
    for col in dummies_col:
        dummies = pd.get_dummies(df_output[col], prefix=col, drop_first=True).astype(int)
        df_dummies = df_dummies.drop(col, axis=1)
        df_dummies = pd.concat([df_dummies, dummies], axis=1)
    df_output = df_dummies
    
    if is_train:
        df_output["Output"] = df_data["Survived"]
    
    if is_debug:
        print("Columns:", df_output.columns.tolist())
        print("Shape:", df_output.shape)
    
    return df_output, None
```

### Đồng thời cập nhật biến cls_age ở đầu notebook:

```python
# CŨ:
# cls_age = {'Babi':0, 'Teen':1, 'Young':2, 'Adult':3, 'Mid_Age':4, 'Old':5}

# MỚI:
cls_age = {'Young':0, 'Adult':1, 'Middle':2, 'Senior':3}
```

---

## ⚙️ Workflow Hoàn Chỉnh

```
1. Mở train.ipynb
2. Sửa preprocessing_feature_01()
3. Sửa các biến define (cls_age, etc.)
4. "Restart & Run All" trong Jupyter
5. Kiểm tra output columns
6. Train models
7. So sánh kết quả với experiment trước
```

---

## 🎯 Tips

### ✅ Best Practices:
1. **Comment code cũ** → Giữ lại để reference
2. **Sửa nhiều chỗ cùng lúc** → Cần sửa cả cls_age khi sửa Age
3. **Chạy lại từ đầu** → Restart & Run All
4. **Kiểm tra columns** → Print ra xem có đúng không
5. **So sánh kết quả** → Ghi vào README

### ❌ Common Mistakes:
1. Sửa binning nhưng quên sửa cls_age
2. Thêm feature nhưng quên handle missing values
3. Không chạy lại notebook sau khi sửa
4. Sửa thiếu chỗ (ví dụ: sửa Age nhưng quên binning)
5. Không test trước khi submit

---

## 📊 Checklist

Khi sửa Feature Engineering:

- [ ] Đã comment code cũ để giữ reference
- [ ] Đã cập nhật toàn bộ code liên quan (cls_age, etc.)
- [ ] Đã handle missing values cho features mới
- [ ] Đã restart & run all notebook
- [ ] Đã kiểm tra columns output
- [ ] Đã train lại models
- [ ] Đã ghi kết quả vào README
- [ ] Đã so sánh với experiment trước

# 📊 No-Code Database Manager (Streamlit + MySQL)

The **No-Code Database Manager** is a web-based tool built with **Streamlit** that allows users to interact with MySQL databases using Excel files — all **without writing any code**. It’s perfect for non-technical users, analysts, and teams who need a clean, user-friendly way to manage data.

---

## 🚀 Key Features

- 📁 **Upload Excel File** and store data as:
  - A new table in an existing database
  - A new table in a new database
  - New columns in an existing table
- 📝 **Edit and update** rows of existing tables
- 🧹 **Delete** tables or entire databases safely
- 🧭 Clean **sidebar navigation** (Store / Edit / Update / Delete)
- ✅ Real-time feedback (success & warning messages)
- 🔄 Automatic UI refresh after every operation
- 🖼️ Live preview of uploaded Excel file
- 🛡️ All operations are validated and error-handled

---

## 🖼️ Screenshots

| Upload Excel & Store | Edit Table Rows |
|----------------------|------------------|
| ![Upload Screenshot](screenshot/Screenshot1.png) | ![Edit Screenshot](screenshot/Screenshot2.png) |

| Append Columns | Delete Table or Database |
|----------------|---------------------------|
| ![Append Screenshot](screenshot/Screenshot3.png) | ![Delete Screenshot](screenshot/Screenshot4.png) |







---

## ⚙️ Setup Instructions

### 🔧 1. Clone the Project

```bash
git clone https://github.com/your-username/no-code-db-manager.git
cd no-code-db-manager

```



### 📦 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 🛠️ 3. MySQL Setup
```bash
Start MySQL via XAMPP or your preferred method.
Default credentials:
host: localhost
user: root
password: "" (empty)
port: 3308 (or 3306 depending on your setup)

```

### 4.▶️ Running the App
```bash
streamlit run app.py
```





# 📊 Big Data Final Exercise

## 👨‍💻 Authors
- **Daniel Avraham**
- **Tomer Avrahami**

## 📂 Project Overview
This project focuses on analyzing **bike rental data in London**, utilizing **DuckDB and SQLite** for data processing and **Streamlit** for visualization. The dataset contains **over 1 million rows and 12 columns**, extracted from [this Kaggle dataset](https://www.kaggle.com/datasets/ajohrn/bikeshare-usage-in-london-and-taipei-network).

## 🚀 Project Structure
### **Python Scripts**
- **`createDuckDBfile.py`** – Loads `london.csv` into DuckDB and creates a database.
- **`QuestionsUsingDuckDB.py`** – Runs queries on the DuckDB dataset and creates summarized tables.
- **`DuckDBtoSQLite.py`** – Converts processed DuckDB tables to SQLite.
- **`app.py`** – A Streamlit dashboard for visualizing rental trends.

### **Data Files**
- **`large_db.duckdb`** – The full dataset in DuckDB format.
- **`db_file.sqlite`** – The processed dataset in SQLite format.
- **`londonSample.csv`** – A 500-row sample for reference.

### **Dependencies**
All required dependencies are listed in `requirements.txt`:
```sh
pip install duckdb sqlite3 pandas streamlit matplotlib plotly
```

## 🛠 How to Run
1. **Setup Environment**
   ```sh
   pip install -r requirements.txt
   ```

2. **Generate DuckDB File** (Only if missing)
   ```sh
   python createDuckDBfile.py
   ```

3. **Process Queries and Create Summary Tables**
   ```sh
   python QuestionsUsingDuckDB.py
   ```

4. **Convert to SQLite**
   ```sh
   python DuckDBtoSQLite.py
   ```

5. **Run Streamlit Dashboard**
   ```sh
   streamlit run app.py
   ```

## 📊 Analysis & Key Insights
### 🔥 **Key Queries (From `QuestionsUsingDuckDB.py`)**
- **Busiest Rental Hours** → Determines peak rental times.
- **Most Popular Stations** → Identifies high-demand rental stations.
- **Average Trip Duration Per Day** → Analyzes weekday vs. weekend usage.
- **Most Traveled Station Pairs** → Detects frequent station-to-station trips.
- **Most Used Bikes** → Tracks the most frequently rented bikes.

## 📈 Dashboard Overview (`app.py`)
- **🚴 Rentals by Hour** – Interactive bar chart with filtering options.
- **📍 Popular Stations** – Pie chart of top rental stations.
- **⏳ Trip Duration Analysis** – Bar chart comparing trip duration by weekday.
- **🔄 Station-to-Station Analysis** – Dropdown for searching station pairs.
- **🚲 Bike Usage Tracker** – Lookup for trips by bike ID.

## 🔧 Known Issues & Future Improvements
- [ ] Optimize performance for large dataset processing.
- [ ] Improve dashboard interactivity with more filtering options.
- [ ] Enhance SQLite storage for faster retrieval.

## 📜 License
This project is for academic purposes. Unauthorized copying, distribution, and modification are prohibited.

## 📧 Contact
For any inquiries, please contact **Daniel Avraham** or **Tomer Avrahami** via GitHub or email.

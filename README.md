
# 🍲 Local Food Wastage Management System

A Streamlit web application for efficiently managing food surplus donations and reducing food waste in local communities.

## 📌 Features

- View available food listings from local providers.
- Filter listings by city, provider type, or meal type.
- Analyze data with 10+ insightful SQL dashboards.
- Identify most active providers and receivers.
- See unclaimed food listings and food type summaries.

## 🚀 Live Demo

👉 [Hosted on Streamlit Cloud](https://share.streamlit.io/YOUR_USERNAME/food-waste-management/main/app.py)

> *(Replace the above link after deployment)*

---

## 🗂️ Dataset Overview

This app uses 4 CSV datasets:

- `providers_data.csv`: Information about food providers.
- `receivers_data.csv`: Registered receivers (NGOs, shelters).
- `food_listings_data.csv`: Food listing details.
- `claims_data.csv`: Claims made by receivers for food.

---

## ⚙️ Technologies Used

- **Python 3**
- **SQLite**
- **Pandas**
- **Streamlit** – Web app framework
- **SQL** – For data insights

---

## 🔧 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/food-waste-management.git
   cd food-waste-management
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 📊 SQL Insights Included

- Providers per city
- Provider type analysis
- Most claimed food types
- Active receivers ranking
- Listings per provider
- Unclaimed food items
- Quantity by food type
- Receiver distribution by city
- Provider contribution counts
- Most common meal types

---

## 🤝 Contributing

Feel free to fork this project and submit PRs to improve features or add visualizations!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

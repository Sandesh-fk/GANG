
# 🧬 Gene Expression Explorer

This project is a web-based tool for analyzing gene expression data using datasets from NCBI's GEO repository. It enables users to query gene expression across healthy vs. disease samples, visualize expression differences, and compute statistical significance.

---

## ✅ Features

- Load real GEO datasets using GEOparse
- Perform differential expression analysis (t-test)
- Query expression of specific genes
- Frontend built with React
- Backend API powered by Flask

---

## ✅ How to Set Up the Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gene-expression-explorer.git
cd gene-expression-explorer
```

### 2. Backend Setup (Python)

Install dependencies:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `requirements.txt` file with the following:

```txt
flask
pandas
scipy
geoparse
```

---

## ✅ How to Run the Project

### Backend

```bash
cd backend
python app.py
```

The Flask server will start at `http://localhost:5000`.

### Frontend

Make sure Node.js and npm are installed.

```bash
cd frontend
npm install
npm start
```

The React app will start at `http://localhost:3000`.

---

## ✅ Usage

- Open the frontend in your browser at `http://localhost:3000`
- Enter a gene name (e.g., `TP53`)
- Submit to view statistical analysis results including:
  - Mean expression in each group
  - t-statistic
  - p-value

---

## 📁 Dataset Used

Example dataset: `GSE183947` from NCBI GEO (can be changed in the backend code).

---

## 📌 Notes

- The backend performs a t-test on gene expression between simulated "disease" and "control" groups.
- You can modify the dataset or improve grouping logic using metadata.

---

## 📬 Contributions Welcome

Feel free to fork, improve, and submit pull requests!

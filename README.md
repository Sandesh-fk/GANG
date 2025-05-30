# Gene Expression Explorer

A simple web application to analyze GEO gene expression datasets for differential expression between two sample groups.

## Features
- Fetch GEO dataset via GEOparse
- Compute differentially expressed genes using t-test
- Simple Flask backend with JSON API
- Frontend with HTML, CSS, and JavaScript for user interaction

## Project Structure
```
.
├── backend/
│   ├── app.py
│   ├── geo_analysis.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```

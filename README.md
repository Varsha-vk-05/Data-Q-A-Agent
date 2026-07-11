# 📊 DataInsight AI – Intelligent CSV & Excel Data Q&A Agent

An AI-powered Data Q&A Agent that enables users to ask plain-English questions about structured datasets and receive accurate, computation-based answers. Instead of generating speculative responses, the agent performs real data analysis using Python and pandas to produce reliable insights supported by tables and calculations.

---

## 🚀 Overview

DataInsight AI is designed to bridge the gap between natural language and data analytics. Users can upload a CSV or Excel dataset, ask questions in plain English, and receive precise answers computed directly from the dataset.

Unlike traditional chatbots that may hallucinate numerical values, this agent performs deterministic computations using Python and pandas, ensuring every answer is backed by actual data.

---

## ✨ Features

- 📁 Upload CSV and Excel datasets
- 💬 Ask questions in natural language
- 📈 Perform real-time data analysis using pandas
- 📊 Display supporting tables behind every answer
- 📉 Generate accurate aggregations, trends, and statistical insights
- ✅ Eliminates hallucinated numerical responses through deterministic computation
- ⚡ Fast, lightweight, and easy to extend for different datasets

---

## 🛠 Tech Stack

- Python
- Pandas
- OpenPyXL
- Streamlit *(or replace with Command Line Interface if applicable)*
- VS Code

---

## 📂 Project Structure

```
DataInsight-AI/
│
├── app.py
├── compute_qa.py
├── sample_sales_data.csv
├── requirements.txt
├── README.md
├── screenshots/
│   ├── home.png
│   ├── output.png
│   └── tables.png
└── assets/
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/DataInsight-AI.git
```

Navigate into the project

```bash
cd DataInsight-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

*(Replace with your run command if you're not using Streamlit.)*

---

## 📊 Sample Dataset

The project includes a sample sales dataset containing transactional information such as:

- Date
- Region
- Product Category
- Sales Revenue
- Units Sold
- Profit

The dataset demonstrates the agent's ability to answer business intelligence and analytics questions.

---

## 💡 Example Questions

- What is the total sales revenue?
- Which region generated the highest profit?
- Which product category sold the most units?
- What is the average profit margin for Electronics?
- Which region experienced the highest growth last quarter?
- How many Furniture units were sold in the East region?
- Show the monthly sales trend for the West region.
- Which transaction generated the highest profit?

---

## 📈 Example Output

**Question**

> Which region had the highest total profit?

**Answer**

```
North Region
Total Profit: $26,650
```

Supporting Table

| Region | Profit |
|---------|--------|
| North | 26650 |
| West | 22175 |
| South | 21725 |
| East | 20725 |

---

## 🧠 How It Works

1. Load the uploaded CSV or Excel dataset into a pandas DataFrame.
2. Interpret the user's natural language question.
3. Translate the request into the appropriate data operation.
4. Execute computations such as filtering, grouping, aggregation, trend analysis, or statistical calculations.
5. Return the computed answer along with the supporting table or figure.

Every numerical response is generated programmatically rather than guessed by the language model.

---

## ✅ Preventing Hallucinations

To ensure factual accuracy, the language model is used only for understanding user intent. All numerical values, summaries, and statistics are computed directly from the dataset using pandas operations such as:

- groupby()
- sum()
- mean()
- count()
- boolean filtering
- sorting
- percentage calculations

This approach guarantees that every answer is reproducible and grounded in the source data.

---

## 📷 Screenshots

<img width="1900" height="907" alt="Screenshot 2026-07-11 121740" src="https://github.com/user-attachments/assets/59f70653-319d-487e-bd8a-6c599ac29e2e" />

---

<img width="1901" height="918" alt="Screenshot 2026-07-11 121802" src="https://github.com/user-attachments/assets/548b7435-ef90-45e8-917a-f599c92acae5" />


---

## 🔍 Design Decisions

- Python was selected for its rich data analysis ecosystem.
- Pandas provides efficient and transparent data processing.
- The application prioritizes correctness over generative responses.
- Supporting tables are displayed alongside every answer to improve transparency.

---

## ⚖️ Tradeoffs

Current limitations include:

- Optimized for structured tabular datasets.
- Requires meaningful column names for best results.
- Does not currently support unstructured documents.
- Large datasets may require additional optimization.

---

## 🚀 Future Enhancements

- Interactive visualizations
- SQL database integration
- Multi-file analytics
- Automated chart generation
- Voice-based querying
- PDF report generation
- Export answers to Excel and PDF

---

## 👩‍💻 Author

**Varsha S**

Computer Science Graduate | Software Developer | Android AppLication Developer | Full stack developer

GitHub: https://github.com/Varsha-vk-05

---

## 📄 License

This project is developed for educational and research purposes as part of an AI Agent Challenge.

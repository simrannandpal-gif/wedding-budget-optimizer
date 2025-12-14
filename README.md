# Wedding Budget Optimizer 💍
## 🌐 Live Interactive App

You can explore the Wedding Budget Optimizer using the live Streamlit app below:

👉 **Live Demo:**  
https://wedding-budget-optimizer-simran.streamlit.app/

**What you can try in the app:**
- Adjust the total wedding budget
- See how spending changes across categories
- Observe how high-impact items like photography are protected
- Understand where cost cuts cause the least regret


A Streamlit app that helps couples decide how to spend their wedding budget and where to cut costs when money is tight.

Instead of cutting randomly, the app protects high-value memories like photography and makeup, and reduces spending on lower-impact categories such as decor or DJ first.

---

## What Problem Does This Solve?

Wedding planning is stressful, especially when the budget changes.

When couples reduce their budget, they often don’t know:
- Which category to cut
- How much quality they will lose
- Whether their money is being spent wisely

This app solves that problem by automatically suggesting the best spending plan within a given budget.

---

## How the App Works (Simple Explanation)

1. The user enters:
   - Total wedding budget
   - How much they want to cut
   - Importance (1–10) for each category

2. Each category has:
   - Budget, Mid, and Luxury options
   - A cost and a quality score

3. The optimizer:
   - Maximizes total value (quality × importance)
   - Keeps total spending within budget
   - Cuts lower-priority items first when needed

---

## Example Insight

When the budget was reduced from **$40,000** to **$38,000**:
- **Decor** was downgraded from **Mid ($4,000)** to **Budget ($2,500)**
- **Photography** stayed **Luxury ($4,500)** because memories last forever

---

## Technologies Used

- Python
- Pandas
- Linear Optimization
- Streamlit

---

## Project Files

- `app.py` — Streamlit UI  
- `optimizer.py` — optimization logic  
- `categories.csv` — category importance  
- `packages.csv` — cost & quality options  
- `requirements.txt` — dependencies  

---

## How to Run the App

```bash
pip install -r requirements.txt
streamlit run app.py

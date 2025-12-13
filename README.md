# Wedding Budget Optimizer 💍

HEAD
A Streamlit app that helps couples decide how to spend their wedding budget and where to cut costs when money is tight.

Instead of cutting randomly, the app protects high-value memories like photography, and reduces spending on lower-impact categories such as decor or DJ first.



# Wedding Budget Optimizer 💍

This project is a Wedding Budget Optimizer that helps couples decide how to spend their wedding budget and where to cut costs when money is tight.

Instead of cutting randomly, the app protects high-value memories like photography and makeup, and reduces spending on lower-impact categories such as decor or DJ first.

---
 3bb8efa (Add project README explanation)

## What Problem Does This Solve?

Wedding planning is stressful, especially when the budget changes.

When couples reduce their budget, they often don’t know:
- Which category to cut
- How much quality they will lose
- Whether their money is being spent wisely

This app solves that problem by automatically suggesting the best spending plan within a given budget.

HEAD


---
 3bb8efa (Add project README explanation)

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

HEAD


## Example Insight

When the budget was reduced from **$40,000** to **$38,000**:
- **Decor** was downgraded from **Mid ($4,000)** to **Budget ($2,500)**
- **Photography** stayed **Luxury ($4,500)** because memories last forever

---

## Example Insight

When the budget was reduced from $40,000 to $38,000:
- Decor was downgraded from **Mid ($4,000)** to **Budget ($2,500)**
- Photography stayed **Luxury ($4,500)** because memories last forever

This shows how the app makes smart, explainable decisions.

---
 3bb8efa (Add project README explanation)

## Technologies Used

- Python
- Pandas
HEAD
- Linear Optimization (Gurobi)
- Streamlit (interactive web app)



## Project Files

- `app.py` — Streamlit UI
- `optimizer.py` — optimization model + logic
- `categories.csv` — category weights (importance)
- `packages.csv` — package options (Budget/Mid/Luxury) with cost + quality
- `requirements.txt` — dependencies



- Linear Optimization
- Streamlit (for interactive web app)

---
 3bb8efa (Add project README explanation)

## How to Run the App

```bash
pip install -r requirements.txt
streamlit run app.py

import pandas as pd

def solve_wedding(budget: float, packages_csv="packages.csv", categories_csv="categories.csv"):
    packages = pd.read_csv(packages_csv)
    categories = pd.read_csv(categories_csv)

    weight = dict(zip(categories["category"], categories["weight"]))

    import gurobipy as gp
    from gurobipy import GRB

    m = gp.Model("wedding_optimizer")
    m.setParam("OutputFlag", 0)

    x = {}
    for i in packages.index:
        x[i] = m.addVar(vtype=GRB.BINARY, name=f"x[{i}]")

    m.update()

    for c in packages["category"].unique():
        idx = packages.index[packages["category"] == c].tolist()
        m.addConstr(gp.quicksum(x[i] for i in idx) == 1)

    m.addConstr(
        gp.quicksum(packages.loc[i, "cost"] * x[i] for i in packages.index) <= budget
    )

    m.setObjective(
        gp.quicksum(
            weight[packages.loc[i, "category"]] * packages.loc[i, "quality"] * x[i]
            for i in packages.index
        ),
        GRB.MAXIMIZE
    )

    m.optimize()

    chosen = []
    for i in packages.index:
        if x[i].X > 0.5:
            chosen.append(packages.loc[i].to_dict())

    solution = pd.DataFrame(chosen).sort_values("category").reset_index(drop=True)

    total_cost = float(solution["cost"].sum())
    total_value = float((solution["category"].map(weight) * solution["quality"]).sum())

    return solution, total_cost, total_value

if __name__ == "__main__":
    base_budget = 30000
    cut_amount = 2000
    new_budget = base_budget - cut_amount  # 38000

    # Run 1: Full budget
    sol1, cost1, value1 = solve_wedding(base_budget)
    print("\n✅ Results for FULL budget ($40,000)")
    print(sol1.to_string(index=False))
    print("\n--- Summary (Full) ---")
    print(f"Budget:      ${base_budget:,.0f}")
    print(f"Spend:       ${cost1:,.0f}")
    print(f"Remaining:   ${base_budget - cost1:,.0f}")
    print(f"Value Score: {value1:,.2f}")

    # Run 2: Reduced budget
    sol2, cost2, value2 = solve_wedding(new_budget)
    print("\n✅ Results AFTER cutting $2,000 (Budget = $38,000)")
    print(sol2.to_string(index=False))
    print("\n--- Summary (Cut) ---")
    print(f"Budget:      ${new_budget:,.0f}")
    print(f"Spend:       ${cost2:,.0f}")
    print(f"Remaining:   ${new_budget - cost2:,.0f}")
    print(f"Value Score: {value2:,.2f}")


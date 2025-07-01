import streamlit as st
import pandas as pd
from datetime import datetime

# --- Sample Constraint Class ---
class Constraint:
    def __init__(self, name, type_, scope, start_date, end_date, logic, source, priority):
        self.name = name
        self.type = type_
        self.scope = scope
        self.start_date = start_date
        self.end_date = end_date
        self.logic = logic
        self.source = source
        self.priority = priority
        self.status = "unknown"

    def evaluate(self, context):
        if self.start_date <= context["date"] <= self.end_date:
            self.status = "violated" if not self.logic(context) else "satisfied"
        else:
            self.status = "inactive"
        return self.status

# --- Sample Constraints ---
constraints = [
    Constraint(
        name="Capacity_Limit_DC1",
        type_="Capacity",
        scope="DC1",
        start_date=datetime(2025, 7, 1),
        end_date=datetime(2025, 7, 31),
        logic=lambda ctx: ctx["demand"] <= ctx["capacity"],
        source="rule_engine",
        priority="high"
    ),
    Constraint(
        name="Inventory_Min_Safety_Stock",
        type_="Inventory",
        scope="SKU123",
        start_date=datetime(2025, 7, 1),
        end_date=datetime(2025, 7, 15),
        logic=lambda ctx: ctx["inventory"] >= ctx["safety_stock"],
        source="manual",
        priority="medium"
    )
]

# --- Sample Contexts ---
contexts = [
    {"date": datetime(2025, 7, 5), "demand": 950, "capacity": 1000, "inventory": 500, "safety_stock": 300},
    {"date": datetime(2025, 7, 10), "demand": 1050, "capacity": 1000, "inventory": 250, "safety_stock": 300},
    {"date": datetime(2025, 7, 20), "demand": 900, "capacity": 1000, "inventory": 350, "safety_stock": 300},
]

# --- Evaluate Constraints ---
event_log = []

for context in contexts:
    for constraint in constraints:
        result = constraint.evaluate(context)
        event_log.append({
            "timestamp": datetime.now(),
            "constraint": constraint.name,
            "type": constraint.type,
            "scope": constraint.scope,
            "status": result,
            "date": context["date"].date(),
            "priority": constraint.priority,
            "source": constraint.source
        })

event_log_df = pd.DataFrame(event_log)

# --- Streamlit UI ---
st.title("📊 Supply Planning Constraint Dashboard")

# Filters
st.sidebar.header("Filters")
selected_status = st.sidebar.multiselect("Constraint Status", options=event_log_df["status"].unique(), default=list(event_log_df["status"].unique()))
selected_type = st.sidebar.multiselect("Constraint Type", options=event_log_df["type"].unique(), default=list(event_log_df["type"].unique()))

filtered_df = event_log_df[
    event_log_df["status"].isin(selected_status) &
    event_log_df["type"].isin(selected_type)
]

# Summary Metrics
st.subheader("Summary")
col1, col2 = st.columns(2)
col1.metric("Total Constraints Evaluated", len(event_log_df))
col2.metric("Violations", len(event_log_df[event_log_df["status"] == "violated"]))

# Constraint Table
st.subheader("Constraint Evaluation Log")
st.dataframe(filtered_df, use_container_width=True)

# Visualization
st.subheader("📈 Violations Over Time")
violation_trend = filtered_df[filtered_df["status"] == "violated"].groupby("date").size().reset_index(name="violations")
st.line_chart(violation_trend.set_index("date"))


import streamlit as st
import pandas as pd
import altair as alt

# Function to calculate the measures
def calculate_measures(tp, fp, fn, tn):
    total = tp + fp + fn + tn
    sensitivity = tp / (tp + fn) if (tp + fn) else 0
    specificity = tn / (tn + fp) if (tn + fp) else 0
    ppv = tp / (tp + fp) if (tp + fp) else 0
    npv = tn / (tn + fn) if (tn + fn) else 0
    lr_plus = sensitivity / (1 - specificity) if (1 - specificity) else 0
    lr_minus = (1 - sensitivity) / specificity if specificity else 0
    accuracy = (tp + tn) / total if total else 0
    prevalence = (tp + fn) / total if total else 0

    measures = {
        'sensitivity': round(sensitivity, 2),
        'specificity': round(specificity, 2),
        'ppv': round(ppv, 2),
        'npv': round(npv, 2),
        'lr_plus': round(lr_plus, 2),
        'lr_minus': round(lr_minus, 2),
        'accuracy': round(accuracy, 2),
        'prevalence': round(prevalence, 2)
    }
    return measures

# Streamlit UI
st.title("Diagnostic Test Performance Analyzer")

# Input fields
st.sidebar.header("Input Parameters")
tp = st.sidebar.number_input("True Positive (TP)", min_value=0, value=85)
fp = st.sidebar.number_input("False Positive (FP)", min_value=0, value=15)
fn = st.sidebar.number_input("False Negative (FN)", min_value=0, value=10)
tn = st.sidebar.number_input("True Negative (TN)", min_value=0, value=90)

# Calculate measures
measures = calculate_measures(tp, fp, fn, tn)

# Display results in a 2x2 table
st.subheader("Results Table")
table_data = [
    ["", "(+) condition", "(-) condition", ""],
    ["(+) test", tp, fp, f"PPV: {measures['ppv']}"],
    ["(-) test", fn, tn, f"NPV: {measures['npv']}"],
    ["", f"Sen: {measures['sensitivity']}", f"Spec: {measures['specificity']}", f"Total: {tp + fp + fn + tn}"],
    ["", f"+LR: {measures['lr_plus']}", f"-LR: {measures['lr_minus']}", f"Accuracy: {measures['accuracy']}"]
]

st.table(table_data)

# Bar chart data
chart_data = pd.DataFrame([
    {"name": "(+) test", "Positive Condition": tp, "Negative Condition": fp},
    {"name": "(-) test", "Positive Condition": fn, "Negative Condition": tn}
])

# Bar chart with custom colors
st.subheader("Contingency Table Visualization")
color_scale = alt.Scale(
    domain=['Positive Condition', 'Negative Condition'],
    range=['#FF6B6B', '#4CAF50']
)

chart = alt.Chart(chart_data).transform_fold(
    fold=['Positive Condition', 'Negative Condition'],
    as_=['Condition', 'Count']
).mark_bar().encode(
    x=alt.X('Count:Q', stack='zero'),
    y=alt.Y('name:N'),
    color=alt.Color('Condition:N', scale=color_scale)
).properties(
    title='Contingency Table Analysis of Diagnostic Test Performance',
    width=600,
    height=300
)

st.altair_chart(chart)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        Web app made by Bashar Hasan, MD
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import altair as alt
import math

# Function to calculate the results
def calculate_results(total_patients, prevalence, sensitivity, specificity):
    disease_positive = round(total_patients * (prevalence / 100))
    disease_negative = total_patients - disease_positive
    true_positive = round(disease_positive * (sensitivity / 100))
    false_negative = disease_positive - true_positive
    true_negative = round(disease_negative * (specificity / 100))
    false_positive = disease_negative - true_negative
    test_positive = true_positive + false_positive
    test_negative = false_negative + true_negative

    ppv = (true_positive / test_positive) * 100 if test_positive else 0
    npv = (true_negative / test_negative) * 100 if test_negative else 0
    lr_plus = (sensitivity / (100 - specificity)) if (100 - specificity) else 0
    lr_minus = ((100 - sensitivity) / specificity) if specificity else 0
    accuracy = ((true_positive + true_negative) / total_patients) * 100

    results = {
        'true_positive': true_positive,
        'false_positive': false_positive,
        'false_negative': false_negative,
        'true_negative': true_negative,
        'test_positive': test_positive,
        'test_negative': test_negative,
        'ppv': ppv,
        'npv': npv,
        'lr_plus': lr_plus,
        'lr_minus': lr_minus,
        'accuracy': accuracy
    }
    return results

# Streamlit UI
st.title("Diagnostic Test Performance Calculator")

# Input fields
total_patients = st.number_input("Total Patients", min_value=1, value=1000)
prevalence = st.number_input("Prevalence (%)", min_value=0.0, max_value=100.0, value=10.0)
sensitivity = st.number_input("Sensitivity (%)", min_value=0.0, max_value=100.0, value=95.0)
specificity = st.number_input("Specificity (%)", min_value=0.0, max_value=100.0, value=60.0)

# Calculate results
results = calculate_results(total_patients, prevalence, sensitivity, specificity)

# Display results in a 2x2 table
st.subheader("Results Table")
table_data = [
    ["", "(+) condition", "(-) condition", ""],
    ["(+) test", results['true_positive'], results['false_positive'], f"PPV: {results['ppv']:.0f}%"],
    ["(-) test", results['false_negative'], results['true_negative'], f"NPV: {results['npv']:.0f}%"],
    ["", f"Sen: {sensitivity}%", f"Spec: {specificity}%", f"Total: {total_patients}"],
    ["", f"+LR: {results['lr_plus']:.2f}", f"-LR: {results['lr_minus']:.2f}", f"Accuracy: {results['accuracy']:.0f}%"]
]

st.table(table_data)

# Bar chart data
chart_data = pd.DataFrame([
    {"name": "(+) test", "Condition (+)": results['true_positive'], "Condition (-)": results['false_positive']},
    {"name": "(-) test", "Condition (+)": results['false_negative'], "Condition (-)": results['true_negative']}
])

# Bar chart with custom colors
st.subheader("Contingency Table Analysis of Diagnostic Test Performance")
color_scale = alt.Scale(
    domain=['Condition (+)', 'Condition (-)'],
    range=['#ef4444', '#22c55e']
)

chart = alt.Chart(chart_data).transform_fold(
    fold=['Condition (+)', 'Condition (-)'],
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

# Decision aid data
def create_decision_aid_data(true_count, false_count, total=100):
    true_percentage = (true_count / (true_count + false_count)) * total
    false_percentage = total - true_percentage
    data = []
    for i in range(total):
        data.append({
            'index': i + 1,
            'Condition': 'Condition (+)' if i < true_percentage else 'Condition (-)',
            'x': i % 10,
            'y': i // 10
        })
    return pd.DataFrame(data)

# Positive test decision aid
positive_test_data = create_decision_aid_data(results['true_positive'], results['false_positive'])

# Negative test decision aid
negative_test_data = create_decision_aid_data(results['false_negative'], results['true_negative'])

# Decision aid charts
st.subheader("Decision Aid for Positive Test")
positive_chart = alt.Chart(positive_test_data).mark_circle(size=100).encode(
    x=alt.X('x:O', axis=None),
    y=alt.Y('y:O', axis=None, sort='descending'),
    color=alt.Color('Condition:N', scale=color_scale)
).properties(
    width=300,
    height=300
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)
st.altair_chart(positive_chart)

st.subheader("Decision Aid for Negative Test")
negative_chart = alt.Chart(negative_test_data).mark_circle(size=100).encode(
    x=alt.X('x:O', axis=None),
    y=alt.Y('y:O', axis=None, sort='descending'),
    color=alt.Color('Condition:N', scale=color_scale)
).properties(
    width=300,
    height=300
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)
st.altair_chart(negative_chart)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 10px; background-color: #0E1117; color: white;">
        Web app made by Bashar Hasan, MD
    </div>
""", unsafe_allow_html=True)

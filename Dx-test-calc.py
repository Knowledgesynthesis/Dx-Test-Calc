import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Display results using st.write
st.subheader("Results")
st.write(f"True Positive: {results['true_positive']}")
st.write(f"False Positive: {results['false_positive']}")
st.write(f"False Negative: {results['false_negative']}")
st.write(f"True Negative: {results['true_negative']}")
st.write(f"PPV: {results['ppv']:.0f}%")
st.write(f"NPV: {results['npv']:.0f}%")
st.write(f"LR+: {results['lr_plus']:.2f}")
st.write(f"LR-: {results['lr_minus']:.2f}")
st.write(f"Accuracy: {results['accuracy']:.0f}%")

# Bar chart data
chart_data = pd.DataFrame([
    {"name": "(+) test", "Condition (+)": results['true_positive'], "Condition (-)": results['false_positive']},
    {"name": "(-) test", "Condition (+)": results['false_negative'], "Condition (-)": results['true_negative']}
])

# Bar chart
st.subheader("Contingency Table Analysis of Diagnostic Test Performance")

fig, ax = plt.subplots()
chart_data.set_index('name').plot(kind='barh', stacked=True, ax=ax, color=['#ef4444', '#22c55e'])
ax.set_xlabel('Count')
ax.set_ylabel('')
ax.set_title('Contingency Table Analysis of Diagnostic Test Performance')
st.pyplot(fig)

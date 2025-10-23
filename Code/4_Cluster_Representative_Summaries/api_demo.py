import time
import google.generativeai as genai

# Configure API key
genai.configure(api_key="ENTER_YOUR_KEY")

# Define model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define prompt and passage
prompt = """Summarize the following passage while retaining all keywords and conveying all key information: Don't use any subscripts or Super Scripts. For example if you want to write R^2, Simply write it R_Square. Don't write as subscript or superscript \n"""
passage = """Today's class, midsem paper was discussed. The following are the key takeaways that I got:
1. In the case of a multivariable dataset, checking for correlation between only two variables alone is not sufficient. One must look for any correlation between a variable and the linear combination of the rest as well. Thus, one fits a linear regression between them, gets the R² value, and finds a metric called Variance Inflation Factor (VIF). We can set a threshold for this metric (say around 8). If a variable has a strong correlation with the linear combination of other variables, one may consider excluding it. This process continues until only variables with VIF below the threshold remain, effectively reducing the number of independent variables in the dataset.
2. Every step of data analysis must be supported by clear thinking and reasoning. One must be able to justify all assumptions and steps in their workflow.
3. In cases where a class is underrepresented in the training dataset, if the difference in support between classes is very large, it is sometimes acceptable to drop the minority class for model creation. Undersampling the majority class weakens training, and oversampling the minority class may not create meaningful data.
4. Dimensionality reduction: Some datasets contain a large number of variables, leading to complexity. If there is insufficient data to capture this complexity, model performance suffers. Solutions include dimensionality reduction, feature selection, regularization, and increasing the dataset size."""

# Measure execution time
start_time = time.time()
response = model.generate_content(prompt + passage)
end_time = time.time()

# Print response and execution time
print(response.text)
print("Time taken:", end_time - start_time)

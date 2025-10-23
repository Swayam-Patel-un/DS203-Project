import google.generativeai as genai
import time

def cluster_rep_summary_generator(summary_list):

    '''Takes in a list of concatenated summaries within a cluster and outputs a list of well-formatted, 
     structured, and comprehensive summaries of the session'''

    API_KEY = "ENTER_YOUR_KEY"
    model_name = "gemini-1.5-flash"
    prompt = """summarize the following passage in a clear, structured, and comprehensive manner. the passage consists of concatenated summaries written by multiple students, so analyze the text to identify the logical flow of the class content and organize the summary accordingly. retain all key ideas and important keywords. do not omit any crucial information. ensure that each point is mentioned only once, without any repetition, while fully preserving its meaning.
                the summary must follow these rules:
                write in plain text with correct punctuation
                no formatting of any kind (no bold, italics, or capital letters)
                no unnecessary spacing between sentences
                expand all contractions (for example, write 'it is' instead of 'it's', 'have not' instead of 'haven't', and 'example fully' instead of 'e.g.')
                do not use subscripts or superscripts; for example, write r_square instead of r²
                very important: for any group of words that together refer to a single concept, write them as a single hyphenated phrase. for example:
                linear-regression
                multiple-linear-regression
                exploratory-data-analysis
                pivot-table
                f-statistic
                mean-square-error
                confusion-matrix
                feature-selection
                this applies not just to the examples above, but to any phrase in the passage where the words together refer to one concept. always think: do these words combine to represent one idea or entity? if yes, then write them with hyphens.
                output only the final summarized text, without any introductory or closing statements."""
    
    # Configure API key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name)

    cluster_rep_summary_list = []

    for i in range(len(summary_list)):
        response = model.generate_content(prompt + "\n" + summary_list[i])
        cluster_rep_summary_list.append(response.text)
        time.sleep(2)

    return cluster_rep_summary_list

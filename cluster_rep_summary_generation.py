import google.generativeai as genai
import time

def cluster_rep_summary_generator(summary_list):

    '''Takes in a list of concatenated summaries within a cluster and outputs a list of well-formatted, 
     structured, and comprehensive summaries of the session'''

    API_KEY = "YOUR_API_KEY"
    model_name = "gemini-1.5-flash"
    prompt = """Summarize the following passage in a structured and comprehensive manner. 
    Retain all key ideas and important keywords while ensuring that no crucial information is lost. 
    The passage contains concatenated summaries from multiple students, so analyze the text to determine 
    the logical flow of the class and structure the summary accordingly. Avoid repeating any idea—each point 
    should be mentioned only once while preserving its full meaning. The summary should be clear and concise 
    with proper punctuation. Contractions should be expanded (e.g., it's → it is, haven't → have not). 
    The final summary should only contain the summarized text, without any introductory or concluding remarks."""
    
    # Configure API key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name)

    cluster_rep_summary_list = []

    for i in range(len(summary_list)):
        response = model.generate_content(prompt + "\n" + summary_list[i])
        cluster_rep_summary_list.append(response.text)
        print(f"Representative summary for Cluster-{i}: " + response.text)
        time.sleep(3)

    return cluster_rep_summary_list

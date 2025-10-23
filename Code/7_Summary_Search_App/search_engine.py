import json
import os

def search(keyword_list):
    # Path relative to this file
    file_path = os.path.join(os.path.dirname(__file__), "top3_summaries_app_data.json")

    # Load the JSON data
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize keywords
    keyword_list = [k.strip().lower() for k in keyword_list]
    
    # Initialize result dictionary
    result_dict = {}

    for cluster_id, values in data.items():
        rep_summary = values[0].lower()
        count_list = []

        for keyword in keyword_list:
            count = rep_summary.count(keyword)
            count_list.append(count)

        result_dict[cluster_id] = count_list

    # Decision logic to find best cluster

    # Count non-zero keyword matches per cluster
    non_zero_counts = {cid: sum(1 for x in counts if x > 0) for cid, counts in result_dict.items()}
    max_non_zero = max(non_zero_counts.values(), default=0)

    # Get all candidate clusters with the same max non-zero keyword count
    candidates = [cid for cid, count in non_zero_counts.items() if count == max_non_zero]

    # Final decision: best cluster
    if len(candidates) == 1:
        best_cluster_index = candidates[0]
    else:
        total_counts = {cid: sum(result_dict[cid]) for cid in candidates}
        best_cluster_index = max(total_counts, key=total_counts.get)

    # Retrieve top 3 summaries for the best cluster
    cluster_data = data.get(str(best_cluster_index))
    if not cluster_data:
        print(f"Cluster ID {best_cluster_index} not found.")
        return []

    top_three = [summary_dict for summary_dict in cluster_data[1:4]]
    key_word_match_list = result_dict[best_cluster_index]

    return best_cluster_index, top_three, key_word_match_list





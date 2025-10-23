import streamlit as st
import urllib.parse
from key_words_list_generator import extract_keywords
from search_engine import search

st.set_page_config(page_title="DS203 Summary Search App")

# Process URL parameters at startup
if "keywords" in st.query_params and "show_results" in st.query_params:
    if st.query_params["show_results"] == "true":
        st.session_state["show_results"] = True
        st.session_state["text_entered"] = st.query_params["keywords"]

# Initialize session state if not already done
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

st.title("DS203 Summary Search App")

# ---------- Input Page ----------
if not st.session_state["show_results"]:
    text_input = st.text_input("Enter keywords (space or comma separated):")

    if st.button("Search") and text_input:
        # Generate a URL with query parameters for the new tab
        query_params = urllib.parse.urlencode({"keywords": text_input, "show_results": "true"})
        results_url = f"/?{query_params}"
        js_code = f"""
        <script>
        window.open("{results_url}", "_blank");
        </script>
        """
        st.markdown(js_code, unsafe_allow_html=True)
        st.markdown(f'<a href="{results_url}" target="_blank">Open results in new tab</a>', unsafe_allow_html=True)

# ---------- Results Page ----------
else:
    # Get text from session state or URL parameters
    text_entered = st.session_state.get("text_entered", "")
    if "keywords" in st.query_params:
        text_entered = st.query_params["keywords"]

    st.subheader("Search Results for:")
    st.code(text_entered)
    st.markdown("---")
    try:
        key_words_list = extract_keywords(text_entered)
        best_match_cluster_id, top_three_summaries_list, key_word_match_list = search(key_words_list)

        # Display cluster ID with the styling previously used for summaries
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <h2 style='color: #1e88e5; font-size: 24px;'>Best matching Session ID: {best_match_cluster_id}</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

  # ---------- Simplified Keyword Statistics Section ----------

        st.markdown("### 🔍 **Keyword Statistics Within Best Match Session**")

        # Create a dictionary to map keywords to their occurrence counts
        keyword_counts = {}
        for i, keyword in enumerate(key_words_list):
            if i < len(key_word_match_list):
                count = key_word_match_list[i]
                keyword_counts[keyword] = count
            else:
                keyword_counts[keyword] = 0

        # Create two columns for found and not found keywords
        col1, col2 = st.columns(2)

        with col1:
            st.write("✅ **Keywords Found**")
            found_keywords = {k: v for k, v in keyword_counts.items() if v > 0}
            if found_keywords:
                sorted_found = sorted(found_keywords.items(), key=lambda x: x[1], reverse=True)
                for keyword, count in sorted_found:
                    st.write(f"🔹**{keyword}**: {count} occurrence{'s' if count > 1 else ''}")
            else:
                st.write("*No keywords were found in the documents.*")

        with col2:
            st.write("❌ **Keywords Not Found**")
            not_found_keywords = [k for k, v in keyword_counts.items() if v == 0]
            if not_found_keywords:
                for keyword in not_found_keywords:
                    st.write(f"- 🔸 {keyword}")
            else:
                st.write("*All keywords were found in the documents.*")

        
        st.markdown("---")

        if top_three_summaries_list:
            for i, summary_dict in enumerate(top_three_summaries_list, 1):
                # Use info style for summary headers (like previously used for cluster ID)
                st.info(f"**Best match summary - {i}**")

                if isinstance(summary_dict, dict):
                    for summary_id, summary_text in summary_dict.items():
                        st.markdown(f"**Summary ID - {summary_id}:** {summary_text}")
                else:
                    st.markdown(f"**Summary {i}:** {str(summary_dict)}")

                if i < len(top_three_summaries_list):
                    st.markdown("---")
        else:
            st.warning("No summaries found.")

    except Exception as e:
        st.error("An error occurred.")
        import traceback
        st.code(traceback.format_exc())


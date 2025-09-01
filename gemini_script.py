import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
# Configure Gemini API key

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def load_json(file_path):
    """Load JSON file (positive/negative keywords)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_text(file_path):
    """Load SoV metrics text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def get_sov_insights(json_file, txt_file):
    """Send SoV metrics + keywords to Gemini and get detailed insights."""
    # Load inputs
    # keywords = load_json(json_file)
    # sov_data = load_text(txt_file)
    with open(json_file, "r", encoding="utf-8") as f:
        comments_data = json.load(f)
    with open(txt_file,'r') as f:
        txt_data=f.read()
        
    data=txt_data + "\n\n" + str(comments_data)
    print(data)
    # Build structured prompt
    prompt = f"""
You are an AI market research assistant. And atomberg is our brand for which we are doing SOV and finding insights.

I have collected Share of Voice (SoV) metrics from social media & YouTube analysis.  
I also have lists of positive and negative keywords users mention.  

### Positive Keywords: given the  below attached file

### Negative Keywords: given the below  attached file
### SoV Metrics: given the below attached file

attached file : {data}

Your task:
1. **Competitive Insights** → Which brands dominate SoV? Who is weak?
2. **Audience Sentiment** → What do people love (from positive keywords)? What frustrates them (from negative keywords)?
3. **Feature Trends** → Which features drive attention (remote, BLDC, quiet operation, etc.)?
4. **Keyword Opportunities** → Suggest related queries worth targeting.
5. **Content Recommendations** → Specific video/article ideas to capture market share.
6. **Action Plan** → 5–7 clear, actionable recommendations for a brand like Atomberg.

Make it structured, concise, and actionable.
"""


    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content( prompt)
    return response.text


def run_gemini():
    json_file="data/final_analysis.json"
    txt_file="data/sov_summary.txt"
    
    insights=get_sov_insights(json_file,txt_file)
    
    with open("data/gemini_report.txt", "w", encoding="utf-8") as f:
        f.write(insights)
        
    print("****** WORK DONE *******")
    print("final results are saved in data folder")
    
if __name__ == "__main__":
    # File paths
    json_file = "data/final_keywords.json"
    txt_file = "data/sov_summary.txt"

    insights = get_sov_insights(json_file, txt_file)

    # Save insights to report
    with open("data/gemini_report.txt", "w", encoding="utf-8") as f:
        f.write(insights)

    print("\n===== GEMINI INSIGHTS =====\n")
    print(insights)
    print("\nInsights also saved to gemini_report.txt ✅")

# 🚀 Automate Socials – SoV Agent Pipeline

This project automates social media analysis by fetching video/comment data, performing sentiment analysis, and generating **Share of Voice (SoV)** metrics across brands.  

---

## 📂 Project Structure

```bash
.
├── data/                        # Input & output data files
│   ├── efficient-fan_comments.csv
│   ├── efficient-fan_videos.csv
│   ├── final_keywords.json
│   ├── smart-fan_comments.csv
│   ├── smart-fan_videos.csv
│   └── sov_summary.txt
│
├── agent_pipeline.py            # Main pipeline orchestrator
├── analyze_comments.py           # Comment analysis module
├── config.py                     # Configurations (queries, brands, API keys)
├── gemini_script.py              # Gemini model integration
├── main_script.py                # Additional script entrypoint
├── requirements.txt              # Python dependencies
├── sentiment.py                  # Sentiment analysis logic
├── sov_metrics.py                # Share of Voice metric calculations
├── utils.py                      # Utility functions
└── youtube_api.py                # YouTube API fetch scripts

# 🔧 How to Run

#### Clone the repository
git clone <your_repo_link>
cd <your_repo_folder>
#### Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

#### Install dependencies
pip install -r requirements.txt

#### Update configuration
Open config.py
Set your queries and brand names

#### run
python agent_pipeline.py

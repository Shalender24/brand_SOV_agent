import os
from main_script import main
from sov_metrics import run_sov
from analyze_comments import run_analyze
from gemini_script import run_gemini

class SoVPipeline:
    def __init__(self,brand="atomberg"):
        self.brand=brand

    def run_fetch(self):
        print("\n[1] Fetching videos and saving CSV...")
        main()

    def run_sov_metrics(self):
        print("\n[2] Calculating SoV metrics...")
        run_sov()

    def run_comments_analysis(self):
        print("\n[3] Analyzing comments and saving JSON...")
        run_analyze()

    def run_gemini_analysis(self):
        print("\n[4] Running Gemini insights...")
        run_gemini()

    def run_all(self):
        """Run complete pipeline in sequence"""
        self.run_fetch()
        self.run_sov_metrics()
        self.run_comments_analysis()
        self.run_gemini_analysis()
        print("\n✅ Pipeline completed! All results saved in /data")



if __name__ == "__main__":
    pipeline = SoVPipeline(brand="atomberg")  # you can change brand here
    pipeline.run_all()
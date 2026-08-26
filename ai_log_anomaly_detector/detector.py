import os
import logging
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)

class LogAnomalyDetector:
    def __init__(self, file_path: str, contamination: float = 0.15):
        self.file_path = file_path
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42, n_estimators=150)
        self.scaler = StandardScaler()
        self.df = None

    def load_data(self) -> bool:
        if not os.path.exists(self.file_path):
            logging.error(f"Target log file '{self.file_path}' not found.")
            return False
        try:
            self.df = pd.read_csv(self.file_path)
            logging.info(f"Successfully ingested {len(self.df)} log entries.")
            return True
        except Exception as e:
            logging.critical(f"Data ingestion failed: {str(e)}")
            return False

    def preprocess_and_train(self):
        features = ['failed_logins', 'data_transferred_mb', 'requests_per_minute']
        X_scaled = self.scaler.fit_transform(self.df[features])
        logging.info("Training Isolation Forest engine...")
        self.model.fit(X_scaled)
        self.df['anomaly_state'] = self.model.predict(X_scaled)
        self.df['anomaly_score'] = self.model.score_samples(X_scaled)

    def generate_threat_report(self, output_path: str = "detected_threats.csv"):
        anomalies = self.df[self.df['anomaly_state'] == -1].copy()
        if anomalies.empty:
            logging.info("Zero anomalies detected. Network SECURE.")
            return
        logging.warning(f"CRITICAL: Found {len(anomalies)} anomalies!")
        anomalies = anomalies.sort_values(by='anomaly_score')
        print("\n" + "="*70 + "\n[!] ANOMALOUS TRAFFIC DETECTED\n" + "="*70)
        print(anomalies[['ip_address', 'failed_logins', 'data_transferred_mb', 'requests_per_minute']])
        print("="*70 + "\n")
        anomalies.to_csv(output_path, index=False)
        logging.info(f"Report saved to '{output_path}'.")

if __name__ == "__main__":
    detector = LogAnomalyDetector(file_path="network_logs.csv", contamination=0.25)
    if detector.load_data():
        detector.preprocess_and_train()
        detector.generate_threat_report()

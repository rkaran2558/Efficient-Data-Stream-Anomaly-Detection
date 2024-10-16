
class EWMAAnomalyDetector:
    """
    A class to apply Exponentially Weighted Moving Average (EWMA) 
    for anomaly detection in a real-time data stream.
    
    Attributes:
        alpha (float): The smoothing factor for EWMA.
        threshold (float): The threshold to detect anomalies.
    """
    def __init__(self, alpha=0.1, threshold=3):
        self.alpha = alpha
        self.threshold = threshold
        self.ewma = None

    def detect_anomalies(self, point):
        """
        Detects anomalies based on the current data point and the EWMA.
        
        Parameters:
            point (float): The current data point from the data stream.
        
        Returns:
            tuple: Contains the current data point, EWMA, and anomaly score.
        """
        if self.ewma is None:
            self.ewma = point  # Initialize EWMA with the first data point
        else:
            self.ewma = self.alpha * point + (1 - self.alpha) * self.ewma  # EWMA calculation

        anomaly_score = abs(point - self.ewma)  # Difference between point and EWMA
        
        # Anomaly detected if score exceeds the threshold
        if anomaly_score > self.threshold:
            print(f"Anomaly detected: Point = {point}, Score = {anomaly_score}")
        
        return point, self.ewma, anomaly_score

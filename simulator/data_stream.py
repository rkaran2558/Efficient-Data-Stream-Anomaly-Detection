
import numpy as np
import time

class DataStreamSimulator:
    """
    Simulates a real-time data stream with a seasonal pattern and noise.
    
    Methods:
        generate_data(): Yields continuous data points from the simulated stream.
    """
    def __init__(self, period=100, noise_std=0.1, delay=0.1):
        self.period = period
        self.noise_std = noise_std
        self.delay = delay

    def generate_data(self):
        """
        Simulates and yields continuous data points with a sine wave and noise.
        
        Yields:
            float: Simulated data point with added noise.
        """
        while True:
            seasonal = np.sin(np.linspace(0, 2 * np.pi, self.period))  # Sine wave
            noise = np.random.normal(0, self.noise_std, self.period)  # Random noise
            for data in seasonal + noise:
                yield data
                time.sleep(self.delay)  # Simulate delay between data points

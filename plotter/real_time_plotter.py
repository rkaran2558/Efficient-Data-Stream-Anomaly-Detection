import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg', 'Qt4Agg', etc. depending on what's installed
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimePlotter:
    """
    Plots real-time data, EWMA, and detected anomalies.
    
    Attributes:
        detector (EWMAAnomalyDetector): The EWMA anomaly detector instance.
        stream (DataStreamSimulator): The data stream simulator instance.
    """
    def __init__(self, detector, stream, window_size=1000):
        self.detector = detector
        self.stream = stream
        self.window_size = window_size
        self.fig, self.ax = plt.subplots()
        self.x_data, self.y_data, self.ewma_data, self.anomaly_data = [], [], [], []

        # Plot lines for data stream, EWMA, and anomaly points
        self.line1, = self.ax.plot([], [], label='Data Stream', lw=1)
        self.line2, = self.ax.plot([], [], label='EWMA', lw=1.5, color='orange')
        self.anomaly_points, = self.ax.plot([], [], 'ro', label='Anomalies', markersize=8)

        # Set plot labels, legends, and limits
        self.ax.set_xlim(0, window_size)
        self.ax.set_ylim(-2, 2)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper right')

    def update_plot(self, frame):
        """
        Updates the plot with the current data, EWMA, and any anomalies.
        
        Parameters:
            frame (tuple): A tuple containing the current point, EWMA, and anomaly score.
        
        Returns:
            tuple: Updated plot lines.
        """
        point, ewma, anomaly_score = frame
        self.x_data.append(len(self.x_data))  # Time/step (x-axis)
        self.y_data.append(point)             # Data point (y-axis)
        self.ewma_data.append(ewma)           # EWMA
        
        # Check for anomaly
        if anomaly_score > self.detector.threshold:
            self.anomaly_data.append((len(self.x_data) - 1, point))

        # Update line data
        self.line1.set_data(self.x_data, self.y_data)
        self.line2.set_data(self.x_data, self.ewma_data)

        # Update anomaly points
        anomaly_x = [x[0] for x in self.anomaly_data]
        anomaly_y = [x[1] for x in self.anomaly_data]
        self.anomaly_points.set_data(anomaly_x, anomaly_y)

        # Update plot limits dynamically
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)

        return self.line1, self.line2, self.anomaly_points

    def start_animation(self):
        """
        Starts the real-time animation of the data stream, EWMA, and anomalies.
        """
        ani = FuncAnimation(self.fig, self.update_plot, frames=self.generate_ewma_frames(), blit=True, interval=1000)
        plt.show()

    def generate_ewma_frames(self):
        """
        Generates frames for the animation by feeding data from the stream 
        into the anomaly detector.
        
        Yields:
            tuple: Current point, EWMA, and anomaly score.
        """
        for point in self.stream.generate_data():
            yield self.detector.detect_anomalies(point)

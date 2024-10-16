
from detector.ewma_detector import EWMAAnomalyDetector
from simulator.data_stream import DataStreamSimulator
from plotter.real_time_plotter import RealTimePlotter

def main():
    """
    Main function to run the real-time data stream visualization with anomaly detection.
    """
    try:
        # Instantiate objects
        stream_simulator = DataStreamSimulator()
        ewma_detector = EWMAAnomalyDetector(alpha=0.1, threshold=3)
        plotter = RealTimePlotter(detector=ewma_detector, stream=stream_simulator)

        # Start the real-time plot
        plotter.start_animation()

    except KeyboardInterrupt:
        print("Execution interrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

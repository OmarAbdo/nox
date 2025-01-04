import math
import random
from entities.delivery_hub import DeliveryHub
from entities.delivery_queue import DeliveryQueue
from entities.truck import Truck
from processes.metrics_collector import MetricsCollector
from processes.order_generation import OrderGenerator
import simpy
from typing import List, Tuple

class Simulation:
    """Encapsulates the entire simulation."""

    def __init__(self, config: dict):
        self.env = simpy.Environment()
        self.config = config
        self.delivery_queue = DeliveryQueue()
        self.metrics = MetricsCollector()
        self.hub_location = config["hub_location"]
        self.hub = DeliveryHub(
            env=self.env,
            num_loading_docks=config["num_loading_docks"],
            loading_time=config["loading_time"],
        )
        self.order_generator = OrderGenerator(
            env=self.env,
            delivery_queue=self.delivery_queue,
            hub_location=self.hub_location,
            order_rate=config["order_rate"],
        )
        self.trucks = [
            Truck(
                env=self.env,
                name=f"Truck_{i+1}",
                hub=self.hub,
                delivery_queue=self.delivery_queue,
                metrics=self.metrics,
                capacity=config["truck_capacity"],
                speed=config["truck_speed"],
                hub_location=self.hub_location,
            )
            for i in range(config["num_trucks"])
        ]

    def run(self):
        """Run the simulation."""
        self.env.run(until=self.config["simulation_time"])
        self.report()

    def report(self):
        """Print simulation results."""
        avg_delivery_time = self.metrics.get_average_delivery_time()
        total_deliveries = self.metrics.total_deliveries
        print("\n--- Simulation Results ---")
        print(f"Total Deliveries: {total_deliveries}")
        print(f"Average Delivery Time: {avg_delivery_time:.2f} minutes")
        if total_deliveries > 0:
            print(
                f"Minimum Delivery Time: {min(self.metrics.delivery_times):.2f} minutes"
            )
            print(
                f"Maximum Delivery Time: {max(self.metrics.delivery_times):.2f} minutes"
            )
        else:
            print("No deliveries were made during the simulation.")


if __name__ == "__main__":
    # Simulation Configuration
    config = {
        "num_loading_docks": 2,
        "loading_time": 10.0,  # minutes
        "num_trucks": 3,
        "truck_capacity": 5,
        "truck_speed": 30.0,  # km/h
        "order_rate": 1 / 2,  # average one order every 2 minutes
        "simulation_time": 120.0,  # minutes (2 hours)
        "hub_location": (0.0, 0.0),  # Coordinates of the hub
    }

    # Seed the random number generator for reproducibility
    random.seed(42)

    # Initialize and run the simulation
    simulation = Simulation(config)
    simulation.run()

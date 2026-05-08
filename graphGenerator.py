from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math

class GraphGenerator:
    def __init__(self):
        self.__graphs = [self.__generate_upgrades, self.__generate_times, self.__generate_drones]
        self.__current_graph = -1 #-1 so next graph would be 0th
        self.__figsize = (7,7)
        self.__get_data()

    def __get_data(self):
        try:
            self.__data = pd.read_csv("statistics.csv")
        except FileNotFoundError:
            self.__data = None

    def next_graph(self):
        if not isinstance(self.__data, pd.DataFrame):
            self.__get_data()
        if not isinstance(self.__data, pd.DataFrame):
            return None

        self.__current_graph = (self.__current_graph+1)%len(self.__graphs)
        return self.__graphs[self.__current_graph]()

    def prev_graph(self):
        if not isinstance(self.__data, pd.DataFrame):
            self.__get_data()
        if not isinstance(self.__data, pd.DataFrame):
            return None

        self.__current_graph = (self.__current_graph-1)%len(self.__graphs)
        return self.__graphs[self.__current_graph]()

    def __generate_upgrades(self):
        filename = "fig_upgrades.png"
        unupgraded = self.__data["unupgraded"].sum()
        factories = self.__data["factories"].sum()
        forts = self.__data["forts"].sum()

        fig, ax = plt.subplots(figsize=self.__figsize, dpi=300)
        plt.pie([unupgraded, factories, forts], labels=["Unupgraded", "Factories", "Forts"], autopct="%1.1f%%", colors=["#777777", "#66DD66", "#6666DD"])
        plt.title("Proportion of planet upgrades")
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_times(self):
        filename = "fig_times.png"

        fig, ax = plt.subplots(figsize=self.__figsize, dpi=300)
        plt.scatter(self.__data["realtime"]/1000, self.__data["gametime"]/1000)
        plt.title("Relation between in-game and real time")
        plt.xlabel("Real time (seconds)")
        plt.ylabel("In-game time (seconds)")
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_drones(self):
        filename = "fig_drones.png"
        fig, ax = plt.subplots(figsize=self.__figsize, dpi=300)

        bin_size = 250
        bins = np.arange(
            math.floor(self.__data["drones_created"].min()/50)*50,
            math.ceil(self.__data["drones_created"].max()/50)*50,
            bin_size
        )
        print(bins)
        bin_labels = []
        for i in range(len(bins)-1):
            bin_labels.append(f"{bins[i]}-{bins[i+1]}")

        grouped_data = self.__data.groupby(pd.cut(self.__data["drones_created"], bins, labels=bin_labels)).sum()
        ratios = grouped_data["drones_destroyed"]/grouped_data["drones_created"]*100
        print(ratios.head())

        plt.bar(ratios.index, 100-ratios, color="#66DD66", label="remaining")
        plt.bar(ratios.index, ratios, bottom=100-ratios, color="#EE5500", label="destroyed")
        plt.title("Distribution of drones spawned and destroyed")
        plt.xlabel("Total number of drones")
        plt.ylabel("Percentage")
        plt.legend()
        plt.savefig(filename)
        plt.close()
        return filename

from matplotlib import pyplot as plt
import pandas as pd

class GraphGenerator:
    def __init__(self):
        self.__graphs = [self.__generate_upgrades, self.__generate_times, self.__generate_drones]
        self.__current_graph = -1 #-1 so next graph would be 0th
        self.__figsize = (6,6)
        self.__data = pd.read_csv("statistics.csv")

    def next_graph(self):
        self.__current_graph = (self.__current_graph+1)%len(self.__graphs)
        return self.__graphs[self.__current_graph]()

    def prev_graph(self):
        self.__current_graph = (self.__current_graph+1)%len(self.__graphs)
        return self.__graphs[self.__current_graph]()

    def __generate_upgrades(self):
        filename = "fig_upgrades.png"
        unupgraded = self.__data["unupgraded"].sum()
        factories = self.__data["factories"].sum()
        forts = self.__data["forts"].sum()
        plt.figure(figsize=self.__figsize, dpi=300)
        plt.pie([unupgraded, factories, forts], labels=["Unupgraded", "Factories", "Forts"], autopct="%1.1f%%", colors=["#777777", "#66DD66", "#6666DD"])
        plt.title("Proportion of planet upgrades")
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_times(self):
        filename = "fig_times.png"
        plt.figure(figsize=(5,5), dpi=300)
        plt.scatter(self.__data["realtime"]/1000, self.__data["gametime"]/1000)
        plt.title("Relation between in-game and real time")
        plt.xlabel("Real time (seconds)")
        plt.ylabel("In-game time (seconds)")
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_drones(self):
        filename = "fig_drones.png"
        plt.figure(figsize=(5,5), dpi=300)

        bins = [0, 500, 1000, 1500, 2000]
        bin_labels = ["0-500", "500-1000", "1000-1500", "1500-2000"]
        grouped_data = self.__data.groupby(pd.cut(self.__data["drones_created"], bins, labels=bin_labels)).sum()
        ratios = grouped_data["drones_destroyed"]/grouped_data["drones_created"]*100

        plt.bar(ratios.index, ratios, color="#EE5500", label="destroyed")
        plt.bar(ratios.index, 100-ratios, bottom=ratios, color="#66DD66", label="remaining")
        plt.title("Distribution of drones spawned and destroyed")
        plt.xlabel("Total number of drones")
        plt.ylabel("Percentage")
        plt.legend()
        plt.savefig(filename)
        plt.close()
        return filename
from matplotlib import pyplot as plt
import pandas

class GraphGenerator:
    def __init__(self):
        self.__graphs = [self.__generate_upgrades]
        self.__current_graph = 0
        self.__data = pandas.read_csv("statistics.csv")

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
        plt.figure(figsize=(5,5), dpi=300)
        plt.pie([unupgraded, factories, forts], labels=["Unupgraded", "Factories", "Forts"])
        plt.title("Proportion of planet upgrades")
        plt.savefig(filename)
        plt.close()
        return filename
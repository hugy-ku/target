from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math
from pathlib import Path

class GraphGenerator:
    def __init__(self):
        self.__graphs = [self.__generate_upgrades, self.__generate_times, self.__generate_drones, self.__generate_table]
        self.__current_graph = -1 #-1 so next graph would be 0th
        self.__figsize = (7,7)
        self.__file_prefix = Path().cwd() / "screenshots" / "visualization"
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
        filename = self.__file_prefix / "fig_upgrades.png"
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
        filename = self.__file_prefix / "fig_times.png"

        fig, ax = plt.subplots(figsize=self.__figsize, dpi=300)
        plt.scatter(self.__data["realtime"]/1000, self.__data["gametime"]/1000)
        plt.title("Relation between in-game and real time")
        plt.xlabel("Real time (seconds)")
        plt.ylabel("In-game time (seconds)")
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_drones(self):
        filename = self.__file_prefix / "fig_drones.png"
        fig, ax = plt.subplots(figsize=(12,12), dpi=300)

        bin_size = 250
        bins = np.arange(
            math.floor(self.__data["drones_created"].min()/50)*50,
            math.ceil(self.__data["drones_created"].max()/50)*50,
            bin_size
        )
        bin_labels = []
        for i in range(len(bins)-1):
            bin_labels.append(f"{bins[i]}-{bins[i+1]}")

        grouped_data = self.__data.groupby(pd.cut(self.__data["drones_created"], bins, labels=bin_labels)).sum()
        ratios = grouped_data["drones_destroyed"]/grouped_data["drones_created"]*100
        # print(ratios.head())

        plt.bar(ratios.index, 100-ratios, color="#66DD66", label="remaining")
        plt.bar(ratios.index, ratios, bottom=100-ratios, color="#EE5500", label="destroyed")
        plt.title("Distribution of drones spawned and destroyed")
        plt.xlabel("Total number of drones")
        plt.ylabel("Percentage")
        plt.legend()
        plt.savefig(filename)
        plt.close()
        return filename

    def __generate_table(self):
        filename = self.__file_prefix / "fig_table.png"
        fig, (ax1, ax2, ax3) = plt.subplots(figsize=self.__figsize, dpi=300, nrows=3)
        ax1.axis("off")
        ax2.axis("off")
        ax3.axis("off")

        # winner,gametime,realtime,drones_created,drones_destroyed,factories,forts,unupgraded

        centrality = {
            "winner": "mode",
            "gametime": "mean",
            "realtime": "mean",
            "drones_created": "mean",
            "drones_destroyed": "mean",
            "factories": "median",
            "forts": "median",
            "unupgraded": "median",
            "created/sec rt.": "mean",
            "destroyed/sec rt.": "mean",
            "created/sec gt.": "mean",
            "destroyed/sec gt.": "mean",
        }

        indexes = ["min", "max", "type", "centrality", "std"]

        df_summary1 = pd.DataFrame(index=indexes)
        df_summary2 = pd.DataFrame(index=indexes)
        df_summary3 = pd.DataFrame(index=indexes)

        new_data = self.__data.copy()
        new_data["created/sec rt."] = round(new_data["drones_created"]/(new_data["realtime"]/1000), 1)
        new_data["destroyed/sec rt."] = round(new_data["drones_destroyed"]/(new_data["realtime"]/1000), 1)
        new_data["created/sec gt."] = round(new_data["drones_created"]/(new_data["gametime"]/1000), 1)
        new_data["destroyed/sec gt."] = round(new_data["drones_destroyed"]/(new_data["gametime"]/1000), 1)

        for column in new_data.columns:
            if column in {"gametime", "realtime", "drones_created", "drones_destroyed"}:
                summary = df_summary1
            elif column in {"winner", "factories", "forts", "unupgraded"}:
                summary = df_summary2
            elif column in {"created/sec rt.", "destroyed/sec rt.", "created/sec gt.", "destroyed/sec gt."}:
                summary = df_summary3
            else:
                continue

            if column in {"winner"}:
                numeric = False
            else:
                numeric = True

            if numeric:
                val_min = new_data[column].min()
                val_max = new_data[column].max()
                val_std = round(new_data[column].std(), 1)
            else:
                val_min = None
                val_max = None
                val_std = None

            val_centrality_type = centrality[column]

            if val_centrality_type == "mean":
                val_centrality = round(new_data[column].mean(), 1)
            if val_centrality_type == "median":
                val_centrality = round(new_data[column].median(), 1)
            if val_centrality_type == "mode":
                val_centrality = new_data[column].mode()[0]

            summary[column] = [
                val_min,
                val_max,
                val_centrality_type,
                val_centrality,
                val_std
            ]

        pd.plotting.table(ax1, df_summary1, loc="center", cellLoc="center")
        pd.plotting.table(ax2, df_summary2, loc="center", cellLoc="center")
        pd.plotting.table(ax3, df_summary3, loc="center", cellLoc="center")
        fig.suptitle("Table of Game Overall")
        plt.savefig(filename)
        plt.close()
        return filename
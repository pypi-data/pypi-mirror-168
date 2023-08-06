import pandas as pd
import seaborn as sns
from scipy.interpolate import interp1d

sns.set_theme(style="whitegrid")
from math import pi

import matplotlib.pyplot as plt


# TODO: move
class PropertyInfo:
    def __init__(self, name):
        self.name = name


class PropertyValue(PropertyInfo):
    def __init__(self, name, best, worst):
        super().__init__(name)
        self.best = best
        self.worst = worst
        self.interp = interp1d(
            [worst, best], [0, 1], bounds_error=False, fill_value=(0, 1)
        )

    def interpolate(self, data):
        return self.interp(data)


# TODO: move
class PropertyName(PropertyInfo):
    def __init__(self):
        super().__init__("name")

    def compute(self, synapse, MTOC, perforin):
        return f"{synapse.cell_1.name}/{synapse.cell_2.name}"


class DataFrameBuilder:
    def __init__(self, index_property, group):
        self.index_property = index_property
        self.group = group
        self.data = {}
        self.data[self.index_property.name] = []
        self.data[self.group.name] = []
        self.properties = {}

    def add(self, cell_property):
        self.data[cell_property.name] = []
        self.properties[cell_property.name] = cell_property

    def compute(self, synapse, MTOC, perforin):
        self.data[self.index_property.name].append(
            self.index_property.compute(synapse, MTOC, perforin)
        )
        self.data[self.group.name].append(self.group.compute(synapse, MTOC, perforin))
        for name, p in self.properties.items():
            self.data[name].append(p.compute(synapse, MTOC, perforin))

    @property
    def dataframe(self):
        return pd.DataFrame(self.data)

    def interpolate(self):
        df = self.dataframe
        for k in self.properties.keys():
            df[k] = self.properties[k].interpolate(df[k])
        return df

    def show(self, filename=None):
        df = self.dataframe
        df_melt = pd.melt(
            df, value_vars=self.properties.keys(), id_vars=self.group.name
        )
        plt.figure(figsize=(3, 3))
        sns.violinplot(
            x="variable",
            y="value",
            hue=self.group.name,
            data=df_melt,
            palette="muted",
            split=True,
            inner="quartile",
        )
        if filename is not None:
            plt.savefig(filename)
        plt.show()

        """
        df = self.interpolate()
        df_melt = pd.melt(df, value_vars=self.properties.keys(), id_vars=self.group.name)
        plt.figure(figsize=(16, 9))
        sns.violinplot(x='variable', y='value', hue=self.group.name, data=df_melt, palette="muted", split=True,
                       inner="quartile")
        plt.show()
        """

    def show_radar(self):
        """
        categories = self.properties.keys()
        N = len(categories)
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        angle = np.deg2rad(67.5)
        figure = FigureSinglePolar(xlabel=categories, size=(4, 4))
        values = df.drop(columns=[self.index_property.name, self.group.name]).mean(axis=0).values.flatten().tolist()
        values += values[:1]

        figure.panel.plot(angles, values, linewidth=1, linestyle='solid', label="P")

        handles, labels = plt.gca().get_legend_handles_labels()
        handles, labels = zip(*[ (handles[i], labels[i]) for i in sorted(range(len(handles)), key=lambda k: labels[k])])
        figure.panel.legend(handles, labels, loc="lower left", bbox_to_anchor=(.5 + np.cos(angle)/2, .5 + np.sin(angle)/2))
        """
        """
        for i, j in df.head(20).iterrows():
            values=j.drop([self.index_property.name, self.group.name]).values.flatten().tolist()
            values += values[:1]

            if i == 0:
                figure.panel.plot(angles, values, linewidth=1, linestyle='dashed', label=f"maximum score", c='k')
            else:

            figure.panel.plot(angles, values, linewidth=1, linestyle='solid', label=f"pair {i}")
        """

        # number of variable
        categories = self.properties.keys()
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels
        plt.xticks(angles[:-1], categories)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks(
            [0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=7
        )
        plt.ylim(0, 1)

        # ------- PART 2: Add plots

        # Plot each individual = each line of the data
        # I don't make a loop, because plotting more than 3 groups makes the chart unreadable

        # Ind1
        df = self.interpolate()
        values = (
            df[df[self.group.name] == "NP"]
            .drop(columns=[self.index_property.name, self.group.name])
            .mean(axis=0)
            .values.flatten()
            .tolist()
        )
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle="solid", label="NP")
        ax.fill(angles, values, "b", alpha=0.1)

        # Ind2
        values = (
            df[df[self.group.name] == "P"]
            .drop(columns=[self.index_property.name, self.group.name])
            .mean(axis=0)
            .values.flatten()
            .tolist()
        )
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle="solid", label="P")
        ax.fill(angles, values, "r", alpha=0.1)

        # Add legend
        plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

        # Show the graph
        plt.show()

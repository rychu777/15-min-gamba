import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class DataAnalyzer:
    def __init__(self, file_path: str):
        """
        Initializes the DataAnalyzer object by loading data from a .feather file.

        :param file_path: Path to the .feather file containing the data.
        """
        self.df = pd.read_feather(file_path)

    def winrate(self) -> None:
        """
        Displays a pie chart showing the win rate of the blue team and the red team.
        """
        sizes = [self.df.blueTeamWin[self.df['blueTeamWin'] == 1].count(),
                 self.df.redTeamWin[self.df['redTeamWin'] == 1].count()]
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.canvas.manager.set_window_title('Winrate')
        ax.pie(sizes, labels=['Blue team wins', 'Red team wins'], autopct='%1.1f%%', startangle=270,
               colors=['#1260CC', '#ff2C2C'])
        ax.axis('equal')
        plt.title("Winrate", size=15)
        plt.show()

    def winrate_per_first_blood(self) -> None:
        """
        Displays a bar chart showing the win rate of the blue team and the red team
        based on whether they achieved the first blood or not.
        """
        winsWithFirstBlood = ((self.df.blueTeamWin[self.df['blueTeamFirstBlood'] == 1].count() / (len(self.df) / 100)),
                              (self.df.redTeamWin[self.df['redTeamFirstBlood'] == 1].count()) / (len(self.df) / 100))
        winsWithoutFirstBlood = (
            (self.df.blueTeamWin[self.df['blueTeamFirstBlood'] == 0].count() / (len(self.df) / 100)),
            (self.df.redTeamWin[self.df['redTeamFirstBlood'] == 0].count()) / (len(self.df) / 100))
        print(winsWithFirstBlood, winsWithoutFirstBlood)
        ind = np.arange(2)
        plt.figure(figsize=(7, 5)).canvas.manager.set_window_title('WinrateAndFirstBloods')
        width = 0.2
        plt.bar(ind, winsWithFirstBlood, width, label=['With First Blood', 'With First Blood'],
                color=['#1260CC', '#C30010'])
        plt.bar(ind + width, winsWithoutFirstBlood, width, label=['Without First Blood', 'Without First Blood'],
                color=['#29C5f6', '#ff2C2C'])
        plt.xlabel('Teams')
        plt.ylabel('Winrate')
        plt.title('Winrate depending on first blood')
        plt.xticks(ind + width / 2, ('Blue', 'Red'))
        plt.legend(loc='best')
        plt.show()

    def gold_and_cs(self) -> None:
        """
        Displays a stack plot showing the correlation between gold per minute (GPM)
        and creep score per minute (CsPM) for the blue team in games that lasted more than 2500 seconds.
        """
        df2 = self.df.loc[(self.df['blueTeamWin'] == 1) & (self.df['gameDuration'] > 2500)]
        goldPerMinute = [x / 10 for x in list(df2.blueTeamGoldPerMinute)]
        csPerMinute = list(df2.blueTeamCsPerMinute)
        xAxis = [x for x in range(len(goldPerMinute))]
        levelCs = {'Gold Per Minute': goldPerMinute, 'CS Per Minute': csPerMinute}
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.canvas.manager.set_window_title('CSPM&GPM')
        ax.stackplot(xAxis, levelCs.values(), labels=levelCs.keys(), alpha=0.95, colors=['#1260CC', '#ff2C2C'])
        ax.legend(loc='upper left')
        ax.set_title('CSPM & GPM correlation')
        plt.axis('off')
        plt.show()

    def heatmap(self) -> None:
        """
        Displays a heatmap showing the correlation matrix of the dataset,
        excluding columns 17 to 35. (Just for one team.)
        """
        self.df.drop(self.df.iloc[:, 17:35], axis=1, inplace=True)
        plt.figure(figsize=(30, 15)).canvas.manager.set_window_title('Heatmap')
        heatMap = sns.heatmap(self.df.loc[:].corr(), annot=True, cmap='jet')
        heatMap.set_xticklabels(heatMap.get_xticklabels(), rotation=45, fontsize=7)
        heatMap.set_yticklabels(heatMap.get_yticklabels(), rotation=0, fontsize=7)
        plt.show()

    def multicollinearity(self) -> None:
        df = self.df.sample(frac=0.01, random_state=777)
        df = df.sample(frac=0.1, random_state=777)
        df = df.loc[(df['blueTeamWin'] == 1)]
        df = df[df['blueTeamFirstBlood'] == 1]

        goldPerMinute = [x / 10 for x in list(df.blueTeamGoldPerMinute)]
        totalMinionsKilled = list(df.blueTeamTotalMinionsKilled)

        yAxis = [x for x in range(len(goldPerMinute))]
        plt.figure().canvas.manager.set_window_title('Multicollinearity')
        plt.plot(yAxis, goldPerMinute, label='Gold per minute', color='#1260CC')
        plt.plot(yAxis, totalMinionsKilled, label='Total minions killed', color='#ff2C2C')

        plt.legend()
        plt.show()

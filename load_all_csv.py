import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DataSet(pd.DataFrame):
    full_path = None
    description = None

    def desc(self):
        print(self.description)


class DataSets():
    datasets = []
    __dataset_full_path_dict__ = None

    def __init__(self, datasets):
        self.datasets = datasets
        __dataset_full_path_arr = []
        for i, ds in enumerate(self.datasets):
            __dataset_full_path_arr.append((ds.full_path, i))
        self.__dataset_full_path_dict__ = dict(__dataset_full_path_arr)

    def desc(self):
        print("\n".join([str(i) + "\t" + ds.full_path for i, ds in enumerate(self.datasets)]))

    def len(self):
        return len(self.datasets)

    @staticmethod
    def __diff__(l1, l2):
        return list(set(l1) - set(l2))

    def get_dataset_with_path(self, required_path):
        try:
            return self.datasets[self.__dataset_full_path_dict__[required_path]]
        except:
            return None
 
    def plot_university_degree_job_relatedness(self):
        path = "./Employment/University-Degree-Job-Relatedness/University-Degree-Job-Relatedness.csv"
        df = self.get_dataset_with_path(path)
        programs = df["Program"].unique()
        all = list(range(len(programs)))
        programs_dict = dict([(program, i) for i, program in enumerate(programs)])
        programs_num = dict([(i, program) for i, program in enumerate(programs)])
        fig, ax = plt.subplots()
        w = 0.2
        bars = []
        #relatedness 1
        for i in range(1,4):
            y = df.loc[df["Relatedness-Level"] == i, :].groupby("Program").sum()["Relatedness-N"]
            x = [programs_dict[program] for program in y.index]
            diff = self.__diff__(all, x)
            for j in diff:
                y.loc[programs_num[j]] = 0
            y = y.sort_index()
            bar = ax.bar(np.array(all) + (i-1)*w, y.tolist(), w)
            bars.append(bar)
        plt.xticks(list(range(len(programs))), programs)
        ax.legend(bars, ("Not Related at all", "Somewhat Related","Closely Related"))
        ax.set_ylabel("No. of people")
        ax.set_xlabel("Program")
        ax.set_title("Surveyed education vs how related their job is to their education")
        plt.show()
        return path

    def plot_university_program_noc(self):
        path = "./Employment/University-Program-NOC/University-Program-NOC.csv"
        df = self.get_dataset_with_path(path)

        programs = df["Program"].unique()
        all = list(range(len(programs)))

        fig, ax = plt.subplots()
        w = 0.3
        bars = []

        for i, year in enumerate(df["Year"].unique()):
            y= df.loc[df["Year"] == year, :].groupby("Program").sum()
            bar = ax.bar(np.array(all)+i*w, y["Employed"].tolist(), w)
            bars.append(bar)
            bar = ax.bar(np.array(all)+i*w, y["Self-Employed"].tolist(), w)
            bars.append(bar)
        plt.xticks(all, programs)
        ax.legend(bars, ("2012 Employed", "2012 Self-Employed", "2013 Employed", "2013 Self-Employed"))
        ax.set_ylabel("No. of people")
        ax.set_xlabel("Program")
        ax.set_title("Number of people employed based on their Education Program")
        plt.show()
 
        return df

    def plot_university_employment_rates(self, program="ENG", period="6"):
        period = str(period)
        path = "./Employment/University-Employment-Rates/University-Employment-Rates.csv"
        df = self.get_dataset_with_path(path)

        df = df.loc[df["Program"] == program, :]
        unis = df.loc[df["Schedule"] == "All", "University"].unique()
        unis_dict = dict([(uni, i) for i, uni in enumerate(unis)])
        unis_num = dict([(i, uni) for i, uni in enumerate(unis)])
        all = list(range(len(unis)))

        fig, ax = plt.subplots()
        w = 0.1
        bars = []
        ymin = 1.0
        
        for i, year in enumerate(df["Year"].unique()):
            y = df.loc[(df["Year"] == year) & (df["Period"] == period) & (df["Schedule"] == "All"), :]
            x = [unis_dict[p] for p in y["University"]]
            diff = self.__diff__(all, x)
            for j in diff:
                y = y.append(pd.DataFrame([["ENG", year, "All", period, unis_num[j], None, None, 0]], columns = y.columns))
            y = y.sort_values(by="University")
            
            y = y['%-Employed'].tolist()
            temp_min = min(y)
            if ymin > temp_min and temp_min > 0:
                ymin = temp_min

            bar = ax.bar(np.array(all)+i*w, y, w)
            bars.append(bar)

        plt.xticks(all, unis)
        ax.legend(bars, df["Year"].unique())
        ax.set_ylabel("Percent Employed")
        ax.set_ylim([0.8*ymin, 1.0])
        ax.set_xlabel("University")
        ax.set_title("Percent of people employed in {} after {} months".format(program, period))
        plt.show()
        return path

    def plot_essential_skills(self):
        path = "./Labour_Market/Essential-Skills-Comptences-Cls/Essential-Skills.csv"
        df = self.get_dataset_with_path(path)

        skill_dict = {
            "S1": "Data Analysis",
            "S2": "Decision Making",
            "S3": "Finding Information",
            "S4": "Job Task Planning and Organizing",
            "S5": "Measurement and Calculation",
            "S6": "Money Math",
            "S7": "Numerical Estimation",
            "S8": "Oral Communication",
            "S9": "Problem Solving",
            "S10": "Reading",
            "S11": "Scheduling or Budgeting and Accounting",
            "S12": "Digital Technology",
            "S13": "Document Use",
            "S14": "Writing",
            "S15": "Critical Thinking"
        } 

        skill_level_count = df.groupby("Skill").count()["TaskCode"]
        x = np.sort(df["Skill"].unique())
        all = list(range(len(x)))
        plt.bar(all, skill_level_count)
        plt.xticks(all, [skill_dict[val] for val in x], rotation='vertical')
        plt.xlabel("Skill")
        plt.title("Number of jobs available per skill level")
        plt.ylabel("Different Job Count")
        plt.show()

        return path

    def plot_no_skill_jobs_per_education_level(self):
        path = "./Labour_Market/Essential-Skills-Comptences-Cls/Essential-Skills.csv"
        df = self.get_dataset_with_path(path)

        skill_dict = {
            "S1": "Data Analysis",
            "S2": "Decision Making",
            "S3": "Finding Information",
            "S4": "Job Task Planning and Organizing",
            "S5": "Measurement and Calculation",
            "S6": "Money Math",
            "S7": "Numerical Estimation",
            "S8": "Oral Communication",
            "S9": "Problem Solving",
            "S10": "Reading",
            "S11": "Scheduling or Budgeting and Accounting",
            "S12": "Digital Technology",
            "S13": "Document Use",
            "S14": "Writing",
            "S15": "Critical Thinking"
        } 

        educations_dict = {
            "0": "None",
            "A": "University Degree(s)",
            "B": "College, vocational, or apprenticeship",
            "C/D": "No formal education"
        }


        educations = df.dropna(subset=["EducationTrainingLevel"])["EducationTrainingLevel"].unique()
        skills = np.sort(df["Skill"].unique())
        skills_x_dict = dict([(skill, i) for i, skill in enumerate(skills)])
        x_skills_dict = dict([(i, skill) for i, skill in enumerate(skills)])
        all = list(range(len(skills)))

        groups = df.groupby("EducationTrainingLevel")

        fig, ax = plt.subplots()
        w = 0.2
        bars = []

        for i, education in enumerate(educations):
            group = groups.get_group(education)
            y = group.groupby("Skill").count()
            x = [skills_x_dict[index] for index in y.index]
            diff = self.__diff__(all, x)
            for j in diff:
                y.loc[x_skills_dict[j]] = [0, 0, 0, 0]
 
            y = y.sort_index()
            y = y["NOC"].tolist()
            bar = ax.bar(np.array(all)+i*w, y, w)
            bars.append(bar)

        ax.legend(bars, [educations_dict[edu] for edu in educations])
        plt.xticks(all, [skill_dict[x_skills_dict[val]] for val in all], rotation='vertical')
        plt.xlabel("Skill")
        plt.title("Number of Tasks in Jobs available per skill level")
        plt.ylabel("Different Task Count")
        plt.show()

        return path

    def plot_program_ranking(self, year = "16-17", confirmed=None):
        path = './Application_and_Enrolment/Applications-by-University-Program/Applications-by-University-Program.csv'
        df = self.get_dataset_with_path(path)
        df = df.loc[df["Year"] == year, :]

        program_names = np.sort(df["Program"].unique())
        all = list(range(len(program_names)))
        choices = list(range(1, 5))

        fig, ax = plt.subplots()
        w = 0.2
        bars = []

        for i, choice in enumerate(choices):
            y = None
            if confirmed is None:
                y = df.loc[df["Choice"] == choice, :].groupby("Program").sum().sort_index()["Count"]
            elif confirmed:
                y = df.loc[(df["Choice"] == choice) & (df["Confirmed"] == "Y"), :].sort_index()["Count"]
            else:
                y = df.loc[(df["Choice"] == choice) & (df["Confirmed"] == "N"), :].sort_index()["Count"]
            bar = ax.bar(np.array(all)+i*w, y, w)
            bars.append(bar)

        ax.legend(bars, ["1st choice", "2nd choice", "3rd choice", "4th choice"])
        plt.xticks(all, program_names)
        plt.xlabel("Program")
        plt.ylabel("Number of Applicants")
        plt.title("Number of Applicants per Program during {}".format(year))
        plt.show()
        return path



def load_all_csv(walk_from = "."):
    directories = os.walk(walk_from)
    dfs = []
    for directory in directories:
        for files in directory[1:]:
            for filename in files:
                if filename.endswith(".csv"):
                    full_path = directory[0] + "/" + filename
                    ds = DataSet(pd.read_csv(full_path, encoding="latin-1"))
                    ds.full_path = full_path
                    description_path = full_path.replace(".csv", "-Dict.txt")
                    try:
                        description_file = open(description_path, "r", encoding="latin-1")
                        ds.description = description_file.read()
                    except:
                        pass
                    dfs.append(ds)

    return DataSets(dfs)
 

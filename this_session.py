# coding: utf-8

from util.load_all_csv import load_all_csv
import matplotlib.pyplot as plt
dfs = load_all_csv()

dfs.plot_program_ranking()
dfs.plot_essential_skills()
dfs.plot_no_skill_jobs_per_education_level()

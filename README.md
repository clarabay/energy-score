# energy-score
Toolkit to calculate the energy score of trajectory-based predictions


# Installation


# Notebook Descriptions

energy_score_tutorial.ipynb - gives examples of how to calculate the energy score, normalized energy score, and weighted interval score with synthetic examples and using Scenario Modeling Hub projections.

energyscore_fcn.py - function used to calculate the energy score

baseline_model-analysis.ipynb - used to generate a naive baseline forecast and trajectories for the predictions. calculate energy score and multi-dimensional energy score with data from the 2023-24 influenza season.

energyscore_flu_rd4-analysis.ipynb - used to calculate all scores for 2023-24 Flu Scenario Modeling Hub round and generate analysis for these projections. Used to generate parts of Figs. 3 and 4, Tables S2 and S3, and Fig. S2 in the paper.

energyscore_sampling_analysis.ipynb - used to calculate the energy score for samples of trajectories and compare to the full energy score. Used to generate Fig. S1.

ensemble_analysis.ipynb - used to generate an ensemble of trajectories and analyze the energy score and multi-dimensional energy score of the resulting ensemble model. Used to generate fig 5 and Table S4 in the paper.

synthetic_data_properness_test.ipynb - used to create synthetic experiments that compare the evaluation methods of the energy score and WIS. Used to generate fig 1 in the paper.

multi-dimensional_energyscore.ipynb - analyze the multi-dimensional energy score with examples looking across all dimensions for influenza hospitalization projections. Used to generate data for Fig. 3E and Table S1.

single_week_scores.ipynb - used to examine the energy score at single time points with synthetic and influenza scenario modeling data. Used to generate part of fig 3 and S2 in the paper.

visualize_scenario_trajectories.ipynb - used to create plots visualizing scenario projections. Used to generate fig 2 in the paper.

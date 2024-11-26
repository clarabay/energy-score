# energy-score
Toolkit to calculate the energy score of trajectory-based predictions


# Installation


# Notebook Descriptions

energy_score_tutorial.ipynb - gives examples of how to calculate the energy score, normalized energy score, and weighted interval score with synthetic examples and using Scenario Modeling Hub projections.

energyscore_fcn.py - function used to calculate the energy score

baseline_model-analysis.ipynb - used to generate a naive baseline forecast and trajectories for the predictions. calculate energy score and multi-dimensional energy score with data from the 2023-24 influenza season.

energyscore_flu_rd4-clean2.ipynb - used to calculate all scores for 2023-24 Flu Scenario Modeling Hub round and generate analysis for these projections. Used to generate parts of figs 4 and 5 in the paper.

energyscore_flu_rd4_sampled.ipynb - used to calculate the energy score for samples of trajectories and compare to the full energy score.

ensemble_analysis.ipynb - used to generate an ensemble of trajectories and analyze the energy score and multi-dimensional energy score of the resulting ensemble model. Used to generate fig 6 in the paper.

es_wis_test.ipynb - used to create synthetic experiments that compare the evaluation methods of the energy score and WIS. Used to generate fig 3 in the paper.

multitarget_energyscore_new.ipynb - analyze the multi-dimensional energy score with examples looking across all dimensions for influenza hospitalization projections. 

score_decomposition.ipynb - used to examine the energy score at single time points with synthetic and influenza scenario modeling data. Used to generate fig 2 and part of fig 4 in the paper.

visualize_scenario_trajectories.ipynb - used to create plots visualizing scenario projections. Used to generate fig 1 in the paper.

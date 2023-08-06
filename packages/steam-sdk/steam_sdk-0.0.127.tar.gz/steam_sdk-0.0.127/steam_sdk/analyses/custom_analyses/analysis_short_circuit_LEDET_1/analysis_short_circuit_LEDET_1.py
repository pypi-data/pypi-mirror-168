import os
from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py

from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.tic_toc import tic, toc
from steam_sdk.utils.unique import unique

from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.calculate_short_parameters import calculate_short_parameters
from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.set_common_parameters import set_common_parameters
from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.set_magnet_specific_parameters import set_magnet_specific_parameters
from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.set_short_circuit_analysis_parameters import set_short_circuit_analysis_parameters
from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.set_simulations_to_prepare_run import set_simulations_to_prepare_run
from steam_sdk.analyses.custom_analyses.analysis_short_circuit_LEDET_1.utils.copy_input_files import copy_input_files


def analysis_short_circuit_LEDET_1(dict_inputs: Dict):
    '''

    :param dict_inputs: Dictionary that contains all input variables
    :return:
    '''
    tic()

    ######################## Unpack inputs ########################
    # Input flags and settings
    magnet_name = dict_inputs['magnet_name']
    list_software = dict_inputs['list_software']
    magnet_name_short_circuit = dict_inputs['magnet_name_short_circuit']
    verbose = dict_inputs['verbose']
    flag_reprepare_sim = dict_inputs['flag_reprepare_sim']
    flag_rerun_sim = dict_inputs['flag_rerun_sim']
    flag_append = dict_inputs['flag_append']
    flag_plots = dict_inputs['flag_plots']
    selectedFont = dict_inputs['selectedFont']
    default_figsize = tuple(dict_inputs['default_figsize'])
    # Short-circuit analysis parametric-sweep parameters
    start_simulation_index = dict_inputs['start_simulation_index']
    R_short_circuit = float(dict_inputs['R_short_circuit'])
    length_short_circuit = float(dict_inputs['length_short_circuit'])
    RRR = float(dict_inputs['RRR'])
    Jc_fit_C1_CUDI1 = float(dict_inputs['Jc_fit_C1_CUDI1'])
    Jc_fit_C2_CUDI1 = float(dict_inputs['Jc_fit_C2_CUDI1'])
    scale_cooling_to_heat_sink = float(dict_inputs['scale_cooling_to_heat_sink'])
    scale_heat_diffusion_between_turns = float(dict_inputs['scale_heat_diffusion_between_turns'])
    # Parameters to select parametric simulations to prepare and run. Note: All model objects will still be present when the analysis is run, but no output simulation files will be generated unless they are listed in "list_simulations_to_prepare"
    n_sims_percentile_M12_100 = dict_inputs['n_sims_percentile_M12_100']  # Number of simulations to select evenly distributed across 100% of the values of M12
    n_sims_percentile_M12_50 = dict_inputs['n_sims_percentile_M12_50']  # Number of simulations to select evenly distributed across  50% of the values of M12
    n_sims_along_conductor = dict_inputs['n_sims_along_conductor']  # Number of simulations to select evenly distributed along the coil conductor. Note: A good choice is a prime number to avoid repeating similar simulations due to symmetry
    list_simulations_manually_added = dict_inputs['list_simulations_manually_added']  # this allows setting desired simulations in addition to those automatically selected
    # Paths to input files (they are generated running the analyses\MCBY_short_circuit analysis)
    path_file_empty_analysis = dict_inputs['path_file_empty_analysis']
    path_file_inductance = dict_inputs['path_file_inductance']
    path_file_reference_model_LEDET = dict_inputs['path_file_reference_model_LEDET']
    path_file_model_geometry = dict_inputs['path_file_model_geometry']
    # Paths to output files
    path_output_file_M12 = dict_inputs['path_output_file_M12']
    path_output_file_analysis = dict_inputs['path_output_file_analysis']
    output_folder_figures = dict_inputs['output_folder_figures']

    tic()
    ######################## Pre-processing ########################
    # Make sure output folders exist
    make_folder_if_not_existing(output_folder_figures)

    # Initialize an empty AnalysisSTEAM object
    # TODO: allow initializing an empty aSTEAM object?
    aSTEAM = AnalysisSTEAM(file_name_analysis=path_file_empty_analysis, verbose=True)

    # TODO reassign the settings if they are set to permanent settings!!!

    # Read self-mutual inductance matrix and half-turn electrical order
    M = np.genfromtxt(path_file_inductance, dtype=float, delimiter=',', skip_header=1)
    dict_LEDET = yaml_to_data(path_file_reference_model_LEDET)
    iContactAlongWidth_From = dict_LEDET['iContactAlongWidth_From']
    iContactAlongWidth_To = dict_LEDET['iContactAlongWidth_To']
    iContactAlongHeight_From = dict_LEDET['iContactAlongHeight_From']
    iContactAlongHeight_To = dict_LEDET['iContactAlongHeight_To']
    n_turns = M.shape[0]

    # Delete indices with value higher than half of the number of turns, i.e. the half-turns defining return paths (first element has index 1)
    # Note: The deleted indices would result in almost identical simulations due to symmetry
    # Contacts along conductor width
    temp_idx_to_delete = np.where(np.array(iContactAlongWidth_From) > n_turns)[0]
    temp_idx_to_delete = np.append(temp_idx_to_delete, np.where(np.array(iContactAlongWidth_To) > n_turns)[0])
    iContactAlongWidth_From_to_consider = np.delete(iContactAlongWidth_From, temp_idx_to_delete)
    iContactAlongWidth_To_to_consider = np.delete(iContactAlongWidth_To, temp_idx_to_delete)
    # Contacts along conductor height
    temp_idx_to_delete = np.where(np.array(iContactAlongHeight_From) > n_turns)[0]
    temp_idx_to_delete = np.append(temp_idx_to_delete, np.where(np.array(iContactAlongHeight_To) > n_turns)[0])
    iContactAlongHeight_From_to_consider = np.delete(iContactAlongHeight_From, temp_idx_to_delete)
    iContactAlongHeight_To_to_consider = np.delete(iContactAlongHeight_To, temp_idx_to_delete)

    # iContactAlongWidth_From_to_consider = iContactAlongWidth_From_to_consider[0:5]  # TODO: delete this line
    # iContactAlongHeight_From_to_consider = iContactAlongHeight_From_to_consider[0:5]  # TODO: delete this line

    # Convert elements to int
    iContactAlongHeight_From_to_consider = [int(i) for i in iContactAlongHeight_From_to_consider]
    iContactAlongHeight_To_to_consider = [int(i) for i in iContactAlongHeight_To_to_consider]
    toc()


    ######################## Set up parameters for short-circuit simulation (independent of the short-circuit position) ########################
    aSTEAM.data_analysis.GeneralParameters.model.name = magnet_name_short_circuit  # important to generate models in a different folder rather than the original magnet name
    copy_input_files(aSTEAM, magnet_name, magnet_name_short_circuit, list_software, verbose)
    set_common_parameters(aSTEAM, magnet_name, magnet_name_short_circuit, list_software, dict_LEDET, verbose)
    set_magnet_specific_parameters(aSTEAM, verbose)
    set_short_circuit_analysis_parameters(aSTEAM, dict_LEDET, RRR, Jc_fit_C1_CUDI1, Jc_fit_C2_CUDI1, scale_cooling_to_heat_sink, scale_heat_diffusion_between_turns, R_short_circuit, verbose)


    ######################## Calculate short-circuit parameters ########################
    # Process pairs of half-turns that touch each other along the conductor long side (along its width)
    list_M12 = np.array([])  # array of all mutual inductances between shorted and non-shorted sections, for each short location
    df_M12 = pd.DataFrame()
    for pair in range(len(iContactAlongWidth_From_to_consider)):
        # Start numbering simulations from start_simulation_index to allow appending new simulations without overwriting
        M_new, df_M12 = calculate_short_parameters(start_simulation_index, pair, pair+1,
                                                   iContactAlongWidth_From_to_consider, iContactAlongWidth_To_to_consider,
                                                   M, length_short_circuit,
                                                   dict_LEDET, magnet_name_short_circuit, list_software,
                                                   path_file_model_geometry, aSTEAM, df_M12, verbose)
        list_M12 = np.append(list_M12, M_new[0, 1])

    # Process pairs of half-turns that touch each other along the conductor short side (along its height)
    for pair in range(len(iContactAlongHeight_From_to_consider)):
        # Start numbering simulations from start_simulation_index+len(iContactAlongWidth_From_to_consider) to avoid over-writing previous steps
        M_new, df_M12 = calculate_short_parameters(start_simulation_index + len(iContactAlongWidth_From_to_consider), pair, pair+len(iContactAlongWidth_From_to_consider)+1,
                                                   iContactAlongHeight_From_to_consider, iContactAlongHeight_To_to_consider,
                                                   M, length_short_circuit,
                                                   dict_LEDET, magnet_name_short_circuit, list_software,
                                                   path_file_model_geometry, aSTEAM, df_M12, verbose)
        list_M12 = np.append(list_M12, M_new[0, 1])


    ######################## Analyze mutual inductances M12 for the different cases ########################
    # Sort the dataframe rows based on the value of the mutual inductance M12
    # df_M12 = df_M12.sort_values(by='M12')  # DISABLED
    n_short_circuit_positions = len(df_M12)

    # Calculate median value and percentile distribution of M12
    range_percentiles = range(1, 101)
    range_percentiles_10 = list(np.linspace(0, 100, num=11))
    M12_median = np.percentile(df_M12['M12'], 50)
    M12_percentiles = [np.percentile(df_M12['M12'], p) for p in range_percentiles]
    M12_percentiles_10 = [np.percentile(df_M12['M12'], p) for p in range_percentiles_10]


    ######################## Select simulations to write and run ########################
    # Identify list of simulations to prepare (Note: first index is 1)
    # Note: All model objects will still be present when the analysis is run, but no output simulation files will be generated unless they are listed in "list_simulations_to_prepare"
    # n_sims_percentile_M12_100 = 11  # Number of simulations to select evenly distributed across 100% of the values of M12
    # n_sims_percentile_M12_50 = 11   # Number of simulations to select evenly distributed across  50% of the values of M12
    # n_sims_along_conductor = 17  # Number of simulations to select evenly distributed along the coil conductor. Note: A good choice is a prime number to avoid repeating similar simulations due to symmetry
    # list_simulations_manually_added = [1, 2, 1128, 3678, 3679]  # this allows setting desired simulations in addition to those automatically selected
    list_simulations_manually_added = [i+(start_simulation_index-1) for i in list_simulations_manually_added]  # TODO better way?
    # Add n_sims_percentile_M12_100 simulations evenly distributed across 100% of the values of M12 #TODO these lists should also depend on start_simulation_index
    list_sims_percentile_M12_100 = list(df_M12.index[np.round(np.linspace(1, n_short_circuit_positions, num=n_sims_percentile_M12_100) - 1).astype(int)])
    # Add n_sims_percentile_M12_50 simulations evenly distributed across 50% of the values of M12
    list_sims_percentile_M12_50 = list(df_M12.index[np.round(np.linspace(1, np.round(n_short_circuit_positions/2), num=n_sims_percentile_M12_50) - 1).astype(int)])

    # Select the n_sims_along_conductor simulations evenly distributed along the coil conductor. Short along the conductor long side (i.e. width)
    idx_selected_half_turn_reordered = np.round(np.linspace(1, n_turns*2, num=n_sims_along_conductor) - 1).astype(int)  # in electrical order
    list_sims_along_conductor = []
    for idx in idx_selected_half_turn_reordered:
        idx_turn_reordered = int(np.floor(idx / 2))
        idx_half_turn = min(np.array(dict_LEDET['el_order_half_turns'])[idx_turn_reordered * 2], np.array(dict_LEDET['el_order_half_turns'])[idx_turn_reordered * 2 + 1])  # in STEAM order
        if idx_half_turn <= len(iContactAlongWidth_From_to_consider):
            list_sims_along_conductor.append(iContactAlongWidth_From_to_consider[idx_half_turn] + (start_simulation_index-1))  # Since the cases are ordered adding first shorts across the width, and then across the height, the index does not need to be modified
        else:
            print(f'WARNING: The short-circuit position at half-turn #{idx_half_turn} was not generated because the list iContactAlongWidth_From_to_consider has length {len(iContactAlongWidth_From_to_consider)}.')  # This case only happens if the list is manually shortened to run a faster analysis

    # Add together all automatically and manually selected simulations
    list_simulations_to_prepare_all = list_sims_percentile_M12_100 + list_sims_percentile_M12_50 + list_sims_along_conductor + list_simulations_manually_added
    # Remove duplicates and transform all elements to int
    list_simulations_to_prepare_all = unique(list_simulations_to_prepare_all)

    # Set which simulations must be re-generated
    if flag_reprepare_sim:
        list_simulations_to_prepare = [int(i) for i in list_simulations_to_prepare_all]
        if verbose:
            print(f'List of selected simulations to prepare: {list_simulations_to_prepare}')
    else:
        list_simulations_to_prepare = []

    # Set which simulations must be run
    if flag_rerun_sim:
        list_simulations_to_run = list_simulations_to_prepare  #[3678]  # first index is 1
        if verbose:
            print(f'List of selected simulations to run: {list_simulations_to_run}')
    else:
        list_simulations_to_run = []

    ######################## Plot pre-processing variables ########################
    if flag_plots:
        fig = plt.figure(figsize=default_figsize)
        plt.plot(M12_percentiles, range_percentiles, 'ko-')
        plt.plot(M12_percentiles_10, range_percentiles_10, 'ro')
        plt.legend(['M12', 'M12 - selected 11 values'])
        plt.xlabel('Mutual inductance M12 per unit length [H/m]', **selectedFont)
        plt.ylabel('Percentile [%]', **selectedFont)
        plt.title(f'{magnet_name} - Percentile distribution of M12')
        plt.grid(which='both')
        fig.savefig(Path(output_folder_figures, f'{magnet_name_short_circuit}_M12_percentile_distribution.png'), format='png')

        # Read model geometry from .mat file
        with h5py.File(path_file_model_geometry, 'r') as simulationSignals:
            XY_in_mm = np.array(simulationSignals['model_geometry']['XY_MAG_ave'])  # in [mm]
        x_conductors, y_conductors = XY_in_mm[:][0]/1000, XY_in_mm[:][1]/1000  # in [m]

        # Plot conductor positions in the coil cross-section and short-circuit positions considered in the analysis
        # Note: All short-circuit positions are displayed, and not only those that are selected to be simulated
        colors_jet = plt.cm.jet(np.linspace(0, 1, len(list_simulations_to_prepare_all)))  # jet color map to use when plotting n_short_circuit_positions curves
        fig = plt.figure(figsize=default_figsize)
        plt.scatter(x_conductors, y_conductors, 10, 'k')
        for p, pair in enumerate(list_simulations_to_prepare_all):
            if pair in df_M12.index:
                idx_ht_from, idx_ht_to = df_M12['idx_ht_from (STEAM order)'][pair]-1, df_M12['idx_ht_to (STEAM order)'][pair]-1
                plt.plot([x_conductors[idx_ht_from], x_conductors[idx_ht_to]], [y_conductors[idx_ht_from], y_conductors[idx_ht_to]], '-', color=colors_jet[p], label=f'#{pair-(start_simulation_index-1)}')
            else:
                print(f'WARNING: Pair #{pair} was not plotted.')
        plt.legend(loc='best')
        # plt.legend(['M12', 'M12 - selected 11 values'])
        plt.xlabel('x [m]', **selectedFont)
        plt.ylabel('y [m]', **selectedFont)
        plt.title(f'{magnet_name} - Conductor positions')
        plt.axis('square')
        plt.grid(which='both')
        fig.savefig(Path(output_folder_figures, f'{magnet_name_short_circuit}_short_circuit_locations_{start_simulation_index}.png'), format='png')


    ######################## Write or update the simulation summary file ########################
    #TODO Known issue: if the csv file is updated by appending simulations, should a new copy of the analysis file be made (only with the newly added sims)?

    # Write lists of simulations to prepare and to run in the AnalysisSTEAM object
    set_simulations_to_prepare_run(aSTEAM, list_simulations_to_prepare, list_simulations_to_run, magnet_name_short_circuit, list_software, verbose)

    # For conveniency, add a column to the dataframe that indicates whether each simulation will be generated and/or run
    col_flag_sims_to_prepare = [df_M12.index[i] in list_simulations_to_prepare for i in range(n_short_circuit_positions)]
    col_flag_sims_to_run = [df_M12.index[i] in list_simulations_to_run for i in range(n_short_circuit_positions)]
    df_M12.insert(loc=0, column='to prepare', value=col_flag_sims_to_prepare)  # Add this flag in the 1st column (after the index column)
    df_M12.insert(loc=1, column='to run', value=col_flag_sims_to_run)  # Add this flag in the 2nd column (after the index column)

    # Add short-circuit parameters used in the analysis
    df_M12['R_short_circuit [Ohm]'] = R_short_circuit
    df_M12['length_short_circuit [m]'] = length_short_circuit
    df_M12['RRR [-]'] = RRR
    df_M12['Jc_fit_C1_CUDI1 [A]'] = Jc_fit_C1_CUDI1
    df_M12['Jc_fit_C2_CUDI1 [A/t]'] = Jc_fit_C2_CUDI1
    df_M12['scale_cooling_to_heat_sink [-]'] = scale_cooling_to_heat_sink
    df_M12['scale_heat_diffusion_between_turns [-]'] = scale_heat_diffusion_between_turns

    # Write the dataframe in a .csv file
    if flag_append and os.path.isfile(path_output_file_M12):
        df_M12.to_csv(path_or_buf=path_output_file_M12, sep=',', mode='a', header=False)  #TODO index column not updated properly (it starts from 1, not from N+1)
    else:
        df_M12.to_csv(path_or_buf=path_output_file_M12, sep=',', mode='w', header=True)
    if verbose:
        print(f'File {path_output_file_M12} saved.')
        toc()


    ######################## Write output files ########################
    # Write the STEAM analysis data to a yaml file
    aSTEAM.write_analysis_file(path_output_file=path_output_file_analysis)
    if verbose: toc()

    ######################## Run STEAM analysis ########################
    # Note: To make sure the automatically-generated STEAM analysis yaml file is a valid one, the analysis is run from the yaml file and not from the aSTEAM object
    bSTEAM = AnalysisSTEAM(file_name_analysis=path_output_file_analysis, verbose=True)
    if verbose: toc()
    bSTEAM.run_analysis()
    if verbose:
        print(f'Analysis {path_output_file_analysis} performed.')
        toc()

    #
    # # print(M.size)
    # print(el_order_half_turns)
    # # print(el_order_turns)
    # print(idx_shorted_half_turns)
    # print(idx_shorted_half_turns_reordered)
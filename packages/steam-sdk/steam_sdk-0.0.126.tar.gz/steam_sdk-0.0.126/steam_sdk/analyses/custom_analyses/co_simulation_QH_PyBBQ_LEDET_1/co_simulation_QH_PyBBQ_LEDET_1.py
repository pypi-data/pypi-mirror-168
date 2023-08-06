import numpy as np
import os
import yaml
from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.data.DataAnalysis import DataAnalysis
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.parsers.ParserYAML import dict_to_yaml
from steam_sdk.parsers.ParserCsv import get_signals_from_csv
from steam_sdk.data.DataModelConductor import DataModelConductor
from typing import Dict

def __cpNbTi_cudi_mat(T, B):

    Tc0 = 9.2
    Bc20 = 14.5
    alpha = .59
    if B >= Bc20:
        B = Bc20-10E-4
    Tc = Tc0 * (1 - B / Bc20)**alpha

    p1 = [0.00000E+00,    4.91000E+01,   0.00000E+00,   6.40000E+01,  0.00000E+00]
    p2 = [0.00000E+00,   1.62400E+01,   0.00000E+00,  9.28000E+02,   0.00000E+00]
    p3 = [-2.17700E-01,   1.19838E+01,   5.53710E+02, - 7.84610E+03,  4.13830E+04]

    if T <= Tc:
        cpNbTi = p1[0] * T**4 + p1[1] * T**3 + p1[2] * T**2 + p1[3] * T + p1[4]
    elif (T > Tc) & (T <= 20.0):
        cpNbTi = p2[0] * T**4 + p2[1] * T**3 + p2[2] * T**2 + p2[3] * T + p2[4]
    elif (T > 20) & (T <= 50):
        cpNbTi = p3[0] * T**4 + p3[1] * T**3 + p3[2] * T**2 + p3[3] * T + p3[4]

    return cpNbTi

def __cpCu_nist_mat(T):
    density = 8960
    if T < 4:
        T = 4
    dc_a = -1.91844
    dc_b = -0.15973
    dc_c = 8.61013
    dc_d = -18.996
    dc_e = 21.9661
    dc_f = -12.7328
    dc_g = 3.54322
    dc_h = -0.3797

    logT1 = np.log10(T)
    tempVar = \
        dc_a + dc_b * (logT1) ** 1 + dc_c * (logT1) ** 2 + dc_d * (logT1) ** 3 + \
        dc_e * (logT1) ** 4 + dc_f * (logT1) ** 5 + dc_g * (logT1) ** 6 + dc_h * (logT1) ** 7
    cpCu_perMass = 10 ** tempVar

    cpCu = density * cpCu_perMass
    return cpCu

def __cpNb3Sn_alternative_mat(T, B, Tc0_Nb3Sn: float = 0.0, Bc20_Nb3Sn: float = 0.0):
    B[B < .001] = 0.001
    alpha = 0.59
    Tc = Tc0_Nb3Sn * (1 - B / Bc20_Nb3Sn) ** alpha
    density = 8950.0  # [kg / m ^ 3]

    betaT = 1.241E-3  # [J / K ^ 4 / kg]
    gammaT = .138  # [J / K ^ 2 / kg]

    if T <= Tc:
        cpNb3Sn = (betaT + 3 * gammaT / Tc0_Nb3Sn ** 2) * T ** 3 + gammaT * B / Bc20_Nb3Sn * T
    elif (T > Tc) & (T <= 20):
        cpNb3Sn = betaT * T ** 3 + gammaT * T
    elif (T > 20) & (T <= 400):
        polyFit_20K_400K = [0.1662252, -0.6827738, -6.3977, 57.48133, -186.90995, 305.01434, -247.44839, 79.78547]
        logT = np.log10(T)
        logCp2 = np.polyval(polyFit_20K_400K, logT)
        cpNb3Sn = 10 ** logCp2

    cpNb3Sn = cpNb3Sn * density

    return cpNb3Sn

def __Jc_Nb3Sn_Summer(T, B, Jc_Nb3Sn0: float = 0.0, Tc0_Nb3Sn: float = 0.0, Bc20_Nb3Sn: float = 0.0):

    if type(T) == int or type(T) == float:
        T = np.repeat(T, len(Jc_Nb3Sn0)).astype(float)

    B[abs(B) < .001] = 0.001
    T[T < 0.001] = 0.001
    f_T_T0 = T / Tc0_Nb3Sn
    f_T_T0[f_T_T0 > 1] = 1
    Bc2 = Bc20_Nb3Sn * (1 - f_T_T0 ** 2) * (1 - 0.31 * f_T_T0 ** 2 * (1 - 1.77 * np.log(f_T_T0)))
    f_B_Bc2 = B / Bc2
    f_B_Bc2[f_B_Bc2 > 1] = 1
    Jc_T_B = Jc_Nb3Sn0 / np.sqrt(B) * (1 - f_B_Bc2) ** 2 * (1 - f_T_T0 ** 2) ** 2
    return Jc_T_B

def __Tc_Tcs_Nb3Sn_approx(J, B, Jc_Nb3Sn0: float = 0.0, Tc0_Nb3Sn: float = 0.0, Bc20_Nb3Sn: float = 0.0):
    J = abs(J)
    B = abs(B)

    f_B_Bc2 = B / Bc20_Nb3Sn
    f_B_Bc2[f_B_Bc2 > 1] = 1
    Tc = Tc0_Nb3Sn * (1 - f_B_Bc2)**.59

    Jc0 = __Jc_Nb3Sn_Summer(0, B, Jc_Nb3Sn0, Tc0_Nb3Sn, Bc20_Nb3Sn)
    f_J_Jc0 = J/ Jc0
    f_J_Jc0[f_J_Jc0 > 1] = 1

    Tcs = (1 - f_J_Jc0) * Tc

    return [Tc, Tcs]

def _quenchPropagationVelocity(I, B, T_bath, A_CableInsulated, f_SC, f_ST, idxNbTi, idxNb3Sn, Tc0_NbTi, Bc20_NbTi, c1_Ic_NbTi, c2_Ic_NbTi, Jc_Nb3Sn0, Tc0_Nb3Sn, Bc20_Nb3Sn):

    # Calculate Quench propagation velocity
    L0 = 2.44E-08
    A_CableBare = A_CableInsulated * (f_SC + f_ST)
    f_SC_inStrand = f_SC / (f_SC + f_ST)
    f_ST_inStrand = f_ST / (f_SC + f_ST)
    I = abs(I)
    J_op = I / A_CableBare
    A_SC = A_CableInsulated * f_SC

    if idxNbTi == 1:
        Tc = Tc0_NbTi * (1 - B / Bc20_NbTi) ** 0.59
        Tcs = (1 - I / (c1_Ic_NbTi + c2_Ic_NbTi * B)) * Tc
    if idxNb3Sn == 1:
        [Tc, Tcs] = __Tc_Tcs_Nb3Sn_approx(I / A_SC, B, Jc_Nb3Sn0, Tc0_Nb3Sn, Bc20_Nb3Sn)

    Ts = (Tcs + Tc) / 2
    cp_ST = __cpCu_nist_mat(Ts)

    if idxNbTi == 1:
        cp_SC = __cpNbTi_cudi_mat(Ts, B)
    if idxNb3Sn == 1:
        cp_SC = __cpNb3Sn_alternative_mat(Ts, B, Tc0_Nb3Sn, Bc20_Nb3Sn)

    cp = cp_ST * f_ST_inStrand + cp_SC * f_SC_inStrand
    vQ = J_op / cp * ((L0 * Ts) / (Ts - T_bath))**0.5

    return vQ

def co_simulation_QH_PyBBQ_LEDET(dict_inputs: Dict):

    # unpack inputs
    magnet_name = dict_inputs['magnet_name']
    heater_numbers_active = dict_inputs['heater_numbers_active']
    turn_number_quench = dict_inputs['turn_number_quench']
    quench_time = dict_inputs['quench_time']

    # inputs to be changed
    file_name_analysis_cond = 'analysis_MBRD_co_simulation_conductor_custom.yaml'
    file_name_analysis_mag = 'analysis_MBRD_co_simulation_magnet_custom.yaml'

    # running PyBBQ simulations
    aSTEAM = AnalysisSTEAM(file_name_analysis=file_name_analysis_cond, verbose=True)
    aSTEAM.run_analysis()

    # Read magnet file
    if os.path.isfile(file_name_analysis_mag):
        # Load yaml keys into DataAnalysis dataclass
        with open(file_name_analysis_mag, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            model_data = DataAnalysis(**dictionary_yaml)
        file_model_data_output = file_name_analysis_mag
        all_data_dict_LEDET = {**model_data.dict()}

    # Read conductor file
    if os.path.isfile(file_name_analysis_cond):
        # Load yaml keys into DataAnalysis dataclass
        with open(file_name_analysis_cond, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            model_data = DataAnalysis(**dictionary_yaml)
        all_data_dict_PyBBQ = {**model_data.dict()}

    # Read model_data_magnet file
    model_data_path = os.path.realpath(os.path.join(os.path.dirname(__file__),'..', '..', 'steam_models', 'magnets', magnet_name, 'input', 'modelData_' + magnet_name + '.yaml'))
    if os.path.isfile(model_data_path):
        # Load yaml keys into DataAnalysis dataclass
        with open(model_data_path, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            model_data = DataModelMagnet(**dictionary_yaml)
        all_data_dict_model = {**model_data.dict()}

    # Read model_data_conductor file
    model_data_conductor_path = os.path.realpath(os.path.join(os.path.dirname(__file__),'..', '..', 'steam_models', 'conductors', magnet_name + '_conductor', 'input', 'modelData_' + magnet_name + '_conductor.yaml'))
    if os.path.isfile(model_data_conductor_path):
        # Load yaml keys into DataAnalysis dataclass
        with open(model_data_conductor_path, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            model_data_conductor = DataModelConductor(**dictionary_yaml)
        all_data_dict_model_conductor = {**model_data_conductor.dict()}

    # getting variables from model_data
    heater_length = all_data_dict_model['Quench_Protection']['Quench_Heaters']['l']
    l_copper = all_data_dict_model['Quench_Protection']['Quench_Heaters']['l_copper']
    l_steel = all_data_dict_model['Quench_Protection']['Quench_Heaters']['l_stainless_steel']
    heater_turns = all_data_dict_model['Quench_Protection']['Quench_Heaters']['iQH_toHalfTurn_To']
    heater_number = all_data_dict_model['Quench_Protection']['Quench_Heaters']['iQH_toHalfTurn_From']
    T_bath = all_data_dict_model['GeneralParameters']['T_initial']
    fraction_cover = all_data_dict_model['Quench_Protection']['Quench_Heaters']['f_cover']

    # getting cable data
    A_CableInsulated = (all_data_dict_model['Conductors'][0]['cable']['bare_cable_width']+all_data_dict_model['Conductors'][0]['cable']['th_insulation_along_width']) * (all_data_dict_model['Conductors'][0]['cable']['bare_cable_height_mean']+all_data_dict_model['Conductors'][0]['cable']['th_insulation_along_height'])
    f_SC = 1/(all_data_dict_model['Conductors'][0]['strand']['Cu_noCu_in_strand']+1)
    f_ST = 1-f_SC
    f_SC = f_SC * all_data_dict_model['Conductors'][0]['cable']['bare_cable_width'] * all_data_dict_model['Conductors'][0]['cable']['bare_cable_height_mean'] * (1-all_data_dict_model['Conductors'][0]['cable']['f_inner_voids']-all_data_dict_model['Conductors'][0]['cable']['f_outer_voids'])/A_CableInsulated
    f_ST = f_ST * all_data_dict_model['Conductors'][0]['cable']['bare_cable_width'] * all_data_dict_model['Conductors'][0]['cable']['bare_cable_height_mean'] * (1-all_data_dict_model['Conductors'][0]['cable']['f_inner_voids']-all_data_dict_model['Conductors'][0]['cable']['f_outer_voids'])/A_CableInsulated

    Tc0_NbTi = 0
    Bc20_NbTi = 0
    c1_Ic_NbTi = 0
    c2_Ic_NbTi = 0
    Jc_Nb3Sn0 = 0
    Tc0_Nb3Sn = 0
    Bc20_Nb3Sn = 0

    if all_data_dict_model['Conductors'][0]['strand']['material_superconductor'] == 'Nb-Ti':
        idxNbTi = 1
        idxNb3Sn = 0
        Tc0_NbTi = all_data_dict_model['Conductors'][0]['Jc_fit']['Tc0_CUDI1']
        Bc20_NbTi = all_data_dict_model['Conductors'][0]['Jc_fit']['Bc20_CUDI1']
        c1_Ic_NbTi = all_data_dict_model['Conductors'][0]['Jc_fit']['C1_CUDI1']
        c2_Ic_NbTi = all_data_dict_model['Conductors'][0]['Jc_fit']['C2_CUDI1']
    else:
        idxNbTi = 0
        idxNb3Sn = 1
        Jc_Nb3Sn0 = all_data_dict_model['Conductors'][0]['Jc_fit']['Jc0_Summers']
        Tc0_Nb3Sn = all_data_dict_model['Conductors'][0]['Jc_fit']['Tc0_Summers']
        Bc20_Nb3Sn = all_data_dict_model['Conductors'][0]['Jc_fit']['Bc20_Summers']

    # getting simulation numbers from PyBBQ input
    number_sims = all_data_dict_PyBBQ['AnalysisStepDefinition']['RunSimList_PyBBQ']['simulation_numbers']

    for i in range(len(number_sims)):
        # initializing scaling_vq, length_HotSpot and timeOfQuench
        scaling_vq = all_data_dict_model['Options_LEDET']['quench_initiation']['fScaling_vQ_iStartQuench']
        scaling_vq = np.ones(len(scaling_vq))
        length_HotSpot = all_data_dict_model['Options_LEDET']['quench_initiation']['lengthHotSpot_iStartQuench']
        length_HotSpot = np.zeros(len(length_HotSpot))
        time_of_quench = all_data_dict_model['Options_LEDET']['quench_initiation']['tStartQuench']

        # reading current from input and calculating magnetic field
        current = all_data_dict_PyBBQ['AnalysisStepDefinition']['modifyModel_' + str(i+1)]['variables_value'][-1][0][0]
        B = current * all_data_dict_model_conductor['Options_PyBBQ']['magnetic_field']['Self_Field']

        # initializing path for PyBBQ output
        simulation_name = all_data_dict_PyBBQ['AnalysisStepDefinition']['setup_folder_LEDET']['simulation_name']
        simulation_number = str(all_data_dict_PyBBQ['AnalysisStepDefinition']['modifyModel_' + str(i+1)]['simulation_numbers'][0])
        input_folder = os.path.join(all_data_dict_LEDET['PermanentSettings']['local_PyBBQ_folder'] + simulation_name, simulation_number, 'Output', 'Results - 0.21', simulation_name, 'summary.csv')

        # reading vq from PyBBQ output
        vQ_PyBBQ = get_signals_from_csv(input_folder, 'NZPV [m/s]')
        vQ_PyBBQ = vQ_PyBBQ['NZPV[m/s]'].iloc[0]
        print('NZPV calculated by PyBBQ is %s' % vQ_PyBBQ)

        # calculating vq with analytic formula
        vQ_analytic = _quenchPropagationVelocity(current, B, T_bath, A_CableInsulated, f_SC, f_ST, idxNbTi, idxNb3Sn, Tc0_NbTi, Bc20_NbTi, c1_Ic_NbTi, c2_Ic_NbTi, Jc_Nb3Sn0, Tc0_Nb3Sn, Bc20_Nb3Sn)
        print('NZPV calculated with the analytic formula is %s' % vQ_analytic)

        # # calculating scaling_vq depending on geometry of heater stations
        # for j in range(len(heater_turns)):
        #     new_scale_vq = round(2 * vQ_PyBBQ / vQ_analytic * round(heater_length[heater_number[j]-1] / (l_copper[heater_number[j]-1] + l_steel[heater_number[j]-1]), 0), 2)
        #     scaling_vq[heater_turns[j]-1] = new_scale_vq

        # calculating scaling_vq depending on geometry of heater stations
        # calculating fraction of turns covered by heater
        # only active heaters are considered
        for n in range(len(heater_numbers_active[i])):
            new_scale_vq = round(2 * vQ_PyBBQ / vQ_analytic * round(heater_length[heater_numbers_active[i][n] - 1] / (l_copper[heater_numbers_active[i][n] - 1] + l_steel[heater_numbers_active[i][n] - 1]), 0), 2)
            new_length_HotSpot = heater_length[heater_numbers_active[i][n] - 1] * fraction_cover[heater_numbers_active[i][n] - 1]
            for j in range(len(heater_turns)):
                if heater_numbers_active[i][n] == heater_number[j]:
                    # 1, 2, -1, -2 for setting scaling_vq and length_HotSpot also to adjacent turns
                    scaling_vq[heater_turns[j]] = new_scale_vq
                    scaling_vq[heater_turns[j] -1] = new_scale_vq
                    scaling_vq[heater_turns[j] - 2] = new_scale_vq
                    scaling_vq[heater_turns[j] + 1] = new_scale_vq
                    scaling_vq[heater_turns[j] + 2] = new_scale_vq
                    length_HotSpot[heater_turns[j]] = new_length_HotSpot
                    length_HotSpot[heater_turns[j] - 1] = new_length_HotSpot
                    length_HotSpot[heater_turns[j] - 2] = new_length_HotSpot
                    length_HotSpot[heater_turns[j] + 1] = new_length_HotSpot
                    length_HotSpot[heater_turns[j] + 2] = new_length_HotSpot

        print('The new scaling factor is %s' % new_scale_vq)

        # making scaling_vq a list and changing type from float64 to float
        scaling_vq = list(scaling_vq)
        scaling_vq = [float(x) for x in scaling_vq]
        length_HotSpot = list(length_HotSpot)
        length_HotSpot = [float(x) for x in length_HotSpot]
        time_of_quench = list(time_of_quench)
        time_of_quench = [float(x) for x in time_of_quench]

        # setting a turn to quench
        if turn_number_quench:
            time_of_quench[turn_number_quench-1] = quench_time
            length_HotSpot[turn_number_quench-1] = 0.01
            scaling_vq[turn_number_quench-1] = 2

        # Write file for LEDET input
        modify_model = 'modifyModel_'+str(2*(i+1))
        all_data_dict_LEDET['AnalysisStepDefinition'][modify_model]['variables_value'] = [[length_HotSpot], [scaling_vq], [time_of_quench]]
        dict_to_yaml(all_data_dict_LEDET, file_model_data_output, list_exceptions=[])

    # running LEDET simulations
    aSTEAM = AnalysisSTEAM(file_name_analysis=file_name_analysis_mag, verbose=True)
    aSTEAM.run_analysis()
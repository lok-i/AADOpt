# AADOpt
- A Framework for Antenna Array Design and Synthesis through Optimisation
<p align="center">
   <img width="260" height="280" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/100Patch_20Gen_None.gif">
   <img width="260" height="280" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/25Patch_25Gen_Spiral2.gif">
   <img width="260" height="280" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/20Patch_100Gen_None.gif">
</p>

<p align="center">
   <img width="260" height="260" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/BTP_00001.gif">
   <img width="260" height="260" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/BTP_00002.gif">
   <img width="260" height="260" src="https://github.com/lok-i/AADOpt/blob/main/plots_figs/BTP_00003.gif">
</p>

## Installation
    git clone https://github.com/lok-i/AADOpt
    cd AADOpt
    pip3 install -r requirements.txt

## To visualise a given experiment

Set the name and configuration of the experiment that you want to test in the file, [config.py](https://github.com/lok-i/AADOpt/blob/main/config.py) file, For example,

    PATCH_TOPOLOGY =  'Spiral2'
    NO_OF_GENERATIONS = 25
    NO_OF_PATCHES = 25 

Then simply run the following command, and the experiment file will be loaded from the experiments folder and the results will be displayed

    python3 readOptimalParams.py

## To run a GA optimisation with custom parameters

Set the name and configuration of the experiment that you want to conduct in the file, config.py. Like

    1) GA Optimisation Parameters
    2) Antena Parameter Ranges
    3) Topological Distribution Function

Based on the current configuration in the config.py, the optimisation will then be conducted and the results shall be saved to ./experiments upon running the following command

    python3 runGA.py 

Note: For implementing your own antenna distribution topology, implement a class title _class topolocy_name_ in the file [./src/PatchTopology.py](https://github.com/lok-i/AADOpt/blob/main/src/PatchTopology.py) and requireed additions in [config.py](https://github.com/lok-i/AADOpt/blob/main/config.py). Refer the same files for pre-implemented examples. For a detailed overview chekcout out our [preprint/mid-report](https://drive.google.com/file/d/1wmBMNA6xBBsBHSVZ0LFgiTTHsTuxB1yn/view?usp=sharing)








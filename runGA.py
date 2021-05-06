import pygad
import numpy
from src.AntennaArray import PatchAntennaArray
from src.PatchTopology import *
import time

# EXPERIMENTE PARAMETERS

PATCH_TOPOLOGY =  'None'# None
NO_OF_GENERATIONS = 100
NO_OF_PATCHES = 5 # give a perfect square for grid


# -----------------------------------------------------------------

delta_angle_for_integration = 2 #keep it 1 for a better surface plot

if 'None' in str(PATCH_TOPOLOGY):

    # only XYZ
    if 'XYZ' in str(PATCH_TOPOLOGY):
        param_opt_range = {'x':{'greater_than':-0.25,'lesser_than':0.25},
                        'y':{'greater_than':-0.25,'lesser_than':0.25},
                        'z':{'equal_to':0.},
                        'A':{'greater_than':0.,'lesser_than':5.},
                        'beta':{'equal_to':0.},
                        'W':{'equal_to':10.7e-3},
                        'L':{'equal_to':10.47e-3},
                        'h':{'equal_to':3e-3},
                            }

    # XYZ + WLH
    else:
        param_opt_range = {'x':{'greater_than':-0.1,'lesser_than':0.1},
                      'y':{'greater_than':-0.1,'lesser_than':0.1},
                      'z':{'equal_to':0.},
                      'A':{'greater_than':0.,'lesser_than':5.},
                      'beta':{'equal_to':0.},
                      'W':{'greater_than':1.0e-3,'lesser_than':10.7e-3},
                      'L':{'greater_than':1.0e-3,'lesser_than':10.47e-3},
                      'h':{'greater_than':1.0e-3,'lesser_than':3e-3},}
else:
    if PATCH_TOPOLOGY == 'Grid':
        PatchDist = Grid(
                    n_patches=NO_OF_PATCHES,
                    Wmax=20.47e-3,
                    Lmax=10.47e-3,
                    clearence= 10.47e-3
                    )

    elif PATCH_TOPOLOGY == 'Spiral':
        PatchDist = Spiral(
                    n_patches=NO_OF_PATCHES,
                    Wmax=20.47e-3,
                    Lmax=10.47e-3,
                    clearence= 10.47e-3
                    )
    elif PATCH_TOPOLOGY == 'Spiral2':
        PatchDist = Spiral2(
                    n_patches=NO_OF_PATCHES,
                    Wmax=20.47e-3,
                    Lmax=10.47e-3,
                    clearence= 10.47e-3
                    )



    x_pos,y_pos = PatchDist.get_path_pos()

    param_opt_range = { 'x':{'equal_to':x_pos},
                        'y':{'equal_to':y_pos},
                        'z':{'equal_to':0},
                        'A':{'greater_than':0.,'lesser_than':5.},
                        'beta':{'equal_to':0.},
                        'W':{'greater_than':1.0e-3,'lesser_than':PatchDist.Wmax},
                        'L':{'greater_than':1.0e-3,'lesser_than':PatchDist.Lmax},
                        'h':{'greater_than':1.0e-3,'lesser_than':3e-3}}

PatchArray = PatchAntennaArray(
                                n_patches=NO_OF_PATCHES,
                                Freq=14e9,
                                Er=2.5,
                                param_range=param_opt_range
                                )

# print('initial_elements:\n',PatchArray.element_array)
# update_to = [0.,0.,1.,0.,0.,1.]
# PatchArray.update_array_params(update_to)
# print('updates_elements:\n',PatchArray.element_array)

steps_per_gen = 0
no_of_generations_done = 0
def fitness_func(solution, solution_idx):
    global steps_per_gen 
    global no_of_generations_done
    steps_per_gen +=1
    # print(steps_per_gen)
    if steps_per_gen%sol_per_pop == 0:
        steps_per_gen = 0
        no_of_generations_done += 1
        print("Generation:",no_of_generations_done)
    PatchArray.CalculateFieldSumPatch(dAngleInDeg=delta_angle_for_integration)
    PatchArray.update_array_params(solution)
    fitness = PatchArray.get_gain(dAngleInDeg=delta_angle_for_integration)
    return fitness

fitness_function = fitness_func

num_generations = NO_OF_GENERATIONS # Number of generations.
num_parents_mating = 15 # Number of solutions to be selected as parents in the mating pool.

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 25 # Number of solutions in the population.
num_genes = len(PatchArray.params_to_opt_range)

gene_ranges = [{'low':p_2_opt_range[0],'high':p_2_opt_range[1]} for p_2_opt_range in PatchArray.params_to_opt_range]
parent_selection_type = "sss" # Type of parent selection.
keep_parents = 10 # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.
crossover_type = "single_point" # Type of the crossover operator.
# Parameters of the mutation operation.
mutation_type = "random" # Type of the mutation operator.
mutation_percent_genes = 10 # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists or when mutation_type is None.

print("Number of Params to Optimize:",num_genes)
print("Number of Patches to Optimize:",NO_OF_PATCHES)
print("TOPOLOGY:",PATCH_TOPOLOGY,'\n')




if __name__ == "__main__":




    ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating, 
                        fitness_func=fitness_function,
                        sol_per_pop=sol_per_pop, 
                        num_genes=num_genes,
                        parent_selection_type=parent_selection_type,
                        keep_parents=keep_parents,
                        crossover_type=crossover_type,
                        mutation_type=mutation_type,
                        mutation_percent_genes=mutation_percent_genes,
                        #    on_generation=callback_generation,
                        gene_space = gene_ranges,
                        save_best_solutions=True
                        )
    # print(ga_instance.initial_population)
    # Running the GA to optimize the parameters of the function.
    ga_instance.run()

    # After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
    #ga_instance.plot_result()




    # print("BEST SOLNS:",ga_instance.best_solutions)
    # Returning the details of the best solution.
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))


    if ga_instance.best_solution_generation != -1:
        print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

    # Saving the GA instance.
    filename = './experiments/'+str(NO_OF_PATCHES)+'Patch_'+str(NO_OF_GENERATIONS)+'Gen_'+str(PATCH_TOPOLOGY) # The filename to which the instance is saved. The name is without extension.
    ga_instance.save(filename=filename)

    # Loading the saved GA instance.
    # loaded_ga_instance = pygad.load(filename=filename)
    # loaded_ga_instance.plot_result()

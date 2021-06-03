import pygad
import numpy
from config import *

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

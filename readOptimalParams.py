import pygad
import numpy
from src.AntennaArray import PatchAntennaArray
from runGA import fitness_func,PatchArray

if __name__ == "__main__":
    
    # W,L,h,Er
    delta_angle_for_integration = 1

    filename = './experiments/5Patches'
    loaded_ga_instance = pygad.load(filename=filename)
    loaded_ga_instance.plot_result()

    # print("BEST SOLNS:")
    max_soln = []
    max_fitness = 0
    _ = 0
    for (soln,fitness) in zip(loaded_ga_instance.best_solutions,loaded_ga_instance.best_solutions_fitness):
        # print("Generation:",_,soln,"Score:",fitness)
        if max_fitness<fitness:
            max_fitness = fitness
            max_soln = soln
        _+=1
    
    # Returning the details of the best solution.


    # update_to = solution
    # solution, solution_fitness, solution_idx = loaded_ga_instance.best_solution()
    # print("Parameters of the best solution : {solution}".format(solution=solution))
    # print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    # print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))


    PatchArray.update_array_params(max_soln)
    print("Best Gain:",max_fitness)
    print("Best Params:\n",PatchArray.element_array)
    PatchArray.CalculateFieldSumPatch(dAngleInDeg=delta_angle_for_integration)
    print('Gain:',PatchArray.get_gain(dAngleInDeg=delta_angle_for_integration))
    PatchArray.plot_radiation_pattern()
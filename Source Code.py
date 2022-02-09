"""
The random module is used to choose a random variable if both the minimum
remaining value and degree heuristics could not choose one.
"""
import random

"""
The class below sets up a constraint-satisfaction problem using the
info found in the input file.
"""
class CSP():
    """
    The class is initialized using the variables, domain_values, and
    neighbors_dictionary read in from the input file. If forward-checking
    is set to true, the current_domains & pruned dictionaries are also set.
    """
    def __init__(self, variables, domain_values, neighbors_dictionary):
        self.current_domains = None
        self.conflicts = None
        self.number_assigned = 0
        self.variables = variables
        self.domain_values = domain_values
        self.neighbors_dictionary = neighbors_dictionary
        self.is_forward_checking = False
        self.assigned_variables = {}
    
    """
    The function below checks if two domain values are equal meaning
    if they are constrained are not.
    """
    def are_values_constrained(self, value1, value2):
        return value1 == value2

    """
    The function below assigns a variable with the passed in domain value and
    adds it to the assigned_variables dictionary. If forward-checking is set to
    true, the forward_checking function will change all the passed in variable's
    neighbors' domains.
    """
    def assign_variable(self, variable, value):
        self.assigned_variables[variable] = value
        self.number_assigned += 1
        
        if self.current_domains and self.is_forward_checking:
            self.forward_checking(variable, value)

    """
    The function below does all the necessary modifications to the neighbors'
    domains of the passed in variable.
    """
    def forward_checking(self, variable, value):
        if self.current_domains:
            """
            Restore conflicted values with neighbors, if any, to perform forward-checking
            correctly. It will only go inside this for loop if the algorithm back-tracked.
            """
            for (neighbor, val) in self.conflicts[variable]:
                self.current_domains[neighbor].append(val)
            self.conflicts[variable] = []
            """
            The section below performs the forward-checking itself. It loops through every
            neighbor of the passed-in variable and checks to see if the values in its domain
            conflict with the value assigned. If so, it will add the neighbor and the
            conflicting value to the list of conflicts for that variable. It will also remove
            the conflicting value from the neighbor's domain.
            """
            for neighbor in self.neighbors_dictionary[variable]:
                if neighbor not in self.assigned_variables:
                    for val in self.current_domains[neighbor][:]:
                        if self.are_values_constrained(value, val):
                            self.conflicts[variable].append((neighbor, val))
                            self.current_domains[neighbor].remove(val)

    """
    The function below calculates the number of conflicts the passed in value
    will have with all the passed in variable's neighbors and returns it.
    """
    def number_of_conflicts(self, variable, value):
        neighbor_value = ""
        count = 0
        for neighbor in self.neighbors_dictionary[variable]:
            if neighbor in self.assigned_variables:
                neighbor_value = self.assigned_variables[neighbor]
            if self.are_values_constrained(value, neighbor_value):
                count += 1
        return count

"""
The function below is a wrapper for the recursive algorithm itself. It also
takes in a boolean specifying whether forward-checking is set to true or not.
If forward-checking is set to true, the current_domains and pruned dictionaries
are set. 
"""
def backtracking_algorithm(csp, is_forward_checking = False):
    if is_forward_checking:
        csp.current_domains, csp.pruned = {}, {}
        for v in csp.variables:
            csp.current_domains[v] = csp.domain_values[v][:]
            csp.pruned[v] = []
        csp.is_forward_checking = True
    csp = csp
    return recursive_backtracking(csp)

"""
The function below is the recursive algorithm itself. It first checks to see if
all the variables have been assigned or not. If not, the algorithm will first pick
an unassigned variable. Then, it will check every domain value to see the number of
conflicts each has. It will only assign a variable to a specific value if the number
of conflicts it has is zero.
"""
def recursive_backtracking(csp):
    if len(csp.assigned_variables) == len(csp.variables):
        return csp.assigned_variables

    variable = select_unassigned_variable(csp)
    for value in order_domain_values(variable, csp):
        if csp.number_of_conflicts(variable, value) == 0:
            csp.assign_variable(variable, value)
            result = recursive_backtracking(csp)
            if result is not None:
                return result
    return None

"""
The function below selects an unassigned variable using the minimum-remaining-value
and degree heuristics.
"""
def select_unassigned_variable(csp):
    """
    This section below in the function is for the minimum-remaining-value heuristic.
    It checks to see the number of assigned neighbors each variable has. It then
    chooses the one with the most assigned neighbors, which corresponds to the
    variable with the least remaining values. 
    """
    minimum_remaining_values_list = []
    current_max = 0
    temp_max = 0
    for variable in csp.variables:
        if variable not in csp.assigned_variables:
            for neighbor in csp.neighbors_dictionary[variable]:
                if neighbor in csp.assigned_variables:
                    temp_max += 1
                if temp_max == current_max:
                    if len(minimum_remaining_values_list) > 0:
                        if minimum_remaining_values_list[-1] != variable:
                            minimum_remaining_values_list.append(variable)
                    else:
                        minimum_remaining_values_list.append(variable)
                elif temp_max > current_max:
                    minimum_remaining_values_list = [variable]
                    current_max = temp_max
                temp_max = 0
    """
    This section below works on the list of variables with the least remaining domain
    values from the previous section. It first checks if there is only one variable
    in the list, in that case it just returns it. If there is more than one variable
    in the list, the degree heuristic is applied. It creates a list of variables with
    the most neighbors. If there is only variable in the list, it is returned. If there
    is more than one variable, meaning both the minimum remaining value and the degree
    heuristics could not choose a variable, a random variable is chosen and returned.
    """
    if len(minimum_remaining_values_list) == 1:
        return minimum_remaining_values_list.pop()
    else:
        current_max = 0
        temp_max = 0
        max_neighbors = []
        for region in minimum_remaining_values_list:
            if len(csp.neighbors_dictionary[region]) == current_max:
                max_neighbors.append(region)
            elif len(csp.neighbors_dictionary[region]) > current_max:
                max_neighbors = [region]
                current_max = len(csp.neighbors_dictionary[region])
        return random.choice(max_neighbors)
    
"""
The function below returns each domain value one by one in the same order written in
the input file. If forward-checking is set to true, it returns each domain value one 
by one from the current variable's domain.
"""
def order_domain_values(variable, csp):
    if csp.current_domains:
        domain = csp.current_domains[variable]
    else:
        domain = csp.domain_values[variable][:]

    while domain:
        yield domain.pop()

"""
The function below reads the input file and returns a CSP object from the class above.
"""
def read_file(filename):
    file = open(filename,'r')
    temp = file.readline()
    temp = temp.split(' ')
    number_of_regions = int(temp[0])
    temp = file.readline()
    temp = temp.strip()
    variables = temp.split(' ')
    temp = file.readline()
    temp = temp.strip()
    domain_values = temp.split(' ')
    constraints_array = []

    for i in range(number_of_regions):
        temp = []
        temp = file.readline()
        temp = temp.strip()
        temp = temp.split(' ')
        for j in range(number_of_regions):
            temp[j] = int(temp[j])
        constraints_array.append(temp)
    
    domain_values.reverse()

    """
    This section below uses the constraints array given in the input file to create
    a dictionary containing the neighbors of each variable. 
    """
    neighbors_dictionary = {name:[] for name in variables}
    for i in range(number_of_regions):
        for j in range(number_of_regions):
            if constraints_array[i][j] == 1:
                if variables[j] not in neighbors_dictionary[variables[i]]:
                    neighbors_dictionary[variables[i]].append(variables[j])
                if variables[i] not in neighbors_dictionary[variables[j]]:
                    neighbors_dictionary[variables[j]].append(variables[i])

    return variables, CSP(neighbors_dictionary.keys(), {name:domain_values for name in variables}, neighbors_dictionary)

"""
The function below writes the result returned from the backtracking algorithm to the
output file.
"""
def write_file(variables, result, filename):
    file = open(filename,'w')
    for name in variables:
        if variables[-1] != name:
            file.write(name + ' = ' + result[name] + '\n')
        else:
            file.write(name + ' = ' + result[name])

"""
The function below is the main function that takes in an input file, an output file,
and an optional third argument for a boolean stating whether forward checking is
enabled or not.
"""
def main(input, output, is_forward_checking = False):
    variables, map = read_file(input)
    result = backtracking_algorithm(map, is_forward_checking)
    write_file(variables, result, output)

main("Input1.txt", "test_output.txt", True)
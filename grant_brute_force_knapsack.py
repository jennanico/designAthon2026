'''
Brute force algorithm for grant application problem
'''

import argparse
import parsecsv
import math

# Decimal to binary helper method that converts a decimal number to a binary number
def decimal_to_binary(decimal, applications_list) -> list:
    binary_number = []
    for i in range(len(applications_list)):
        if decimal % 2 == 0:
            binary_number.append(0)
        else:
            binary_number.append(1)
        decimal = decimal // 2
    return binary_number


# Score method: impact to cost ratio
def score_by_impact_to_cost_ratio(applications_list, binary_list) -> int:
    score = 0
    for i in range(len(applications_list)):
        if binary_list[i] == 1:
            score += applications_list[i].impact / applications_list[i].requested_money
    return score


# Score method: impact
def score_by_impact(applications_list, binary_list) -> int:
    score = 0
    for i in range(len(applications_list)):
        if binary_list[i] == 1:
            score += applications_list[i].impact
    return score


# Score method: people served
def score_by_people(applications_list, binary_list) -> int:
    score = 0
    for i in range(len(applications_list)):
        if binary_list[i] == 1:
            score += applications_list[i].people_served
    return score


# Calculate total cost of selected applications based on binary number
def calculate_total_cost(applications_list, binary_list) -> int:
    total_cost = 0
    for i in range(len(applications_list)):
        if binary_list[i] == 1:
            total_cost += applications_list[i].requested_money
    return total_cost


# Remove ineligible applications from consideration

#### Madeleine made changes to this- list was being edited during
#### iteration, causing an index out of bound error in test cases
#### constaining programs which were ineligible - fixed by editing a
#### copy of the applications list 

def remove_ineligible(applications_list) -> list:
    viable_list = applications_list.copy()
    print(len(applications_list))
    for i in range(len(applications_list) - 1):
        if applications_list[i].eligible == "No":
            viable_list.remove(applications_list[i])
    applications_list = viable_list




# Main algorithm: generate all combinations of selections, and store the best based on score and budget
def select_applications(applications_list, budget, score_method) -> list:
    best_combination = []
    best_score = 0
    best_cost = 0

    # Remove ineligible applications from consideration
    remove_ineligible(applications_list)

    for i in range( 0, int(math.pow(2, len(applications_list))) ):
        # Create binary number representing selection (0 or 1) of application
        binary_number = decimal_to_binary(i, applications_list)

        # Calculate total cost of selected applications and check if it is within budget
        total_cost = calculate_total_cost(applications_list, binary_number)
        if total_cost > budget:
            continue

        # Score based on heuristic
        if score_method == "impact_to_cost_ratio":
            score = score_by_impact_to_cost_ratio(applications_list, binary_number)
        elif score_method == "impact":
            score = score_by_impact(applications_list, binary_number)
        elif score_method == "people":
            score = score_by_people(applications_list, binary_number)
        
        # Update best score and combination if result is better than current best
        if score > best_score:
            best_score = score
            best_cost = total_cost
            best_combination = binary_number

    # Return best find
    return best_combination, best_score, best_cost



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("budget")
    parser.add_argument("score_by")
    args = parser.parse_args()

    # Basic check for valid score_by argument
    if args.score_by != "impact_to_cost_ratio" and args.score_by != "impact" and args.score_by != "people":
        print("Invalid score_by argument. Must be one of: impact_to_cost_ratio, impact, people")
        return

    # Read in file and parse into list of Application objects
    applications = parsecsv.parse_csv(args.file_name)

    # Brute force algorithm
    best_combination, best_score, best_cost = select_applications(applications, int(args.budget), args.score_by)



   # Print results & write to file

    total_impact = 0
    total_people_served = 0

    file = open("brute_force_output.txt", "w")

    for i in range(len(applications)):
        if best_combination[i] == 1:
            print(applications[i].name, "|", applications[i].requested_money, "|", applications[i].impact, "|", applications[i].people_served)
            file.write(f"{applications[i].name} | {applications[i].requested_money} | {applications[i].impact} | {applications[i].people_served}\n")
            
            total_impact += applications[i].impact
            total_people_served += applications[i].people_served

    print()
    print("Total impact: ", total_impact)
    file.write(f"\nTotal impact: {total_impact}\n")
    print("Total cost: ", best_cost)
    file.write(f"Total cost: {best_cost}\n")
    print("Total people served: ", total_people_served)
    file.write(f"Total people served: {total_people_served}\n")
    file.close()


if __name__ == "__main__":
    main()

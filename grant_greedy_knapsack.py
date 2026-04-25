'''
Greedy algorithm for grant applications problem
'''

import argparse
import parsecsv


# Heuristic for impact-to-cost ratio
def sort_by_impact_to_cost_ratio(applications_list) -> list:
    return sorted(applications_list, key = lambda application: application.impact / application.requested_money, reverse=True)

# Heuristic for impact
def sort_by_impact(applications_list) -> list:
    return sorted(applications_list, key = lambda application : application.impact, reverse=True)

# Heuristic for people served
def sort_by_people(applications_list) -> list:
    return sorted(applications_list, key = lambda application : application.people_served, reverse=True)


# Selection algorithm
def select_applications(applications_list, budget) -> list:
    selected_list = []
    total_cost = 0

    for application in applications_list:
        if total_cost + application.requested_money <= budget and application.eligible == "Yes":
            selected_list.append(application)
            total_cost += application.requested_money
        if total_cost == budget:
            break
    
    return selected_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("budget")
    parser.add_argument("sort_by")
    args = parser.parse_args()

    # Read in file and parse into list of Application objects
    applications = parsecsv.parse_csv(args.file_name)

    # Sort by heuristic
    if args.sort_by == "impact_to_cost_ratio":
        applications_sorted = sort_by_impact_to_cost_ratio(applications)
    elif args.sort_by == "impact":
        applications_sorted = sort_by_impact(applications)
    elif args.sort_by == "people":
        applications_sorted = sort_by_people(applications)

    # Select applications based on sorted list and budget constraint
    selected_applications = select_applications(applications_sorted, int(args.budget))



    # Print selected applications

    total_impact = 0
    total_cost = 0
    total_people_served = 0

    for application in selected_applications:
        print(application.name, "|", application.requested_money, "|", application.impact, "|", application.people_served)
        total_impact += application.impact
        total_cost += application.requested_money
        total_people_served += application.people_served
    
    print()
    print("Total impact: ", total_impact)
    print("Total cost: ", total_cost)
    print("Total people served: ", total_people_served)



if __name__ == "__main__":
    main()
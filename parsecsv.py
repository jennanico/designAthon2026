'''
Helper method for parsing CSV file into list of Application objects.
'''

import argparse

class Application():
    def __init__(self, name, category, requested_money, impact, people_served, eligible):
        self.name = name
        self.category = category
        self.requested_money = requested_money
        self.impact = impact
        self.people_served = people_served
        self.eligible = eligible


def parse_csv(file_name) -> list:
    file = open(file_name, "r")

    applications_list = []
    for line in file:
        line = line.strip()
        if line == "":
            continue

        line_list = line.split(",")
        application_instance = Application(line_list[0], line_list[1], int(line_list[2]), int(line_list[3]), int(line_list[4]), line_list[5])
        applications_list.append(application_instance)

    file.close()
    
    return applications_list


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    args = parser.parse_args()

    applications = parse_csv(args.file_name)


if __name__ == "__main__":
    main()
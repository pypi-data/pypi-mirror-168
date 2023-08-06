import random

from math import ceil
from seauval.groups import Group, GroupCollection


def allowedStudents(students, assignment):
    """Return the list of students that are not part of the assignment yet"""
    allowed = []
    for s in students.students:
        if not assignment.hasStudent(s):
            allowed += [s]
    return allowed


def getNbCollaborations(students, assignments, student):
    """
    Return a dictionary mapping students with the number of times they have been
    matched with the provided student
    """
    nb_collab = {}
    for s in students.students:
        if s != student:
            nb_collab[s] = 0
    for assignment in assignments:
        for group in assignment.groups:
            if student in group.students:
                for s in group.students:
                    if s != student:
                        nb_collab[s] += 1
    return nb_collab


def getStudentCost(students, assignments, nb_groups, nb_collab, student):
    nb_students = len(students.students)
    total_collab = sum([v for k, v in nb_collab.items()])
    avg_collab = total_collab / (nb_students - 1)
    cost = 0
    for s in students.students:
        if s != student:
            # Adding a huge penalty when coop/opp is 0 to enforce every team play at least once with
            # or against every team.
            if (nb_collab[s] == 0):
                cost += 100
            cost += (nb_collab[s] - avg_collab) ** 2
    # Pushing towards balancing total number of collaborators
    avg_group_size = nb_students / nb_groups
    avg_collab_per_assignment = avg_group_size - 1
    expected_total_collab = len(assignments) * avg_collab_per_assignment
    if abs(total_collab - expected_total_collab) >= 1.0:
        cost += 1
    return cost


def getModificationCost(students, assignments, nb_groups, new_student, coworkers):
    """
    What is the cost of adding new_team to game with the given allies and
    opponents inside this tournament
    Aim: try to minimize the number of team couples as allies or against
    """
    nb_collab = getNbCollaborations(students, assignments, new_student)
    current_cost = getStudentCost(students, assignments, nb_groups, nb_collab, new_student)
    for team in coworkers:
        nb_collab[team] += 1
    new_cost = getStudentCost(students, assignments, nb_groups, nb_collab, new_student)
    return new_cost - current_cost


def getAssignmentsTotalCost(students, assignments, nb_groups):
    cost = 0
    for s in students.students:
        nb_collab = getNbCollaborations(students, assignments, s)
        cost += getStudentCost(students, assignments, nb_groups, nb_collab, s)
    return cost


def sampleNextAssignment(students, assignments, nb_groups):
    """
    Compute the next assignment which should be added given previous assignments
    On failure, returns None
    """
    nb_students = len(students.students)
    group_max_size = ceil(nb_students / nb_groups)
    current_assignment = GroupCollection([])
    for game_id in range(nb_groups):
        current_assignment.groups += [Group()]
    # Adding the first student to each group, then the second, etc...
    for pos_idx in range(group_max_size):
        for group_id in range(nb_groups):
            # If all students have been assigned, job is done
            if (current_assignment.getNbStudents() == nb_students):
                continue
            coworkers = current_assignment.groups[group_id].students
            allowed_students = allowedStudents(students, current_assignment)
            random.shuffle(allowed_students)
            # Getting allowed student with lowest local cost
            best_student = allowed_students[0]
            best_cost = getModificationCost(students, assignments, nb_groups, best_student, coworkers)
            for allowed_student_idx in range(1, len(allowed_students)):
                student = allowed_students[allowed_student_idx]
                cost = getModificationCost(students, assignments, nb_groups, student, coworkers)
                if (cost < best_cost):
                    best_student = student
                    best_cost = cost
            current_assignment.groups[group_id].students += [best_student]
    return current_assignment


def getNextAssignment(students, assignments, nb_groups):
    nb_attempts = 100
    best_assignment = None
    best_cost = None
    for i in range(nb_attempts):
        assignment = sampleNextAssignment(students, assignments, nb_groups)
        cost = getAssignmentsTotalCost(students, assignments + [assignment], nb_groups)
        if best_cost is None or best_cost > cost:
            best_cost = cost
            best_assignment = assignment
    return best_assignment


def randomizeGroupsForAssignments(students, nb_groups, nb_assignments, nb_attempts=10):
    """
    Create a complete tournament based on the current state of global variables
    On failure to create the tournament, returns None
    """
    best_solution = None
    best_cost = None
    for i in range(nb_attempts):
        assignments = []
        for assignment_id in range(nb_assignments):
            assignments += [getNextAssignment(students, assignments, nb_groups)]
        cost = getAssignmentsTotalCost(students, assignments, nb_groups)
        print(f"Attempt {i:3d} Cost: {cost}")
        if best_cost is None or best_cost > cost:
            best_solution = assignments
            best_cost = cost
    print(f"Final cost: {cost}")
    return best_solution


def getCollabStats(students, assignments):
    """
    Return a dictionary 'd' such as d[s1][s2] is the number of time where s1 has worked with s2
    """
    dic = {}
    for s1 in students.students:
        dic[s1] = {}
        for s2 in students.students:
            if s1 != s2:
                dic[s1][s2] = 0
    for assignment in assignments:
        for group in assignment.groups:
            group_size = len(group.students)
            for idx1 in range(group_size):
                s1 = group.students[idx1]
                for idx2 in range(idx1+1, group_size):
                    s2 = group.students[idx2]
                    dic[s1][s2] += 1
                    dic[s2][s1] += 1
    return dic


def displayCollabStats(students, collab_stats):
    """
    Terminal display of mates statistics,
    """
    nb_students = len(students.students)
    for idx1 in range(nb_students):
        s1 = students.students[idx1]
        for idx2 in range(idx1+1, nb_students):
            s2 = students.students[idx2]
            print(f"({s1},{s2}) -> {collab_stats[s1][s2]}")


def getHistogram(students, collab_stats):
    """
    Returns one dictionary with:
    - as key: the number of time a couple of students are working together
    - as value: how many couples of students are working together 'key' times
    """
    histogram = {}
    nb_students = len(students.students)
    for idx1 in range(nb_students):
        s1 = students.students[idx1]
        for idx2 in range(idx1+1, nb_students):
            s2 = students.students[idx2]
            collabs = collab_stats[s1][s2]
            if collabs in histogram:
                histogram[collabs] += 1
            else:
                histogram[collabs] = 1
    return histogram

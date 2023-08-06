#!python

import argparse
import os
import tarfile

from os.path import join
from seauval.groups import Group, GroupCollection
from seauval.randomizer import randomizeGroupsForAssignments, getCollabStats, displayCollabStats, getHistogram


def pack(project_path, group_id):
    if not os.path.isdir(project_path):
        raise RuntimeError("'" + project_path + "' is not a valid directory path")

    group_path = os.path.join(project_path, "group.csv")
    # When using 'groups.csv' files, read appropriate group and create the associated archive
    if group_id > -1:
        groups_path = os.path.join(project_path, "groups.csv")
        groups = GroupCollection.readCSV(groups_path)
        group_key = str(group_id)
        if group_key not in groups.groups:
            raise RuntimeError(f'Cannot find group "{group_id}" in {groups_path}')
        groups.groups[group_key].writeCSV(group_path)
    if not os.path.isfile(group_path):
        raise RuntimeError("No file named 'group.csv' in " + project_path)
    group = None
    with open(group_path) as f:
        group = Group.readCSV(group_path)
    files_path = os.path.join(project_path, "to_pack.txt")
    if not os.path.isfile(group_path):
        raise RuntimeError("No file named 'to_pack.txt' in " + project_path)
    dst_file = group.getKey() + ".tar.gz"
    archive = tarfile.open(dst_file, "w:gz")
    with open(files_path) as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            full_path = os.path.join(project_path, line.strip())
            if not os.path.isfile(full_path):
                raise RuntimeError("Failed to find file" + full_path)
            # Making sure all elements are in an archive
            archive_name = os.path.join(group.getKey(), line.strip())
            archive.add(full_path, arcname=archive_name)
    archive.close()


def discover(path):
    os.chdir(path)
    print(GroupCollection.discover("./"))


def randomize_groups(students_path, nb_groups, nb_assignments, output_directory):
    students = Group.readCSV(students_path)
    assignments = randomizeGroupsForAssignments(students, nb_groups, nb_assignments)
    collab_stats = getCollabStats(students, assignments)
    displayCollabStats(students, collab_stats)
    print(getHistogram(students, collab_stats))
    for i in range(len(assignments)):
        output_path = join(output_directory, f"assignment_{i+1}.csv")
        assignments[i].writeCSV(output_path)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help="Sub-commands help")
parser_pack = subparsers.add_parser("pack", help="Pack the work of a group")
parser_pack.add_argument("project_path", help="The path to the project directory")
parser_pack.add_argument("--group", type=int, default=-1,
                         help="Uses a group id from a multiple files 'groups.csv'")
parser_randomize = subparsers.add_parser("randomize", help="Randomize students attributions for a teaching unit")
parser_randomize.add_argument("students_path", help="The path to the csv file containing the students")
parser_randomize.add_argument("nb_groups", type=int, help="The number of groups")
parser_randomize.add_argument("nb_assignments", type=int, help="The number of assignments")
parser_randomize.add_argument("--output_directory", default="./",
                              help="The path to the csv file containing the created groups")
# NOTE: this action is probably obsolete since it is based on the mandatory use of a group.csv file in archives
# which is no longer active
discover_pack = subparsers.add_parser("discover", help="Discover groups in path")
discover_pack.add_argument("path", help="The path to discover")
discover_pack.set_defaults(func=discover)
args = parser.parse_args()
if args.command == 'pack':
    pack(args.project_path, args.group)
elif args.command == 'randomize':
    randomize_groups(args.students_path, args.nb_groups, args.nb_assignments, args.output_directory)
elif args.command == 'discover':
    discover(args.path)
else:
    print(f"Unknown command: '{args.command}'")
    parser.print_help()

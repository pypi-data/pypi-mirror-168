import copy
import csv
import io
import json
import os
import random
import sys
import tarfile

from math import floor
from os.path import isfile, join
from seauval.tools import prompt, tarOpenUTF8Proof


class Student:
    def __init__(self, last_name="LastName", first_name="FirstName"):
        self.last_name = last_name.strip().upper()
        self.first_name = first_name.strip().title()

    def __repr__(self):
        return "[" + self.last_name + "," + self.first_name + "]"

    def asDict(self):
        return {'last_name': self.last_name, 'first_name': self.first_name}


class Group:
    # The maximal number of students in a group before using shortened names
    max_explicit_size = 3

    # The separator between LastName and FirstName
    name_separator = '.'

    # The separator between GroupMembers
    student_separator = '_'

    def __init__(self, students=[]):
        self.students = students
        self.sortStudents()

    def sortStudents(self):
        # Sorting student based on last_name first and then first_name
        # Note: Still some unexpected behavior possible if last_name of a
        #       student is prefix of another student last_name
        self.students = sorted(self.students, key=lambda s: s.last_name + "|" + s.first_name)

    def getKey(self):
        """
        Return the group name based on students names
        """
        use_full_names = len(self.students) <= self.max_explicit_size
        key = ""
        for s in self.students:
            if len(key) != 0:
                key += self.student_separator
            if use_full_names:
                key += s.last_name + self.name_separator + s.first_name
            else:
                key += s.last_name[0] + s.first_name[0]
        return key

    def addStudent(self, s):
        self.students.append(s)
        self.sortStudents()

    def findArchive(self, path, extension):
        """
        Return: archive_path

        Perform the following operation:
        1. Test if there is an archive with a valid name in folder 'path'
        2. If no available names are found, list all the archive files and
           request user choice to see if it's valid
        3. If user chooses an archive name manually, it asks if the name is
           valid
        """
        key = self.getKey()
        candidate = os.path.join(path, key + extension)
        if os.path.exists(candidate):
            return candidate
        msg = "Failed to find file with default name, is one of the following file valid?\n"
        msg += "Default name was: " + str(candidate) + "\n"
        msg += "-> answer 'n' if no file is valid\n"
        file_options = [f for f in os.listdir(path) if f.endswith(extension)]
        options = []
        for i in range(len(file_options)):
            msg += "{:2d}: {:}\n".format(i, file_options[i])
            options += [str(i)]
        choice = prompt(msg, options + ["n"])
        if choice == "n":
            return None
        choice_idx = int(choice)
        archive_path = file_options[choice_idx]
        return archive_path

    def __repr__(self):
        return str(self.students)

    def writeCSV(self, file_path):
        """Write a group to a CSV file with header"""
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, ['LastName', 'FirstName'])
            writer.writeheader()
            for student in self.students:
                entry = {
                    "LastName": student.last_name,
                    "FirstName": student.first_name
                }
                writer.writerow(entry)

    def asList(self):
        return [s.asDict() for s in self.students]

    @staticmethod
    def readCSV(file_path):
        """
        Reads a group from a CSV file, raising exceptions if content is invalid
        """
        with open(file_path) as f:
            students = []
            reader = csv.DictReader(f)
            for required_key in ["LastName", "FirstName"]:
                if required_key not in reader.fieldnames:
                    raise RuntimeError(f'Missing key {required_key} in {file_path}')
            for row in reader:
                students.append(Student(row["LastName"], row["FirstName"]))
            return Group(students)


class GroupCollection:

    def __init__(self, groups):
        """
        Create a group collection composed of the given groups
        """
        self.groups = groups

    def getNbStudents(self):
        return sum([len(g.students) for g in self.groups])

    def hasStudent(self, student):
        for g in self.groups:
            if student in g.students:
                return True
        return False

    def writeCSV(self, file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, ['Group', 'LastName', 'FirstName'])
            writer.writeheader()
            for idx in range(len(self.groups)):
                for student in self.groups[idx].students:
                    entry = {
                        "Group": idx+1,
                        "LastName": student.last_name,
                        "FirstName": student.first_name
                    }
                    writer.writerow(entry)

    @staticmethod
    def loadFromJson(self, path):
        """
        Parameters
        ----------
        path : str
            The path to a json file containing an array of groups

        Returns
        -------
        collection : GroupCollection
            The collection build from the json file
        """
        collection = GroupCollection([])
        with open(path) as f:
            val = json.load(f)
            if not isinstance(val, list):
                raise RuntimeError("GroupCollection should be an array in file {:}".format(path))
            for group in val:
                if not isinstance(group, list):
                    raise RuntimeError("Each group should be an array in file {:}".format(path))
                g = Group()
                for student in group:
                    if not isinstance(student, list):
                        raise RuntimeError("Each student should be an array in file {:}".format(path))
                    if len(student) != 2:
                        raise RuntimeError("Expecting an element of size 2 in file {:}".format(path))
                    g.append(Student(student[0], student[1]))
                collection.groups.append(g)

    @staticmethod
    def readCSV(file_path):
        """
        Reads a group collection from a CSV file, raising exceptions if content is invalid
        """
        with open(file_path) as f:
            reader = csv.DictReader(f)
            for required_key in ["Group", "LastName", "FirstName"]:
                if required_key not in reader.fieldnames:
                    raise RuntimeError(f'Missing key {required_key} in {file_path}')
            groups = {}
            for row in reader:
                group = row["Group"]
                student = Student(row["LastName"], row["FirstName"])
                if group in groups:
                    groups[group].addStudent(student)
                else:
                    groups[group] = Group([student])
            return GroupCollection(groups)

    @staticmethod
    def discover(path):
        """
        Analyze the content of a directory and consider that each `tar.gz` file
        in it is a different group. Extract all the archives and look up for the
        `group.csv` file in it to extract names of the group.

        Parameters
        ----------
        path : str
            The path to the directory

        Returns
        -------
        collection : GroupCollection
            The list of groups discovered
        """
        archives = [f for f in os.listdir(path) if isfile(join(path, f)) and f.endswith(".tar.gz")]
        archives.sort()
        group_collection = GroupCollection([])
        for a in archives:
            group_name = a.replace(".tar.gz", "")
            try:
                with tarOpenUTF8Proof(join(path, a)) as tar:
                    group_inner_path = join(group_name, "group.csv")
                    with tar.extractfile(group_inner_path) as group_file:
                        if group_file is None:
                            print("Archive '" + a +
                                  "' failed to read file '" +
                                  group_inner_path + "'", file=sys.stderr)
                        else:
                            reader = csv.DictReader(io.StringIO(group_file.read().decode('utf-8')),
                                                    fieldnames=["LastName", "FirstName"])
                            students = []
                            for row in reader:
                                students.append(Student(row["LastName"], row["FirstName"]))
                            group_collection.groups.append(Group(students))
            except tarfile.ReadError as error:
                print("Failed to extract archive in '" + a + "': " + str(error))
        return group_collection

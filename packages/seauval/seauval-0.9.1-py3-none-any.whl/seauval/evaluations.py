#!/usr/bin/env python3

from anytree import NodeMixin, RenderTree
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
import argparse
import json
import os
import subprocess
import sys
import traceback
import abc

from seauval.groups import GroupCollection
import seauval.tools as tools
from os.path import join
from textwrap import TextWrapper

"""
Documentation in progress...

Examples of generated outputs: TO BE DESCRIBED

Module classes:

- Student: The core properties of a student
- Group: A simple list of students
- GroupCollection: A list of student groups
- Eval: Simple evaluation on an exercise
- EvalNode: The core element of the evaluation is the node of a tree
  - Can be exported to both, result
- EvaluationProcess: This is the class that should be inherited from when creating an assignment
- Assignment: The results of all the group on a specific assignment.
  - Results can be exported as json files or csv files
- TeachingUnit: A class allowing to regroup multiples assignment and to produce
  a recap for all the students

Different ways to evaluate a task: TO BE DESCRIBED

Handling invalid configurations: TO BE DESCRIBED

Different languages: TO BE DESCRIBED
"""

SAE_LG = "EG"

messages = {
    "NO_ARCHIVE": {
        "EG": "No archive file received",
        "FR": "Pas d'archive reçue"
    },
    "FAILED_EXTRACTION": {
        "EG": "Unable to extract archive automatically",
        "FR": "Impossible d'extraire l'archive automatiquement"
    },
    "AND": {
        "EG": "AND",
        "FR": "ET"
    },
    "ARCHIVE_FOLDER_FAILED": {
        "EG": "All files should be in a single folder",
        "FR": "Tous les fichiers doivent être dans un dossier unique"
    },
    "SEE": {
        "EG": "See",
        "FR": "Voir"
    },
    "RULES_NODE": {
        "EG": "Rules",
        "FR": "Règles"
    },
    "MAIL_TITLE_NODE": {
        "EG": "Mail title",
        "FR": "Titre du mail"
    },
    "MAIL_CC_NODE": {
        "EG": "Mail recipients",
        "FR": "Destinataires du mail"
    },
    "ARCHIVE_NAME_NODE": {
        "EG": "Archive name",
        "FR": "Nom de l'archive"
    },
    "ARCHIVE_CONTENT_NODE": {
        "EG": "Archive content",
        "FR": "Contenu de l'archive"
    },
}


def getMessage(id):
    if id not in messages:
        return "<UNKNOWN MESSAGE ID: {:}>".format(id)
    if SAE_LG not in messages[id]:
        return "<UNSUPPORTED LANGUAGE '{:}' for message id '{:}'>".format(SAE_LG, id)
    return messages[id][SAE_LG]


class Eval:
    """
    A simple class representing an exercise

    Members
    -------
    points: float
        The number of points achieved on the exercise
    max_points: float
        The maximal number of points that can be obtained on the exercise
    adjustment_points: float
        A manual adjustment of the points for the node, can be used for bonus
        valid over a subtree
    msg: str
        The name of the exercise
    evaluated: bool
        Has the node already been evaluated or has it just been created
    eval_func: lambda EvalNode : None
        An evaluation function which updates the node points and the node
        message
    """
    def __init__(self, max_points=1.0, points=0, msg="", evaluated=False):
        self.max_points = max_points
        self.points = points
        self.adjustment_points = 0.0
        self.msg = msg
        self.evaluated = evaluated


class EvalNode(Eval, NodeMixin):
    def __init__(self, name, max_points=1.0, points=0,  msg="",
                 eval_func=None, set_up_func=None, tear_down_func=None,
                 evaluated=False, parent=None, children=None):
        super().__init__()
        Eval.__init__(self, max_points, points, msg, evaluated)
        self.name = name
        self.parent = parent
        self.eval_func = eval_func
        self.set_up_func = set_up_func
        self.tear_down_func = tear_down_func
        if children is not None:
            self.children = children
        self.syncPoints()

    def syncPoints(self):
        if len(self.children) == 0:
            return
        self.points = self.adjustment_points
        self.max_points = 0
        for c in self.children:
            c.syncPoints()
            self.points += c.points
            self.max_points += c.max_points

    def setSuccess(self, successRatio=1.0):
        self.points = successRatio * self.max_points

    def setRecursive(self, msg=None, points_ratio=None, evaluated=None):
        for children in self.descendants:
            if msg is not None:
                children.msg = msg
            if points_ratio is not None:
                children.points = children.max_points * points_ratio
            if evaluated is not None:
                children.evaluated = True

    def exportToDict(self):
        dict_exporter = DictExporter(
            attriter=lambda attrs: [
                (k, v) for k, v in attrs if k.find("func") == -1 and (k != "adjustment_points" or v != 0)
            ])
        return dict_exporter.export(self)

    def exportToJson(self, json_path):
        with open(json_path) as out:
            print(json.dumps(self.exportToDict(), sort_keys=False, indent=2), file=out)

    def eval(self):
        if self.evaluated:
            return
        if self.set_up_func is not None:
            self.set_up_func()
        for c in self.children:
            c.eval()
        if self.eval_func is not None:
            self.eval_func(self)
        if self.tear_down_func is not None:
            self.tear_down_func()

    def importContent(self, src):
        """
        Import all the evaluation content from 'src' to current node.

        If a node is missing in src (e.g. has been added to the assignment), a warning is printed.
        If a node is present in src but not in current node, an error is raised.
        """
        nb_imported_children = 0
        for i in range(len(self.children)):
            for src_child in src.children:
                if (self.children[i].name == src_child.name):
                    self.children[i].importContent(src_child)
                    nb_imported_children += 1
        if nb_imported_children != len(src.children):
            raise RuntimeError(f"Failed to import some children of {src.children}")
        if hasattr(src, "points"):
            self.points = src.points
        if hasattr(src, "adjustment_points"):
            self.adjustment_points = src.adjustment_points
        if hasattr(src, "msg"):
            self.msg = src.msg
        if hasattr(src, "evaluated"):
            self.evaluated = src.evaluated


class EvaluationProcess:
    def __init__(self, path, group):
        """
        Parameters
        ----------
        path : str
            The path to the assignment directory
        group : Group
            The group which will be evaluated
        """
        self._archive_path = None
        self._path = path
        self._group = group
        self.root = self.getStructure()

    def run(self, original_eval=None):
        """
        Run a complete evaluation for the given group

        Parameters
        ----------
        original_eval : EvalNode
            The root of a previous evaluation.

        Returns
        -------
        root : EvalNode
            The evaluation tree after evaluation
        """
        print("Running evaluation for group:")
        for s in self._group.students:
            print("->" + s.last_name + ", " + s.first_name)
        if original_eval is not None:
            self.root.importContent(original_eval)
        self._archive_path = self._group.findArchive(self._path, ".tar.gz")
        try:
            self._set_up()
        except Exception as exc:
            print("Failed to set up environment with the following error:")
            print(exc)
            if not tools.question("Would you like to proceed with evaluation?"):
                return self.root
        self._eval()
        self._tear_down()
        self.root.syncPoints()
        return self.root

    @abc.abstractmethod
    def getStructure(self):
        """
        Return the evaluation tree prior to any evaluation
        """

    def getDefaultRulesTree(self):
        """
        Return a tree for evaluation regarding respect of the rules
        """
        rules_root = EvalNode(getMessage("RULES_NODE"), children=[
            EvalNode(getMessage("MAIL_TITLE_NODE"), 1.0, eval_func=manualEval),
            EvalNode(getMessage("MAIL_CC_NODE"), 1.0, eval_func=manualEval),
            EvalNode(getMessage("ARCHIVE_NAME_NODE"), 1.0, eval_func=manualEval,
                     set_up_func=lambda: print("Archive name: " + self._archive_path)),
            EvalNode(getMessage("ARCHIVE_CONTENT_NODE"), 1.0, eval_func=manualEval,
                     set_up_func=lambda: tools.tarOpenUTF8Proof(self._archive_path).list())
        ])
        return rules_root

    def _set_up(self):
        """
        Perform tasks which needs to be run prior to evaluation, default is
        extracting archive in its own folder
        """
        dst = os.path.dirname(self._archive_path)
        with tools.tarOpenUTF8Proof(self._archive_path) as tar:
            tar.extractall(dst)
        return None

    def _eval(self):
        """
        Run the evaluation process, default is to launch eval procedure on the
        whole tree
        """
        self.root.eval()

    def _tear_down(self):
        """
        Cleans the environment after an evaluation has been performed
        """
        return None


class Assignment:
    """
    Members
    -------
    groups : GroupCollection
        The list of the groups involved in this assignment
    evaluations : dict [str,EvalNode]
        A correspondance between group keys and their evaluation
    """

    def __init__(self):
        self.groups = GroupCollection()
        self.evaluations = {}


def evalToString(eval_root):
    """
    Convert evaluation to a printable version
    """
    result_txt = ""
    max_width = 80
    max_tree_width = 0
    oversized_messages = []
    for pre, _, node in RenderTree(eval_root):
        line_width = len(u"%s%s" % (pre, node.name))
        if max_tree_width < line_width:
            max_tree_width = line_width
    max_msg_width = max_width - max_tree_width - 10 - 5
    for pre, _, node in RenderTree(eval_root):
        treestr = u"%s%s" % (pre, node.name)
        line = "{:} {:5.2f} / {:5.2f}".format(treestr.ljust(max_tree_width), node.points, node.max_points)
        if node.msg is not None:
            if len(node.msg) <= max_msg_width:
                line += " " + node.msg
            else:
                msg_index = len(oversized_messages) + 1
                line += " {:} *{:}".format(getMessage("SEE"), msg_index)
                oversized_messages.append(node.msg)
        result_txt += line + "\n"
    for idx in range(len(oversized_messages)):
        msg = oversized_messages[idx]
        first_paragraph = True
        default_indent = "    "
        for paragraph in msg.split('\n'):
            if paragraph == "":
                continue
            init_indent = default_indent
            if first_paragraph:
                init_indent = "*{:}: ".format(idx+1)
                first_paragraph = False
            wrapper = TextWrapper(initial_indent=init_indent,
                                  subsequent_indent=default_indent,
                                  width=80)
            for line in wrapper.wrap(paragraph):
                result_txt += "{:}\n".format(line)
    return result_txt


def importEvalJson(group, assignment_path):
    json_path = join(assignment_path, group.getKey() + ".json")
    if not os.path.isfile(json_path):
        return None
    with open(json_path) as f:
        content = json.load(f)
        if 'eval' not in content:
            raise RuntimeError(f"Missing field 'eval' in {json_path}")
        return DictImporter().import_(content['eval'])


def importResultFromJson(json_path):
    with open(json_path) as f:
        content = json.load(f)
        required_fields = ['group', 'eval']
        for f in required_fields:
            if f not in content:
                raise RuntimeError(f"Missing field '{f}' in {json_path}")
        return content['group'], content['eval']


def writeEvalJson(eval_root, group, assignment_path):
    eval_dict = eval_root.exportToDict()
    with open(join(assignment_path, group.getKey() + ".json"), "w") as out:
        json.dump({"group": group.asList(), "eval": eval_dict}, indent=2, fp=out)


def writeEvalTxt(eval_root, group, assignment_path):
    txt_content = evalToString(eval_root)
    txt_path = join(assignment_path, group.getKey() + ".txt")
    with open(txt_path, "w") as f:
        f.write(txt_content)


def manualEval(node):
    result = tools.prompt("Is '{:}' valid? y(es), n(o), p(artially)".format(node.name), ['y', 'n', 'p'])
    if (result == 'y'):
        node.points = node.max_points
    else:
        if (result == 'p'):
            node.points = tools.askFloat("How many points? (max_points={:})".format(node.max_points))
        node.msg = tools.freeTextQuestion("What is the problem?")
    node.evaluated = True


def assertionEval(node, func, header=None, show_assert=True):
    """
    Parameters
    ----------
    node : EvalNode
        The node to be evaluated
    func : lambda
        The test function to run
    header : str or None
        The header to add to node.msg if test fails
    show_assert : boolean
        When enabled, display AssertionError message in node.msg
    """
    try:
        func()
        node.points = node.max_points
    except Exception:
        if header is not None:
            node.msg += "# {:}\n".format(header)
        if show_assert:
            # node.msg += "{:}: ".format(type(e).__name__)
            # for msg in e.args:
            #     node.msg += str(msg)
            node.msg += traceback.format_exc()
    except:
        if header is not None:
            node.msg += "# {:}\n".format(header)
        node.msg += "Generic_error: "
        node.msg += str(sys.exc_info()[0])
    finally:
        node.evaluated = True


def systemCall(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate()
    return [proc.returncode, stdout.decode("utf8").strip(), stderr.decode("utf8").strip()]


def approxEq(d1, d2, epsilon=10**-6):
    return abs(d1 - d2) <= epsilon


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The path to the directory")
    args = parser.parse_args()

    os.chdir(args.path)

    print(GroupCollection.discover("./"))


import subprocess
import datetime
import string

latex_template = """
\\documentclass[a4paper,10pt]{scrreprt}
\\usepackage[utf8]{inputenc}

\\usepackage{bytefield}
\\usepackage{hyperref}

\\title{Totally Unofficial VideoCore MMIO Reference}
\\author{}

\\begin{document}

\\maketitle

\\tableofcontents

\\chapter{Introduction}

TBD: What is this document?

This document was automatically generated on $DATE from the videocore
register database, version $VERSION.

\\chapter{Register Documentation}

\\section{List of MMIO Regions}

\\begin{center}
\\begin{tabular}{|l|l|l|l|}
\\hline
Address & Size & Name & Description\\\\
\\hline
$REGION_TABLE_ENTRIES
\\hline
\\end{tabular}
\\end{center}


$REGIONS

\\end{document}
"""

latex_region_table_template = """
\\texttt{$REGION_ADDRESS} & \\texttt{$REGION_SIZE} & \\texttt{$REGION_NAME} &
$REGION_BRIEF \\\\"""

latex_region_template = """
\\section{\\texttt{$REGION_NAME}: $REGION_BRIEF}

\\subsection{Overview}

\\subsubsection*{Description:}

$REGION_DESC

\\subsubsection*{Registers:}

\\begin{center}
\\begin{tabular}{|l|l|l|l|}
\\hline
Address & Access & Name & Description\\\\
\\hline
$REGISTER_TABLE_ENTRIES
\\hline
\\end{tabular}
\\end{center}

\\subsection{Registers}

$REGISTERS

"""

latex_register_table_template = """
\\texttt{$REGISTER_ADDRESS} & $REGISTER_ACCESS & \\texttt{$REGISTER_NAME} &
$REGISTER_BRIEF \\\\"""

latex_register_template = """
\\subsubsection*{$REGISTER_NAME: $REGISTER_BRIEF}

$REGISTER_DESC
"""

def escapeLatex(text):
    return text.replace('_', '\\_')

def generateRegisterTable(group):
    text = ''
    template = string.Template(latex_register_table_template)
    for reg in group.registers:
        regdict = dict(REGISTER_ADDRESS=hex(reg.offset),
                       REGISTER_ACCESS=escapeLatex(reg.access),
                       REGISTER_NAME=escapeLatex(reg.name),
                       REGISTER_BRIEF=escapeLatex(reg.brief),
                       REGISTER_DESC=escapeLatex(reg.desc))
        text += template.substitute(regdict)
    return text;

def generateRegisterDocumentation(group):
    text = ''
    template = string.Template(latex_register_template)
    for reg in group.registers:
        regdict = dict(REGISTER_ADDRESS=hex(reg.offset),
                       REGISTER_ACCESS=escapeLatex(reg.access),
                       REGISTER_NAME=escapeLatex(reg.name),
                       REGISTER_BRIEF=escapeLatex(reg.brief),
                       REGISTER_DESC=escapeLatex(reg.desc))
        text += template.substitute(regdict)
    return text;

def generateRegionTable(db):
    text = ''
    template = string.Template(latex_region_table_template)
    for group in db.groups:
        groupdict = dict(REGION_ADDRESS=hex(group.offset),
                         REGION_SIZE=hex(group.size),
                         REGION_NAME=escapeLatex(group.name),
                         REGION_BRIEF=escapeLatex(group.brief),
                         REGION_DESC=escapeLatex(group.desc))
        text += template.substitute(groupdict)
    return text;

def generateRegionDocumentation(db):
    text = ''
    template = string.Template(latex_region_template)
    for group in db.groups:
        groupdict = dict(REGION_ADDRESS=hex(group.offset),
                         REGION_SIZE=hex(group.size),
                         REGION_NAME=escapeLatex(group.name),
                         REGION_BRIEF=escapeLatex(group.brief),
                         REGION_DESC=escapeLatex(group.desc),
                         REGISTER_TABLE_ENTRIES=generateRegisterTable(group),
                         REGISTERS=generateRegisterDocumentation(group))
        text += template.substitute(groupdict)
    return text;


def generateLatex(db, filename, vcdbdir):
    # Retrieve the git hash of the version
    git = subprocess.Popen(['git', 'rev-parse', 'HEAD'], cwd=vcdbdir,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if git.wait() != 0:
        version = 'UNKNOWN'
    else:
        version = git.stdout.read().rstrip('\n')
    # Global text replacement
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    global_dict = dict(DATE=date,
                       VERSION=version,
                       REGION_TABLE_ENTRIES=generateRegionTable(db),
                       REGIONS=generateRegionDocumentation(db))
    text = string.Template(latex_template).substitute(global_dict)
    with open(filename, 'w') as f:
        f.write(text)
    # TODO
    pass
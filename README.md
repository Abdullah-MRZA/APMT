# APMT - A Highly advanced PDF manipulation tool

A highly advanced pdf **page** manipulation tool

To learn how to use, write `python main_program.py --help`

To install the dependencies, run `pip install -r requirements.txt`

## How to write the custom filetype

There are certain rules to follow when writing the filetype:

```
SHIFTAMOUNT 10
# Shiftamount tells the program how much to shift
# the page numbers, so that they align with the actual
# page numbers of the pdf file



# As you can see, any line that begins with # is treated as a comment
# is not currently supported at ends of lines


# Write a comma at the end of the bookmark, with the page number of the bookmark
# Indented bookmarks are child bookmarks to the parent bookmark before it
# WARNING: indents MUST BE 4 SPACES!!


# An example of a possible document:

Practical skills, 1
    Experiment Design, 1
    Data, 4
    Graphs, 6
    Error Analysis, 9
    Uncertainty Calculations, 12
    Evaluating and Concluding, 15
    The Practical Endorsement, 17

Section 1: Particles and Radiation, 19
    Atomic Structure, 19
    Stable and Unstable Nuclei, 23
    Antiparticles and Photons, 27
    Hadrons and Leptons, 31
    Strange Particles and Conservation Properties, 35
    Quarks and Antiquarks, 38
    Particle Interactions, 42
    Exam-style Questions, 48

Section 2: Electromagnetic Radiation and Quantum Phenomena, 51
    The Photoelectric Effect, 51
    Energy Levels in Atoms, 56
    Wave-Particle Duality, 60
    Exam-style Questions, 65
```

# Map-Coloring-Problem

## Overview

This is a complete program that solves the Map-Coloring Problem (Constraint-Specification Problem). It takes an input in the form of a text file containing the regions on the map (variables), the colors (domain), and a matrix filled with 0s and 1s indicating whether or not two regions are neighbors on the map (constraints). It then produces an output file with each variable mapped to an appropriate domain value that satisfies all the constraints given.

Sample input and output files are provided for reference.

## Instructions on how to run the program:

At the end of the source code, there is one line that calls a function named main. It takes   two arguments and an optional third argument. The first argument is for the input file name,   the second argument is for the output file name, the optional third argument is a boolean that tells the program whether forward checking should be enabled.
  Ex. main("Input1.txt", "Output1.txt")
      main("Input2.txt", "Output2.txt", True)

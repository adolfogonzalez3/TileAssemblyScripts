# Turing Machine Generator

This set of scripts is used to generate tiles for a Turing Machine based on the design in the paper [The program-size complexity of self-assembled squares](https://dl.acm.org/citation.cfm?id=335358).

The format of the turing machine is as follows:

- s: symbol
- i: state ID
- L: Move head left
- R: Move head Right
- _: Don't replace symbol under head

Language Definition:

- E -> X>Y
- E -> X>Y,E
- X -> s
- X -> s/X
- Y -> s/D/i
- Y -> _/D/i
- D -> L
- D -> R

<p>Each line in the text file represents a state's id in the Turing Machine.</p>

An example would be:

```
0>1/R/1,1>_/R/1,#>_/R/2

```

These two lines would produce a tile set which simulates a Turing Machine which replaces all zeros with ones in a binary string.


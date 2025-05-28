# Calculusator
This python3 program is a calculus calculator which uses sympy.
This program requires a virtual environment with the modules sympy and matplotlib.
You will need to activate the enivironmental variable from the commandline.
(See https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
It has been tested on python 3.11 on a raspberry pi and and 3.14 on a mac.
A show information section gives basic user instructions. There are also links for more information on syntax accepted by sympy. 
The user enters an expression and clicks a button: differentiation, integration or definite integral. The answer appears in the relevant section. The answer is also copied to the clipboard. 
Sympy will calculate the signed area, but sometinmes a user is interested in the total geometric area under the curve.  The program tries to take account of geometric area by considering the roots of the equation. There are different ourcomes if the roots are imaginary numbers, there are no roots, there is is one, or 2 or more. A geometric area is calculated for each of these, but a plot function is provided to make sure this makes mathematical sense.  

# Calculusator
This python3 program is a calculus calculator which uses sympy.
This program requires a virtual environment with the modules sympy and matplotlib.
You will need to activate the enivironmental variable from the commandline.
(See https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
It has been tested on python 3.11 on a raspberry pi 5 and and 3.14 on a macbook (Big Sur).
A show information section gives basic user instructions. There are also links for more information on syntax accepted by sympy. 
The user enters an expression and clicks a button: differentiation, integration or definite integral. The answer appears in the relevant section. The answer is also copied to the clipboard. 
Sympy will calculate the signed area, but a user may be interested in the total geometric area under the curve.  This program calculates the geometric area by considering the roots of the equation. There are different ourcomes:  if the roots are imaginary numbers, there are no roots, there is is one, or 2 or more roots. A geometric area is calculated for each of these, but an additional plot function is provided in the program for a user to check the  mathematical validity. It's also always fun to have a plot function!

V9 has a numerical integrator. I improved the processing ability on a raspberry pi by reducing the number of widgets. (The raspberry pi lost focus on widgets). I achieved the widget reduction by combining input and result lables and boxes for all mathematical operations. I added a latex imafge of the question so that a user can now easily tell if they have input the right question.  I also used I also improved the information page.

V10 is very similar to V9, but has a tidier landing page.

I developed the calculator to practice GUI development in python. The calculator development also matched my interest in learning and teaching maths. I started a blog to track my journey into the calculus calculator. (https://www.blogger.com/blog/post/edit/3710951870764407474/486998060452562925). 

I also post about my coding and other stuff on LinkedIn: https://www.linkedin.com/in/dr-david-e-87217957/


from tkinter import *
from tkinter import messagebox 
import sympy
from sympy.parsing.mathematica import parse_mathematica
#from sympy import init_session
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import webbrowser 
#init_session()
def math_ops():
    webbrowser.open_new("https://docs.sympy.org/latest/tutorials/intro-tutorial/intro.html") #Link which will open when you click label

def trig_ops():
    webbrowser.open_new("https://docs.sympy.org/latest/modules/functions/elementary.html") #Link which will open when you click label


x = sympy.Symbol('x')
#import sys """next 2 lines test where modules are being picked up from
# print(f"Python Interpreter for Tkinter: {sys.executable}")

# make the window
root = Tk()

root.title("Calculusator")


def plot():

    try:
        plot_window = Tk()
        plot_window.title("Plot of Expression")
        expression_str = def_int_plot_entry.get()
        upper_x = float(sympy.sympify(upper_entry_plot.get()))
        lower_x = float(sympy.sympify(lower_entry_plot.get()))
        expression = sympy.sympify(expression_str)
        xplot = np.linspace(lower_x, upper_x, 1000) # Uses the linspace() function from NumPy to create an array of 1000 evenly spaced numbers between lower_x and upper_x (inclusive). This array represents the x-values at which the function will be evaluated for plotting.
        y = [float(expression.subs(x, val).evalf()) for val in xplot] # converts to float - needed for numpy as it can't recognise symbolic output, evalf() needed to numerically evaluate a symbolic expression.
        fig, ax = plt.subplots(figsize=(5, 4), dpi=70)
        ax.plot(xplot, y, color='red')
        ax.fill_between(xplot, y)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Plot of {expression_str}")
        ax.grid(True)
        ax.axhline(y=0, lw=1, color='k') # plot line y=0 in bold
        ax.axvline(x=0, lw=1, color='k')  # plot line x=0 in bold

        canvas = FigureCanvasTkAgg(fig, master = plot_window )
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=15, pady=15, sticky="NSEW")

    except Exception as e:
        print(f"Error: {e}")
       
        messagebox.showinfo("Error", f" {e}. If entering a symbol ensure correct symbols are used (E, pi)" )


def copy(text):
    root.clipboard_clear()
    root.clipboard_append(text)

def integ():
    try:
        """integrate an expression"""
        expression_str = int_entry.get()
        expression = sympy.sympify(expression_str)  # Convert input string to SymPy expression
        ans = str(sympy.integrate(expression, x) ) # Perform integration using SymPy
        lbl_result_int["text"] = "ans: " + ans # Display the SymPy expression as a string
        copy(ans)
        
    except NameError:
        messagebox.showinfo("Error", "Value is not defined in SymPy. Check https://docs.sympy.org/latest/index.html,then try again.")
    except SyntaxError:
        messagebox.showinfo("Error", "Syntax Error")
    except Exception as e:
        messagebox.showinfo("Error", f"Incorrect expression format: {e}. Check https://docs.sympy.org/latest/index.html,then try again.")

def differentiate():

    try: 
       
        value1 = str(diff_entry.get())
        ans =  str (sympy.diff(value1, x))
        lbl_result_diff["text"] = "ans: "+ ans
        copy(ans)
      
   
    except NameError:
        messagebox.showinfo("Error", "Value is not defined in SymPy. Check https://docs.sympy.org/latest/index.html,then try again.") 
    except SyntaxError:
        messagebox.showinfo("Error", "Syntax Error") 
    except Exception as e:
        messagebox.showinfo("Error", f"NameError: {e}")
        print("Error", f"Error: {e}")


def roots_calc(expression):
    roots = sympy.solve (expression,x) # used in the integration around the roots section 
    print(f"roots are {roots}.")
    return roots

def sympy_defint(expression, low, high):
    integral = sympy.Integral(expression, (x, low, high)) #create an integral object
    sympy_integral = integral.doit() #calculate the integral
    return sympy_integral

def convert_to_round(symbol):
    return round(symbol,2)
def geometric_message(geom, roots):
    return f"The geometric  area is {geom} ({round(float(geom),2)}, 2 d.p.). The roots are {roots}"

def def_integ():
    try:
        expression = str(def_int_entry.get())
        upper_str = str(upper_entry.get()) 
        upper = parse_mathematica(upper_str) # this step can change pi etc into as number
        lower_str = str(lower_entry.get())
        lower= parse_mathematica(lower_str) # this step can change pi etc into as number
        lbl_result_def_int_1 ["text"] = ""
        lbl_result_def_int_2 ["text"] = ""
        lbl_result_def_int_3 ["text"] = ""
        def_int_message_1 = ""
        def_int_message_2 = ""
        def_int_message_3 = ""
      

        signed_area =  sympy_defint(expression, lower, upper)
        lbl_result_def_int_2["text"]= f"Signed area is {signed_area} ({convert_to_round(float(signed_area))}, 2 d.p)"
        def_int_message_2 = f"Signed area is {signed_area} ({convert_to_round(float(signed_area))}, 2 d.p). "
       
     

        roots =roots_calc(expression)
        number_roots = len(roots)

        roots_txt = str(roots)


######################################## Next section of codes retrieves root values from the list as long as roots <=2 
        if number_roots == 1:
            roots_one = float(roots[0])
        elif number_roots == 2 and ("I" in roots_txt)==False:
            roots_one = float(roots[0])
            roots_two= float(roots[1])
        
        if upper > lower:
            if "I" in roots_txt:
                def_int_message_1 = "Roots are imaginary. Integrate abs| upper and lower| but plot to confirm. "
                lbl_result_def_int_1["text"] = "Roots are imaginary. Integrate abs| upper and lower| but plot to confirm. "

               
                number_roots = 0
            if "*" in roots_txt:
                lbl_result_def_int_1["text"] ="There are more than 2 roots, plot and inspect the limits around the roots and calculate the 'definite integral' manually. "
                def_int_message_1 = "There are more than 2 roots, plot and inspect the limits around the roots and calculate the 'definite integral' manually. "

                number_roots = 3 # artificially set the roots > 2 so that the geometric area is not calculated
            
            match number_roots:
                case 0 : # and for imaginary roots!
                    geometric_area = abs(signed_area)
                    def_int_message_3 = geometric_message(geometric_area, roots)
                    #lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                case 1  if (lower < roots_one and upper > roots_one): # L and U lie either side of R
                    geometric_area = abs(sympy_defint(expression, lower, roots_one)) + abs(sympy_defint(expression, roots_one, upper))
                    def_int_message_3 = geometric_message(geometric_area, roots)
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                case 1 if (roots_one <= lower or roots_one >= upper):
                    geometric_area = abs(signed_area)
                    def_int_message_3 = geometric_message(geometric_area, roots)
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                case 2 if (roots_one > lower and  roots_two < upper):
                    geometric_area= abs(sympy_defint(expression,lower, roots_one)) + abs(sympy_defint(expression,roots_one, roots_two)) +  abs(sympy_defint(expression,roots_two, upper))
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)

                    def_int_message_3 = geometric_message(geometric_area, roots)
                case 2 if (roots_one <= lower and  roots_two >= upper):
                    geometric_area = abs(signed_area)
                    print(geometric_area)
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                    def_int_message_3 = geometric_message(geometric_area, roots)
                   
                    
                case 2 if (roots_one <= lower and  roots_two > lower and  roots_two< upper):
                    geometric_area = abs(sympy_defint(expression,lower, roots_two)) + abs (sympy_defint(expression,roots_two, upper) )
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                  
                    def_int_message_3 = geometric_message(geometric_area, roots)

                  
                case 2 if (roots_one > lower and roots_one < upper and  roots_two >= upper):
                    geometric_area = abs(sympy_defint(expression,lower, roots_one ) + abs(sympy_defint(expression, roots_one, upper)))
                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                    def_int_message_3 = geometric_message(geometric_area, roots)
                case 2 if (roots_one>= upper or roots_two<=lower):
                    geometric_area = abs(signed_area)

                    lbl_result_def_int_1["text"] = ""
                    lbl_result_def_int_3["text"] = geometric_message(geometric_area, roots)
                    def_int_message_3 = geometric_message(geometric_area, roots)
                case _:
                    print("No match")
              
            ans = def_int_message_1 + def_int_message_2 + def_int_message_3
            copy(ans)
        else:
            print("Upper< lower") ## calculation not made if the lower> upper
            lbl_result_def_int_1["text"] = "You have entered an upper limit < a lower limit. Please try again."
            lbl_result_def_int_2["text"] = "You have entered an upper limit < a lower limit. Please try again."
            lbl_result_def_int_3["text"] = "You have entered an upper limit < a lower limit. Please try again."
    except NameError:
        messagebox.showinfo("NameError", "Value is not defined in SymPy. Check https://docs.sympy.org/latest/index.html,then try again.") 
    except SyntaxError:
        messagebox.showinfo("SyntaxError", "Syntax Error") 
    except Exception as e:
        messagebox.showinfo("Error", f"Error: {e}")
        print ("Error", f"Error: {e}")
    
        
    
def show():
#https://www.geeksforgeeks.org/how-to-print-superscript-and-subscript-in-python/
#https://en.wikipedia.org/wiki/List_of_Unicode_characters
    
    # messagebox.showinfo("Syntax Information", "Check https://docs.sympy.org/latest/index.html.") 
    info_window = Tk()
    info_window.title("Information")
    # note I have mistakenly calles the labelfram intructions not instructions throughout
    intructions = LabelFrame(info_window, text="Instructions")
    intructions.config(font=("Helvetica", 12, "bold"))
    intructions.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
 

    links = LabelFrame(info_window, text="Links")
    links.config(font=("Helvetica", 12, "bold"))
    links.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

    syntax= LabelFrame(info_window, text="Syntax")
    syntax.config(font=("Helvetica", 12, "bold"))
    syntax.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

    label_show_intro1_line1 = Label (intructions, text = "This calculator uses sympy, a python library for symbolic math.") 
    label_show_intro1_line1.grid(row=0, column=1, sticky="W")
    label_show_intro1_a = Label (intructions, text = "Enter an expression and hit the calculus operation button.") 
    label_show_intro1_a.grid(row=1, column=1, sticky="W")
    label_show_intro1_b = Label (intructions, text = "Note: this calculator can only use x as a variable.") 
    label_show_intro1_b.grid(row=2, column=1, sticky="W")
    label_show_intro1_c = Label(intructions, text = "Definite Integration")
    label_show_intro1_c.config(font=("Helvetica", 11, "bold"))
    label_show_intro1_c.grid(row=3, column = 1, sticky="W")
    label_show_intro1_d = Label(intructions, text = "Two answers are given for definite integration.")
    label_show_intro1_d.grid(row=4, column = 1, sticky="W")
    label_show_intro1_e = Label(intructions, text = "a)The signed area (adds negative to positive regions of a function).")
    label_show_intro1_e.grid(row=5, column = 1, sticky="W")
    label_show_intro1_e = Label(intructions, text = "b)The total geometric area,")
    label_show_intro1_e.grid(row=6, column = 1, sticky="W")
    label_show_intro1_f = Label(intructions, text = "(the absolute area, that bounded by the expression and the x-axis).")
    label_show_intro1_f.grid(row=7, column = 1, sticky="W")

    label_show_intro2_a = Label (syntax, text = "Expressions must use the correct sympy syntax.") 
    label_show_intro2_a.grid(row=1, column=1, sticky = "W")

    label_show_specials= Label (syntax, text = "Special characters:  For \u03C0 write pi; for e write E, for infinity write oo.")
    label_show_specials.grid(row=2, column=1, sticky="W")

    label_show_powers1= Label (syntax, text = "Powers:  For x\u2074 write x**4; for  \u221Ax write x**(1/2) for e\u02E3 write exp(x)")
    label_show_powers1.grid(row=3, column=1, sticky="W")

    label_show_intro_trig = Label (syntax, text = "Trig: cos(x), sin(x), tan(x), sec(x), asin(x) etc (other examples in Trig Ops link)") 
    label_show_intro_trig.grid(row=4, column=1, sticky="W")

    label_show_example = Label (syntax, text = "A complex example: write cos(e\u207b\u02E3) as cos(exp(-x))") 
    label_show_example.grid(row=6, column=1, sticky="W")


    #label_show_math_ops = (info_window, text = "Math Ops | ", fg="blue", cursor="hand2")
    label_show_math_ops = Label(links, text="Math Ops |", fg="blue", cursor="hand2")
    label_show_math_ops.bind("<Button-1>", lambda e: math_ops())
    label_show_math_ops.grid(row=0, column=0, sticky="W")
    label_show_trig = Label(links, text="Trig Ops", fg="blue", cursor="hand2")
    label_show_trig.bind("<Button-1>", lambda e: trig_ops())
    label_show_trig.grid(row=0, column=1, sticky="W")


# Show Info Frame
show_frame = LabelFrame(root, text="Show Information")
show_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
btn_show = Button(master=show_frame,text="Show",command=show)
btn_show.grid(row=0, column=0)




# Differential Frame
diff_frame = LabelFrame(root, text="Differentiation")
diff_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

diff_label = Label(diff_frame, text="Expression:")
diff_label.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

diff_entry = Entry(diff_frame)
diff_entry.grid(row=0, column=1, sticky="NSEW", padx=5, pady=5)

btn_differentiate = Button(master=diff_frame,text="Differentiation",command=differentiate)
btn_differentiate.grid(row=0, column=2)

lbl_result_diff = Label(master=diff_frame, text="answer")
lbl_result_diff.grid(row=1, column=2, sticky="W", padx=5, pady=5)

diff_frame.columnconfigure(1, weight=1) # parameters are row and weight

# Integration Frame
int_frame = LabelFrame(root, text="Integration")
int_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

int_label = Label(int_frame, text="Expression:")
int_label.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

int_entry = Entry(int_frame)
int_entry.grid(row=0, column=1, sticky="W", padx=5, pady=5)

btn_integrate = Button(master=int_frame,text="Integration",command=integ)
btn_integrate.grid(row=0, column=2, sticky="W", padx=5, pady=5)

lbl_result_int= Label(master=int_frame, text="answer")
lbl_result_int.grid(row=1, column=2, sticky="W", padx=5, pady=5)

int_frame.columnconfigure(2, weight=1) # parameters are row and weight


# Definite Integral Frame
def_int_frame = LabelFrame(root, text="Definite Integral")
def_int_frame.grid(row=3, column=0, padx=10, pady=10, sticky="NSEW")
def_int_frame.columnconfigure(2, weight=1) # parameters are row and weight - used to stretch - not sure it works

#lable and box for expression
def_int_label = Label(def_int_frame, text="Expression:")
def_int_label.grid(row=0, column=0, padx=5, pady=5)
def_int_entry = Entry(def_int_frame)
def_int_entry.grid(row=0, column=1, sticky="WE",padx=5, pady=5)

#lable and box for lower limit
def_int_lower_label = Label(def_int_frame, text="Lower limit:")
def_int_lower_label.grid(row=1, column=0, padx=5, pady=5)
lower_entry = Entry(def_int_frame)
lower_entry.grid(row=1, column=1, sticky="WE", padx=5, pady=5)

#lable and box for upper limit
def_int_upper_label = Label(def_int_frame, text="Upper limit:")
def_int_upper_label.grid(row=2, column=0, sticky="WE",  padx=5, pady=5)
upper_entry = Entry(def_int_frame)
upper_entry.grid(row=2, column=1, sticky="WE", padx=5, pady=5)

#intergal button
btn_def_integrate = Button(master=def_int_frame,text="Definite Integral",command=def_integ)
btn_def_integrate.grid(row=3, column=0, sticky="WE")


lbl_result_def_int_1= Label(master=def_int_frame, text="answer")
lbl_result_def_int_1.grid(row=4, column=2, sticky="W", padx=5, pady=5)
lbl_result_def_int_2= Label(master=def_int_frame, text="answer")
lbl_result_def_int_2.grid(row=5, column=2, sticky="W", padx=5, pady=5)
lbl_result_def_int_3= Label(master=def_int_frame, text="answer")
lbl_result_def_int_3.grid(row=6, column=2, sticky="W", padx=5, pady=5)



# Def Int Plot  Frame

def_int_plot_frame = LabelFrame(root, text="Plot Expression")
def_int_plot_frame.grid(row=4, column=0, padx=10, pady=10, sticky="NSEW")

# expression label
def_int_plot_label = Label(def_int_plot_frame, text="Expression:")
def_int_plot_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

# expression entry
def_int_plot_entry = Entry(def_int_plot_frame)
def_int_plot_entry.grid(row=0, column=1, sticky="W", padx=5, pady=5)


#lable and box for lower plot limit
def_plot_lower_label = Label(def_int_plot_frame, text="Lower plot limit:")
def_plot_lower_label.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
lower_entry_plot = Entry(def_int_plot_frame)
lower_entry_plot.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)


#lable and box for upper plot limit
def_plot_upper_label = Label(def_int_plot_frame, text="Upper plot limit:")
def_plot_upper_label.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)
upper_entry_plot = Entry(def_int_plot_frame)
upper_entry_plot.grid(row=2, column=1, sticky="NSEW", padx=5, pady=5)


# plot button
btn_plot = Button(master=def_int_plot_frame, text="Plot", command=plot)
btn_plot.grid(row=5, column=0, sticky="W", padx=5, pady=5)

# error label
error_label = Label(def_int_plot_frame, text="")
error_label.grid(row=7, column=0, columnspan=3, sticky="W")

# the below expression didn't seem to do anything
#def_int_plot_frame.columnconfigure(2, weight=1) # parameters are row and weight


root.mainloop()
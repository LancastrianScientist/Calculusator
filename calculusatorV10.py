# V9 = Development of a changing lable size to accomodate large images . 
# The image size of the qjustion and answer now adapt to the string lentgh up to a string lentgh of 100.
# This can be changed later  for larger string sizes, should it  be necessary



from tkinter import *
from tkinter import messagebox 
import tkinter.font as tkFont # Import the font module
from tkinter.scrolledtext import ScrolledText   
import sympy
from sympy import latex # removed  'symbols,'
from sympy.parsing.mathematica import parse_mathematica

#from sympy import init_session
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # used in the plot
from matplotlib.backends.backend_agg import FigureCanvasAgg # used to convert LaTw=ex to png
from matplotlib.figure import Figure
import numpy as np
import webbrowser
import io
from PIL import Image, ImageTk
import pyperclipimg
from scipy.integrate import quad


# Initialize latest_generated_image at the top level
latest_generated_image = None
# Intitialize coipy buttons, so I can remove them when not needed
btn_copy_txt_sympy = None
btn_copy_txt_LaTex = None
btn_copy_img = None  

def math_ops():
    webbrowser.open_new("https://docs.sympy.org/latest/tutorials/intro-tutorial/intro.html") #Link which will open when you click label

def trig_ops():
    webbrowser.open_new("https://docs.sympy.org/latest/modules/functions/elementary.html") #Link which will open when you click label

 
def scipy_ops():
     webbrowser.open_new("https://docs.scipy.org/doc/scipy-1.15.3/tutorial/integrate.html") #Link which will open when you click label

def blog_ops():
    webbrowser.open_new("https://evylearnsskills.blogspot.com/") #Link which will open when you click label

x = sympy.Symbol('x')
#import sys """next 2 lines test where modules are being picked up from
# print(f"Python Interpreter for Tkinter: {sys.executable}")

# make the window
root = Tk()

root.title("Calculusator")
default_font = tkFont.nametofont("TkDefaultFont") # used to change the font size
default_font.configure(size=12) # Change 12 to your desired size

def plot():
    try:
        plot_window = Tk()
        plot_window.title("Plot of Expression")      
        expression_str = expr_entry.get()
        upper_x = float(sympy.sympify(upper_entry.get()))
        lower_x = float(sympy.sympify(lower_entry.get()))
        expression = sympy.sympify(expression_str)
        xplot = np.linspace(lower_x, upper_x, 1000)
        y = [float(expression.subs(x, val).evalf()) for val in xplot]
        fig, ax = plt.subplots(figsize=(5, 4), dpi=70)
        ax.plot(xplot, y, color='red')
        ax.fill_between(xplot, y)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Plot of {expression_str}")
        ax.grid(True)
        ax.axhline(y=0, lw=1, color='k')
        ax.axvline(x=0, lw=1, color='k')

        canvas = FigureCanvasTkAgg(fig, master = plot_window )
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=15, pady=15, sticky="NSEW")

        # Save the plot to an in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Open the image with Pillow
        img = Image.open(buf)

        plot_button = Button(master= plot_window, text ="Copy Plot", command= lambda: copy_img(img))
        plot_button.grid(row=1, column=0, padx=15, pady=15, sticky="NSEW")
    
      
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showinfo("Error", f" {e}. If entering a symbol ensure correct symbols are used (E, pi)" )

def copy(text):
    try:
        root.clipboard_clear()  # Use a temporary Tk instance
        root.clipboard_append(text)
    except Exception as e:
        print(f"Error copying text to clipboard  {e}")

def copy_img(img):
    try:
        if img: 
            pyperclipimg.copy(img)
        else:
            print("No image to copy")
    except Exception as e:
        print(f"Error copying image to clipboard with pyperclipimg: {e}")
        # Fallback for systems where image copying isn't directly supported by pyperclipimg or its dependencies
        root.clipboard_clear()  # Use a temporary Tk instance
        root.clipboard_append("Image data cannot be directly copied via pyperclipimg.")


def display_sympy_as_latex_in_label(label_widget, latex_str):
    global latest_generated_image  # Declare intent to modify global variable
    #print (f"latex str = {latex_str} string length = {len(latex_str)}")
   
   
    try:
        if len(latex_str) <= 20:
            figx=1
        elif len(latex_str) > 20 and len(latex_str) <= 30:
            figx=2
        elif len(latex_str) > 30 and len(latex_str) <= 40:
            figx=3
        elif len(latex_str) > 40 and len(latex_str) <= 50:
            figx=4
        elif len(latex_str) > 50 and len(latex_str) <= 60:
            figx=5
        elif len(latex_str) > 60 and len(latex_str) <= 70:
            figx=6
        elif len(latex_str) > 70 and len(latex_str) <= 80:
            figx=7
        elif len(latex_str) > 80 and len(latex_str) <= 90:
            figx=8
    
        else :
            figx=10
   
       
    
        fig = Figure(figsize=(figx, 1), dpi=60)
        fig.text(0.5, 0.5, f'${latex_str}$', usetex=False, fontsize=18, ha='center', va='top') # font size changes the size of the image text
        plt.close(fig)

        buf = io.BytesIO()
        canvas_agg = FigureCanvasAgg(fig)
        canvas_agg.print_png(buf)
        buf.seek(0)

        img = Image.open(buf)
        tk_img = ImageTk.PhotoImage(image=img)

        label_widget["image"]= tk_img
        # Insert a newline before the image for spacing, then the image, then more newlines
        #text_widget.insert(END, '\t')  # Use END
        #text_widget.image_create(END, image=tk_img)  # Use END
        #text_widget.insert(END, "")  # Use tk.END

        # Store a reference to prevent garbage collection
        if not hasattr(label_widget, 'photo_images'):
            label_widget.photo_images = []
        label_widget.photo_images.append(tk_img)

        latest_generated_image = img  # Update the global reference to the PIL image

    except Exception as e:
        messagebox.showinfo("Error", f"Error displaying LaTeX image: {e}")
        print(f"Error displaying LaTeX image: {e}")
       

def integ():
    try:
        """integrate an expression"""
     
        expr = str(expr_entry.get())
        expression = sympy.sympify(expr)  # Convert input string to SymPy expression
        latex_question = r"\int_{a}^{b} " + latex(expression) + r"\, dx  = "  
        display_sympy_as_latex_in_label(results_label, latex_question)
        
        ans_int = sympy.integrate(expression, x) # Keep it as a SymPy expression for latex()
        latex_str_int = latex(ans_int) +' + c'
        ans_int = str(ans_int) + ' + c'
        
        clear_Results_Pane() 
        



        display_sympy_as_latex_in_label(results_label2, latex_str_int) 
        
        
        
        #results_buttons(ans_int, latex_str_int, results_frame)
        results_buttons(ans_int, latex_str_int, results_frame)

        # Pass the SymPy expression 'ans' directly to display_sympy_as_latex_in_label
        # We will add "+ c" to the LaTeX output inside the display function if needed,
        # or render it as part of the SymPy expression itself if SymPy allows it.
        # For a simple "+ c", you might add it as plain text after the LaTeX if necessary.
         # Convert SymPy expression to LaTeX string

        #display_sympy_as_latex_in_label(results_label2, latex_str_int)

    except NameError:
        messagebox.showinfo("Name Error", "Value is not defined in SymPy. Check https://docs.sympy.org/latest/index.html,then try again.")
    except SyntaxError:
        messagebox.showinfo("Syntax Error", "Syntax Error")
    except Exception as e:
        messagebox.showinfo("Error", f"Incorrect expression format: {e}. Check https://docs.sympy.org/latest/index.html,then try again.")


def copy_txt(text2copy):
    copy(text2copy)

def results_buttons(sympy_ans, latex_str, results_frame): # Pass results_frame as an argument
    global btn_copy_txt_sympy, btn_copy_txt_LaTex, btn_copy_img # Declare as global if they are global

  
    if sympy_ans != "null":
        # Create buttons if they don't exist, otherwise just ensure they are gridded and UPDATE THEIR COMMAND
        if btn_copy_txt_sympy is None:
            btn_copy_txt_sympy = Button(master=results_frame, text="Copy sympy ans")
            # previously the button was fixed with lambda: 
            # btn_copy_txt_sympy = Button(master=results_frame, text="Copy sympy ans", command=lambda: copy_txt(sympy_ans))
        btn_copy_txt_sympy.config(command=lambda: copy_txt(sympy_ans)) # Update the command
        btn_copy_txt_sympy.grid(row=3, column=0)

        if btn_copy_txt_LaTex is None:
            btn_copy_txt_LaTex = Button(master=results_frame, text="Copy LaTeX ans")
        btn_copy_txt_LaTex.config(command=lambda: copy_txt(latex_str)) # Update the command
        btn_copy_txt_LaTex.grid(row=4, column=0)

        if btn_copy_img is None:
            btn_copy_img = Button(master=results_frame, text="Copy Image")
        # Ensure latest_generated_image is properly updated *before* this function is called
        btn_copy_img.config(command=lambda: copy_img(latest_generated_image)) # Update the command
        btn_copy_img.grid(row=5, column=0)
    else:
        # If buttons exist, forget them
        if btn_copy_txt_sympy is not None:
            btn_copy_txt_sympy.grid_forget()
        if btn_copy_txt_LaTex is not None:
            btn_copy_txt_LaTex.grid_forget()
        if btn_copy_img is not None:
            btn_copy_img.grid_forget()

def differentiate():
    try:
        expr = str(expr_entry.get())
        ans_diff = sympy.diff(expr, x)
        
    
        clear_Results_Pane()
        latex_question = latex_str= r"\frac{dy}{dx}  " + latex(sympy.sympify(expr)) + " =" # sympy.sympify(string) is needed to convert string to a functiomn - which is the input for sympy 
 
        display_sympy_as_latex_in_label(results_label, latex_question)
     
        latex_str = latex(ans_diff)
      
        ans_diff = str(ans_diff)

        display_sympy_as_latex_in_label(results_label2, latex_str)
        
        results_buttons(ans_diff, latex_str, results_frame)

    except NameError:
        messagebox.showinfo("Error", "Value is not defined in SymPy. Check https://docs.sympy.org/latest/index.html,then try again.")
    except SyntaxError:
        messagebox.showinfo("Error", "Syntax Error")
    except Exception as e:
        messagebox.showinfo("Error", f"Error: {e}")
        print("Error", f"Error: {e}")



def roots_calc(expression):
    roots = sympy.solve (expression,x) # used in the integration around the roots section 
    return roots

def sympy_defint(expression, low, high):
    integral = sympy.Integral(expression, (x, low, high)) #create an integral object
    sympy_integral = integral.doit() #calculate the integral
    return sympy_integral

def convert_to_round(symbol):
    return round(symbol,4)
def geometric_message(geom, roots):
    return f"\nThe geometric  area is {geom} ({round(float(geom),4)}, 4 d.p.).\nThe roots are {roots}" 

def num_integration():
    try:
        results_label["image"] = ""
        results_label2["image"] = ""
        results_buttons("null", "null", results_frame)
        expr = str(expr_entry.get())
        # Parse the string into a SymPy expression
        sympy_expr = sympy.sympify(expr) # from here
        upper_str = str(upper_entry.get()) 
        upper = parse_mathematica(upper_str) # this step can change pi etc into as number
        lower_str = str(lower_entry.get())
        lower= parse_mathematica(lower_str) # this step can change pi etc into as number
        # The 'r' before the string makes it a raw string, so backslashes are treated literally.
        latex_question = r"\int_{" + lower_str + r"}^{" + upper_str + r"} " + latex(sympy_expr) + r"\, dx = "
        #latex_question = r"\int_{" + lower_str+"}^{" + upper_str+ "} " + latex(sympy_expr) + "\, dx  = "  
        #latex_question = "\\int_{" + lower_str+"}^{" + upper_str+ "} " + latex(sympy_expr) + "\, dx  = "  

        display_sympy_as_latex_in_label(results_label, latex_question)
    
        func = sympy.lambdify(x, sympy_expr, 'numpy') 


        I, error = quad(func, lower, upper)
        roots = roots_calc(expr)
        report1 = f"Numerical Integration.\nThe signed area (numerical integration) is {round(I,4)} (4 d.p.), "
        report2 = f"and the error is {np.format_float_scientific(error, unique=False, precision=4)} (5 s.f.).\n" # np.format_float_scientific is used to rounfd the scientific number t0 4dp.
        report3 = f"\nThe roots are {roots}"
       
        clear_Results_Pane()
        result1_text.insert("1.0", report1 + report2 + report3)

       
        messagebox.showinfo ("Numerical Integarion Information", f"Note: This method is reserved for functions that will not integrate with sympy. Roots are {roots}. Use these and inspect a plot of the expression to decide on the limits of integration" )
    except Exception as e:
        messagebox.showinfo("Error", f"Error: {e}")
        print ("Error", f"Error: {e}")

def clear_Results_Pane():
     result1_text.delete("1.0", END)  # Use END

def def_integ():
    try:
        results_label["image"] = ""
        results_label2["image"] = ""
        results_buttons("null", "null", results_frame)
        expr = str(expr_entry.get())
        sympy_expr = sympy.sympify(expr)
        upper_str = str(upper_entry.get()) 
        upper = parse_mathematica(upper_str) # this step can change pi etc into as number
        lower_str = str(lower_entry.get())
        lower= parse_mathematica(lower_str) # this step can change pi etc into as number
        latex_question = r"\int_{" + lower_str+ r"}^{" + upper_str+ r"} " + latex(sympy_expr) + r"\, dx  = "  
        #latex_question = r"\int_{" + lower_str+"}^{" + upper_str+ "} " + latex(sympy_expr) + "\, dx  = "  

        display_sympy_as_latex_in_label(results_label, latex_question)
       
        signed_area =  sympy_defint(expr, lower, upper)
        
        if 'Float' in str(type(signed_area)):
                
                signed_area = round(float(signed_area), 4)
        roots =roots_calc(expr)
        number_roots = len(roots)
        
        roots_txt = str(roots)
        message_1 = f"Definite Integration.\nSigned area is {signed_area} ({convert_to_round(float(signed_area))}, 4 d.p). "
        clear_Results_Pane()
        result1_text.insert("1.0", message_1)  # Insert text answer

######################################## Next section of codes retrieves root values from the list as long as roots <=2 
        if number_roots == 1:
            roots_one = float(roots[0])
        elif number_roots == 2 and ("I" in roots_txt)==False:
            roots_one = float(roots[0])
            roots_two= float(roots[1])
 
        
        if upper > lower:
            if "I" in roots_txt:
                message = " \nRoots are imaginary. We can treat this as though there are no roots, but plot to confirm. "
                result1_text.insert(END, message)  # Do not remove
                number_roots = 0
            if "*" in roots_txt:
                message= f" \nThere are more than 2 roots. Roots: {roots_txt} Plot and inspect the roots to inform you on how to calculate geometrical area manually. "
                result1_text.insert(END, message)  # Insert text answer
                number_roots = 3 # artificially set the roots > 2 so that the geometric area is not calculated
            
            match number_roots:
                case 0 : # and for imaginary roots!
                    geometric_area = abs(signed_area)
              
                case 1  if (lower < roots_one and upper > roots_one): # L and U lie either side of R eg. 2*x, L = -2, U = 2
                    geometric_area = abs(sympy_defint(expr, lower, roots_one)) + abs(sympy_defint(expr, roots_one, upper))
                case 1 if (roots_one <= lower or roots_one >= upper):
                    geometric_area = abs(signed_area)
               
                case 2 if (roots_one > lower and  roots_two < upper):
                    #print("roots_one > lower and  roots_two < upper")
                    #print("Example: x**2-1, L = -2, U = 2")
                    geometric_area= abs(sympy_defint(expr,lower, roots_one)) + abs(sympy_defint(expr,roots_one, roots_two)) +  abs(sympy_defint(expr,roots_two, upper))
                  
                case 2 if (roots_one <= lower and  roots_two >= upper):
                    # e.g. x**2 -1, L = -0.9 U = 0.9
                    # print ("roots_one <= lower and  roots_two >= upper")
                    geometric_area = abs(signed_area)
   
                    
                case 2 if (roots_one <= lower and  roots_two > lower and  roots_two< upper):
                    #print("(roots_one <= lower and  roots_two > lower and  roots_two< upper")
                    #print("Example: x**2-1: L=0.5, U = 2 ")
                    geometric_area = abs(sympy_defint(expr,lower, roots_two)) + abs (sympy_defint(expr,roots_two, upper) )
           
                  
                case 2 if (roots_one > lower and roots_one < upper and  roots_two >= upper):
                    #print ("roots_one > lower and roots_one < upper and  roots_two >= upper")
                    #print("Example x**2-1: L = -2, U = 0.5")
                    geometric_area = (abs(sympy_defint(expr,lower, roots_one ) + abs(sympy_defint(expr, roots_one, upper)))).round(4)
               

                case 2 if (roots_one>= upper or roots_two<=lower):
                    geometric_area = abs(signed_area)
                  
                    #print("roots_one>= upper or roots_two<=lower")
                    #print("Example: x**2-1 U = -1 or L = 1 ")
              

                case _:
                    print("No or multiple roots")
              
           
        else:
            #print("Upper< lower") ## calculation not made if the lower> upper
            message_2= "You have entered an upper limit < a lower limit. Please try again."
            clear_Results_Pane()
            result1_text.insert(END, message_2)  # Insert text answer



        if "*" not in roots_txt: # only do this if there are no multiple roots (geometric area is not calculated for multiplke roots, the user needs to do this manually.)
            if 'Float' in str(type(geometric_area)): # if the sympy number is a float then round, if not leave alone.
                        
                        geometric_area = round(float(geometric_area), 4)
            result1_text.insert(END, geometric_message(geometric_area, roots))
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
    
    intructions = LabelFrame(info_window, text="Instructions")
    intructions.config(font=("Helvetica", 14, "bold"))
    intructions.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
 

    links = LabelFrame(info_window, text="Links")
    links.config(bg = "azure", font=("Helvetica", 14, "bold"))
    links.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

    syntax= LabelFrame(info_window, text="Syntax")
    syntax.config(font=("Helvetica", 14,  "bold"))

    syntax.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")
    
# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/

    show_text_box_instructions =  ScrolledText(intructions, width =60, height = 14, bg = "azure", wrap = WORD)
    show_text_box_instructions.config(font=("Helvetica", 14))
    show_text_box_instructions .grid(row=0, column=0, sticky="NSEW")
    instructions = "This calculator uses sympy, a python library for symbolic math. " \
    "Enter an expression (function) and click the desired calculus operation button\nNote: this calculator can only use x as a variable ." 
    
    show_text_box_instructions.insert("1.0",instructions)
    show_text_box_instructions.tag_configure('boldline', font= ("Helvetica", 14, "bold"))
    #show_text_box_instructions.insert('end', ' \nNote:', 'boldline')
    #instructions = " this calculator can only use x as a variable." 
    #show_text_box_instructions.insert('end',instructions)
    show_text_box_instructions.tag_configure('boldheader', font= ("Helvetica", 14, "bold"))
    show_text_box_instructions.insert('end', ' \nDefinite Integration\n', 'boldheader')
    instructions = "Two answers are given for definite integration." \
    "\na)The signed area (adds negative to positive regions of a function)." \
    "\nb)The total geometric area," \
    "(the absolute area, that bounded by the expression and the x-axis)."
    show_text_box_instructions.insert('end',instructions)
    show_text_box_instructions.insert('end', "\nNumerical Integration\n", 'boldheader')
    instructions = "Not all expresiions can be solved symbolically." \
    "For example, the definite integral of cos(x\u00B2) will not generate a simple numerical answer." \
    " As I developed the calculusator I found the symbolic answer long-winded and unsatisfatory. " \
    " For this reason I developed numerical integration as an alternative option. " \
    "However, I have since developed a way to round symbolic answers. For the definitive integration of cos(x\u00B2), " \
    "a rounded numerical integration now gives the same answer as the numerical integration, which is reassuring." \
    "There are instances when the numerical integration may still be preferable, and I have kept it for such occasions "\
    "The numerical integration functon on this calculator uses quad from SciPy to integrate a function of one variable between two points. " \
    "The numerical integrator will calculate the signed area. " \
    "If you need to calculate the geometric area , then inspect a plot of the expression, and check if there are any roots of the equation, "\
    "within the limits you are interested in."\
    "This will help if you need to determine the geometric area, but need not be any concern if you need the signed area."\
    "Use these to manually calculate the geometric area by summing the absolute regions of the positive and negative areas of the equation."\
    " More information on signed v geometric areas can be found in my blog. "
    show_text_box_instructions.insert('end',instructions)
    
    
    # syntax ##################
    
    show_text_box_syntax =  ScrolledText(syntax, width =60, height = 14, bg = "azure", wrap = WORD)
    show_text_box_syntax.config(font=("Helvetica", 14))
    show_text_box_syntax.grid(row=0, column=0, sticky="NSEW")
    show_text_box_syntax.tag_configure('italicline', font = ("Helvetica", 14, "italic", "bold"))
    
    syntax_text = "Expressions must use the correct sympy syntax." 
    show_text_box_syntax.insert("1.0", syntax_text)
    show_text_box_syntax.insert('end', "\nSpecial characters: " , 'italicline')
    
    syntax_text ="For \u03C0 write pi; for e write E, for \u221E, write oo." 
    show_text_box_syntax.insert(END,syntax_text)
    show_text_box_syntax.insert('end', "\nPowers: " , 'italicline')
    syntax_text = "For x\u2074 write x**4; for  \u221Ax write x**(1/2) for e\u02E3 write exp(x)" 
    show_text_box_syntax.insert(END,syntax_text)
    show_text_box_syntax.insert('end', "\nTrigonometry examples" , 'italicline')
    syntax_text = "cos(x), sin(x), tan(x), sec(x), asin(x) etc (see the Trig Ops link)\n" \
    "\nA complex example: write cos(e\u207b\u02E3) as cos(exp(-x))\n" \
    "\nMy Blog has more examples."

    show_text_box_syntax.insert(END,syntax_text)
    


    ########## LINKS 

    label_show_math_ops = Label(links, text="Math Ops |", fg="blue", bg = "azure", cursor="hand2")
    label_show_math_ops.bind("<Button-1>", lambda e: math_ops())
    label_show_math_ops.grid(row=0, column=0, sticky="W")
    
    label_show_trig = Label(links, text="Trig Ops |", fg="blue",bg = "azure", cursor="hand2")
    label_show_trig.bind("<Button-1>", lambda e: trig_ops())
    label_show_trig.grid(row=0, column=1, sticky="W")

    label_show_trig = Label(links, text="SciPy |", fg="blue",bg = "azure", cursor="hand2")
    label_show_trig.bind("<Button-1>", lambda e: scipy_ops())
    label_show_trig.grid(row=0, column=2, sticky="W")

   


    label_show_trig = Label(links, text="My Blog", fg="blue", bg = "azure", cursor="hand2")
    label_show_trig.bind("<Button-1>", lambda e: blog_ops())
    label_show_trig.grid(row=0, column=3, sticky="W")

####################################
# Menu Frame
####################################

menu_frame = LabelFrame(root, text="Menu")
menu_frame .config(font=("Helvetica", 14, "bold"))
menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

show_label = Label(menu_frame, text="Show Information")
show_label.config(font=("Helvetica", 12, "underline"))
show_label.grid(row = 0, column = 0 , padx = 5 , pady = 5, sticky = "W")
btn_show = Button(master=menu_frame,text="Show Info",command=show) #show button
btn_show.grid(row=1, column=0)

expression_title = Label(menu_frame, text="Function/ equation/ expression input")
expression_title.config(font=("Helvetica", 12, "underline"))
expression_title.grid(row = 2, column = 0 , padx = 5 , pady = 5, sticky = "W")
expression_label = Label(menu_frame, text="Expression:")
expression_label.grid(row=3, column=0, padx=5, pady=5)
expr_entry = Entry(menu_frame)
expr_entry.grid(row=3, column=1, sticky="WE",padx=5, pady=5)

btn_diff = Button(master=menu_frame,text="Differentiate",command=differentiate) # = differentiate button
btn_diff.grid(row=4, column=0)
btn_int = Button(master=menu_frame,text="Integrate",command=integ) # integrate button
btn_int.grid(row=4, column=1, padx= 5, pady=5)

intergral_label = Label(menu_frame, text="Integrals and Plot")
intergral_label.config(font=("Helvetica", 12, "underline"))
intergral_label.grid(row = 5, column = 0 , padx = 5 , pady = 5, sticky = "W")

#lable and box for lower limit
lower_label = Label(menu_frame, text="Lower limit:")
lower_label.grid(row=6, column=0, padx=5, pady=5)
lower_entry = Entry(menu_frame)
lower_entry.grid(row=6, column=1, sticky="W", padx=5, pady=5)

#lable and box for upper limit
upper_label = Label(menu_frame, text="Upper limit:")
upper_label.grid(row=6, column=2, sticky="W",  padx=5, pady=5)
upper_entry = Entry(menu_frame)
upper_entry.grid(row=6, column=3, sticky="W", padx=5, pady=5)

btn_def_integ = Button(master=menu_frame,text="Definite Integral",command = def_integ) # = definite integral button
btn_def_integ.grid(row=7, column = 0)
btn_numerical_integ = Button(master=menu_frame,text="Numerical Integral",command=num_integration) # = numerical integration button
btn_numerical_integ.grid(row=7, column = 1, padx=1)
btn_numerical_integ = Button(master=menu_frame,text="Plot",command=plot) # = numerical integration button
btn_numerical_integ.grid(row=7, column = 2, padx=1)

######################
# Results Frame  #####
######################
results_frame = LabelFrame(root, text="Results")
results_frame .config(font=("Helvetica", 14, "bold"))
results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
results_label = Label(results_frame, image="")
results_label.grid(row=0, column=0, sticky="W")
results_label2 = Label(results_frame, image="")
results_label2.grid(row=1, column=0, sticky="W")
result1_text = Text(results_frame, width =60, height = 8, wrap = WORD)
result1_text.grid(row=2, column=0, sticky="NSEW")

root.mainloop()
"""
This script is the main executable, calling the main_module_function which does
the rest of the work.
"""

# Import the main package
import csvfilter
import tkinter

def run():
    solved = csvfilter.main_module_function()
    return solved
    # tk=tkinter.Tk()
    # tk.wm_title('中文标题')
    # label1=tkinter.Label(tk,text='Label')

    # label1['width']=20
    # label1['height']=4
    # label1['background']='red'

    # label1.pack()
    # tk.mainloop()


# Run the function if this is the main file executed
if __name__ == "__main__":
    run()

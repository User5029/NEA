import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import random as rand
import scipy as sc
import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import webbrowser
from collections import deque

#=========================================================================================================================================

def Task_1():

     root.destroy()
     
     class Task_1_GUI(tk.Frame):


          def __init__(self,master=None):
               super().__init__(master)
               self.master.title("Task One: Projectile Motion")
               self.master.geometry("915x675")
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text=f'Projectile Motion with ajustable constants and constant timestep: tmax/10000 s.', font=('Helvetica bold', 14))

               self.Plot = tk.Button(self.master, text="Plot The Projectile", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0.01', to='20', resolution='0.01', label='Initial Velocity / ms^-1', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(5)

               self.Theta = tk.Scale(self.master, from_='0', to='90', resolution='0.01', label='Angle from the horizontal', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.Theta.set(45)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)#
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.animation = tk.Button(self.master, text='Animate the trajectory', command=self.animate)

               self.Set_Sliders = tk.Button(self.master, text='Set the sliders to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close the App', command=self.Close)

               self.Save_ = tk.Button(self.master,text='Save The Figure',command=self.Save)


               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=5)
               self.U.grid(row=6, column=0, columnspan=2)
               self.Theta.grid(row=7, column=0, columnspan=2)
               self.Set_Sliders.grid(row=8,column=0,columnspan=2)

               
               self.Plot.grid(row=6, column=2)
               self.animation.grid(row=7, column=2)
               self.Close_.grid(row=8,column=2)
               self.g_Label.grid(row=1,column=2)
               self.g.grid(row=2,column=2)
               self.h_Label.grid(row=3,column=2)
               self.h.grid(row=4,column=2)
               self.Save_.grid(row=5,column=2)

               self.Projectile(5,9.81,45,0)
          
          def Save(self):

               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.fig.savefig(f'Projectile Timestep, u={u}, a={a}, h={h}, ang={theta}.png')


          def Projectile(self, u, a, ang, h):

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)
               y_max = ((u*np.sin(theta))**2)/(2*a)
               tmax = s_xmax/(u*np.cos(theta))

               t = np.linspace(0,tmax,10000)
               
               x = np.zeros(10000)
               y = np.zeros(10000)

               for n in range(10000):

                    x[n] = u*np.cos(theta)*t[n]
                    y[n] = h + u*np.sin(theta)*t[n] -0.5*a*t[n]**2

               self.ax.clear()
               self.ax.plot(x,y)
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Height / m')
               self.ax.set_xlabel('Distance / m')
               self.ax.grid(True)
               self.ax.set_title(f'Projectile with: u = {u}ms^-1 , g = {a}ms^-2 , θ = {round(theta, 2)}rad , h = {h}m \n timestep = {round(tmax/10000 , 6)}s , tmax = {round(tmax,3)} s')
               self.canvas.draw()


          def Projectile_Update(self, event):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.Projectile(u, a, theta, h)

          def Projectile_Update_B(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.Projectile(u, a, theta, h)

          def animate(self):

               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               ang = self.Theta.get()

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)

               y_max = ((u*np.sin(theta))**2)/(2*a)
               
               tmax = s_xmax/(u*np.cos(theta))

               t = np.linspace(0,tmax,10000)
               
               x = np.zeros(10000)
               y = np.zeros(10000)

               for n in range(10000):

                    x[n] = u*np.cos(theta)*t[n]
                    y[n] = h + u*np.sin(theta)*t[n] - 0.5*a*t[n]**2


               self.ball, = plt.plot(0,h,'o')
               
               def anima(frame):
                    f = (10000)/(60*math.ceil(tmax))
                    
                    j = frame*int(math.floor(f))

                    xx = x[j]
                    yy = y[j]

                    self.ball.set_data(xx,yy)

                    return self.ball
               
               anim = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(tmax)), interval = 1/60)

               self.canvas.draw()
          
          def setsliders(self):
               self.U.set(5)
               self.Theta.set(45)#

          def Close(self):
               root1.destroy()
               Open_Gui()


     # Defines the first GUI    
     root1 = tk.Tk()
     center_screen_1(915,675,root1)
     # Defines the contents of the GUI as the class
     app1 = Task_1_GUI(root1)
     # Opens the GUI
     app1.mainloop()

#=========================================================================================================================================

def Task_2():

     root.destroy()
     
     class Task_2_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.title("Task Two: Projectile Motion")
               self.master.geometry("900x675")
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text='Projectile Motion with ajustable constants.', font=('Helvetica bold', 18))

               self.Plot = tk.Button(self.master, text="Plot The Projectile", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0.01', to='20', resolution='0.01', label='Initial Velocity / ms^-1', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(5)

               self.Theta = tk.Scale(self.master, from_='0', to='90', resolution='0.01', label='Angle from the horizontal', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.Theta.set(45)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)#
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.animation = tk.Button(self.master, text='Animate the trajectory', command=self.animate)

               self.Set_Sliders = tk.Button(self.master, text='Set the sliders to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close The App', command=self.Close)

               self.Save_ = tk.Button(self.master,text='Save The Figure',command=self.Save)


               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=5)
               self.U.grid(row=6, column=0, columnspan=2)
               self.Theta.grid(row=7, column=0, columnspan=2)
               self.Set_Sliders.grid(row=8,column=0,columnspan=2)

               
               self.Plot.grid(row=6, column=2)
               self.animation.grid(row=7, column=2)
               self.Close_.grid(row=8,column=2)
               self.g_Label.grid(row=1,column=2)
               self.g.grid(row=2,column=2)
               self.h_Label.grid(row=3,column=2)
               self.h.grid(row=4,column=2)
               self.Save_.grid(row=5,column=2)

               self.Projectile(5,9.81,45,0)

          def Save(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.fig.savefig(f'Projectile Analytical, u={u}, a={a}, h={h}, ang={theta}.png')


          def Projectile(self, u, a, ang, h):

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)

               y_max = ((u*np.sin(theta))**2)/(2*a) + h
               xymax = (np.sin(theta)*np.cos(theta)*u**2)/(a)
               
               s_x = np.linspace(0,s_xmax,10000)
               y = np.zeros(10000)

               for n in range(10000):

                    y[n] = h + s_x[n]*np.tan(theta) + b*s_x[n]**2

               self.ax.clear()
               self.ax.plot(s_x,y, label='Projectile')
               self.ax.plot(xymax,y_max,'o',label='Apogee')
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Height / m')
               self.ax.set_xlabel('Distance / m')
               self.ax.legend()
               self.ax.grid(True)
               self.ax.set_title(f'Projectile with: u = {u}ms^-1 , g = {a}ms^-2 , θ = {round(theta, 2)}rad , h = {h}m \n x_max = {round(s_xmax, 2)}m , y_max = {round(y_max, 2)}m')
               self.canvas.draw()


          def Projectile_Update(self, event):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.Projectile(u, a, theta, h)

          def Projectile_Update_B(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               theta = self.Theta.get()

               self.Projectile(u, a, theta, h)

          def animate(self):

               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               ang = self.Theta.get()

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)

               y_max = ((u*np.sin(theta))**2)/(2*a)
               
               tmax = s_xmax/(u*np.cos(theta))

               t = np.linspace(0,tmax,10000)
               
               x = np.zeros(10000)
               y = np.zeros(10000)

               for n in range(10000):

                    x[n] = u*np.cos(theta)*t[n]
                    y[n] = h + u*np.sin(theta)*t[n] - 0.5*a*t[n]**2


               self.ball, = plt.plot(0,h,'o')
               
               def anima(frame):
                    f = (10000)/(60*math.ceil(tmax))
                    
                    j = frame*int(math.floor(f))

                    xx = x[j]
                    yy = y[j]

                    self.ball.set_data(xx,yy)

                    return self.ball
               
               anim = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(tmax)), interval = 1/60)

               self.canvas.draw()
          
          def setsliders(self):
               self.U.set(5)
               self.Theta.set(45)

          def Close(self):
               root1.destroy()
               Open_Gui()


     # Defines the first GUI    
     root1 = tk.Tk()
     center_screen_1(900,675,root1)
     # Defines the contents of the GUI as the class
     app1 = Task_2_GUI(root1)
     # Opens the GUI
     app1.mainloop()

#=========================================================================================================================================

def Task_3():

     root.destroy()
     
     class Task_3_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.title("Task Three: Projectile Motion Through a Fixed Point")
               self.master.geometry("900x650")
               self.Widgets(100,100,9.81)
          
          def Widgets(self, x , y,a):

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.Title = tk.Label(self.master, text=f"3 Projectile paths to hit the Point, ({x},{y})", font=('Helvetica bold', 18))

               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.X_Label = tk.Label(self.master, text='X coordinate', font=('Helvetica bold', 12))
               self.X = tk.Entry(self.master, width = 10)
               self.X.insert(0,'100')

               self.Y_Label = tk.Label(self.master, text='Y coordinate', font=('Helvetica bold', 12))
               self.Y = tk.Entry(self.master, width = 10)
               self.Y.insert(0,'100')

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)#
               self.g.insert(0,"9.81")

               self.Plot = tk.Button(self.master, text='Plot the projectiles', command=self.Projectile_Update_B)

               self.animat = tk.Button(self.master, text='Animate the projectiles', command=self.animate)

               self.Set_Slider = tk.Button(self.master, text='Set the sliders to original values.', command=self.setslider)

               self.Close_ = tk.Button(self.master, text='Close The App', command=self.Close)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)
               self.Set_Slider.grid(row=10,column=0,columnspan=2)

               self.Save_ = tk.Button(self.master,text='Save The Figure', command=self.Save)

               self.Slider(x,y,9.81)

               
               self.Plot.grid(row=9, column=2)
               self.animat.grid(row=10, column=2)
               self.Close_.grid(row=11,column=2)
               self.X_Label.grid(row=1,column=2)
               self.X.grid(row=2,column=2)
               self.Y_Label.grid(row=3,column=2)
               self.Y.grid(row=4,column=2)
               self.h_Label.grid(row=5,column=2)
               self.h.grid(row=6,column=2)
               self.g_Label.grid(row=7,column=2)
               self.g.grid(row=8,column=2)
               self.Save_.grid(row=11,column=0,columnspan=2)

               self.Projectile(u+10, x, y, 9.81, 0)
          
          def Save(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               self.fig.savefig(f'Projectile Through Fixed Point,X={x},y={y},u={u},h={h},a={a}.png')


          def Slider(self, x, y, a):

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.U = tk.Scale(self.master, from_=u, to=3*u, resolution=0.01, label='Initial velocity',orient=tk.HORIZONTAL,command=self.Projectile_Update)
               self.U.set(u+10)
               self.U.grid(row=9, column=0, columnspan=2)

          def Projectile(self, u, x, y, a, h):
               
               U = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               A = a/(2*U**2)*x**2

               b = -x
                
               c = y-h+(a*x**2)/(2*U**2)

               theta = np.arctan((-b + np.sqrt(b**2 - 4*A*c))/(2*A))

               T = (-a)/(2*U**2*np.cos(theta)**2)
               
               x1max = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*T))/(2*T)

               X1 = np.linspace(0,x1max,10000)
               Y1 = np.zeros(10000)




               A1 = a/(2*u**2)*x**2

               b1 = -x
                
               c1 = y-h+(a*x**2)/(2*u**2)

               theta1 = np.arctan((-b1 + np.sqrt(b1**2 - 4*A1*c1))/(2*A1))
               theta2 = np.arctan((-b1 - np.sqrt(b1**2 - 4*A1*c1))/(2*A1))

               T1 = (-a)/(2*u**2*np.cos(theta1)**2)
               T2 = (-a)/(2*u**2*np.cos(theta2)**2)
               
               x2max = (-np.tan(theta1) - np.sqrt(np.tan(theta1)**2 - 4*h*T1))/(2*T1)
               x3max = (-np.tan(theta2) - np.sqrt(np.tan(theta2)**2 - 4*h*T2))/(2*T2)

               X2 = np.linspace(0,x2max,10000)
               Y2 = np.zeros(10000)

               X3 = np.linspace(0,x3max,10000)
               Y3 = np.zeros(10000)

               for n in range(10000):

                    Y1[n] = h + X1[n]*np.tan(theta) + T*X1[n]**2

                    Y2[n] = h + X2[n]*np.tan(theta1) + T1*X2[n]**2

                    Y3[n] = h + X3[n]*np.tan(theta2) + T2*X3[n]**2



               
               self.ax.clear()
               self.ax.plot(X1,Y1, label=f'Minimum u: {round(U, 2)}ms^-1 , {round(theta,2)}rad')
               self.ax.plot(X2,Y2, label=f'High ball: {round(u, 2)}ms^-1 , {round(theta1,2)}rad')
               self.ax.plot(X3,Y3, label=f'Low Ball: {round(u, 2)}ms^-1 , {round(theta2,2)}rad')
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Y / m')
               self.ax.set_xlabel('X / m')
               self.ax.legend()
               self.ax.grid(True)
               self.ax.plot(x,y,'o')
               self.canvas.draw()




          def Projectile_Update(self,event):


               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())


               self.Projectile(u, x, y, a, h)

          def Projectile_Update_B(self):

               x = float(self.X.get())
               y = float(self.Y.get())
               a = float(self.g.get())

               self.Slider(x,y, a)
               
               u = self.U.get()
               h = float(self.h.get())


               self.Projectile(u+10, x, y, a, h)
          
          def setslider(self):
               a = float(self.g.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.U.set(u+10)


          def animate(self):

               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               U = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               A = a/(2*U**2)*x**2

               b = -x
                
               c = y-h+(a*x**2)/(2*U**2)

               theta = np.arctan((-b + np.sqrt(b**2 - 4*A*c))/(2*A))

               A1 = a/(2*u**2)*x**2

               b1 = -x
                
               c1 = y-h+(a*x**2)/(2*u**2)
               theta1 = np.arctan((-b1 + np.sqrt(b1**2 - 4*A1*c1))/(2*A1))
               theta2 = np.arctan((-b1 - np.sqrt(b1**2 - 4*A1*c1))/(2*A1))

               T = (-a)/(2*U**2*np.cos(theta)**2)
               T1 = (-a)/(2*u**2*np.cos(theta1)**2)
               T2 = (-a)/(2*u**2*np.cos(theta2)**2)
               
               x1max = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*T))/(2*T)
               t1max = x1max/(U*np.cos(theta))

               x2max = (-np.tan(theta1) - np.sqrt(np.tan(theta1)**2 - 4*h*T1))/(2*T1)
               t2max = x2max/(u*np.cos(theta1))

               x3max = (-np.tan(theta2) - np.sqrt(np.tan(theta2)**2 - 4*h*T2))/(2*T2)
               t3max = x3max/(u*np.cos(theta2))

               t1 = np.linspace(0,t1max,10000)
               x1 = np.zeros(10000)
               y1 = np.zeros(10000)

               t2 = np.linspace(0,t2max,10000)
               x2 = np.zeros(10000)
               y2 = np.zeros(10000)

               t3 = np.linspace(0,t3max,10000)
               x3 = np.zeros(10000)
               y3 = np.zeros(10000)

               for n in range(10000):

                    x1[n] = U*np.cos(theta)*t1[n]
                    y1[n] = h + U*np.sin(theta)*t1[n] - 0.5*a*t1[n]**2

                    x2[n] = u*np.cos(theta1)*t2[n]
                    y2[n] = h + u*np.sin(theta1)*t2[n] - 0.5*a*t2[n]**2

                    x3[n] = u*np.cos(theta2)*t3[n]
                    y3[n] = h + u*np.sin(theta2)*t3[n] - 0.5*a*t3[n]**2


               self.ball1, = plt.plot(0,h,'o')
               self.ball2, = plt.plot(0,h,'o')
               self.ball3, = plt.plot(0,h,'o')

               def anima(frame):
                    f1 = (10000)/(60*math.ceil(t1max))
                    f2 = (10000)/(60*math.ceil(t2max))
                    f3 = (10000)/(60*math.ceil(t3max))
                    j = frame*int(math.floor(f1))
                    i = frame*int(math.floor(f2))
                    k = frame*int(math.floor(f3))

                    if j >= 10000:
                         j=10000-1

                    if k >= 10000:
                         k=10000-1

                    if i >= 10000:
                         i=10000-1



                    self.ball1.set_data(x1[j],y1[j])
                    self.ball2.set_data(x2[i],y2[i])
                    self.ball3.set_data(x3[k],y3[k])
               
               animation = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(t2max)+100), interval = 1/60)
               self.canvas.draw()

          def Close(self):
               root3.destroy()
               Open_Gui()

     # Defines the first GUI    
     root3 = tk.Tk()
     center_screen_1(900,650,root3)
     # Defines the contents of the GUI as the class
     app3 = Task_3_GUI(root3)
     # Opens the GUI
     app3.mainloop()

#=========================================================================================================================================

def Task_4():

     root.destroy()
     
     class Task_4_GUI(tk.Frame):
          def __init__(self,master=None):
               super().__init__(master)
               self.master.title('Task 4: Maximising Projectile Range And Colour Maps')
               self.master.geometry('975x700')
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text='Maximum Horizontal Range For a Given Height.', font=('Helvetica bold', 15))

               self.Plot = tk.Button(self.master, text="Plot The Projectile", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0.01', to='20', resolution='0.01', label='Initial Velocity / ms^-1', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(5)

               self.Theta = tk.Scale(self.master, from_='0', to='90', resolution='0.01', label='Angle from the horizontal', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.Theta.set(60)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.animat = tk.Button(self.master, text='Animate the trajectory', command=self.animate)

               self.Set_Slider = tk.Button(self.master, text='Set the sliders to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close the App', command=self.Close)

               self.Check1_ = tk.BooleanVar()
               self.Check2_ = tk.BooleanVar()
               self.Check3_ = tk.BooleanVar()
               
               self.Check1 = tk.Checkbutton(self.master, text='Print Colour Map: Maximum Range .', font=('Helvetica', 8), variable=self.Check1_)
               self.Check2 = tk.Checkbutton(self.master, text='Print Colour Map: Rg/U^2                .', font=('Helvetica', 8), variable=self.Check2_)
               self.Check3 = tk.Checkbutton(self.master, text='Print Colour Map: Launch Elavation.', font=('Helvetica', 8), variable=self.Check3_)

               self.Color_Map = tk.Button(self.master,text='Print The Color Map.', command=self.color_map)

               self.remove = tk.Button(self.master,text='Remove colourbar', command=self.Remove)

               self.Save_ = tk.Button(self.master,text='Save The Current Figure', command=self.Save)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)
               self.U.grid(row=9,column=0,columnspan=2)
               self.Theta.grid(row=10,column=0,columnspan=2)
               self.Set_Slider.grid(row=11,column=0,columnspan=2)

               
               self.Plot.grid(row=9, column=2,columnspan=1)
               self.animat.grid(row=10, column=2,columnspan=1)
               self.Close_.grid(row=11,column=2,columnspan=2)
               self.h_Label.grid(row=1,column=2,columnspan=2)
               self.h.grid(row=2,column=2,columnspan=2)
               self.g_Label.grid(row=3,column=2,columnspan=2)
               self.g.grid(row=4,column=2,columnspan=2)

               self.Check1.grid(row=5,column=2)
               self.Check2.grid(row=6,column=2)
               self.Check3.grid(row=7,column=2)
               self.Color_Map.grid(row=5,column=3,rowspan=3)
               self.remove.grid(row=9,column=3)
               self.Save_.grid(row=10,column=3)

               self.Projectile(60, 9.81, 5, 0)

          def Projectile(self, ang, a, u, h):
               
               theta = ang*(math.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)


               thetamax = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))
               xmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               b1 = (-a)/(2*u**2*np.cos(thetamax)**2)

               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)
               y_max = ((u*np.sin(theta))**2)/(2*a) + h
               xymax = (np.sin(theta)*np.cos(theta)*u**2)/(a)
               
               x = np.linspace(0,s_xmax,10000)
               y = np.zeros(10000)
               x1 = np.linspace(0,xmax,10000)
               y1 = np.zeros(10000)

               for n in range(10000):

                    y[n] = h + x[n]*np.tan(theta) + b*x[n]**2

                    y1[n] = h + x1[n]*np.tan(thetamax) + b1*x1[n]**2

               global T

               T = 'Projectile Maximum Range'
               
               self.ax.clear()
               self.ax.plot(x,y, label='Projectile')
               self.ax.plot(x1,y1, '--' ,label='Maximum Range')
               self.ax.plot(xymax,y_max,'o',label='Apogee')
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Height / m')
               self.ax.set_xlabel('Distance / m')
               self.ax.legend()
               self.ax.grid(True)
               self.ax.set_title(f'Projectile with: u = {u}ms^-1 , g = {a}ms^-2 , θ = {round(theta, 2)}rad , h = {h}m \n x_max = {round(s_xmax, 2)}m , y_max = {round(y_max, 2)}m , θ_max = {round(thetamax,2)}rad , R_max = {round(xmax,2)}m')
               self.canvas.draw()
          
          def Save(self):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.fig.savefig(f'{T},u={u}, a={a}, h={h}.png')
          
          def Projectile_Update_B(self):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(ang, a, u, h)

          def Projectile_Update(self, event):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(ang, a, u, h)

          def animate(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               ang = self.Theta.get()

               thetamax = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))
               xmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               b1 = (-a)/(2*u**2*np.cos(thetamax)**2)

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)

               y_max = ((u*np.sin(theta))**2)/(2*a)
               
               tmax = s_xmax/(u*np.cos(theta))
               t1max = xmax/(u*np.cos(thetamax))

               if t1max >= tmax:
                    t2max = t1max
               if t1max < tmax:
                    t2max=tmax

               t = np.linspace(0,tmax,10000)
               t1 = np.linspace(0,t1max,10000)
               
               x = np.zeros(10000)
               y = np.zeros(10000)
               x1 = np.zeros(10000)
               y1 = np.zeros(10000)

               for n in range(10000):

                    x[n] = u*np.cos(theta)*t[n]
                    y[n] = h + u*np.sin(theta)*t[n] - 0.5*a*t[n]**2

                    x1[n] = u*np.cos(thetamax)*t1[n]
                    y1[n] = h + u*np.sin(thetamax)*t1[n] - 0.5*a*t1[n]**2


               self.ball, = plt.plot(0,h,'o')
               self.ball1, = plt.plot(0,h,'o')
               
               def anima(frame):
                    f1 = (10000)/(60*math.ceil(tmax))
                    f2 = (10000)/(60*math.ceil(t1max))
                    
                    j = frame*int(math.floor(f1))
                    i = frame*int(math.floor(f2))

                    if i >= 10000:
                         i = 10000-1
                    if j >= 10000:
                         j = 10000-1

                    self.ball.set_data(x[j],y[j])
                    self.ball1.set_data(x1[i],y1[i])
               
               anim = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(t2max)), interval = 1/60)

               self.canvas.draw()

          def setsliders(self):
               self.U.set(5)
               self.Theta.set(60)

          def Close(self):
               root4.destroy()
               Open_Gui()

          def color_map(self):
               I = self.Check1_.get()
               J = self.Check2_.get()
               K = self.Check3_.get()

               if (K and J) or (J and I) or (K and I) == True:
                    pass
               else:
                    if I == True:
                         self.color_map_one()
                    if J == True:
                         self.color_map_two()
                    if K == True:
                         self.color_map_three()

          def color_map_one(self):

               a = float(self.g.get())

               u , h = np.mgrid[0.01:50:complex(0,1000), 0.01:50:complex(0,1000)]

               R = (u**2/a)*np.sqrt(1+(2*a*h)/(u**2))

               global T
               
               T = 'Colour Map Max Range'
               
               self.fig.clear()
               self.Canvas()
               self.ax.clear()
               pmc = self.ax.pcolor(u,h,R , vmin=0 , vmax=250,cmap='gist_rainbow')
               self.fig.colorbar(pmc, ax=self.ax)
               self.ax.set_ylabel('h / m')
               self.ax.set_xlabel('u / ms^-1')
               T = self.ax.set_title('Max Range /m')
               self.canvas.draw()


          def color_map_two(self):

               a = float(self.g.get())

               u , h = np.mgrid[0.01:50:complex(0,1000), 0.01:50:complex(0,1000)]

               Theta = np.arcsin(1/(np.sqrt(2+(2*a*h)/(u**2))))*180/np.pi
               
               
               global T
               
               T = 'Colour Map Rg/u2'
               
               self.fig.clear()
               self.Canvas()
               self.ax.clear()
               pmc = self.ax.pcolor(u,h,Theta , vmin=0 , vmax=45,cmap='gist_rainbow')
               self.fig.colorbar(pmc, ax=self.ax)
               self.ax.set_ylabel('h / m')
               self.ax.set_xlabel('u / ms^-1')
               self.ax.set_title('Launch Elevation / degrees')
               self.canvas.draw()

          def color_map_three(self):

               a = float(self.g.get())

               u , h = np.mgrid[0.01:50:complex(0,1000), 0.01:50:complex(0,1000)]

               R = np.sqrt(1+(2*a*h)/(u**2))
               
               global T
               
               T = 'Colour Map Angle'
               
               self.fig.clear()
               self.Canvas()
               self.ax.clear()
               pmc = self.ax.pcolor(u,h,R , vmin=0 , vmax=10,cmap='gist_rainbow')
               self.fig.colorbar(pmc, ax=self.ax)
               self.ax.set_ylabel('h / m')
               self.ax.set_xlabel('u / ms^-1')
               self.ax.set_title('Rg/u^2')
               self.canvas.draw()

          def Canvas(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)

          def Remove(self):
               self.fig.clear()
               self.Widgets()



     root4 = tk.Tk()
     center_screen_1(975,675,root4)
     app4 = Task_4_GUI(root4)
     app4.mainloop()

#=========================================================================================================================================

def Task_5():

     root.destroy()
     
     class Task_5_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.title("Task Five: Bounding Parabola For Projectiles Through A Fixed Point.")
               self.master.geometry("900x675")
               self.Widgets(100,100,9.81)
          
          def Widgets(self, x , y,a):

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.Title = tk.Label(self.master, text=f"Bounding Parabola For Projectiles Through A Fixed Point \n ({x},{y})", font=('Helvetica bold', 18))

               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.X_Label = tk.Label(self.master, text='X coordinate', font=('Helvetica bold', 12))
               self.X = tk.Entry(self.master, width = 10)
               self.X.insert(0,'100')

               self.Y_Label = tk.Label(self.master, text='Y coordinate', font=('Helvetica bold', 12))
               self.Y = tk.Entry(self.master, width = 10)
               self.Y.insert(0,'100')

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)#
               self.g.insert(0,"9.81")

               self.Plot = tk.Button(self.master, text='Plot the projectiles', command=self.Projectile_Update_B)

               self.animat = tk.Button(self.master, text='Animate the projectiles', command=self.animate)

               self.Set_Slider = tk.Button(self.master, text='Set the sliders to original values.', command=self.setslider)

               self.Close_ = tk.Button(self.master, text='Close The App', command=self.Close)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)
               self.Set_Slider.grid(row=10,column=0,columnspan=2)

               self.Save_ = tk.Button(self.master,text='Save The Figure',command=self.Save)

               self.Slider(x,y,9.81)

               
               self.Plot.grid(row=9, column=2)
               self.animat.grid(row=10, column=2)
               self.Close_.grid(row=11,column=2)
               self.X_Label.grid(row=1,column=2)
               self.X.grid(row=2,column=2)
               self.Y_Label.grid(row=3,column=2)
               self.Y.grid(row=4,column=2)
               self.h_Label.grid(row=5,column=2)
               self.h.grid(row=6,column=2)
               self.g_Label.grid(row=7,column=2)
               self.g.grid(row=8,column=2)
               self.Save_.grid(row=11,column=0,columnspan=2)

               self.Projectile(u+10, x, y, 9.81, 0)

          def Save(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               self.fig.savefig(f'Bounding Projectile Through Fixed Point,X={x},y={y},u={u},h={h},a={a}.png')

          def Slider(self, x, y, a):

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.U = tk.Scale(self.master, from_=u, to=3*u, resolution=0.01, label='Initial velocity',orient=tk.HORIZONTAL,command=self.Projectile_Update)
               self.U.set(u+10)
               self.U.grid(row=9, column=0, columnspan=2)

          def Projectile(self, u, x, y, a, h):
               
               U = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               A = a/(2*U**2)*x**2

               b = -x
                
               c = y-h+(a*x**2)/(2*U**2)

               theta = np.arctan((-b + np.sqrt(b**2 - 4*A*c))/(2*A))

               T = (-a)/(2*U**2*np.cos(theta)**2)
               
               x1max = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*T))/(2*T)

               X1 = np.linspace(0,x1max,10000)
               Y1 = np.zeros(10000)


               A1 = a/(2*u**2)*x**2

               b1 = -x
                
               c1 = y-h+(a*x**2)/(2*u**2)

               theta1 = np.arctan((-b1 + np.sqrt(b1**2 - 4*A1*c1))/(2*A1))
               theta2 = np.arctan((-b1 - np.sqrt(b1**2 - 4*A1*c1))/(2*A1))


               theta3 = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))

               T3 = (-a)/(2*u**2*np.cos(theta3)**2)

               T1 = (-a)/(2*u**2*np.cos(theta1)**2)
               T2 = (-a)/(2*u**2*np.cos(theta2)**2)
               
               x2max = (-np.tan(theta1) - np.sqrt(np.tan(theta1)**2 - 4*h*T1))/(2*T1)
               x3max = (-np.tan(theta2) - np.sqrt(np.tan(theta2)**2 - 4*h*T2))/(2*T2)

               X2 = np.linspace(0,x2max,10000)
               Y2 = np.zeros(10000)

               X3 = np.linspace(0,x3max,10000)
               Y3 = np.zeros(10000)

               XBmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               
               XB = np.linspace(0,XBmax,10000)
               YB = np.zeros(10000)

               XM = np.linspace(0,XBmax,10000)
               YM = np.zeros(10000)

               for n in range(10000):

                    Y1[n] = h + X1[n]*np.tan(theta) + T*X1[n]**2

                    Y2[n] = h + X2[n]*np.tan(theta1) + T1*X2[n]**2

                    Y3[n] = h + X3[n]*np.tan(theta2) + T2*X3[n]**2

                    YB[n] = u**2/(2*a) + h - (a)/(2*u**2)*XB[n]**2

                    YM[n] = h + XM[n]*np.tan(theta3) + T3*XM[n]**2



               
               self.ax.clear()
               self.ax.plot(X1,Y1, label=f'Minimum u')
               self.ax.plot(X2,Y2, label=f'High ball')
               self.ax.plot(X3,Y3, label=f'Low Ball')
               self.ax.plot(XB,YB, '--' ,label=f'Bounding Curve')
               self.ax.plot(XM,YM, '--' ,label=f'Maximum Range')
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Y / m')
               self.ax.set_xlabel('X / m')
               self.ax.legend()
               self.ax.grid(True)
               self.ax.plot(x,y,'o')
               self.canvas.draw()




          def Projectile_Update(self,event):


               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())


               self.Projectile(u, x, y, a, h)

          def Projectile_Update_B(self):

               x = float(self.X.get())
               y = float(self.Y.get())
               a = float(self.g.get())

               self.Slider(x,y, a)
               
               u = self.U.get()
               h = float(self.h.get())


               self.Projectile(u+10, x, y, a, h)
          
          def setslider(self):
               a = float(self.g.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               u = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               self.U.set(u+10)


          def animate(self):

               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               x = float(self.X.get())
               y = float(self.Y.get())

               U = np.sqrt(a)*np.sqrt(y+np.sqrt(x**2+y**2))

               A = a/(2*U**2)*x**2

               b = -x
                
               c = y-h+(a*x**2)/(2*U**2)

               theta = np.arctan((-b + np.sqrt(b**2 - 4*A*c))/(2*A))

               A1 = a/(2*u**2)*x**2

               b1 = -x
                
               c1 = y-h+(a*x**2)/(2*u**2)

               theta1 = np.arctan((-b1 + np.sqrt(b1**2 - 4*A1*c1))/(2*A1))
               theta2 = np.arctan((-b1 - np.sqrt(b1**2 - 4*A1*c1))/(2*A1))
               theta3 = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))

               T = (-a)/(2*U**2*np.cos(theta)**2)
               T1 = (-a)/(2*u**2*np.cos(theta1)**2)
               T2 = (-a)/(2*u**2*np.cos(theta2)**2)
               
               x1max = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*T))/(2*T)
               t1max = x1max/(U*np.cos(theta))

               x2max = (-np.tan(theta1) - np.sqrt(np.tan(theta1)**2 - 4*h*T1))/(2*T1)
               t2max = x2max/(u*np.cos(theta1))

               x3max = (-np.tan(theta2) - np.sqrt(np.tan(theta2)**2 - 4*h*T2))/(2*T2)
               t3max = x3max/(u*np.cos(theta2))

               XBmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               tBmax = XBmax/(u*np.cos(theta3))

               t1 = np.linspace(0,t1max,10000)
               x1 = np.zeros(10000)
               y1 = np.zeros(10000)

               t2 = np.linspace(0,t2max,10000)
               x2 = np.zeros(10000)
               y2 = np.zeros(10000)

               t3 = np.linspace(0,t3max,10000)
               x3 = np.zeros(10000)
               y3 = np.zeros(10000)

               tB = np.linspace(0,tBmax,10000)
               xB = np.zeros(10000)
               yB = np.zeros(10000)

               for n in range(10000):

                    x1[n] = U*np.cos(theta)*t1[n]
                    y1[n] = h + U*np.sin(theta)*t1[n] - 0.5*a*t1[n]**2

                    x2[n] = u*np.cos(theta1)*t2[n]
                    y2[n] = h + u*np.sin(theta1)*t2[n] - 0.5*a*t2[n]**2

                    x3[n] = u*np.cos(theta2)*t3[n]
                    y3[n] = h + u*np.sin(theta2)*t3[n] - 0.5*a*t3[n]**2

                    xB[n] = u*np.cos(theta3)*tB[n]
                    yB[n] = h + u*np.sin(theta3)*tB[n] - 0.5*a*tB[n]**2


               self.ball1, = plt.plot(0,h,'o')
               self.ball2, = plt.plot(0,h,'o')
               self.ball3, = plt.plot(0,h,'o')
               self.ball4, = plt.plot(0,h,'o')

               def anima(frame):
                    f1 = (10000)/(60*math.ceil(t1max))
                    f2 = (10000)/(60*math.ceil(t2max))
                    f3 = (10000)/(60*math.ceil(t3max))
                    f4 = (10000)/(60*math.ceil(tBmax))
                    j = frame*int(math.floor(f1))
                    i = frame*int(math.floor(f2))
                    k = frame*int(math.floor(f3))
                    l = frame*int(math.floor(f4))

                    if j >= 10000:
                         j=10000-1

                    if k >= 10000:
                         k=10000-1

                    if i >= 10000:
                         i=10000-1
                    
                    if l >= 10000:
                         l=10000-1


                    self.ball1.set_data(x1[j],y1[j])
                    self.ball2.set_data(x2[i],y2[i])
                    self.ball3.set_data(x3[k],y3[k])
                    self.ball4.set_data(xB[l],yB[l])
               
               animation = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(t2max)+100), interval = 1/60)
               self.canvas.draw()

          def Close(self):
               root5.destroy()
               Open_Gui()

     # Defines the first GUI    
     root5 = tk.Tk()
     center_screen_1(900,650,root5)
     # Defines the contents of the GUI as the class
     app5 = Task_5_GUI(root5)
     # Opens the GUI
     app5.mainloop()

#=========================================================================================================================================

def Task_6():

     root.destroy()
     
     class Task_6_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.title('Task 6: Path Length Of Projectiles And The Optimum Angle')
               self.master.geometry('990x700')
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text='Maximum Horizontal Range For a Given Height \n With Calculated Path Lengths.', font=('Helvetica bold', 15))

               self.Plot = tk.Button(self.master, text="Plot The Projectile", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0.01', to='20', resolution='0.01', label='Initial Velocity / ms^-1', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(5)

               self.Theta = tk.Scale(self.master, from_='0', to='89.9', resolution='0.01', label='Angle from the horizontal', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.Theta.set(60)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.animat = tk.Button(self.master, text='Animate the trajectory', command=self.animate)

               self.Set_Slider = tk.Button(self.master, text='Set the sliders to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close the App', command=self.Close)

               self.Check1_ = tk.BooleanVar()
               self.Check2_ = tk.BooleanVar()
               
               self.Check1 = tk.Checkbutton(self.master, text='Print Graph: Path Length colour map.', font=('Helvetica', 8), variable=self.Check1_)
               self.Check2 = tk.Checkbutton(self.master, text='Print Graph: Path length with angle  .', font=('Helvetica', 8), variable=self.Check2_)

               self.remove = tk.Button(self.master,text='Remove colourbar', command=self.Remove)

               self.Graph_ = tk.Button(self.master,text='Print The Graph.', command=self.Graph)

               self.Save_ = tk.Button(self.master,text='Save The Current Figure',command=self.Save)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)
               self.U.grid(row=9,column=0,columnspan=2)
               self.Theta.grid(row=10,column=0,columnspan=2)
               self.Set_Slider.grid(row=11,column=0,columnspan=2)

               
               self.Plot.grid(row=9, column=2,columnspan=1)
               self.animat.grid(row=10, column=2,columnspan=1)
               self.Close_.grid(row=11,column=2,columnspan=2)
               self.h_Label.grid(row=1,column=2,columnspan=2)
               self.h.grid(row=2,column=2,columnspan=2)
               self.g_Label.grid(row=3,column=2,columnspan=2)
               self.g.grid(row=4,column=2,columnspan=2)

               self.Check1.grid(row=5,column=2)
               self.Check2.grid(row=6,column=2)
               self.Graph_.grid(row=5,column=3,rowspan=2)
               self.remove.grid(row=9, column=3, columnspan=1)
               self.Save_.grid(row=10,column=3)

               self.Projectile(60, 9.81, 5, 0)
          
          def Save(self):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.fig.savefig(f'{Z},u={u}, a={a}, h={h}.png')

          def Projectile(self, ang, a, u, h):
               
               theta = ang*(math.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)


               theta1 = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))
               xmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               b1 = (-a)/(2*u**2*np.cos(theta1)**2)

               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)
               y_max = ((u*np.sin(theta))**2)/(2*a) + h
               xymax = (np.sin(theta)*np.cos(theta)*u**2)/(a)
               
               x = np.linspace(0,s_xmax,10000)
               y = np.zeros(10000)
               x1 = np.linspace(0,xmax,10000)
               y1 = np.zeros(10000)


               T = np.tan(theta)
               T1 = np.tan(theta1)

               B = T-(a*s_xmax)/(u**2)*((1+T**2))
               B1 = T1-(a*xmax)/(u**2)*((1+T1**2))

               
               S = (u**2)/(a*(1+T**2)) * ((0.5*np.log(abs(np.sqrt(1+T**2) + T)) + 0.5*T*np.sqrt(1+T**2))-(0.5*np.log(abs(np.sqrt(1+B**2) + B)) + 0.5*B*np.sqrt(1+B**2)))
               S1 = (u**2)/(a*(1+T1**2)) * ((0.5*np.log(abs(np.sqrt(1+T1**2) + T1)) + 0.5*T1*np.sqrt(1+T1**2))-(0.5*np.log(abs(np.sqrt(1+B1**2) + B1)) + 0.5*B1*np.sqrt(1+B1**2)))


               for n in range(10000):

                    y[n] = h + x[n]*np.tan(theta) + b*x[n]**2

                    y1[n] = h + x1[n]*np.tan(theta1) + b1*x1[n]**2

               global Z
               
               Z = 'Projectile Path Length'
               
               self.ax.clear()
               self.ax.plot(x,y, label='Projectile')
               self.ax.plot(x1,y1, '--' ,label='Maximum Range')
               self.ax.plot(xymax,y_max,'o',label='Apogee')
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(xmin=0)
               self.ax.set_ylabel('Height / m')
               self.ax.set_xlabel('Distance / m')
               self.ax.legend()
               self.ax.grid(True)
               self.ax.set_title(f'Projectile with: u = {u}ms^-1 , g = {a}ms^-2 , θ = {round(theta, 2)}rad , h = {h}m \n s = {round(S, 2)}m , s_max = {round(S1, 2)}m ')
               self.canvas.draw()
          
          def Projectile_Update_B(self):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(ang, a, u, h)

          def Projectile_Update(self, event):
               u = self.U.get()
               ang = self.Theta.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(ang, a, u, h)

          def animate(self):
               u = self.U.get()
               a = float(self.g.get())
               h = float(self.h.get())
               ang = self.Theta.get()

               thetamax = np.arcsin(1/np.sqrt(2+(2*a*h)/(u**2)))
               xmax = (u**2)/(a)*np.sqrt(1+(2*a*h)/(u**2))
               b1 = (-a)/(2*u**2*np.cos(thetamax)**2)

               theta = ang*(np.pi/180)

               b = (-a)/(2*u**2*np.cos(theta)**2)
               
               s_xmax = (-np.tan(theta) - np.sqrt(np.tan(theta)**2 - 4*h*b))/(2*b)

               y_max = ((u*np.sin(theta))**2)/(2*a)
               
               tmax = s_xmax/(u*np.cos(theta))
               t1max = xmax/(u*np.cos(thetamax))

               if t1max >= tmax:
                    t2max = t1max
               if t1max < tmax:
                    t2max=tmax

               t = np.linspace(0,tmax,10000)
               t1 = np.linspace(0,t1max,10000)
               
               x = np.zeros(10000)
               y = np.zeros(10000)
               x1 = np.zeros(10000)
               y1 = np.zeros(10000)

               for n in range(10000):

                    x[n] = u*np.cos(theta)*t[n]
                    y[n] = h + u*np.sin(theta)*t[n] - 0.5*a*t[n]**2

                    x1[n] = u*np.cos(thetamax)*t1[n]
                    y1[n] = h + u*np.sin(thetamax)*t1[n] - 0.5*a*t1[n]**2


               self.ball, = plt.plot(0,h,'o')
               self.ball1, = plt.plot(0,h,'o')
               
               def anima(frame):
                    f1 = (10000)/(60*math.ceil(tmax))
                    f2 = (10000)/(60*math.ceil(t1max))
                    
                    j = frame*int(math.floor(f1))
                    i = frame*int(math.floor(f2))

                    if i >= 10000:
                         i = 10000-1
                    if j >= 10000:
                         j = 10000-1

                    self.ball.set_data(x[j],y[j])
                    self.ball1.set_data(x1[i],y1[i])
               
               anim = ani.FuncAnimation(fig=self.fig, func=anima, frames = int(60*math.ceil(t2max)), interval = 1/60)

               self.canvas.draw()

          def setsliders(self):
               self.U.set(5)
               self.Theta.set(60)

          def Close(self):
               root6.destroy()
               Open_Gui()

          def Graph(self):
               I = self.Check1_.get()
               J = self.Check2_.get()

               if (I and J) == True:
                    pass
               else:
                    if I == True:
                         self.color_map()
                    if J == True:
                         self.Path_length()

          def Path_length(self):

               N = 1000

               global Z
               
               Z = 'Projectile Path Length Optimum Curve'
               
               theta = np.linspace(0,(np.pi/2),N)
               theta1 = theta/(2*np.pi)
               z = [0]*N
               fx1= [0]*N
               fx2 = [0]*N
               fx3 = [0]*N
               Der = [2]*N


               for n in range(1, N):

                    fx1[n] = ((10)/(9.81)) * (1/2)*((np.sin(theta[n-1]) + (np.cos(theta[n-1])**2)*np.log( ((1 + np.sin(theta[n-1])) / (np.cos(theta[n-1])))) ))

                    fx2[n] = ((20)/(9.81)) * (1/2)*((np.sin(theta[n-1]) + (np.cos(theta[n-1])**2)*np.log( ((1 + np.sin(theta[n-1])) / (np.cos(theta[n-1])))) ))

                    fx3[n] = ((30)/(9.81)) * (1/2)*((np.sin(theta[n-1]) + (np.cos(theta[n-1])**2)*np.log( ((1 + np.sin(theta[n-1])) / (np.cos(theta[n-1])))) ))

                    Der[n] = np.cos(theta[n-1])*( (1 + np.sin(theta[n-1])) + ( (np.cos(theta[n-1])**2) / (np.sin(theta[n-1]) + 1) ) - 2*np.sin(theta[n-1])*np.log(np.tan(theta[n-1]) + 1/(np.cos(theta[n-1]))))

               self.fig.clear()
               self.Canvas()
               self.ax.clear()
               self.ax.plot( theta1,fx1, '-', label = 'L(θ) at 10m/s',  color = [1,0,0] )
               self.ax.plot( theta1,fx2, '-', label = 'L(θ) at 20m/s',  color = [1,0,1] )
               self.ax.plot( theta1,fx3, '-', label = 'L(θ) at 30m/s',  color = [1,1,0] )
               self.ax.plot( theta1,Der, '-', label = 'd/dθ L(θ)', color = [0,1,0] )
               self.ax.set_title( "Path length of a Projectile vs its Angle for h = 0m and g = 9.81ms^-2, Optimum angle = 56.5°")
               self.ax.set_xlabel("θ / Pi Radians")
               self.ax.set_ylabel("Path Length / m")
               self.ax.legend(loc='upper right')
               self.ax.set_xlim(0, 0.25)
               self.ax.set_ylim(-0.5, 2.5)
               self.ax.grid(True)
               self.ax.set_ylabel('h / m')
               self.ax.set_xlabel('u / ms^-1')
               self.ax.set_title('Launch Elevation / degrees')
               self.canvas.draw()


          def color_map(self):

               a = float(self.g.get())

               u , h = np.mgrid[0.01:50:complex(0,1000), 0.01:50:complex(0,1000)]

               theta = np.arcsin(1/(np.sqrt(2+(2*a*h)/(u**2))))*180/np.pi

               R = (u**2/a)*np.sqrt(1+(2*a*h)/(u**2))

               T = np.tan(theta)

               B = T-(a*R)/(u**2)*((1+T**2))

               S = (u**2)/(a*(1+T**2)) * ((0.5*np.log(abs(np.sqrt(1+T**2) + T)) + 0.5*T*np.sqrt(1+T**2))-(0.5*np.log(abs(np.sqrt(1+B**2) + B)) + 0.5*B*np.sqrt(1+B**2)))
               
               global Z
               
               Z = 'Projectile Path Length Colour Map'
               
               self.fig.clear()
               self.Canvas()
               self.ax.clear()
               pmc = self.ax.pcolor(u,h,S , vmin=0 , vmax=150,cmap='gist_rainbow')
               self.fig.colorbar(pmc, ax=self.ax)
               self.ax.set_ylabel('h / m')
               self.ax.set_xlabel('u / ms^-1')
               self.ax.set_title('Path Length of Optimum Horizontal Distance / m')
               self.canvas.draw()

          def Canvas(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=8)

          def Remove(self):
               self.fig.clear()
               self.Widgets()



     root6 = tk.Tk()
     center_screen_1(975,675,root6)
     app6 = Task_6_GUI(root6)
     app6.mainloop()

#=========================================================================================================================================

def Task_7():

     root.destroy()
     
     class Task_7_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.geometry('900x530')
               self.master.title('Task 7: Minima And Maxima In Range Vs Time For Varying Angles')
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text='Range of the projectile vs Time for angles from 10 to 80.', font=('Helvetica Bold', 18))

               self.Plot = tk.Button(self.master, text="Plot The Figure", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0', to='100', resolution='0.01', label='Initial Velocity', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(10)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.animat = tk.Button(self.master, text='Animate the trajectory', command=self.Check)

               self.Set_Slider = tk.Button(self.master, text='Set the Constants to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close the App', command=self.Close)

               self.Graph_ = tk.Button(self.master,text='Plot the Projectiles.', command=self.Graph)

               self.Save_ = tk.Button(self.master,text='Save The Current Figure',command=self.Save)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=10)
               self.U.grid(row=9,column=2,columnspan=2)
               self.Set_Slider.grid(row=10,column=2,columnspan=2)

               self.h_Label.grid(row=1,column=2,columnspan=2)
               self.h.grid(row=2,column=2,columnspan=2)
               self.g_Label.grid(row=3,column=2,columnspan=2)
               self.g.grid(row=4,column=2,columnspan=2)
               self.Plot.grid(row=5, column=2)
               self.animat.grid(row=8,column=2,columnspan=2)
               self.Close_.grid(row=5,column=3)
               self.Graph_.grid(row=7,column=2,columnspan=2)
               self.Save_.grid(row=6,column=2,columnspan=2)

               self.Projectile(10,9.81,0)


          def Projectile(self, u, a, h):
               
               tmax = (u/a)*np.sqrt(2+(2*a*h)/(u**2))

               t = np.linspace(0,2*tmax,10000)

               th1 = 30*np.pi/180
               th2 = 45*np.pi/180
               th3 = 60*np.pi/180
               th4 = 70.5*np.pi/180
               th5 = 78*np.pi/180
               th6 = 85*np.pi/180

               r1 = np.sqrt((u*t*np.cos(th1))**2 + (u*t*np.sin(th1)-0.5*a*t**2)**2)
               r2 = np.sqrt((u*t*np.cos(th2))**2 + (u*t*np.sin(th2)-0.5*a*t**2)**2)
               r3 = np.sqrt((u*t*np.cos(th3))**2 + (u*t*np.sin(th3)-0.5*a*t**2)**2)
               r4 = np.sqrt((u*t*np.cos(th4))**2 + (u*t*np.sin(th4)-0.5*a*t**2)**2)
               r5 = np.sqrt((u*t*np.cos(th5))**2 + (u*t*np.sin(th5)-0.5*a*t**2)**2)
               r6 = np.sqrt((u*t*np.cos(th6))**2 + (u*t*np.sin(th6)-0.5*a*t**2)**2)

               R1 = np.roots([a**2, -3*u*a*np.sin(th1), 2*u**2-2*0*a, 2*u*0*np.sin(th1)])
               R2 = np.roots([a**2, -3*u*a*np.sin(th2), 2*u**2-2*0*a, 2*u*0*np.sin(th2)])
               R3 = np.roots([a**2, -3*u*a*np.sin(th3), 2*u**2-2*0*a, 2*u*0*np.sin(th3)])
               R4 = np.roots([a**2, -3*u*a*np.sin(th4), 2*u**2-2*0*a, 2*u*0*np.sin(th4)])
               R5 = np.roots([a**2, -3*u*a*np.sin(th5), 2*u**2-2*0*a, 2*u*0*np.sin(th5)])
               R6 = np.roots([a**2, -3*u*a*np.sin(th6), 2*u**2-2*0*a, 2*u*0*np.sin(th6)])

               R1ma,R1mi = self.Roots(R1)
               R2ma,R2mi = self.Roots(R2)
               R3ma,R3mi = self.Roots(R3)
               R5ma,R5mi = self.Roots(R5)
               R6ma,R6mi = self.Roots(R6)

               R1min = np.sqrt((u*R1mi*np.cos(th1))**2 + (u*R1mi*np.sin(th1)-0.5*a*R1mi**2)**2)
               R1max = np.sqrt((u*R1ma*np.cos(th1))**2 + (u*R1ma*np.sin(th1)-0.5*a*R1ma**2)**2)

               R2min = np.sqrt((u*R2mi*np.cos(th2))**2 + (u*R2mi*np.sin(th2)-0.5*a*R2mi**2)**2)
               R2max = np.sqrt((u*R2ma*np.cos(th2))**2 + (u*R2ma*np.sin(th2)-0.5*a*R2ma**2)**2)

               R3min = np.sqrt((u*R3mi*np.cos(th3))**2 + (u*R3mi*np.sin(th3)-0.5*a*R3mi**2)**2)
               R3max = np.sqrt((u*R3ma*np.cos(th3))**2 + (u*R3ma*np.sin(th3)-0.5*a*R3ma**2)**2)
               
               R5min = np.sqrt((u*R5mi*np.cos(th5))**2 + (u*R5mi*np.sin(th5)-0.5*a*R5mi**2)**2)
               R5max = np.sqrt((u*R5ma*np.cos(th5))**2 + (u*R5ma*np.sin(th5)-0.5*a*R5ma**2)**2)

               R6min = np.sqrt((u*R6mi*np.cos(th6))**2 + (u*R6mi*np.sin(th6)-0.5*a*R6mi**2)**2)
               R6max = np.sqrt((u*R6ma*np.cos(th6))**2 + (u*R6ma*np.sin(th6)-0.5*a*R6ma**2)**2)

               
               
               if h >= 0:
                    R4max = np.sqrt((u*R4[0].real*np.cos(th4))**2 + (u*R4[0].real*np.sin(th4)-0.5*a*R4[0].real**2)**2)
                    R4min = 0
               else:
                    R4ma,R4mi = self.Roots(R4)
                    R4max = np.sqrt((u*R4ma*np.cos(th4))**2 + (u*R4ma*np.sin(th4)-0.5*a*R4ma**2)**2)
                    R4min = np.sqrt((u*R4mi*np.cos(th4))**2 + (u*R4mi*np.sin(th4)-0.5*a*R4mi**2)**2)

               

               global Z , X4, Y4 , X5mi , Y5mi , X5ma , Y5ma, X6mi , Y6mi , X6ma , Y6ma

               Z = 'Range of Projectile With Time'
               
               self.ax.clear()
               self.ax.plot(t,r1,label='30°')
               self.ax.plot(t,r2,label='45°')
               self.ax.plot(t,r3,label='60°')
               self.ax.plot(t,r4,label='70.5°')
               self.ax.plot(t,r5,label='78°')
               self.ax.plot(t,r6,label='85°')

               if R1mi > 0:
                    self.ax.plot(R1mi,R1min,'o',color=[0,0,1])
               if R1ma > 0:
                    self.ax.plot(R1ma,R1max,'o',color=[1,0,1])

               if R2mi > 0:
                    self.ax.plot(R2mi,R2min,'o',color=[0,0,1])
               if R2ma > 0:
                    self.ax.plot(R2ma,R2max,'o',color=[1,0,1])

               if R3mi > 0:
                    self.ax.plot(R3mi,R3min,'o',color=[0,0,1])
               if R3ma > 0:
                    self.ax.plot(R3ma,R3max,'o',color=[1,0,1])
               
               if h >= 0:
                    self.ax.plot(R4[0].real,R4max,'o',color=[0,1,1])
                    X4 = u*np.cos(th4)*R4[0].real
                    Y4 = u*np.sin(th4)*R4[0].real - 0.5*a*R4[0].real**2

               if R5mi > 0:
                    self.ax.plot(R5mi,R5min,'o',color=[0,0,1])
               if R5ma > 0:
                    self.ax.plot(R5ma,R5max,'o',color=[1,0,1])
                    X5mi = u*np.cos(th5)*R5mi
                    Y5mi = u*np.sin(th5)*R5mi - 0.5*a*R5mi**2

                    X5ma = u*np.cos(th5)*R5ma
                    Y5ma = u*np.sin(th5)*R5ma - 0.5*a*R5ma**2

               if R6mi > 0:
                    self.ax.plot(R6mi,R6min,'o',color=[0,0,1])
               if R6ma > 0:
                    self.ax.plot(R6ma,R6max,'o',color=[1,0,1])

                    X6mi = u*np.cos(th6)*R6mi
                    Y6mi = u*np.sin(th6)*R6mi - 0.5*a*R6mi**2

                    X6ma = u*np.cos(th6)*R6ma
                    Y6ma = u*np.sin(th6)*R6ma - 0.5*a*R6ma**2

               self.ax.grid(True)
               self.ax.set_ylim(ymin=0)
               self.ax.set_xlim(0,2*tmax)
               self.ax.legend(loc='upper left')
               self.ax.set_ylabel('Range /m')
               self.ax.set_ylabel('Time /s')
               self.ax.set_title('The Range of 6 Different Angles With Time \n Plotting Their Minima And Maxima.')
               self.canvas.draw()
          
          def Check(self):
               if Z == 'Projectile Trajectories task 7':
                    self.animate()
               else:
                    pass

          def Roots(self,R1):

               n = 0               
               if R1[0].imag == 0:
                    if R1[0] > 0:
                         n = 1
                         if R1[1].imag == 0:
                              if R1[1] > 0:
                                   if R1[1] < R1[0]:
                                        R1max = R1[0]
                                        R1min = R1[1]
                                   else:
                                        R1max = R1[1]
                                        R1min = R1[0]
                              else:
                                   if R1[2].imag == 0:
                                        if R1[2] > 0:
                                             if R1[2] < R1[0]:
                                                  R1max = R1[0]
                                                  R1min = R1[2]
                                             else:
                                                  R1max = R1[2]
                                                  R1min = R1[2]
                                   else:
                                        R1max = 0
                                        R1min = R1[0]
               else:
                    if R1[1].imag == 0:
                         if R1[1] > 0:
                              n = 1
                              if R1[2].imag == 0:
                                   if R1[2] > 0:
                                        if R1[2] < R1[1]:
                                             R1max = R1[1]
                                             R1min = R1[2]
                                        else:
                                             R1max = R1[2]
                                             R1min = R1[1]
                                   else:
                                        R1min = R1[1]
                                        R1max = 0
               if n == 0:
                    if R1[2].imag == 0:
                         if R1[2] > 0:
                              R1min = R1[2]
                              R1max = 0
                         else:
                              R1max = 0
                              R1min = 0
               
               return R1max, R1min

          def animate(self):

               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               tmax = (u/a)*np.sqrt(2+(2*a*h)/(u**2))

               t = np.linspace(0,2*tmax,10000)

               th1 = 30*np.pi/180
               th2 = 45*np.pi/180
               th3 = 60*np.pi/180
               th4 = 70*np.pi/180
               th5 = 78*np.pi/180
               th6 = 85*np.pi/180

               x1 = u*t*np.cos(th1)
               y1 = h + u*t*np.sin(th1) - 0.5*a*t**2
               x2 = u*t*np.cos(th2)
               y2 = h + u*t*np.sin(th2) - 0.5*a*t**2
               x3 = u*t*np.cos(th3)
               y3 = h + u*t*np.sin(th3) - 0.5*a*t**2
               x4 = u*t*np.cos(th4)
               y4 = h + u*t*np.sin(th4) - 0.5*a*t**2
               x5 = u*t*np.cos(th5)
               y5 = h + u*t*np.sin(th5) - 0.5*a*t**2
               x6 = u*t*np.cos(th6)
               y6 = h + u*t*np.sin(th6) - 0.5*a*t**2

               y_min = h + u*2*tmax*np.sin(th1) - 0.5*4*a*tmax**2
               xmax = u*tmax*1.25*np.cos(th1)

               t1 = (-u*np.sin(th1) - np.sqrt((u*np.sin(th1))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)
               t2 = (-u*np.sin(th2) - np.sqrt((u*np.sin(th2))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)
               t3 = (-u*np.sin(th3) - np.sqrt((u*np.sin(th3))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)
               t4 = (-u*np.sin(th4) - np.sqrt((u*np.sin(th4))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)
               t5 = (-u*np.sin(th5) - np.sqrt((u*np.sin(th5))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)
               t6 = (-u*np.sin(th6) - np.sqrt((u*np.sin(th6))**2 - 4*(-0.5*a)*(h-y_min)))/(-a)

               self.ball, = plt.plot(0,h,'o')
               self.ball1, = plt.plot(0,h,'o')
               self.ball2, = plt.plot(0,h,'o')
               self.ball3, = plt.plot(0,h,'o')
               self.ball4, = plt.plot(0,h,'o')
               self.ball5, = plt.plot(0,h,'o')
               
               def anima(frame):
                    f1 = (10000)/(60*math.ceil(t1))
                    f2 = (10000)/(60*math.ceil(t2))
                    f3 = (10000)/(60*math.ceil(t3))
                    f4 = (10000)/(60*math.ceil(t4))
                    f5 = (10000)/(60*math.ceil(t5))
                    f6 = (10000)/(60*math.ceil(t6))

                    j = frame*int(math.floor(f1))
                    i = frame*int(math.floor(f2))
                    k = frame*int(math.floor(f3))
                    l = frame*int(math.floor(f4))
                    m = frame*int(math.floor(f5))
                    n = frame*int(math.floor(f6))

                    if i >= 10000:
                         i = 10000-1
                    if j >= 10000:
                         j = 10000-1
                    if k >= 10000:
                         k = 10000-1
                    if l >= 10000:
                         l = 10000-1
                    if m >= 10000:
                         m = 10000-1
                    if n >= 10000:
                         n = 10000-1

                    self.ball.set_data(x1[j],y1[j])
                    self.ball1.set_data(x2[i],y2[i])
                    self.ball2.set_data(x3[k],y3[k])
                    self.ball3.set_data(x4[l],y4[l])
                    self.ball4.set_data(x5[m],y5[m])
                    self.ball5.set_data(x6[n],y6[n])

               anim = ani.FuncAnimation(self.fig, func=anima,frames=(120*math.ceil(tmax)), interval=1/60)

               self.canvas.draw()


          def Projectile_Update(self,event):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(u,a,h)

          def Projectile_Update_B(self):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.Projectile(u,a,h)

          def Graph(self):

               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               tmax = (u/a)*np.sqrt(2+(2*a*h)/(u**2))

               t = np.linspace(0,2*tmax,10000)

               th1 = 30*np.pi/180
               th2 = 45*np.pi/180
               th3 = 60*np.pi/180
               th4 = 70*np.pi/180
               th5 = 78*np.pi/180
               th6 = 85*np.pi/180

               x1 = u*t*np.cos(th1)
               y1 = h + u*t*np.sin(th1) - 0.5*a*t**2
               x2 = u*t*np.cos(th2)
               y2 = h + u*t*np.sin(th2) - 0.5*a*t**2
               x3 = u*t*np.cos(th3)
               y3 = h + u*t*np.sin(th3) - 0.5*a*t**2
               x4 = u*t*np.cos(th4)
               y4 = h + u*t*np.sin(th4) - 0.5*a*t**2
               x5 = u*t*np.cos(th5)
               y5 = h + u*t*np.sin(th5) - 0.5*a*t**2
               x6 = u*t*np.cos(th6)
               y6 = h + u*t*np.sin(th6) - 0.5*a*t**2

               y_min = h + u*2*tmax*np.sin(th1) - 0.5*2*a*tmax**2
               xmax = u*tmax*1.25*np.cos(th1)

               global Z

               Z = 'Projectile Trajectories task 7'
               
               self.ax.clear()
               self.ax.plot(x1,y1,label='30°')
               self.ax.plot(x2,y2,label='45°')
               self.ax.plot(x3,y3,label='60°')
               self.ax.plot(x4,y4,label='70°')
               self.ax.plot(x5,y5,label='78°')
               self.ax.plot(x6,y6,label='85°')
               self.ax.plot(X4,Y4,'o',color=[0,1,1])
               self.ax.plot(X5mi,Y5mi,'o',color=[0,0,1])
               self.ax.plot(X5ma,Y5ma,'o',color=[1,0,1])
               self.ax.plot(X6mi,Y6mi,'o',color=[0,0,1])
               self.ax.plot(X6ma,Y6ma,'o',color=[1,0,1])
               self.ax.grid(True)
               self.ax.set_ylim(ymin=y_min)
               self.ax.set_xlim(0,xmax)
               self.ax.legend()
               self.ax.set_ylabel('y /m')
               self.ax.set_xlabel('x /m')
               self.ax.set_title('Trajectories of the projectiles from the previous plot.')
               self.canvas.draw()

          def Close(self):
               root7.destroy()
               Open_Gui()

          def setsliders(self):
               self.U.set(10)
               self.g.delete(0,tk.END)
               self.h.delete(0,tk.END)
               self.g.insert(0,'9.81')
               self.h.insert(0,'0')

               self.Projectile(10,9.81,0)

          
          def Save(self):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.fig.savefig(f'{Z},u={u}, a={a}, h={h}.png')

     root7 = tk.Tk()
     center_screen_1(900,530,root7)
     app7 = Task_7_GUI(root7)
     app7.mainloop()

#=========================================================================================================================================

def Task_8():
     
     root.destroy()
     
     class Task_8_GUI(tk.Frame):

          def __init__(self,master=None):
               super().__init__(master)
               self.master.geometry('900x560')
               self.master.title('Task 8: Numerical Timestep Method To Animate A Bouncing Ball')
               self.Widgets()

          def Widgets(self):
               self.fig, self.ax = plt.subplots()
               self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

               self.Title = tk.Label(self.master, text='Numerical Method To Find The\nTrajectory Of A Bouncing Ball', font=('Helvetica Bold', 18))

               self.Plot = tk.Button(self.master, text="Plot The Figure", command=self.Projectile_Update_B)

               self.U = tk.Scale(self.master, from_='0', to='100', resolution='0.01', label='Initial Velocity', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.U.set(10)

               self.theta = tk.Scale(self.master, from_='0', to='89.9', resolution='0.01', label='Horizontal Angle', orient=tk.HORIZONTAL, command=self.Projectile_Update)
               self.theta.set(45)

               self.g_Label = tk.Label(self.master, text="Gravitational Field Strength / ms^-2.", font=('Helvetica bold', 12))
               self.g = tk.Entry(self.master, width=10)
               self.g.insert(0,"9.81")

               self.h_Label = tk.Label(self.master, text="Height / m", font=('Helvetica bold', 12))
               self.h = tk.Entry(self.master, width=10)
               self.h.insert(0,"0")

               self.C_Label = tk.Label(self.master, text="Coefficient of Restitution", font=('Helvetica bold', 12))
               self.C = tk.Entry(self.master, width=10)
               self.C.insert(0,"0.6")

               self.animat = tk.Button(self.master, text='Animate the trajectory', command=self.animate)

               self.Set_Slider = tk.Button(self.master, text='Set the Constants to original values.', command=self.setsliders)

               self.Close_ = tk.Button(self.master, text='Close the App', command=self.Close)


               self.Save_ = tk.Button(self.master,text='Save The Current Figure',command=self.Save)

               self.Title.grid(row=0, column=0, columnspan=2)
               self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=12)
               self.U.grid(row=11,column=2,columnspan=2)
               self.theta.grid(row=10,column=2,columnspan=2)
               self.Set_Slider.grid(row=12,column=2,columnspan=2)

               self.h_Label.grid(row=1,column=2,columnspan=2)
               self.h.grid(row=2,column=2,columnspan=2)
               self.g_Label.grid(row=3,column=2,columnspan=2)
               self.g.grid(row=4,column=2,columnspan=2)
               self.C_Label.grid(row=5,column=2,columnspan=2)
               self.C.grid(row=6,column=2,columnspan=2)
               self.Plot.grid(row=7, column=2)
               self.animat.grid(row=9,column=2,columnspan=2)
               self.Close_.grid(row=7,column=3)
               self.Save_.grid(row=8,column=2,columnspan=2)

               self.Projectile(10,45,9.81,0,0.6)


          def Projectile(self, u, ang, a, h, C):

               tmax = (u/a)*np.sqrt(2+(2*a*h)/(u**2))

               N = 6
               
               th = ang*np.pi/180

               uy = u*np.sin(th)

               y_max = ((u*np.sin(th))**2)/(2*a) + h
               xymax = (np.sin(th)*np.cos(th)*u**2)/(a)

               t = [0]*50000
               dt = (4*tmax)/(10000)

               x = [0]*50000
               t1 = [0]*50000
               y = [h]*50000
               vy = [uy]*50000

               i = 0

               for n in range(50000):

                    t[n] = t[n-1] + dt

                    x[n] = u*np.cos(th)*t[n]

                    t1[n] = t1[n-1] + dt

                    y[n] = h + uy*t1[n] - 0.5*a*t1[n]**2

                    vy[n] = uy - a*t1[n]

                    if y[n] < 0:
                         y[n] = 0
                         uy = -C*vy[n]
                         t1[n] = 0
                         h = 0
                         i = i+1
                    
                    if i == N+1:
                         tend = t[n]
                         xend = x[n]
                         it = n


               self.ax.clear()
               self.ax.plot(x,y)
               self.ax.grid(True)
               self.ax.set_ylabel('y /m')
               self.ax.set_xlabel('x /m')
               self.ax.set_title(f'Bouncing Projectile: u = {u}ms^-1, C = {C}, Theta = {ang}°\n h = {h}m, t_max = {round(tend,2)}s , Bounces = {N}')
               self.ax.set_xlim(0,xend)
               self.ax.set_ylim(0,1.1*y_max)
               self.canvas.draw()

          def animate(self):

               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())
               ang = self.theta.get()
               C = float(self.C.get())

               tmax = (u/a)*np.sqrt(2+(2*a*h)/(u**2))

               N = 6
               
               th = ang*np.pi/180

               uy = u*np.sin(th)

               y_max = ((u*np.sin(th))**2)/(2*a) + h
               xymax = (np.sin(th)*np.cos(th)*u**2)/(a)

               t = [0]*10000
               dt = (4*tmax)/(10000)

               x = [0]*10000
               t1 = [0]*10000
               y = [h]*10000
               vy = [uy]*10000

               i = 0

               for n in range(10000):

                    t[n] = t[n-1] + dt

                    x[n] = u*np.cos(th)*t[n]

                    t1[n] = t1[n-1] + dt

                    y[n] = h + uy*t1[n] - 0.5*a*t1[n]**2

                    vy[n] = uy - a*t1[n]

                    if y[n] < 0:
                         y[n] = 0
                         uy = -C*vy[n]
                         t1[n] = 0
                         h = 0
                         i = i+1
                    
                    if i == N+1:
                         tend = t[n]
                         xend = x[n]
                         it = n

               history_len = it

               self.ax.clear()
               self.ball, = self.ax.plot(0,h,'o')
               self.trace, = self.ax.plot([], [], '-', ms=2)
               history_x1, history_y1 = deque(maxlen=history_len), deque(maxlen=history_len)
               self.ax.grid(True)
               self.ax.set_ylabel('y /m')
               self.ax.set_xlabel('x /m')
               self.ax.set_xlim(0,xend)
               self.ax.set_ylim(0,1.1*y_max)
               self.ax.set_title(f'Bouncing Projectile: u = {u}ms^-1, C = {C}, Theta = {ang}°\n h = {h}m, t = 0s of {round(tend,2)}s , Bounces = {N}')
               
               def trace_(frame):
                    f1 = (it)/(60*math.ceil(tend))

                    i = frame*int(math.floor(f1))

                    if i >= 10000:
                         i = 10000-1
                    
                    thisx = [0, x[i]]
                    thisy = [0, y[i]]

                    if i == 0:
                         history_x1.clear()
                         history_y1.clear()

                    history_x1.appendleft(thisx[1])
                    history_y1.appendleft(thisy[1])

                    self.trace.set_data(history_x1, history_y1)

                    return self.trace
               
               def anima(frame):
                    f1 = (it)/(60*math.ceil(tend))

                    i = frame*int(math.floor(f1))

                    if i >= 10000:
                         i = 10000-1

                    self.ball.set_data(x[i],y[i])

                    self.trace = trace_(frame)

                    self.ax.set_title(f'Bouncing Projectile: u = {u}ms^-1, C = {C}, Theta = {ang}°\n h = {h}m, t = {round(t[i],1)}s of {round(tend,2)}s , Bounces = {N}')


               anim = ani.FuncAnimation(self.fig, func=anima,frames=(60*math.ceil(tend)), interval=1/60)

               self.canvas.draw()


          def Projectile_Update(self,event):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())
               ang = self.theta.get()
               C = float(self.C.get())

               if C > 1:
                    pass
               else:
                    self.Projectile(u, ang, a, h, C)

          def Projectile_Update_B(self):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())
               ang = self.theta.get()
               C = float(self.C.get())

               if C > 1:
                    pass
               else:
                    self.Projectile(u, ang, a, h, C)

          def Close(self):
               root8.destroy()
               Open_Gui()

          def setsliders(self):
               self.U.set(10)
               self.theta.set(45)
               self.g.delete(0,tk.END)
               self.h.delete(0,tk.END)
               self.C.delete(0,tk.END)
               self.g.insert(0,'9.81')
               self.h.insert(0,'0')
               self.C.insert(0,'0.6')

               self.Projectile(10,45,9.81,0)

          
          def Save(self):
               u = self.U.get()
               h = float(self.h.get())
               a = float(self.g.get())

               self.fig.savefig(f'Ball Bounce Animation,u={u}, a={a}, h={h}.png')

     root8 = tk.Tk()
     center_screen_1(900,560,root8)
     app8 = Task_8_GUI(root8)
     app8.mainloop()

#=========================================================================================================================================

def Task_9():
     pass

#=========================================================================================================================================

def Task_10():
     pass

#=========================================================================================================================================

def callback(url):
     webbrowser.open_new_tab(url)


#=========================================================================================================================================

def center_screen_1(window_width,window_height, root1):
    """ gets the coordinates of the center of the screen """
    global screen_height, screen_width, x_cordinate, y_cordinate
    screen_width = root1.winfo_screenwidth()
    screen_height = root1.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root1.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

#=========================================================================================================================================
     
# Creates the root for the GUI
root = tk.Tk()
center_screen_1(500,400,root)
# Defines the geometry of the GUI
root.geometry("500x400")
# Defines the title of the GUI
root.title("BPho Computational Challenge 2024 App")

# Defines a label using tkinter
label = tk.Label(root, text="An App Storing all of the Tasks and any additional recources created.")
# Packs the label into the GUI
label.pack()

# Defines a button and sets the button to trigger Task_1 function when pressed
button1 = tk.Button(root, text="Task 1: Projectile Motion Plotter, Timestep Method", command=Task_1)
# Packs the button into the GUI
button1.pack()

# Defines a button and sets the button to trigger Task_2 function when pressed
button2 = tk.Button(root, text="Task 2: Projectile Motion Plotter, Analytical Method", command=Task_2)
# Packs the button into the GUI
button2.pack()

# Defines a button and sets the button to trigger Task_3 function when pressed
button3 = tk.Button(root, text="Task 3: Projectiles Through A Fixed Point", command=Task_3)
# Packs the button into the GUI
button3.pack()

# Defines a button and sets the button to trigger Task_4 function when pressed
button4 = tk.Button(root, text="Task 4: Maximising Projectile Range And Colour Maps", command=Task_4)
# Packs the button into the GUI
button4.pack()

# Defines a button and sets the button to trigger Task_5 function when pressed
button5 = tk.Button(root, text="Task 5: Bounding Parabola For Peojectiles Through A Fixed Point", command=Task_5)
# Packs the button into the GUI
button5.pack()

# Defines a button and sets the button to trigger Task_6 function when pressed
button6 = tk.Button(root, text="Task 6: Path Length Of Projectiles And The Optimum Angle", command=Task_6)
# Packs the button into the GUI
button6.pack()

# Defines a button and sets the button to trigger Task_7 function when pressed
button7 = tk.Button(root, text="Task 7: Minima And Maxima In Range Vs Time For Varying Angles", command=Task_7)
# Packs the button into the GUI
button7.pack()

# Defines a button and sets the button to trigger Task_8 function when pressed
button8 = tk.Button(root, text="Task 8: Numerical Timestep Method To Animate A Bouncing Ball", command=Task_8)
# Packs the button into the GUI
button8.pack()

# Defines a button and sets the button to trigger Task_9 function when pressed
button9 = tk.Button(root, text="Task 9: Comparing Drag-Free Models Against Drag Models", command=Task_9)
# Packs the button into the GUI
button9.pack()

Label = tk.Label(root, text="Paper Download", fg='Blue', cursor='hand2', font=('Helvetica',12))
Label.pack()
Label.bind("<Button-1>", lambda e: callback("https://www.overleaf.com/project/651fbbd349bbcbe01a085191"))


#=========================================================================================================================================

# WIDGETS
     
def Open_Gui():

     # Creates the root for the GUI
     global root
     root = tk.Tk()
     center_screen_1(500,400,root)
     # Defines the geometry of the GUI
     root.geometry("500x400")
     # Defines the title of the GUI
     root.title("BPho Computational Challenge 2024 App")

     # Defines a label using tkinter
     label = tk.Label(root, text="An App Storing all of the Tasks and any additional recources created.")
     # Packs the label into the GUI
     label.pack()

     # Defines a button and sets the button to trigger Task_1 function when pressed
     button1 = tk.Button(root, text="Task 1: Projectile Motion Plotter, Timestep Method", command=Task_1)
     # Packs the button into the GUI
     button1.pack()

     # Defines a button and sets the button to trigger Task_2 function when pressed
     button2 = tk.Button(root, text="Task 2: Projectile Motion Plotter, Analytical Method", command=Task_2)
     # Packs the button into the GUI
     button2.pack()

     # Defines a button and sets the button to trigger Task_3 function when pressed
     button3 = tk.Button(root, text="Task 3: Projectiles Through A Fixed Point", command=Task_3)
     # Packs the button into the GUI
     button3.pack()

     # Defines a button and sets the button to trigger Task_4 function when pressed
     button4 = tk.Button(root, text="Task 4: Maximising Projectile Range And Colour Maps", command=Task_4)
     # Packs the button into the GUI
     button4.pack()

     # Defines a button and sets the button to trigger Task_5 function when pressed
     button5 = tk.Button(root, text="Task 5: Bounding Parabola For Peojectiles Through A Fixed Point", command=Task_5)
     # Packs the button into the GUI
     button5.pack()

     # Defines a button and sets the button to trigger Task_6 function when pressed
     button6 = tk.Button(root, text="Task 6: Path Length Of Projectiles And The Optimum Angle", command=Task_6)
     # Packs the button into the GUI
     button6.pack()

     # Defines a button and sets the button to trigger Task_7 function when pressed
     button7 = tk.Button(root, text="Task 7: Minima And Maxima In Range Vs Time For Varying Angles", command=Task_7)
     # Packs the button into the GUI
     button7.pack()

     # Defines a button and sets the button to trigger Task_8 function when pressed
     button8 = tk.Button(root, text="Task 8: Numerical Timestep Method To Animate A Bouncing Ball", command=Task_8)
     # Packs the button into the GUI
     button8.pack()

     # Defines a button and sets the button to trigger Task_9 function when pressed
     button9 = tk.Button(root, text="Task 9: Comparing Drag-Free Models Against Drag Models", command=Task_9)
     # Packs the button into the GUI
     button9.pack()

     Label = tk.Label(root, text="Paper", fg='Blue', cursor='hand2')
     Label.pack()
     Label.bind("<Button-1>", lambda e: callback("https://www.overleaf.com/project/651fbbd349bbcbe01a085191"))

     root.mainloop()


#=======================================================================================================================================================

# Opens the GUI

root.mainloop()
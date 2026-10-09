import tkinter as tk
import math

class RefractionSimulator:
    def __init__(self, master):
        self.master = master
        master.title("光折射模拟器")
      
        self.n1 = 1.0
        self.n2 = 1.5         
        self.theta1 = 30       

        self.canvas = tk.Canvas(master, width=700, height=500, bg='white')
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        control = tk.Frame(master)
        control.pack(side=tk.BOTTOM, pady=10)

        tk.Label(control, text="介质折射率 n2:").grid(row=0, column=0, padx=5)
        self.n2_entry = tk.Entry(control, width=8)
        self.n2_entry.insert(0, "1.5")
        self.n2_entry.grid(row=0, column=1, padx=5)
        self.n2_entry.bind('<Return>', self.update)

        tk.Label(control, text="入射角 θ1 (°):").grid(row=0, column=2, padx=5)
        self.slider = tk.Scale(control, from_=0, to=89, resolution=0.1,
                               orient=tk.HORIZONTAL, length=200, command=self.update)
        self.slider.set(30)
        self.slider.grid(row=0, column=3, padx=5)

        self.info_label = tk.Label(control, text="θ1 = 30°, θ2 = 19.47°")
        self.info_label.grid(row=0, column=4, padx=10)

        tk.Button(control, text="更新", command=self.button_click).grid(row=0, column=5, padx=5)

        tk.Label(control, text="精确入射角:").grid(row=1, column=0, padx=5, pady=5)
        self.angle_entry = tk.Entry(control, width=6)
        self.angle_entry.insert(0, "30.0")
        self.angle_entry.grid(row=1, column=1, padx=5, pady=5)
        self.angle_entry.bind('<Return>', self.angle_entry_update)
        self.angle_entry.bind('<FocusOut>', self.angle_entry_update)

        self.update()

    def update(self, event=None):
        try:
            n2 = float(self.n2_entry.get())
            if n2 <= 0:
                raise ValueError
            self.n2 = n2
        except:
            self.n2 = 1.5
            self.n2_entry.delete(0, tk.END)
            self.n2_entry.insert(0, "1.5")

        theta1_deg = self.slider.get()
        self.theta1 = theta1_deg

        theta1_rad = math.radians(theta1_deg)
        sin_theta2 = (self.n1 / self.n2) * math.sin(theta1_rad)

        if sin_theta2 > 1:
            theta2_deg = None
        else:
            theta2_rad = math.asin(sin_theta2)
            theta2_deg = math.degrees(theta2_rad)

        if theta2_deg is not None:
            self.info_label.config(text=f"θ1 = {theta1_deg:.1f}°, θ2 = {theta2_deg:.1f}°")
        else:
            self.info_label.config(text=f"θ1 = {theta1_deg:.1f}°, 全反射！")

        self.draw(theta1_deg, theta2_deg)

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, f"{self.theta1:.1f}")

    def draw(self, theta1_deg, theta2_deg):
        self.canvas.delete("all")

        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 700
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 500

        x_line = w // 2
        self.canvas.create_line(x_line, 0, x_line, h, fill='black', width=2)

        self.canvas.create_text(x_line // 2, 30, text="空气 (n1 = 1.0)", fill='gray')
        self.canvas.create_text(x_line + x_line // 2, 30, text="介质 (n2 = 1.5)", fill='gray')

        cx, cy = x_line, h // 2
        self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill='red', outline='red')
        self.canvas.create_text(cx + 10, cy - 10, text="入射点", fill='gray', anchor='w')
        
        self.canvas.create_line(50, cy, w - 50, cy, dash=(4, 4), fill='gray')

        theta1_rad = math.radians(theta1_deg)
        start_x = 50
        start_y = cy - (cx - start_x) * math.tan(theta1_rad)
        self.canvas.create_line(start_x, start_y, cx, cy,
                                fill='blue', width=2, arrow=tk.LAST)
        
        if theta2_deg is not None:
            theta2_rad = math.radians(theta2_deg)
            end_x = w - 50
            end_y = cy + (end_x - cx) * math.tan(theta2_rad)
            self.canvas.create_line(cx, cy, end_x, end_y,
                                    fill='red', width=2, arrow=tk.LAST)

            arc_r = 40
            self.canvas.create_arc(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                                   start=180 - theta1_deg, extent=theta1_deg,
                                   style=tk.ARC, outline='blue', width=2)
            self.canvas.create_text(cx - 70, cy - 30, text=f"θ1 = {theta1_deg:.1f}°", fill='blue')

            self.canvas.create_arc(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                                   start=0-theta2_deg, extent=theta2_deg,
                                   style=tk.ARC, outline='red', width=2)
            self.canvas.create_text(cx + 70, cy + 30, text=f"θ2 = {theta2_deg:.1f}°", fill='red')
        else:
            self.canvas.create_text(cx + 100, cy - 50, text="全反射", fill='red', font=('Arial', 20))

        self.canvas.create_text(40, 20, text="入射光", fill='blue', anchor='w')
        self.canvas.create_line(10, 15, 30, 15, fill='blue', width=2)
        self.canvas.create_text(40, 40, text="折射光", fill='red', anchor='w')
        self.canvas.create_line(10, 35, 30, 35, fill='red', width=2)
        self.canvas.create_text(40, 60, text="法线", fill='gray', anchor='w')
        self.canvas.create_line(10, 55, 30, 55, dash=(4, 4), fill='gray', width=2)

    def angle_entry_update(self, event=None):
        try:
            val = float(self.angle_entry.get())
            if val < 0:
                val = 0
            elif val > 89:
                val = 89
            self.slider.set(val)
            self.update()  
        except ValueError:
      
            self.angle_entry.delete(0, tk.END)
            self.angle_entry.insert(0, f"{self.slider.get():.1f}")

    def button_click(self):
  
        self.angle_entry_update()

if __name__ == "__main__":
    root = tk.Tk()
    app = RefractionSimulator(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd

# ----------------- Menu -----------------
menu = {'Pizza': 100, 'Burger': 120, 'Sandwich': 150, 'Coffee': 50, 'Pasta': 200}
order_list = []

# ----------------- GUI Application -----------------
class FoodOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍔 Food Ordering System")
        self.root.geometry("500x700")
        self.username = ""

        # --- Welcome Label ---
        tk.Label(root, text="Welcome to Food Ordering App 🍕", font=("Helvetica", 18, "bold")).pack(pady=20)

        # --- Username Entry ---
        self.username_btn = tk.Button(root, text="Enter Your Name", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                                      command=self.get_username)
        self.username_btn.pack(pady=10)

        # --- Menu Display ---
        tk.Label(root, text="Menu", font=("Helvetica", 16, "underline")).pack(pady=10)
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()
        for item, price in menu.items():
            tk.Label(self.menu_frame, text=f"{item} : ₹{price}", font=("Helvetica", 12)).pack(anchor='w')

        # --- Buttons ---
        self.order_btn = tk.Button(root, text="New Order", font=("Helvetica", 12), bg="#2196F3", fg="white",
                                   command=self.new_order)
        self.order_btn.pack(pady=10)

        self.display_btn = tk.Button(root, text="Display Order", font=("Helvetica", 12), bg="#FF9800", fg="white",
                                     command=self.display_order)
        self.display_btn.pack(pady=5)

        self.bill_btn = tk.Button(root, text="Generate Bill", font=("Helvetica", 12), bg="#f44336", fg="white",
                                  command=self.generate_bill)
        self.bill_btn.pack(pady=5)

    # --- Get Username ---
    def get_username(self):
        self.username = simpledialog.askstring("Username", "Enter your name:")
        if self.username:
            messagebox.showinfo("Welcome", f"Hello {self.username}! Let's start ordering.")

    # --- New Order ---
    def new_order(self):
        if not self.username:
            messagebox.showwarning("Warning", "Please enter your name first!")
            return
        while True:
            item = simpledialog.askstring("Order", f"Enter food item (or type 'ok' to finish):\nMenu: {', '.join(menu.keys())}")
            if item is None or item.lower() == 'ok':
                messagebox.showinfo("Info", "Order completed.")
                break
            item_title = item.title()
            if item_title in menu:
                quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {item_title}:")
                if quantity and quantity > 0:
                    order_list.append((item_title, menu[item_title], quantity))
                    messagebox.showinfo("Added", f"Added {item_title} x {quantity} to your order.")
                else:
                    messagebox.showwarning("Invalid", "Please enter a valid quantity!")
            else:
                messagebox.showwarning("Invalid", "Item not in menu!")

    # --- Display Order ---
    def display_order(self):
        if not order_list:
            messagebox.showinfo("Order", "No items ordered yet.")
            return
        display_win = tk.Toplevel(self.root)
        display_win.title("Current Order")
        df = pd.DataFrame(order_list, columns=["Item", "Price", "Quantity"])
        tree = ttk.Treeview(display_win, columns=("Item", "Price", "Quantity"), show='headings')
        tree.pack(expand=True, fill='both')
        tree.heading("Item", text="Item")
        tree.heading("Price", text="Price")
        tree.heading("Quantity", text="Quantity")
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row["Item"], row["Price"], row["Quantity"]))

    # --- Generate Bill ---
    def generate_bill(self):
        if not order_list:
            messagebox.showinfo("Bill", "No items to generate a bill.")
            return
        total = sum(price * quantity for item, price, quantity in order_list)
        filename = f"{self.username}.csv"
        with open(filename, 'w') as file:
            file.write("Food Item,Price,Quantity\n")
            for item, price, quantity in order_list:
                file.write(f"{item},{price},{quantity}\n")
            file.write(f"Total,,{total}\n")
        messagebox.showinfo("Bill Generated", f"Your total bill is: ₹{total}\nBill saved to {filename}.")


# ----------------- Run App -----------------
root = tk.Tk()
app = FoodOrderApp(root)
root.mainloop()

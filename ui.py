import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import database


def create_application():

    root = tk.Tk()

    root.title("Job Application Tracker")
    root.geometry("1000x700")
    root.minsize(900, 600)

    # ---------------- STYLING ----------------

    style = ttk.Style()

    style.configure(
        "Treeview",
        rowheight=32,
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold")
    )

    style.configure(
        "TButton",
        font=("Arial", 10)
    )

    style.configure(
        "TCombobox",
        font=("Arial", 10)
    )

    # ---------------- FUNCTIONS ----------------

    def update_dashboard():

        total = database.get_total_count()

        applied = database.get_status_count(
            "Applied"
        )

        oa = database.get_status_count(
            "Online Assessment"
        )

        interview = database.get_status_count(
            "Interview"
        )

        rejected = database.get_status_count(
            "Rejected"
        )

        offer = database.get_status_count(
            "Offer"
        )

        total_label.config(
            text=f"Total\n{total}"
        )

        applied_label.config(
            text=f"Applied\n{applied}"
        )

        oa_label.config(
            text=f"Online Assessment\n{oa}"
        )

        interview_label.config(
            text=f"Interview\n{interview}"
        )

        rejected_label.config(
            text=f"Rejected\n{rejected}"
        )

        offer_label.config(
            text=f"Offer\n{offer}"
        )


    def display_applications(applications):

        for item in table.get_children():
            table.delete(item)

        for index, application in enumerate(applications):

            tag = (
                "evenrow"
                if index % 2 == 0
                else "oddrow"
            )

            table.insert(
                "",
                tk.END,
                values=application,
                tags=(tag,)
            )


    def load_applications():

        applications = database.get_applications()

        display_applications(applications)

        update_dashboard()


    def clear_form():

        company_entry.delete(
            0,
            tk.END
        )

        role_entry.delete(
            0,
            tk.END
        )

        date_entry.delete(
            0,
            tk.END
        )

        status_combo.set("Applied")


    def validate_input(
        company,
        role,
        date_applied,
        status
    ):

        if not company:

            messagebox.showerror(
                "Invalid Input",
                "Company name is required."
            )

            return False


        if not role:

            messagebox.showerror(
                "Invalid Input",
                "Job role is required."
            )

            return False


        if not date_applied:

            messagebox.showerror(
                "Invalid Input",
                "Date applied is required."
            )

            return False


        try:

            datetime.strptime(
                date_applied,
                "%d-%m-%Y"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Date must be in DD-MM-YYYY format."
            )

            return False


        if not status:

            messagebox.showerror(
                "Invalid Input",
                "Please select a status."
            )

            return False


        return True


    def set_today():

        today = datetime.now().strftime(
            "%d-%m-%Y"
        )

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            today
        )


    def add_application():

        company = company_entry.get().strip()
        role = role_entry.get().strip()
        date_applied = date_entry.get().strip()
        status = status_combo.get()


        if not validate_input(
            company,
            role,
            date_applied,
            status
        ):
            return


        database.add_application(
            company,
            role,
            date_applied,
            status
        )


        clear_form()

        load_applications()

        messagebox.showinfo(
            "Success",
            "Application added successfully."
        )


    def select_application(event):

        selected = table.selection()

        if not selected:
            return

        values = table.item(
            selected[0],
            "values"
        )


        company_entry.delete(
            0,
            tk.END
        )

        company_entry.insert(
            0,
            values[1]
        )


        role_entry.delete(
            0,
            tk.END
        )

        role_entry.insert(
            0,
            values[2]
        )


        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            values[3]
        )


        status_combo.set(
            values[4]
        )


    def update_application():

        selected = table.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select an application to update."
            )

            return


        values = table.item(
            selected[0],
            "values"
        )

        application_id = values[0]


        company = company_entry.get().strip()
        role = role_entry.get().strip()
        date_applied = date_entry.get().strip()
        status = status_combo.get()


        if not validate_input(
            company,
            role,
            date_applied,
            status
        ):
            return


        database.update_application(
            application_id,
            company,
            role,
            date_applied,
            status
        )


        clear_form()

        load_applications()

        messagebox.showinfo(
            "Success",
            "Application updated successfully."
        )


    def delete_application():

        selected = table.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select an application to delete."
            )

            return


        values = table.item(
            selected[0],
            "values"
        )

        application_id = values[0]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this application?"
        )

        if not confirm:
            return


        database.delete_application(
            application_id
        )


        clear_form()

        load_applications()

        messagebox.showinfo(
            "Success",
            "Application deleted successfully."
        )


    def search_applications():

        search_text = search_entry.get().strip()

        selected_status = filter_combo.get()


        applications = database.search_applications(
            search_text,
            selected_status
        )


        display_applications(
            applications
        )


    def reset_search():

        search_entry.delete(
            0,
            tk.END
        )

        filter_combo.set(
            "All"
        )

        load_applications()


    def sort_table(column, reverse):

        data = [
            (
                table.set(item, column),
                item
            )
            for item in table.get_children("")
        ]


        data.sort(
            reverse=reverse
        )


        for index, (_, item) in enumerate(data):

            table.move(
                item,
                "",
                index
            )


        table.heading(
            column,
            command=lambda: sort_table(
                column,
                not reverse
            )
        )


    # ---------------- HEADER ----------------

    header_frame = tk.Frame(root)

    header_frame.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )


    title = tk.Label(
        header_frame,
        text="Job Application Tracker",
        font=("Arial", 24, "bold")
    )

    title.pack(
        anchor="w"
    )


    subtitle = tk.Label(
        header_frame,
        text="Track and manage your job applications",
        font=("Arial", 11)
    )

    subtitle.pack(
        anchor="w",
        pady=(3, 0)
    )


    # ---------------- DASHBOARD ----------------

    dashboard_frame = tk.Frame(root)

    dashboard_frame.pack(
        pady=10
    )


    total_label = tk.Label(
        dashboard_frame,
        text="Total\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    total_label.grid(
        row=0,
        column=0,
        padx=5
    )


    applied_label = tk.Label(
        dashboard_frame,
        text="Applied\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    applied_label.grid(
        row=0,
        column=1,
        padx=5
    )


    oa_label = tk.Label(
        dashboard_frame,
        text="Online Assessment\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    oa_label.grid(
        row=0,
        column=2,
        padx=5
    )


    interview_label = tk.Label(
        dashboard_frame,
        text="Interview\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    interview_label.grid(
        row=0,
        column=3,
        padx=5
    )


    rejected_label = tk.Label(
        dashboard_frame,
        text="Rejected\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    rejected_label.grid(
        row=0,
        column=4,
        padx=5
    )


    offer_label = tk.Label(
        dashboard_frame,
        text="Offer\n0",
        font=("Arial", 11, "bold"),
        width=15,
        relief="groove",
        padx=10,
        pady=10
    )

    offer_label.grid(
        row=0,
        column=5,
        padx=5
    )


    # ---------------- FORM ----------------

    form_frame = tk.Frame(root)

    form_frame.pack(
        pady=5
    )


    tk.Label(
        form_frame,
        text="Company:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5
    )


    company_entry = tk.Entry(
        form_frame,
        width=25
    )

    company_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )


    tk.Label(
        form_frame,
        text="Role:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=5
    )


    role_entry = tk.Entry(
        form_frame,
        width=25
    )

    role_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
    )


    tk.Label(
        form_frame,
        text="Date Applied:"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=5
    )


    date_entry = tk.Entry(
        form_frame,
        width=17
    )

    date_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=5
    )


    today_button = tk.Button(
        form_frame,
        text="Today",
        command=set_today
    )

    today_button.grid(
        row=2,
        column=2,
        padx=5
    )


    tk.Label(
        form_frame,
        text="Status:"
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=5
    )


    status_combo = ttk.Combobox(
        form_frame,
        values=[
            "Applied",
            "Online Assessment",
            "Interview",
            "Rejected",
            "Offer"
        ],
        state="readonly",
        width=22
    )

    status_combo.grid(
        row=3,
        column=1,
        padx=10,
        pady=5
    )

    status_combo.set("Applied")


    # ---------------- BUTTONS ----------------

    button_frame = tk.Frame(root)

    button_frame.pack(
        pady=10
    )


    tk.Button(
        button_frame,
        text="Add Application",
        command=add_application,
        width=18,
        padx=5,
        pady=5
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    tk.Button(
        button_frame,
        text="Update Application",
        command=update_application,
        width=18,
        padx=5,
        pady=5
    ).grid(
        row=0,
        column=1,
        padx=5
    )


    tk.Button(
        button_frame,
        text="Delete Application",
        command=delete_application,
        width=18,
        padx=5,
        pady=5
    ).grid(
        row=0,
        column=2,
        padx=5
    )


    tk.Button(
        button_frame,
        text="Clear",
        command=clear_form,
        width=18,
        padx=5,
        pady=5
    ).grid(
        row=0,
        column=3,
        padx=5
    )


    # ---------------- SEARCH ----------------

    search_frame = tk.Frame(root)

    search_frame.pack(
        pady=5
    )


    tk.Label(
        search_frame,
        text="Search:"
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    search_entry = tk.Entry(
        search_frame,
        width=25
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )


    tk.Label(
        search_frame,
        text="Status:"
    ).grid(
        row=0,
        column=2,
        padx=5
    )


    filter_combo = ttk.Combobox(
        search_frame,
        values=[
            "All",
            "Applied",
            "Online Assessment",
            "Interview",
            "Rejected",
            "Offer"
        ],
        state="readonly",
        width=18
    )

    filter_combo.grid(
        row=0,
        column=3,
        padx=5
    )

    filter_combo.set("All")


    tk.Button(
        search_frame,
        text="Search",
        command=search_applications,
        width=12
    ).grid(
        row=0,
        column=4,
        padx=5
    )


    tk.Button(
        search_frame,
        text="Reset",
        command=reset_search,
        width=12
    ).grid(
        row=0,
        column=5,
        padx=5
    )


    # ---------------- TABLE ----------------

    table_frame = tk.Frame(root)

    table_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=20,
        pady=10
    )


    columns = (
        "ID",
        "Company",
        "Role",
        "Date Applied",
        "Status"
    )


    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    for column in columns:

        table.heading(
            column,
            text=column,
            command=lambda c=column:
                sort_table(c, False)
        )


    table.column(
        "ID",
        width=50,
        anchor="center"
    )

    table.column(
        "Company",
        width=150
    )

    table.column(
        "Role",
        width=250
    )

    table.column(
        "Date Applied",
        width=120,
        anchor="center"
    )

    table.column(
        "Status",
        width=160,
        anchor="center"
    )


    table.tag_configure(
        "evenrow"
    )

    table.tag_configure(
        "oddrow"
    )


    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )


    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )


    table.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )


    table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    vertical_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )


    horizontal_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    table_frame.grid_rowconfigure(
        0,
        weight=1
    )


    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    table.bind(
        "<ButtonRelease-1>",
        select_application
    )


    # ---------------- STARTUP ----------------

    load_applications()


    return root
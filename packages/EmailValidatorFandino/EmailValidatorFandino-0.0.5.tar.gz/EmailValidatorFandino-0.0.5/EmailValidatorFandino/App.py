import tkinter as tk
from tkinter import ttk
from EmailValidatorFandino import validateMail as vm
# import validateMail as vm


class Model:
    def __init__(self, email):
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        vm.validate(value)
        aux = vm.validate_mail()
        if aux[0] == 'OK 2' and aux[1] == 'OK 2' or aux[0] == 'OK' and aux[1] == 'OK' or aux[0] == 'OK' and aux[1] == \
                'OK 2':
            self.__email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    def save(self):
        pass


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # create widgets
        self.label = ttk.Label(self, text='Email:')
        self.label.grid(row=1, column=0)

        # email entry
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # save button
        self.save_button = ttk.Button(self, text='Verify', command=self.save_button_clicked)
        self.save_button.grid(row=1, column=3, padx=10)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=2, column=1, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def save_button_clicked(self):
        if self.controller:
            self.controller.save(self.email_var.get())

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        self.email_entry['foreground'] = 'red'

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.email_entry['foreground'] = 'black'
        self.email_var.set('')

    def hide_message(self):
        self.message_label['text'] = ''


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, email):
        try:

            # save the model
            self.model.email = email
            self.model.save()

            # show a success message
            self.view.show_success(f'The email {email} is correct!')

        except ValueError as error:
            # show an error message
            self.view.show_error(error)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Validator mail')

        # create a model
        model = Model('sample@mail.com')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.iconbitmap('darth.ico')
    app.mainloop()

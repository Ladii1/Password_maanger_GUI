from tkinter import *
from tkinter import messagebox
import random
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)


    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_num= [random.choice(numbers) for char in range(nr_numbers)]
    password_list = password_symbols + password_letters +password_num

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0,password)
    #pyperclip.copy(password)
    #print(f"Your password is: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = str(website_entry.get())
    user = str(user_entry.get())
    password = str(password_entry.get())
    new_file = {
        website : {
            "Email" : user,
            "Password": password,
        }
    }

    if website_entry.index('end') == 0 or user_entry.index('end') ==0 or password_entry.index('end') == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any fields empty")

    else:
        is_true = messagebox.askokcancel(title="Website confirmation", message=f"Details entered\nWebsite: {website}\n"
                                                                               f"Email/Username: {user}\n"
                                                                               f"Password: {password}")
        if is_true:

            try:
                with open("myfile.json","r") as file:
                    data = json.load(file)

            except (FileExistsError, FileNotFoundError, json.decoder.JSONDecodeError):
                with open("myfile.json", "w") as file:
                    json.dump(new_file,file, indent=4)

            else:
                data.update(new_file) #updating old data with new data

                with open("myfile.json", "w") as file:
                    json.dump(data, file, indent=4) # saving updated file


            finally:
                website_entry.delete(0,'end')
                user_entry.delete(0,'end')
                password_entry.delete(0,'end')

#-------------------------------WEBSITE SEARCH---------------------------------------#

def find_password():
    website = str(website_entry.get())
    try:
        with open("myfile.json", "r") as files:
            search = json.load(files)
    except (FileNotFoundError, FileExistsError):
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website in search:
            messagebox.showinfo(title=website, message= (f"Email: {search[website]['Email']}\n"
                                                           f"Password: {search[website]['Password']}"))
        else:
            messagebox.showerror(title="Error",message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window =Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(width=200,height=200)
logo= PhotoImage(file="logo.png")
canvas.create_image(100,100,image= logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1,column=0)

website_entry = Entry(width= 21)
website_entry.grid(row=1, column=1 , sticky="EW")
website_entry.focus()

search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2,sticky="EW" )

user_label = Label(text="Email/Username:")
user_label.grid(row=2,column=0)

user_entry = Entry(width= 35)
user_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
#user_entry.insert()

password_label = Label(text="Password:")
password_label.grid(row=3,column=0)

password_entry = Entry(width= 21)
password_entry.grid(row=3, column=1, sticky="EW")

gen_pass_button = Button(text="Generate Password", command=generate_pass)
gen_pass_button.grid(row=3,column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4,column=1, columnspan=2, sticky="EW")



window.mainloop()
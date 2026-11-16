import datetime
import csv
from datetime import datetime, timedelta
import requests




def user_search():
    """
    Function Name: user_search()
    1. Prompts Users to search for book_name (1), recommended topic(2) or quit (q)
    2. return a tuple: get_book_name, user_choice_topic_name .
    2.1:               ("book",name) / ("topic", topic) 
    2.3:                (None, None)== quit
    """
    while True:
        chocie_of_topic = input("please choice 1 = Search for a book 2 = Get book recommendations by topic q = Quit ")
        if chocie_of_topic == "1":
            book_name = input("Enter a book: ").strip()
            book_name = book_name.lower()
            return "book", book_name
        elif chocie_of_topic == "2":
            topic = user_topic()
            return "topic",topic
        elif chocie_of_topic.lower() =="q":
            return None, None
        else: 
            print("Invalid input: please press 1 = Search for a book 2 = Get book recommendations by topic or q to  Quit ")



def user_topic():
    """
    Function NAme:user_topic()
    1. would only execute if user_choice_of_topic inside user_search() funciotn  ==2 
    2. Prompts user to choice a topic 
    3. return users chosen topic or None if it was not valid
    
    
    """
    try:
        user_topic_choice = int(input("Enter a topic:\n1 = computer science\n2 = Maths\n3 = Chemistry\n4 = Biology\n"))
    except ValueError:
        # if user inputs a ltter or out the range 1-4
        print("Please enter a number between 1–4")
        return None

    if user_topic_choice == 1:
        topic = "computer science"
    elif user_topic_choice == 2:
        topic = "mathematics"
    elif user_topic_choice == 3:
        topic = "Chemistry"
    elif user_topic_choice == 4:
        topic = "Biology"
    else:
        print("Invalid please enter a number between 1-4")
        return None

    return topic





def get_book_info(get_book_name, user_choice_topic_name):
    """
    # Function  name:  get_book_info(get_book_name, user_choice_topic_name)  

    1.  Parameter Args:  from user_search()
    get_book_name : book title or topic keyword
    user_choice_topic_name : "book" or "topic"

    2. Send HTTP GET request to OpenLibrary  endpoint. 

    3. return a 5 books each as [title, author].  
    books : ([title, author], [title, author] ) 
    or return an Empty lisst if the request fails/no results
    Returning Empty list so when i call len(books) later so doesnt crash/


    """
    #  url query book name or topic
    if user_choice_topic_name == "book":
        url = f"https://openlibrary.org/search.json?q={get_book_name}"

    elif user_choice_topic_name == "topic":
         url = f"https://openlibrary.org/search.json?q={get_book_name}"
    
    else:
        print("sorry we could not get your book ")
        return []
# try and catch to validate api request an
    try:
        # Sends GET request to the api
        response = requests.get(url)
        # checks if the request was a sucess  if not  Raises HTTPError for 404, 500 etc.
        response.raise_for_status() 
    ## Client - server interation error
    except requests.exceptions.HTTPError as e:
        print(f"Unfortunately a HTTPError has occured, please try again later:  {e}" ) 
        return []

    except requests.exceptions.RequestException as e:
        print(f"Unfortunately a Api Error, please try again later: {e}")
        return []


    #API request works (status code should be 200)
    # response converted to json and stored in data_book_name
    data_book_name = response.json()
    ## create an empty list: stores author + title 
    books= []
    # Loops each book in the API's docs list 
    for i in data_book_name["docs"]:   
        # If book doesn't have title author name skips throse
        if "title" not in i or "author_name" not in i or not i["author_name"]:
               continue
        else:
            title=i["title"]
            author=i["author_name"][0]
            books.append([title, author] )  
            # stops after COLLECTING  5 books so it doesn't return all books in api
            if len(books)==5:
                break
    return books    # return a list e.g. [[title, author], [title, author]
    
   



           
def userface_show_books(books):
    """
    1. Print  list of book alongside its index number
    2. Truncates long titles to 40 chars for clearner output 
    3. parameter argument: books: list of books passed by get_book_info()
    """
    if len(books) == 0:
        print("Sorry no books have been found ")
        return

    for i, item in enumerate(books, start=1):
            title_topic = item[0][:40]   # string slicing
            author_topic = item[1]
            print(f"{i}. {title_topic} by {author_topic}")



def choose_book_and_option(books):
    """
    Function Name: choose_book_and_option(books)
    1. Prompt user to pick one book by its number from list books
    1.1 try and except used to prevent value error 
    2. return the book user choice as a list [title, author]
    2. parameter argument: books-  is from get_book_info() funciton   
    3. return: List, selected book  or none 
   
    """
    try:
        complete_books= int(input
        ("Please select a book you aim to complete. Select from the list 1-5  ") )
    except ValueError:
        print("Please provide a number between 1-5.")
        return None
    
    if 1 <= complete_books<=len(books):
        print(books[complete_books-1])
        chosen_book_topic =books[complete_books-1]
        print(chosen_book_topic[0], chosen_book_topic[1]) 
        return chosen_book_topic

    else:
        print("please provide correct input ")
        return None
    


def creating_deadline(chosen_book_topic):

    """
    1. Prompts user to set a "deadline" or "read later"
    2. Calculate date using timedela/datetime: assigns status based on remaning time
    3. parameter Argument: from choose_book_and_option 
    4. Return:
    4.1 : list: [chosen_book_topic[0] titile , chosen_book_topic [1] author, deadline, status]
    4.2: None: if deadline input is invalid
    """
    user_input= input(
        "Would you like to set a Deadline (type 'deadline' or press '1) or Read later (type 'Read later' or press '2)").lower().strip()

    valid_outputs= ["deadline", "read later", "1" ,"2"]

    while user_input not in valid_outputs:
        print("invalid input")

        user_input= input("Do you want to set a deadline or read later? ").lower()
        if user_input =="q":
            exit()
        else:
            pass
    
    ## Get number-days and number_hourse after vaalditing
    if user_input == "deadline" or user_input== "1":
        print("how many days do you want to complete this by our hours")
        try:
            number_day=int(input("Days: "))
            number_hours=float(input("hors:"))
        except ValueError:
            print("please enter a balid number") 
            return None
        
        ## Calculates dealdine using timedelta and set status 
        current_time= datetime.now()
        end = current_time + timedelta(days=number_day, hours=number_hours)
        # Formatting the date
        formatted_deadline= end.strftime("%A, %B %d, %Y")
       
       
        deadline = (end - datetime.now()).days
        # deadlne 1 day or less due son 2-3 soon else on track
        # Provides encorunages sets to status
        if deadline <= 1:
            status = "Due soon: Let's complete this book"
        elif deadline == 2:
            status= "Day 2: Lets start great"
        elif deadline <=3:
            status = "Almost due: You've got this"
        else:
            status = "On track: You're on track!"
        # retruns chosend_book[0] being book title chosen_book_topic[1] being author-name, formatted_deadline = deadline, status 
        return [chosen_book_topic[0],chosen_book_topic[1], formatted_deadline , status]
    

    elif user_input == "read later" or user_input =="2":
        deadline= "Read later"
        status="read later"
        return [chosen_book_topic[0], chosen_book_topic[1], deadline, status]
    
    


def user_selects_deadline(user_selected_book):
    """
    1. Shows Reading status:
    2. return:
    - 2.1  the chosen staus 
    - 2.2  None if it isnot valid 
    3. args:  user_selected_book is for main later

    """
    options = ["Have Not started ", "Currently reading book", "Completed book", "Haven't finished book", "Will not read this book"]
    # Show the menu using a for loop and f{string}
    print("What's your reading status?")
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
    
    user_input = input("Enter number or status: ").strip()

    ## Accepts if user_input is a int and within the range or the string in the list.
    if user_input.isdigit():
        choice = int(user_input)
        if 1 <= choice <= len(options):
            return options[choice - 1]
    ## try use string 
    for chosen_status  in options:
        if user_input.lower() == chosen_status .lower():  #case-senstive
            return chosen_status # returns string e.g Not started
    return None 


#--------------------------------Main fucntion------------------------#

def main():
    """
    1. Get book or topic from  user_search() 
    2. Fetch 5 book from API :Call get_book_info()
    3. SHOW books and let user pick one : userface_show_books(saved_books)
    4. choose_book_and_option(saved_books): user selects 
    5. Call creating_deadline(user_selected_book); book_with_deadline stores: [title, author, deadline, auto_status] 
    6. Call user_selects_deadline(user_selected_book); user_selected_status: stores chosen status
    7. Add + Append to final_book_list
    8. return  final_book_list


    """
    final_book_list=[]    # List of all varibles :  [title, author, deadline, auto_status, user_status]
    
    
    while True:
        user_choice_topic_name, get_book_name=user_search()    
        
        if get_book_name is  None: 
            break
        else: 
            # Fetches 5 books from the api Library
            saved_books =  get_book_info(get_book_name,user_choice_topic_name)  ## saved books is get book info dependin on user chocie saved the list of book based onuser choice 
            userface_show_books(saved_books)
            
            # Lets user (select) pick one of the 5 book from the list shown  
            user_selected_book= choose_book_and_option(saved_books)   


            if user_selected_book is None:
                print("Invalid book please try again and select a book between 1-5s")
            else:
                book_with_deadline = creating_deadline(user_selected_book)   ### Adds a  deadline to the selected book 
            
            # get the reading status for the selected book
                user_selected_status = user_selects_deadline(user_selected_book) 

                if book_with_deadline is not None:
                    ##  Adds Deadline and status cerating final_headers 
                    final_headers= book_with_deadline + [user_selected_status]  

                    ## saves/appends them all to a list: final_book_list
                    final_book_list.append(final_headers)
                else:
                    print("Deadline not created.")
                    pass   
    # return final_book_list : most likely is not empty anymore 
    return final_book_list
        




final_book_list = main()


#---------------------CREATING THE CSV ---------------------------------#

# Creates a CSV file and mode = "w" : write final_book_list data 
# encoding="utf-8": prevents UnicodeEncodeErros - handles other char in library
# csv.DictWriter: cretaing columns 
# enumarte: print index as column number and the book in the list 
#------------------------------------------------------------------------#
with open("reading_checklist.csv", mode="w",encoding="utf-8", newline="") as file:
    header= ["number", 'book name', "author", "deadline", "status", "current_status"]
    writer= csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    #print(saved_books)
# print index (i+1) and the book
    for i, book in enumerate(final_book_list):
        writer.writerow({
            "number": i+1,
            "book name": book[0],
            "author": book[1],
            "deadline": book[2],
            "status": book[3],
            "current_status": book[4]
            })
from replit import db

# 200: successfully email is listed
# 409: email id already present

# 500: internal server erro

# create new entry
def create_account(email):
    try:
        docs = db[email]
        return 409
    except:
        try:
            db[email] = {'email': email}
            return 200
        except:
            return 500

# print all the elements of the database
def print_db():
    all_keys = db.keys()
    for each_key in all_keys:
        print(db[each_key])

# clear full database
def clear():
    all_keys = db.keys()
    for each_key in all_keys:
        del db[each_key]

# getting all email addresses
def get_all_emails():
    all_keys = db.keys()
    final_email_list = []
    for each_key in all_keys:
        temp_dict = db[each_key]
        final_email_list.append(temp_dict['email'])
    return final_email_list  # Return a list of all registered users' emails
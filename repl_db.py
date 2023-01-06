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

def get_all_emails():
    all_keys = db.keys()
    final_email_list = []
    for each_key in all_keys:
        temp_dict = db[each_key]
        final_email_list.append(temp_dict['email'])
    return final_email_list  # Return a list of all registered users' emails
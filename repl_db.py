from replit import db

# 409: email id already present

# create new entry
def create_account(email):
    try:
        docs = db[email]
        return 409
    except:
	    db[email] = {'email': email}

def get_all_emails():
    all_keys = db.keys()
    final_email_list = []
    for each_key in all_keys:
        temp_dict = db[each_key]
        final_email_list.append(temp_dict['email'])
    return final_email_list  # Return a list of all registered users' emails
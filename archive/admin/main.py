import admin as admin
from pprint import pprint

admin = admin.Admin()
if __name__ == '__main__':
    admin.delete_all_orgs()
    admin.delete_all()
    try:
        for x in admin.get_tokens():
            admin.delete_token(x)
            print(f"Deleted token: {x}")
    except:
        pass
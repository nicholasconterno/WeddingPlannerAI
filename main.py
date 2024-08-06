import time
from email.utils import parsedate_to_datetime
from utils.email_utils import send_email, receive_emails
from utils.ai_utils import create_openai_client, generate_email_content, generate_user_content, analyze_email_for_information, summarize_information, get_next_step
from utils.storage_utils import store_information

def converse_with_vendor(api_key, user_request, sender_email, sender_password, recipient_email):
    client = create_openai_client(api_key)
    
    email_body = generate_email_content(client, f"write an email to a Vendor based upon this requested information from the user: [{user_request}] remember they can contact you at {sender_email}")
    last_sent_date = send_email(sender_email, sender_password, recipient_email, "Request for Quote", email_body)
    print("Initial email sent.")
    
    time.sleep(10)

    info = None
    while info is None:
        time.sleep(10)
        print("Checking for responses...")
        emails = receive_emails(sender_email, sender_password)
        for email in emails:
            email['from'] = email['from'][email['from'].find('<') + 1:email['from'].find('>')]
            if email['from'] == recipient_email and email['date'] > parsedate_to_datetime(last_sent_date):
                has_info = analyze_email_for_information(client, user_request, email['body'])
                if has_info:
                    info = email['body'][:email['body'].find('>') - 1]
                    break

                if info is None:
                    follow_up_body = generate_email_content(client, "We didn't receive the quote information we requested. Can you please provide the details?")
                    last_sent_date = send_email(sender_email, sender_password, recipient_email, "Follow-up Request for Quote", follow_up_body)
                    print("Follow-up email sent.")
                    time.sleep(10)

    store_information(user_request + "-- answer: " + info)
    response = generate_user_content(client, f"based upon this reply from the vendor: {info}: give the bride the requested information. ONLY STATE THINGS FROM THE REPLY AND BE EXTREMELY SUCCINCT. DO NOT ADD ANY ADDITIONAL INFORMATION.")
    print(response)
    return response

def get_summary(api_key):
    client = create_openai_client(api_key)
    with open('information.txt', 'r') as f:
        info = f.read()
    summary = summarize_information()
    return summary

def get_next_step_for_bride(api_key):
    client = create_openai_client(api_key)
    summary = get_summary(api_key)
    next_step = get_next_step(summary)
    return next_step

if __name__ == "__main__":
    user_request = "Help me find the price of wedding photography from ABC Photography"
    converse_with_vendor("sk-no-key-required", user_request, 'wendyplanterweddings@gmail.com', 'nqel uytt fzxn iqbr', 'abneyjohnson0@gmail.com')

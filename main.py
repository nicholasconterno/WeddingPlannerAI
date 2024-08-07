import time
from email.utils import parsedate_to_datetime
from utils.email_utils import send_email, receive_emails
from utils.ai_utils import (
    create_openai_client,
    generate_email_content,
    generate_user_content,
    analyze_email_for_information,
    summarize_information,
    get_next_step,
)
from utils.storage_utils import store_information

"""
This script is the main entry point for the AI wedding planner application.
It uses OpenAI's GPT-3 model to generate email content,
subject lines, and user responses based on user input and
vendor emails. The AI wedding planner can converse with vendors
to gather information and respond to brides with the requested
information. The AI can also summarize the information gathered
and provide the next step for the bride in the wedding planning
process.
"""


def generate_subject_line(client, user_input):
    """
    Generate a concise and relevant email subject line based on the provided user query."""
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant for wedding planning. Generate a concise and relevant email subject line based on the provided user query.",
            },
            {
                "role": "user",
                "content": f"Generate a subject line for the following query: {user_input}",
            },
        ],
        temperature=0.5,
    )
    # extract the subject line from the completion
    temp = completion.choices[0].message.content.strip()
    # remove quotation marks and '</s>' if present
    for char in ['"', "'", "</s>"]:
        temp = temp.replace(char, "")
    temp = " ".join(temp.split())
    return temp


def converse_with_vendor(
    api_key, user_request, sender_email, sender_password, recipient_email
):
    """
    Converse with a vendor to gather information based on the user request.
    """
    client = create_openai_client(api_key)

    # generate email content to send to the vendor
    email_body = generate_email_content(
        client,
        f"""write an email to a Vendor based upon this requested information from the
        user: [{user_request}] remember they can contact you at {sender_email}""",
    )

    subject_line = generate_subject_line(client, user_request)
    # subject_line = "Request for Quote"
    last_sent_date = send_email(
        sender_email, sender_password, recipient_email, subject_line, email_body
    )
    print("Initial email sent.")

    time.sleep(10)

    info = None
    count = 0
    # check for responses from the vendor
    while info is None:
        time.sleep(10)
        print("Checking for responses...")
        # receive emails and analyze for information
        emails = receive_emails(sender_email, sender_password)
        # iterate through the emails in reverse order
        for email in emails:
            email["from"] = email["from"][
                email["from"].find("<") + 1 : email["from"].find(">")
            ]
            # check if the email is from the vendor and is more recent than the last sent date
            if email["from"] == recipient_email and email[
                "date"
            ] > parsedate_to_datetime(last_sent_date):
                # analyze the email for information
                has_info = analyze_email_for_information(
                    client, user_request, email["body"]
                )
                # extract the information from the email
                if has_info:
                    info = email["body"][: email["body"].find(">") - 1]
                    break
                # check if the information was not found
                if info is None:
                    count += 1
                    # if the information was not found after 3 attempts, send a failure alert
                    if count == 3:
                        return (
                            "Information about the vendor request: "
                            + user_request
                            + " was not found."
                        )
                    # send a follow-up email to the vendor
                    follow_up_body = generate_email_content(
                        client,
                        "Generate an email in response to this vendor email:"
                        + email["body"]
                        + " to request the information from this request: "
                        + user_request
                        + " REMEMBER YOU ARE THE WEDDING PLANNER, NOT THE VENDOR.",
                    )
                    # send the follow-up email and update the last sent date
                    last_sent_date = send_email(
                        sender_email,
                        sender_password,
                        recipient_email,
                        "Follow-up Request for Quote",
                        follow_up_body,
                    )
                    print("Follow-up email sent.")
                    time.sleep(10)
    # generate a user response based on the vendor reply
    response = generate_user_content(
        client,
        f"""based upon this reply from the vendor: {info}: give the bride the requested information.
          ONLY STATE THINGS FROM THE REPLY AND BE EXTREMELY SUCCINCT. DO NOT ADD ANY ADDITIONAL INFORMATION.""",
    )
    # store the information in the database
    store_information(user_request + "-- answer: " + response)
    print(response)
    return response


def get_summary(api_key):
    """
    Summarize the information gathered from vendors in list format."""
    summary = summarize_information()
    return summary


def get_next_step_for_bride(api_key):
    """
    Get the next step for the bride based on the summarized
    """
    summary = get_summary(api_key)
    next_step = get_next_step(summary)
    return next_step


if __name__ == "__main__":
    user_request = "Help me find the price of wedding photography from ABC Photography"
    converse_with_vendor(
        "sk-no-key-required",
        user_request,
        "wendyplanterweddings@gmail.com",
        "nqel uytt fzxn iqbr",
        "abneyjohnson0@gmail.com",
    )

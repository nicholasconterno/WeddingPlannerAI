from openai import OpenAI


def create_openai_client(api_key):
    """
    Create an OpenAI client with the specified API key.
    """
    return OpenAI(
        base_url="http://host.docker.internal:8080/v1",
        api_key=api_key,  # Adjust as needed
    )


def generate_email_content(client, user_input):
    """
    Generate an email to send to a vendor based on the user input."""
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": "You are Wendy Planter, an AI wedding planner. Your job is to "
                """email vendors for information and manage previous information.
                 NEVER show that you are an AI, and never add information not stated in the vendor emails;"""
                "do not put [missing info]. Respond naturally and provide complete information wherever possible.",
            },
            {"role": "user", "content": user_input},
        ],
    )
    # extract the email content from the completion
    temp = completion.choices[0].message.content

    # remove quotation marks and '</s>' if present
    for char in ["</s>"]:
        temp = temp.replace(char, "")
    # replace '[Vendor's Name]' with the word 'Colleague'
    temp = temp.replace("[Vendor's Name]", "Colleague")
    temp = temp.replace("[Vendor Name]", "Colleague")
    # remove any line starting with Subject:
    for line in temp.split("\n"):
        if line.startswith("Subject: "):
            temp = temp.replace(line, "")
    return temp


def generate_user_content(client, user_input):
    """
    Generate a response to the user based on the user input.
    """
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": "You are Wendy Planter, an AI wedding planner. Your job is to "
                "speak to the bride about information gathered from vendors and manage previous information. "
                "NEVER show that you are an AI, and omit missing information; "
                "do not put [missing info]. Respond naturally and provide complete information wherever possible.",
            },
            {"role": "user", "content": user_input},
        ],
    )
    # extract the response from the completion
    temp = completion.choices[0].message.content

    # remove quotation marks and '</s>' if present
    for char in ["</s>"]:
        temp = temp.replace(char, "")
    return temp


def analyze_email_for_information(client, user_request, email_body):
    """
    Analyze the email body to determine if it contains the requested information.
    """
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": """You are an assistant that helps determine if the requested
                 information is present in the email response. """
                "You must only respond with 'yes' or 'no'.",
            },
            {
                "role": "user",
                "content": f"""User request: {user_request}\nEmail body: {email_body}\nDoes the email
                 body provide the requested information? Respond with 'yes' or 'no' """,
            },
        ],
        max_tokens=1,
        temperature=0,
    )
    temp = completion.choices[0].message.content.strip().lower()
    # remove '</s>' if present
    for char in ["</s>"]:
        temp = temp.replace(char, "")

    return temp == "yes"


# function to read information.txt and summarize the information using the llm
def summarize_information():
    """
    Summarize the information gathered from the vendors."""
    with open("information.txt", "r") as f:
        info = f.read()
    # if no information is available, return a message
    if not info:
        return "No information available."
    client = OpenAI(
        base_url="http://host.docker.internal:8080/v1",  # "http://<Your api-server IP>:port"
        api_key="sk-no-key-required",
    )
    # generate a summary of the information
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": "You are Wendy Planter, an AI wedding planner. Your job is to "
                "summarize the information you have gathered from vendors."
                " NEVER show that you are an AI, and never add information not stated in the vendor emails; "
                "do not put [missing info]. Respond naturally and provide complete information wherever possible.",
            },
            {"role": "user", "content": "summarize this info in list format: " + info},
        ],
    )
    temp = completion.choices[0].message.content

    # remove quotation marks and '</s>' if present
    for char in ["</s>"]:
        temp = temp.replace(char, "")
    return temp


# get next step for the bride based on the summary
def get_next_step(summary):
    """
    Get the next step for the bride based on the summary of the information gathered."""
    client = OpenAI(
        base_url="http://host.docker.internal:8080/v1",  # "http://<Your api-server IP>:port"
        api_key="sk-no-key-required",
    )
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": "You are Wendy Planter, an AI wedding planner. Your job is to "
                "speak directly to the bride with the next part of the wedding to plan based"
                " on the information you have gathered. NEVER show that you are an AI,"
                " and never add information not stated in the vendor emails; "
                "do not put [missing info]. Respond naturally and provide complete information wherever possible.",
            },
            {
                "role": "user",
                "content": summary
                + ":[ based on the summary before] respond with the next vendor"
                " type for the bride to contact for a quote (e.g. 'You should"
                " now book the florist/photographer.') (do not say Based on the information provided)",
            },
        ],
    )
    # extract the next step from the completion
    temp = completion.choices[0].message.content

    # remove quotation marks and '</s>' if present
    for char in ["</s>"]:
        temp = temp.replace(char, "")
    return temp

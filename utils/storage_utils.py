def store_information(info):
    with open('information.txt', 'a') as f:
        f.write(info + '\n')

def get_original_message(email_content):
    # Split the content by newlines
    lines = email_content.split('\n')
    
    # Find the index of the first forwarded message indicator
    forwarded_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('On '):
            forwarded_index = i
            break
    
    # If a forwarded message is found, return content up to two lines before it
    if forwarded_index is not None and forwarded_index > 1:
        return '\n'.join(lines[:forwarded_index]).strip()
    else:
        # If no forwarded message is found, return the whole content
        return email_content.strip()

import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
# SLACK_BOT_TOKEN consists of the user access auth token
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# Course Descriptions Bot's user ID in Slack: value is assigned after the bot starts up
course_desc_bot_id = None

# constants
# 1 second delay between reading from RTM (polling based chat)
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
    Parses a list of events coming from the Slack RTM API to find bot commands.
    If a bot command is found, this function returns a tuple of command and
    channel.
    If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == course_desc_bot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
    Finds a direct mention (a mention that is at the beginning) in message text
    and returns the user ID which was mentioned. If there is no direct mention,
     returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def about_course(command):
    """
    Returns the course descriptions of the asked course
    """

    if re.search('ENPM611', command):
        return 'ENPM 611; Software Engineering; Christopher Ackermann; 0101; Monday 4:00 - 6:40 PM; JMP 2121'
    elif re.search('ENPM613', command):
        return 'ENPM 613; Software Design and Implementation; Ioana Rus; 0101; Wednesday 7:00 - 9:40 PM; TBA'
    elif re.search('ENPM631', command):
        return 'ENPM631; TCP/IP Networking; Pedram Fard; 0101; Tuesday 7:00 - 9:40 PM; TBA'
    elif re.search('ENPM687', command):
        return 'ENPM687; Digital Forensics and Incidence Response; Jonas Amoonarquah; Online;'
    elif re.search('ENPM691', command):
        return 'ENPM691; Hacking of C Programs and Unix Binaries; Dharmalingam Ganesan; 0101; Thursday 7:00 - 9:40 PM; JMP 3201'
    elif re.search('ENPM693', command):
        return 'ENPM693; Network Security; Sohraab Soltani; 0101; Tuesday 7:00 - 9:40 PM; JMP 3201'
    elif re.search('ENPM694', command):
        return 'ENPM694; Networks and Protocols; Sohraab Soltani; 0101; Wednesday 7:00 - 9:40 PM; JMP 3201'
    elif re.search('ENPM696', command):
        return 'ENPM696; Reverse Software Engineering; Allen Hazelton; 0101; Tuesday 4:00 - 6:40 PM; TBA'
    elif re.search('ENPM809J', command):
        return 'ENPM809J; Cloud Security; Kevin Shivers; 0101; Monday 7:00 - 9:40 PM; TBA; 0201; Thursday 4:00 - 6:40 PM; TBA'
    elif re.search('ENPM809R', command):
        return 'ENPM809R; Software Defined Networking; Emre Gunduzhan; 0101; Monday 4:00 - 6:40 PM; TBA'
    elif re.search('ENPM809W', command):
        return 'ENPM809W; Security and Software; Mikael Lindvall; 0101; Thursday 7:00 - 9:40 PM; TBA'

def help_text(command):
    """
    Return app usage help text
    """

    courses_list = ('ENPM611', 'ENPM613', 'ENPM631', 'ENPM687',\
                    'ENPM691', 'ENPM693', 'ENPM694', 'ENPM696',\
                    'ENPM809J','ENPM809R', 'ENPM809W')

    response = 'I have course descriptions for: '
    for course_name in courses_list:
        response = response + course_name + ' '

    response = response + '\nTo get the course description, execute command: about ENPM<course_number>'

    return response

def handle_command(command, channel):
    """
    Executes bot command if the command is known
    """

    # Default response is help text for the user
    default_response = "Hmm, I don't understand."

    ABOUT_COMMAND = 'about'
    HELP_COMMAND = 'help'

    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more commands!
    if command.startswith(ABOUT_COMMAND):
        response = about_course(command)
    elif command.startswith(HELP_COMMAND):
        response = help_text(command)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    # Connect to Slack's Real Time Message (RTM) API
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        course_desc_bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

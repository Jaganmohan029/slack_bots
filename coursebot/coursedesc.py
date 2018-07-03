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

    response = {'code': None, 'title': None,\
                'prof': None, 'section1': None,\
                'timing1': None, 'room1' : None,\
                'section2': None, 'timing2': None,\
                'room2': None, 'description': None,\
                'prereq': None, 'perm': None}
                 
    if re.search('ENPM611', command):
        response = {'code': 'ENPM 611', 'title': 'Software Engineering',\
                    'prof': 'Christopher Ackermann', 'section1': '0101',\
                    'timing1': 'Monday 4:00 - 6:40 PM', 'room1': 'JMP 2121',\
                    'description': 'Software engineering concepts, methods, and practices important to both the theorist and the practitioner will be covered. The entire range of responsibilities expected of a software engineer are presented. The fundamental areas of requirements development, software design, programming languages, and testing are covered extensively. Sessions on supporting areas such as systems engineering, project management, and software estimation are also included.', 'prereq': 'Competency in one programming language; and must have completed an undergraduate software engineering course. Or permission of instructor.', 'perm': 'Permission of ENGR-CDL-Office of Advanced Engineering Education.'
}
    elif re.search('ENPM613', command):
        response = {'code': 'ENPM 613', 'title': 'Software Design and Implementation', 'prof': 'Ioana Rus', 'section1': '0101', 'timing1': 'Wednesday 7:00 - 9:40 PM', 'room1': 'TBA', 'description': 'Software design concepts and practices within the field important to both the practitioner and the theorist will be covered. Architectural and detailed designs are included for batch, client/server, and real-time systems. Design considerations for structured, object-oriented, and Web-based systems are covered. Design of databases, user interfaces, forms, and reports are also included. Implementation issues that affect the design, including error handling, performance, and inter-process communication, are presented.', 'perm': 'Permission of ENGR-CDL-Office of Advanced Engineering Education.'}
    elif re.search('ENPM631', command):
        response = {'code': 'ENPM631', 'title': 'TCP/IP Networking', 'prof': 'Pedram Fard', 'section1': '0101', 'timing1': 'Tuesday 7:00 - 9:40 PM', 'room1': 'TBA' , 'description': 'Describe how IP datagram travels through the internet and are routed from the source to the destination. Introduce the two transport protocols: UDP and TCP, the proper context to use each one, and related parameters and issues. Cover some other protocols, closely related to the TCP/IP that are responsible for the seamless operation of the Internet.', 'perm': 'ENPM602; or permission of instructor. And permission of ENGR-CDL-Office of Advanced Engineering Education.'}
    elif re.search('ENPM687', command):
        response = {'code': 'ENPM687', 'title': 'Digital Forensics and Incidence Response', 'prof': 'Jonas Amoonarquah', 'section1': 'Online', 'timing1': 'NA', 'room1': 'NA', 'description': 'Students will implement a robust incident response methodology, including proper forensic handling of evidence, and cover legal aspects of national and international law regarding forensics. The bulk of the course covers evidence acquisition, preservation, analysis and reporting on multiple platforms.', 'perm':'None'}
    elif re.search('ENPM691', command):
        response = {'code': 'ENPM691', 'title': 'Hacking of C Programs and Unix Binaries', 'prof': 'Dharmalingam Ganesan', 'section1': '0101', 'timing1': 'Thursday 7:00 - 9:40 PM', 'room1': 'JMP 3201', 'description': 'Teaches the fundamentals of secure programming in C. An in depth discussion on various security vulnerabilities (e.g., buffer overflows) in C applications will be taught with hands-on demo of concepts during the class. Students will learn how a C program runs "under-the-hood". The course will teach nitty-gritty of C programs by analyzing at the assembly level. The course discusses best practices (e.g., coding standards) and design principles for secure programming so that security can be built-in during design time. In addition to assignments, students are required to present papers related to this course.', 'perm': None, 'prereq': 'ENEE150; or students who have taken courses with comparable content may contact the department.'}
    elif re.search('ENPM693', command):
        response = {'code': 'ENPM693', 'title': 'Network Security', 'prof': 'Sohraab Soltani', 'section1': '0101', 'timing1': 'Tuesday 7:00 - 9:40 PM', 'room1' : 'JMP 3201', 'description': 'Introduction to various approaches to design; specify and verify security protocols used in large systems and networks; familiarization with some current technologies. Security threats and countermeasures, communication security and basic encryption techniques, authentication protocols, data confidentiality and integrity, analysis of cryptographic protocols, and access control in large systems and networks.', 'perm': None, 'prereq': 'An operating systems and/or network protocol course or equivalent.'}
    elif re.search('ENPM694', command):
        response = {'code': 'ENPM694', 'title': 'Networks and Protocols', 'prof': 'Sohraab Soltani', 'section1': '0101', 'timing1': 'Wednesday 7:00 - 9:40 PM', 'room1': 'JMP 3201', 'description': 'Provides a deep understanding of TCP/IP protocol suit and routing in the internet. The course topics are: overview of TCP/IP, basics of IP protocol, basics of TCP protocol, Network Address Translation (NAT), Dynamic Host Configuration Protocol (DHCP), Internet Protocol Security (IPsec), Internet Control Message Protocol (ICMP), Simple Mail Transfer Protocol (SMTP), Domain Name Service (DNS), IPv6, Concepts of routing (Bellman-Ford and Dijkstra algorithms), Routing Information Protocol (RIP), Open Shortest Path First (OSPF), Interior Gateway Routing Protocol (IGRP), Enhance Gateway Routing Protocol (EIGRP), and Border Gateway Protocol (BGP).'}
    elif re.search('ENPM696', command):
        response = {'code': 'ENPM696', 'title': 'Reverse Software Engineering', 'prof': 'Allen Hazelton', 'section1': '0101', 'timing1': 'Tuesday 4:00 - 6:40 PM', 'room1': 'TBA', 'description': 'An in-depth understanding of software reverse engineering concepts and hands-on training with reverse engineering tools, including disassemblers, decompilers, and code analyzers. Students will become familiar with both low-level software and the x86 instruction set through binary reversing sessions. This course also provides insights into many subjects such as system security, source code analysis, software design, and program understanding that will be beneficial in a variety of fields.', 'prereq': 'ENPM691 and CMSC106; or permission of instructor. And permission of ENGR-CDL-Office of Advanced Engineering Education.'}
    elif re.search('ENPM809J', command):
        response = {'code': 'ENPM809J', 'title': 'Cloud Security', 'prof': 'Kevin Shivers', 'section1': '0101', 'timing1': 'Monday 7:00 - 9:40 PM', 'room1': 'TBA', 'section2': '0201', 'timing2': 'Thursday 4:00 - 6:40 PM', 'room2': 'TBA', 'description': 'NA'}
    elif re.search('ENPM809R', command):
        response = {'code': 'ENPM809R', 'title': 'Software Defined Networking', 'prof': 'Emre Gunduzhan', 'section1': '0101', 'timing1': 'Monday 4:00 - 6:40 PM', 'room1': 'TBA', 'description': 'NA'}
    elif re.search('ENPM809W', command):
        response = {'code': 'ENPM809W', 'title': 'Security and Software', 'prof': 'Mikael Lindvall', 'section1': '0101', 'timing1': 'Thursday 7:00 - 9:40 PM', 'room1': 'TBA', 'description': 'NA'}

    return response

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

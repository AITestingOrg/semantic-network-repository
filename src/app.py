from flask import Flask
from flask import jsonify
from analysis.nlp import NLP
from flask_cors import CORS
from common.persitence.wrapper_factory import WrapperFactory
from nltk.corpus import brown
import re
import os
import time
import re
from slackclient import SlackClient

# init db constraints
init_db = WrapperFactory.build_neo4j_init_wrapper('localhost', 7687, 'neo4j', 'test')
init_db.initialize_db()

mode = 'nice'

def main():
    print(os.environ.get('SLACK_BOT_TOKEN'))
    # instantiate Slack client
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    EXAMPLE_COMMAND = "Hi"
    # starterbot's user ID in Slack: value is assigned after the bot starts up
    starterbot_id = None

    # constants
    RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    nlp = NLP()
    #for sent in brown.sents():
    #    NLP().find_useful_stuff(re.sub(r'[^\w]', ' ', ' '.join(sent)), False, True)

    def parse_bot_commands(slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = parse_direct_mention(event["text"])
                if user_id == starterbot_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(command, channel):
        global mode
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        if mode == 'insulting':
            default_response = "Stop insulting me, moron."
        else:
            default_response = "Sorry, I don't know that one yet."

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        print('TEXT: "{}"'.format(command))
        if command.startswith('mode:'):
            if command.split(' ')[1] == 'insulting':
                mode = 'insulting'
                response = '...'
            else:
                mode = 'nice'
                response = "I'll be nice!"
        elif command.startswith('input:'):
            result = nlp.find_useful_stuff(text=command, write=True)
            response = "Ok, I may remember that."
        else:
            result = nlp.find_useful_stuff(text=command)
            if result and 'is_question' in result and result['is_question']:
                print('Question found.')
                if 'ideas' in result and len(result['ideas']) > 0:
                    if 'gen_answer' in result and result['gen_answer']:
                        response = 'The answer may be "{}".\n'.format(result['gen_answer'])
                    else:
                        response = 'The answer may be "{}".\n'.format(result['answer'])
                    response += 'Here is what I know about {}'.format(result['structure']['nsubj'])
                    response += "\n"
                    for idea in result['ideas']:
                        response += ' '.join(idea)
                        response += "\n"
                else:
                    subject = 'that'
                    if 'structure' in result and 'nsubj' in result['structure']: 
                        subject = result['structure']['nsubj']
                    if mode == 'insulting':
                        response = "What, you don't know that? lol"
                    else:
                        response = 'Sorry, I do not know anything about {} yet.'.format(subject)
            elif any(word in command.lower() for word in ['greetings', 'hi', 'hai', 'hello', 'hola', 'what\'s up', 'whats up']):
                print('Greeting.')
                if mode == 'insulting':
                    response = ':middle_finger:'
                else:
                    response = 'Hai Hai!'
            

        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


# "main" function
if __name__ == "__main__":
    main()

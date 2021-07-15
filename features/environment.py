import json
import os.path


def before_all(context):
    env = context.config.userdata.get("env", "staging")
    if os.path.exists(env+".json"):
        more_userdata = json.load(open(env+".json"))
        context.config.update_userdata(more_userdata)



import asana
import json
import os
# import request
import pandas as pd

# pandas set max column width
pd.set_option('display.max_colwidth', 150)


def user_select_option(message, options):
    option_lst = list(options)
    print_(message)
    for i, val in enumerate(option_lst):
        print_(i, ': ' + val['name'])
    index = int(input("Enter choice (default 0): ") or 0)
    return option_lst[index]

def get_client():
    with open(os.path.expanduser('~/.dt_config.json')) as f:
        config = json.load(f)
        api_key = config['asana_api_key']
        
    # create asana client
    client = asana.Client.access_token(api_key)
    return client


def asana_list_todos(filtering, workspace_name):
    # read api key from ~/.dt_config.json
    client = get_client()
    (url, state) = client.session.authorization_url()
        
    me = client.users.me()
    workspace_id = me['workspaces'][0]['gid']
    
    
    # tasks = str(client.tasks)
    tasks = list(client.tasks.find_all(workspace=workspace_id, assignee='me'))
    df = pd.DataFrame(tasks)
    df = df[['name']]
    
    print(df)
    
    
def add_todo(task_text, project_id=0):
    client = get_client()
    me = client.users.me()
    workspace_id = me['workspaces'][0]['gid']
    
    projects = list(client.projects.get_projects_for_workspace(workspace_id))
    
    # docs https://developers.asana.com/docs/create-a-task
    
    data =  {'name': task_text,
        "resource_subtype": "default_task",
        "assignee": me['gid'],
        "due_on": "2019-09-15",
        "projects": projects[project_id]['gid'],
        # 'notes': 'Note: This is a test task created with the python-asana client.',
        # 'projects': [workspace_id]
    }
    
    result = client.tasks.create_in_workspace(workspace_id, data)

    print(json.dumps(result, indent=4))
    
def done_todo():
    pass
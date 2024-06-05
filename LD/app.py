# to-do list flask app

import os
from flask import Flask,request,render_template
from datetime import date

# Import the LaunchDarkly client.
import ldclient
from ldclient import Context
from ldclient.config import Config

# Create a helper function for rendering messages.
def show_message(s):
  print("*** %s" % s)
  print()
  
ldclient.set_config(Config("sdk-key-goes-here"))

# The SDK starts up the first time ldclient.get() is called.
if ldclient.get().is_initialized():
  show_message("SDK successfully initialized!")
else:
  show_message("SDK failed to initialize")
  exit()

# Set up the evaluation context. This context should appear on your LaunchDarkly contexts
# dashboard soon after you run the demo.
context = Context.builder('example-user-key').name('Brian').build()

# Call LaunchDarkly with the feature flag key you want to evaluate.
flag_value = ldclient.get().variation("Clear_List", context, True)

show_message("Feature flag 'Clear_List' is %s for this user" % (flag_value))

# Track flag changes with a listener function
def flag_value_change_listener(flag_change):
    print(f"{flag_change.key} has changed from {flag_change.old_value} to {flag_change.new_value}")
    
listener = ldclient.get().flag_tracker.add_flag_value_change_listener('Clear_List', context, flag_value_change_listener)

#### Defining Flask App
app = Flask(__name__)

# function to return current flag values based on the listener function
def get_current_flag_value():
    return ldclient.get().variation("Clear_List", context, True)


#### Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


#### If this file doesn't exist, create it
if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt','w') as f:
        f.write('')


def gettasklist():
    with open('tasks.txt','r') as f:
        tasklist = f.readlines()
    return tasklist

def createnewtasklist():
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.write('')
        
def dontcreatenewtasklist():
    with open('tasks.txt','r') as f:
        tasklist = f.readlines()
    return tasklist

def updatetasklist(tasklist):
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.writelines(tasklist)     


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 

# Function to clear the to-do list (functionality based on the feature flag)
@app.route('/clear')
def clear_task_list():
    if get_current_flag_value():
        createnewtasklist()
    else:
        dontcreatenewtasklist()
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist()))


# Function to add a task to the to-do list
@app.route('/addtask',methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    with open('tasks.txt','a') as f:
        f.writelines(task+'\n')
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to remove a task from the to-do list
@app.route('/deltask',methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = gettasklist()
    print(task_index)
    print(tasklist)
    if task_index < 0 or task_index > len(tasklist):
        return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist),mess='Invalid Index...') 
    else:
        removed_task = tasklist.pop(task_index)
    updatetasklist(tasklist)
    return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist)) 
    


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
    
# Here we ensure that the SDK shuts down cleanly and has a chance to deliver analytics
# events to LaunchDarkly before the program exits. If analytics events are not delivered,
# the user properties and flag usage statistics will not appear on your dashboard. In a
# normal long-running application, the SDK would continue running and events would be
# delivered automatically in the background.
ldclient.get().close()

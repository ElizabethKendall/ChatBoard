from __future__ import unicode_literals
from django.shortcuts import render, reverse, redirect
from ..user_app.models import User
from .models import Message, Comment
from .forms import CreateMessageForm, CreateMessage_Form, CreateCommentForm, CreateComment_Form
from datetime import tzinfo, timedelta, datetime
import pytz
from math import floor

#https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes/25662061#25662061  
class UTC(tzinfo):
    # ZERO = timedelta(0)
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return timedelta(0)

def time_since_created(created_at_datetime):
    #https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes/25662061#25662061    
    utc = UTC()
    # from Anentropic at: https://stackoverflow.com/questions/18541051/datetime-and-timezone-conversion-with-pytz-mind-blowing-behaviour
    # whether Django stores naive datetimes of not is controlled by the USE_TZ setting. If that is True then Django treats datetimes in forms etc as being in the current timezone and stores them in the db converted to UTC.
    # note: USE_TZ is True in settings.py for this project
    delta = datetime.now(utc) - created_at_datetime
    td_minutes = divmod(delta.days*86400 + delta.seconds, 60)[0]
    td_hours = divmod(delta.days*86400 + delta.seconds, 60*60)[0]
    td_days = divmod(delta.days*86400 + delta.seconds, 60*60*24)[0]
    if td_days > 0:           
        return "{} days ago".format(td_days)
    elif td_hours > 0: 
        return "{} hours and {} minutes ago".format(td_hours, td_minutes%60)
    elif td_minutes > 0 :
        return "{} minutes ago".format(td_minutes)
    else:
        return "just now"

# Create your views here.
def show(request, number, *bound_forms):
    # number is the user_id of selected_user, who is being messaged
    # in session is the user_id of the logged in user, who is writing messages and comments
    selected_user = User.objects.get(id=number)
    selected_messages = selected_user.messages_received.all().order_by('-created_at')
    # selected_comments is a dictionary with keys equal to message ids and values equal to a flitered list of comment instances
    selected_comments = {}
    if len(selected_messages)>0:
        selected_messages_tuples = []
        for message_instance in selected_messages:
            selected_comments[message_instance.id] = message_instance.comments_for_message.all()
        for message in selected_messages:
            selected_messages_tuples.append((message, time_since_created(message.created_at)))   
    else: 
        selected_messages_tuples = []       
    # go into each value, a list of comments
    # iterate through the list of comments
    # replace each comment with a tuple of (comment, time_since_created)
    for key_msg_id, value_comment_list in selected_comments.iteritems():
        list_of_comment_tuples = []
        for comment in value_comment_list:
            list_of_comment_tuples.append((comment, time_since_created(comment.created_at)))
        selected_comments[key_msg_id] = list_of_comment_tuples
    
    if bound_forms: 
        error = bound_forms[0]['error']
    else: 
        error = "False"

    context = {
        'selected_user_id':selected_user.id,
        'selected_user_first_name':selected_user.first_name,
        'selected_user_last_name':selected_user.last_name,
        'selected_user_created_at':selected_user.created_at,
        'selected_user_email':selected_user.email,
        'selected_user_description':selected_user.description,
        'selected_user_message_form':CreateMessageForm(),
        'message_comment_form':CreateCommentForm(),
        'selected_messages':selected_messages_tuples,
        'selected_comments':selected_comments,
        'error':error
    }
    # ******************************************************************
    # everything above here works and outputs for initial render correctly with 
    # return render(request, "msg_app/messages.html", context)
    # ******************************************************************
    # https://stackoverflow.com/questions/14017996/is-there-a-way-to-pass-optional-parameters-to-a-function
    # print "*MSG APP BOUND FORMS*"*10
    # print bound_forms[0]['selected_user_message_form']
    # print "*MSG APP BOUND FORMS*"*10
    # # this sends the bound form back through but it also makes hidden fields visible
    # if bound_forms[0]:
    #     if bound_forms[0]['selected_user_message_form']:
    #         context['selected_user_message_form'] = bound_forms[0]['selected_user_message_form']

    return render(request, "msg_app/messages.html", context)


def process_message(request):
    if request.method == "POST":    
        print request.POST
        bound_form = CreateMessage_Form(request.POST)
        error = "False"
        if bound_form.is_valid() and (request.session['user_id'] == 17 or request.session['user_id'] == 18 or request.session['user_id'] == 19 or request.session['user_id'] == 20):
            #https://stackoverflow.com/questions/621212/another-django-forms-foreign-key-in-hidden-field
            bound_form.save()        
        else:
            error = 'There was an error with your message, and it was not saved. Message content must be at least 15 characters, and you must be logged in as a user with ID 17, 18, 19, or 20, i.e. as one of the Bluth family.'
        selected_user_id = int(request.POST['receiver'])
        bound_forms = {
            'selected_user_message_form': bound_form,
            'error': error
        }
        # TODO: just pass errors through. it's only 1 field. and then have them show above the message box. will be a lil more complex for comments. 
        # req = self.request
        return show(request, selected_user_id, bound_forms)

def process_comment(request):
    if request.method == "POST":    
        bound_form = CreateComment_Form(request.POST)
        error = "False"
        print "processing comment..."
        if bound_form.is_valid() and (request.session['user_id'] == 17 or request.session['user_id'] == 18 or request.session['user_id'] == 19 or request.session['user_id'] == 20):
            #https://stackoverflow.com/questions/621212/another-django-forms-foreign-key-in-hidden-field
            bound_form.save()
        else: 
            error = 'There was an error with your comment, and it was not saved. Comment content must be at least 15 characters, and you must be logged in as a user with ID 17, 18, 19, or 20, i.e. as one of the Bluth family.'
        #     if request.session['user_level'] >= 9:
        #         return redirect(reverse("users:dashboard_admin")) 
        #     else:
        #         return redirect(reverse("users:dashboard"))
        # else:
        #     if request.session['user_level'] >= 9:
        #         return redirect(reverse("users:dashboard_admin")) 
        #     else:
        #         return redirect(reverse("users:dashboard"))
        # number is the id of the message
        message_number = int(request.POST['message'])
        message_instance = Message.objects.get(id=message_number)
        selected_user = message_instance.receiver
        selected_messages = selected_user.messages_received.all().order_by('-created_at')
        # selected_comments is a dictionary with keys equal to message ids and values equal to a flitered list of comment instances
        selected_comments = {}
        if len(selected_messages)>0:
            selected_messages_tuples = []
            for message_instance in selected_messages:
                selected_comments[message_instance.id] = message_instance.comments_for_message.all()
            for message in selected_messages:
                selected_messages_tuples.append((message, time_since_created(message.created_at)))          
        # go into each value, a list of comments
        # iterate through the list of comments
        # replace each comment with a tuple of (comment, time_since_created)
        for key_msg_id, value_comment_list in selected_comments.iteritems():
            list_of_comment_tuples = []
            for comment in value_comment_list:
                list_of_comment_tuples.append((comment, time_since_created(comment.created_at)))
            selected_comments[key_msg_id] = list_of_comment_tuples
        context = {
            'selected_user_id':selected_user.id,
            'selected_user_first_name':selected_user.first_name,
            'selected_user_last_name':selected_user.last_name,
            'selected_user_created_at':selected_user.created_at,
            'selected_user_email':selected_user.email,
            'selected_user_description':selected_user.description,
            'selected_user_message_form':CreateMessageForm(),
            'message_comment_form':CreateCommentForm(),
            'selected_messages':selected_messages_tuples,
            'selected_comments':selected_comments,
            'error':error            
        }
        return render(request, "msg_app/messages.html", context)
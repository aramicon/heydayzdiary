from django import template
from datetime import timedelta

register = template.Library() 

@register.filter(name='diff_in_time') 
def diff_in_time(start,end):
    startdelta=timedelta(hours=start.hour,minutes=start.minute,seconds=start.second)
    enddelta=timedelta(hours=end.hour,minutes=end.minute,seconds=end.second)
    return (enddelta-startdelta).seconds/60
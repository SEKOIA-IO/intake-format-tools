from parser_1 import *
from grok_regex import *
import re

def toregex(log_pattern):
    pattern_replaced=log_pattern
    if ':source_ip' in log_pattern:
        pattern_replaced=log_pattern.replace(':source_ip','')
    if ':source_port' in pattern_replaced:
        pattern_replaced=pattern_replaced.replace(':source_port','')
    if '(?:#VARIABLE)' in pattern_replaced:
        pattern_replaced=pattern_replaced.replace('(?:#VARIABLE)','#VARIABLE')
    if '#VARIABLE' in pattern_replaced:
        pattern_replaced=pattern_replaced.replace(' #VARIABLE','#VARIABLE')
        pattern_replaced=pattern_replaced.replace('#VARIABLE ','#VARIABLE')
        pattern_replaced=pattern_replaced.replace('#VARIABLE','.*')
    for grok in developped_grok:
        if grok in pattern_replaced:
            pattern_replaced=pattern_replaced.replace(grok,developped_grok.get(grok))
    for date in grok_time_unleveled:
        if date in pattern_replaced:
            pattern_replaced=pattern_replaced.replace(date,grok_time_unleveled.get(date))
    return(pattern_replaced)

def test(clusters):
    all_accuracy=[]
    for log_pattern in clusters:
        regex_pattern=toregex(log_pattern)
        right=0
        total=len(clusters.get(log_pattern))
        for log in clusters.get(log_pattern):
            if re.match(regex_pattern,log):
                right+=1
        accuracy=right*100/total
        print('Pattern : '+log_pattern)
        print('Accuracy : '+str(accuracy)+'%')
        print('-----------------------------------------------------------------')
        all_accuracy.append(accuracy)
    print('\n////////////////////////////////////////////////////////////////////\n')
    print('Total accuracy : '+str(sum(all_accuracy)/len(all_accuracy))+'%')


def evaluate(clusters):
    for log_pattern in clusters:
        print(log_pattern)
        regex_pattern=toregex(log_pattern)
        print(regex_pattern+'\n')
        for log in clusters.get(log_pattern):
            matching_pattern=regex_pattern
            while matching_pattern!='' and re.match(regex_pattern,log)==None:
                matching_pattern=matching_pattern[:-1]
                while matching_pattern.count('(')!=matching_pattern.count(')') and matching_pattern.count('[')!=matching_pattern.count(']') and matching_pattern!='':
                    matching_pattern=matching_pattern[:-1]
            if matching_pattern=='':
                print(log+'\n   error\n')
            else:
                print(log+'\n   '+matching_pattern+'\n')
        print('\n===============================================================\n')

evaluate(final_pattern )
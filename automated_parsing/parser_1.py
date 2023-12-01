import re
from ast import literal_eval
import enchant
from langdetect import detect
from string import punctuation
import time
import math
from nltk.tokenize import word_tokenize
from grok_regex import *

open_punctuation = "<([{"
closed_punctuation = ">)]}.:,;?!-"

def frequent_punctuation(ltext):
	s_punct=""
	for log in ltext:
		if ' ' not in log:
			maxi=max(log.count(p) for p in punctuation)
			for p in punctuation:
				if log.count(p)==maxi:
					s_punct = s_punct + p
	if s_punct == "":
		punct=' '
	else:
		punct = max(set(s_punct),key=s_punct.count)
	return (punct)

#construct pairs of words (avoid punctuation or numbers)
def pairs(ltext):
	logs_pairs = {}
	for log in ltext:
		pairs = set()
		words=word_tokenize(log)
		for first in words:
			if first in punctuation or first.isnumeric():
				continue
			seconds = words[words.index(first)+1:]
			for second in seconds:
				if second in punctuation or second.isnumeric():
					continue
				pairs.add((first.lower(),second.lower()))
		logs_pairs.update({log:pairs})
	return(logs_pairs)

#Try for each log to count how many pairs are in common with other logs
#Render a dict to the form logs_count={first_log:{n number of similar pairs:set(logs with n pairs similar to first_log)}}
#logs_count.get(log) = { n similar pairs : {logs with n pairs similar to log}}
def count(ltext, logs_pairs):
	logs_count = {}
	for log in ltext:
		pairs_set= logs_pairs.get(log)
		log_count = {}
		for log_comp in ltext:
			if log_comp == log:
				continue
			pairs_comp = logs_pairs.get(log_comp)
			compt = 0
			for pair in pairs_comp:
				if pair in pairs_set:
					compt += 1
			if log_count.get(compt) == None:
				log_count.update({compt:{log_comp}})
			else:
				log_count.get(compt).add(log_comp)
		logs_count.update({log:log_count})
	return(logs_count)

#Try clusterize if at least sqrt(#pairs) in common
def clustering(ltext,logs_pairs,logs_count):
	clusters = {}
	for log in ltext:
		index = math.sqrt(len(logs_pairs.get(log)))
		pattern = set()
		for common in logs_count.get(log):
			for log2 in logs_count.get(log).get(common):
				index2 = pow(len(logs_pairs.get(log2)), 1/2)
				index_comp = min(index,index2)
				if common >= index_comp:
					pattern.add(log2)
		clusters.update({log:pattern})
	clusters_temp = clusters.copy()
	for log_temp in clusters_temp:
		if clusters_temp.get(log_temp) == set():
			clusters.pop(log_temp)
	return(clusters)

	
#Issue with words present in all the logs in the cluster, but not in the same place. Fix in double check function (next)
def pattern_base(clusters):
	pattern=dict()
	for log in clusters:
		words=word_tokenize(log)
		mini=len(words)
		log_min=log
		words_min=words
		for compare in clusters.get(log):
			words_compare=word_tokenize(compare)
			if len(words_compare)<mini:
				mini=len(words_compare)
				words_min=words_compare
				log_min=compare
		set_temp=set()
		if log_min==log:
			set_temp=clusters.get(log).copy()
		else:
			set_temp={other for other in clusters.get(log) if other != log_min}
			set_temp.add(log)
		pat=words_min
		for word in pat:
			if word.isnumeric():
				pat.remove(word)
		for log_comp in set_temp:
			log_comp_words=word_tokenize(log_comp)
			for word in words_min:
				if word in pat and word not in log_comp_words:
					pat=[elt for elt in pat if elt != word]
				while word in pat and pat.count(word)>log_comp_words.count(word):
					pat.remove(word)
		pattern.update({log:pat})
	return(pattern)

#Check if the clustered words are correctly ordered in all logs
#Not optimal yet, still one case to treat
def double_check(pattern_def):
	res=dict()
	pat_corrected=pattern_def.copy()
	for flat_pat in pattern_def:
		pat=literal_eval(flat_pat)
		pat_bis=pat.copy()
		problems=set()
		for log in pattern_def.get(flat_pat):
			words_log=word_tokenize(log)
			word_prec=words_log[0]
			for word in pat:
				if word in words_log:
					ind=words_log.index(word)
					words_log=words_log[ind+1:]
				else:
					problems.add(word)
				word_prec=word
		if len(problems)==1 and len(pattern_def.get(flat_pat))==2:
			pat_corrected.pop(flat_pat)
			new_pat=pat.copy()
			new_pat.remove(list(problems)[0])
			pat_corrected.update({str(new_pat):pattern_def.get(flat_pat)})
		elif len(problems)>1 and len(pattern_def.get(flat_pat))==2:
			dictemp=dict()
			for log in pattern_def.get(flat_pat):
				log_words=word_tokenize(log)
				place_log=[]
				for word in pat:
					ind=log_words.index(word)
					log_words[ind]=""
					place_log.append((ind,word))
				place_log=sorted(place_log)
				dictemp.update({log:place_log})
			pats=[]
			for elt_pats in dictemp.values():
				pat_temp=[b for (a,b) in elt_pats]
				pats.append(pat_temp)
			false_positive=[]
			for i in range (len(pats[0])):
				if pats[0][i]!=pats[1][i]:
					elt=pats[0][i]
					j=pats[1].index(elt)
					if i==0 or j==0:
						if pats[0][i+1]!=pats[1][j+1]:
							false_positive.append(elt)
					elif i==len(pats[0])-1 or j==len(pats[1])-1:
						if pats[0][i-1]!=pats[1][j-1]:
							false_positive.append(elt)
					else:
						if pats[0][i-1]!=pats[1][j-1] and pats[0][i+1]!=pats[1][j+1]:
							false_positive.append(elt)
			pat_corrected.pop(flat_pat)
			new_pat=pat.copy()
			new_pat=[elt for elt in new_pat if elt not in false_positive]
			if pat_corrected.get(str(new_pat))==None:
				pat_corrected.update({str(new_pat):pattern_def.get(flat_pat).copy()})
			else:
				for log in pattern_def.get(flat_pat):
					if log not in pat_corrected.get(str(new_pat)):
						pat_corrected.get(str(new_pat)).add(log)
		elif len(problems)==1 and len(pattern_def.get(flat_pat))>2:
			dictemp=dict()
			for log in pattern_def.get(flat_pat):
				log_words=word_tokenize(log)
				place_log=[]
				for word in pat:
					ind=log_words.index(word)
					log_words[ind]=""
					place_log.append((ind,word))
				place_log=sorted(place_log)
				key=str([b for (a,b) in place_log])
				if dictemp.get(key)==None:
					dictemp.update({key:{log}})
				else:
					dictemp.get(key).add(log)
				dic_sub=dictemp.copy()
				if flat_pat in pat_corrected:
					pat_corrected.pop(flat_pat)
				for key in dictemp:
					if len(dictemp.get(key))==1:
						dic_sub.pop(key)
					else:
						pat_corrected.update({key:dictemp.get(key).copy()})
		# ~ if more than one problem with more than two logs in the cluster
		else:
			pat_corrected.pop(flat_pat)
			for log in pattern_def.get(flat_pat):
				l_words=word_tokenize(log)
				pat_temp=pat.copy()
				s=[]
				for word in l_words:
					if word in punctuation:
						continue
					if word in pat_temp:
						s.append(word)
						pat_temp[pat_temp.index(word)]='treated'
				if pat_corrected.get(str(s))==None:
					pat_corrected.update({str(s):{log}})
				else:
					pat_corrected.get(str(s)).add(log)
				
		res.update({flat_pat:problems})
	res_copy=res.copy()
	for k in res_copy:
		if res_copy.get(k)==set():
			res.pop(k)
	return(res,pat_corrected)


#IDEA: Get the template: check the log in the cluster with minimum length, and check each word to see if it is in all the other words in the cluster

#create dict with flattened list of the pattern and the logs matching the pattern
#Input: dictionnary of clusters, dictionnary of patterns
#Output: dictionnary of pattern with associated logs
def pattern(clusters,pattern):
	pattern_def = {}
	for log in clusters:
		set_temp = clusters.get(log).copy()
		set_temp.add(log)
		pat = str(pattern.get(log))
		pattern_def.update({pat:set_temp})
	return(pattern_def)


#Input: pattern_def
#Output: dict of patterns and the possible values found between each word
def pattern_ordered(pattern_def):
	places_cons_pattern=dict()
	for pattern in pattern_def:
		places=dict()
		words_pattern=literal_eval(pattern)
		for log in pattern_def.get(pattern):
			j=-1
			s=""
			i=0
			ind_word=0
			size=len(words_pattern[ind_word])
			while i<len(log):
				if i+size<len(log) and log[i:i+size]==words_pattern[ind_word]:
					if s not in [""," "]:
						if s[0]==" ":
							s=s[1:]
						if s[-1]==" ":
							s=s[:-1]
						if places.get(j)==None:
							places.update({j:[s]})
						else:
							places.get(j).append(s)
						j+=1
					i+=size
					s=""
					j+=1
					if ind_word+1<len(words_pattern):
						ind_word+=1
						size=len(words_pattern[ind_word])
				else:
					s+=log[i]
					i+=1
			if s not in [""," "]:
				if s[0]==" ":
					s=s[1:]
				if s[-1]==" ":
					s=s[:-1]
				if places.get(j)==None:
					places.update({j:[s]})
				else:
					places.get(j).append(s)
		places_cons_pattern.update({pattern:places})
	return (places_cons_pattern)
	
#Currently, only works with IP, UUID, TTY and MAC (+similar words) --> Need to work on the MAC utilisation, unoptimized right now
def regex_extractor(places_cons_pattern):
	dict_regex=dict()
	for pat in places_cons_pattern:
		dict_pat=dict()
		for place in places_cons_pattern.get(pat):
			corpus=list(set(places_cons_pattern.get(pat).get(place).copy()))
			grokpat=None
			for (key,regex) in grokpat_spec.items():
				if all(re.fullmatch(regex,string)!=None for string in corpus):
					grokpat=(key,"Grok")
					break
			if grokpat==None and all(any(re.fullmatch(grokpat_spec.get(ip),string)!=None for ip in ["%{IPV4}","%{IPV6}"]) for string in corpus):
				grokpat=("%{IP}","Grok")
			form=time_format(corpus)
			if form != None:
				grokpat=(form,"Date")
			if grokpat ==None and all(string.isnumeric() for string in corpus):
				grokpat=('%{INT}',"Grok")
			if grokpat==None and all(string==corpus[0] for string in corpus) and len(corpus)>1:
				grokpat=(corpus[0],"string")
			if grokpat != None:
				if len(places_cons_pattern.get(pat).get(place))>1:
					dict_pat.update({place:grokpat[0]})
				elif grokpat[1]!="string":
					dict_pat.update({place:"(?:"+grokpat[0]+")"})
			else:
				grokpat=[]
				rdmpat=[]
				corpus_bis=corpus.copy()
				corpus_ter=corpus_bis.copy()
				for (key,regex) in grokpat_spec.items():
					if all(re.search(regex,string)!=None for string in corpus):
						grokpat.append(key)
						for elt in corpus:
							elt_bis=' '.join(re.split(grokpat_spec.get(key),elt))
							corpus_bis[corpus.index(elt)]=elt_bis
							corpus_ter=corpus_bis.copy()
				if grokpat==[] and all(any(re.search(grokpat_spec.get(ip),string)!=None for ip in ["%{IPV4}","%{IPV6}"]) for string in corpus):
					grokpat.append("%{IP}")
					for elt in corpus:
						if re.search(grokpat_spec.get("%{IPV4}"),elt)!=None:
							elt_bis=' '.join(re.split(grokpat_spec.get("%{IPV4}"),elt))
						else:
							addresses=[re.findall(grokpat_spec.get("%{IPV6}"),elt)[i][0] for i in range(len(re.findall(grokpat_spec.get("%{IPV6}"),elt)))]
							i=0
							l=elt
							split=[]
							while i<len(addresses):
								split.append(l.split(addresses[i])[0])
								l=l.split(addresses[i])[1]
								i+=1
							elt_bis=' '.join(split)
						if elt_bis != None:
							corpus_bis[corpus_bis.index(elt)]=elt_bis
							corpus_ter=corpus_bis.copy()
				all_logs = ' '.join(corpus_bis)
				vocabulary=list(set(word_tokenize(all_logs)))
				for word in vocabulary:
					if any(re.match(grokpat_spec.get(grok),word)!=None for grok in grokpat if grok != '%{IP}') or word in punctuation or word.isnumeric():
						vocabulary.remove(word)
					else:
						if all(word in logs for logs in corpus_bis):
							rdmpat.append(word)
							for elt in corpus_bis:
								elt_bis=elt.replace(word,'')
								corpus_ter[corpus_bis.index(elt)]=elt_bis
				intpat=[]
				if all(re.search('\d+',string)!=None for string in corpus_ter):
					for i in range (min(len(re.findall('\d+',string)) for string in corpus_ter)):
						intpat.append('%{INT}')
				key=[]
				key.extend(elt for elt in grokpat)
				key.extend(elt for elt in rdmpat)
				key.extend(intpat)
				### WIP to improve result in one string describing pattern when possible
				corpus_bis=corpus.copy()
				messages=[]
				for message in corpus:
					if "%{IP}" in grokpat:
						message_patternized=message.split()
					else:
						message_patternized=word_tokenize(message)
					messages.append(message_patternized)
					ind_mess=len(messages)-1
					index=corpus.index(message)
					for elt in message_patternized:
						elt_temp=messages[ind_mess][message_patternized.index(elt)]
						for grok in grokpat:
							if grok == "%{IP}" and any(re.search(grokpat_spec.get(ip),elt)!=None for ip in ["%{IPV4}","%{IPV6}"]):
								if re.search(grokpat_spec.get("%{IPV4}"),elt)!=None:
									addresses=re.findall(grokpat_spec.get("%{IPV4}"),elt)
								else:
									addresses=[re.findall(grokpat_spec.get("%{IPV6}"),elt)[i][0] for i in range(len(re.findall(grokpat_spec.get("%{IPV6}"),elt)))]
								for add in addresses:
									corpus_bis[index]=corpus_bis[index].replace(add,grok)
									messages[ind_mess][message_patternized.index(elt)]=corpus_bis[index]
									elt_temp=corpus_bis[index]
							elif grok != "%{IP}" and re.match(grokpat_spec.get(grok),elt)!=None:
								corpus_bis[index]=corpus_bis[index].replace(elt,grok,1)
								messages[ind_mess][message_patternized.index(elt)]=grok
								elt_temp=grok
							elif grok != "%{IP}" and re.search(grokpat_spec.get(grok),elt):
								corpus_bis[index]=corpus_bis[index].replace(elt,grok.join(re.split(grokpat_spec.get(grok),elt)))
								messages[ind_mess][message_patternized.index(elt)]=grok.join(re.split(grokpat_spec.get(grok),elt))
								elt_temp=grok.join(re.split(grokpat_spec.get(grok),elt))
						if "%{IP}" not in grokpat and re.search(r"(?<!IPV)\d+",elt_temp) and all(re.search(grokpat_spec.get(grok),elt_temp)==None for grok in grokpat if grok != "%{IP}"):
							corpus_bis[index]=corpus_bis[index].replace(elt_temp,'%{INT}'.join(re.split(r"(?<!IPV)\d+",elt_temp)))
							messages[ind_mess][message_patternized.index(elt_temp)]='%{INT}'.join(re.split(r"(?<!IPV)\d+",elt_temp))
						if elt.isalnum()==False and all(re.search(grokpat_spec.get(grok),elt)==None for grok in grokpat if grok != "%{IP}") and re.search(r"\d",elt)==None:
							p=frequent_punctuation(elt)
							sub_word=elt.split(p)
							elt_bis=elt
							for sub in sub_word:
								if sub.isnumeric():
									elt_bis=elt_bis.replace(sub,'%{INT}',1)
							corpus_bis[index]=corpus_bis[index].replace(elt,elt_bis)
							temp=elt_bis.split(p)
							while '' in temp:
								temp.remove('')
							if temp==[]:
								messages[ind_mess][message_patternized.index(elt)]=p
							else:
								messages[ind_mess][message_patternized.index(elt)]=p.join(temp)
				if all(message==corpus_bis[0] for message in corpus_bis) and len(corpus)>1:
					dict_pat.update({place:corpus_bis[0]})
				#Need to work with '-','/' symbols, as it is not treated by word_tokenize. Might use regex "(\W+)"
				else:
					key_bis=[]
					message_min=min(messages, key=len)
					for part in message_min:
						if all(part in message for message in messages):
							key_bis.append(part)
						elif len(word_tokenize(part))>1:
							l=re.split("(\W+)",part)
							for sub in l:
								for message in messages:
									if any(sub in re.split("(\W+)",elt) for elt in message):
										b=True
									else:
										b=False
										break
								if b==True:
									key_bis.append(sub)
					key_ter=key_bis.copy()
					for elt in range (1,len(key_bis)-2):
						if "%{"+key_bis[elt]+"}" in developped_grok:
							ind=key_ter.index(key_bis[elt])
							s=key_ter[ind-1]+key_ter[ind]+key_ter[ind+1]
							key_ter= key_ter[:ind-1]+[s]+key_ter[ind+2:]
					while '' in key_ter:
						key_ter.remove('')
					### End of WIP
					if len(corpus)>1:
						if key_ter!=[]:
							corpus_temp=corpus_bis.copy()
							dter=dict()
							s=""
							for elt in range (len(key_ter)):
								if elt>0:
									s+=key_ter[elt-1]
								b=[]
								for message in corpus_temp:
									ind=corpus_temp.index(message)
									sep=message.split(key_ter[elt],1)
									if sep[0] != '':
										b.append(sep[0])
									if len(sep)>1:
										corpus_temp[ind]=sep[1]
								if b==[]:
									b=None
								if elt==0 and b!=None:
									dter.update({"":b})
								elif b!=None:
									dter.update({s:b})
									s=""
							a=[]
							for message in corpus_temp:
								if message != '':
									a.append(message)
							if a==[]:
								a=None
							dter.update({s+key_ter[elt]:a})
							dict_pat.update({place:dter})
						else:
							dict_pat.update({place:"%{GREEDYDATA}"})
					elif grokpat != []:
						dict_pat.update({place:"%{GREEDYDATA}"})
		dict_regex.update({pat:dict(sorted(dict_pat.items(), key=lambda t: t[0]))})
	return(dict_regex)
		
#grok_time is a more developed form of grokpat_date, explaining all grok patterns as regex. As above, the keys corresponds to the level of needed subpatterns
grok_time={}
for i in grokpat_date:
	lvl_i_time=dict()
	for pat in grokpat_date.get(i):
		s=grokpat_date.get(i).get(pat)
		if i>0:
			j=i-1
			while j>=0:
				for pat_prec in grok_time.get(j):
					s=s.replace(pat_prec,grok_time.get(j).get(pat_prec))
				j-=1
		lvl_i_time.update({pat:s})
	grok_time.update({i:lvl_i_time})
	
#grok_time_unleveled gives all the regex of time/date GROK, without considering levels
grok_time_unleveled=dict()
for i in grok_time:
	grok_time_unleveled.update({key:value for key,value in grok_time.get(i).items()})
			
		
#Tool for direct replacement of dates by a Grok pattern in clusterization
def time_format(corpus):
	i=3
	l=[]
	for j in range(3):
		for k in grok_time.get(i-j):
			if all(re.search(grok_time.get(i-j).get(k),string)!=None for string in corpus) and k not in ["%{ISO8601_SECOND}",'%{ISO8601_TIMEZONE}']:
				l.append((k,i-j))
				if (k in ["%{DATE}","%{DATE_EU}","%{DATE_US}"]):
					if any(len(set(re.findall("\W|_",re.search(grok_time.get(i-j).get(k),string).group())))>1 for string in corpus):
						l.remove((k,i-j))
	for (elt,lvl) in l:
		if 'STAMP' in elt:
			return(elt)
	if l!= []:
		return(l[0][0])
	for k in ["%{MONTH}","%{DAY}"]:
		if all(re.search(grok_time.get(0).get(k),string)!=None for string in corpus):
			return(k)


#Same purpose as pattern_ordered, but considering the extracted Grok
def reorder(def_dict_V2,explicit_pattern,pattern_def):
	updated_patterns=dict()
	pattern_with_logs=dict()
	for str_pat in def_dict_V2:
		pat=literal_eval(str_pat)
		log_size=len(pat)+len(def_dict_V2.get(str_pat))
		l=[]
		j=0
		temp=0
		updated_sub=dict()
		for i in range(-1,log_size):
			if i in def_dict_V2.get(str_pat):
				if type(explicit_pattern.get(str_pat).get(i))==str:
					l.append(explicit_pattern.get(str_pat).get(i))
				elif type(explicit_pattern.get(str_pat).get(i))==dict:
					for k in explicit_pattern.get(str_pat).get(i):
						if k!="":
							l.append(k)
							temp+=1
						if explicit_pattern.get(str_pat).get(i).get(k)!=None:
							if len(explicit_pattern.get(str_pat).get(i).get(k))<len(def_dict_V2.get(str_pat).get(i)):
								l.append("(?:%{GREEDYDATA})")
							elif all(elt[0]==" " for elt in explicit_pattern.get(str_pat).get(i).get(k)):
								l.append(" %{GREEDYDATA}")
							else:
								l.append("%{GREEDYDATA}")
							updated_sub.update({i+temp+1:explicit_pattern.get(str_pat).get(i).get(k)})
				else:
					l.append("%{GREEDYDATA}")
					updated_sub.update({i+temp+1:def_dict_V2.get(str_pat).get(i)})
			elif j<len(pat):
				l.append(pat[j])
				j+=1
		for ind in range (len(l)):
			if ind<len(l)-1:
				if l[ind] not in open_punctuation and l[ind+1][0] not in closed_punctuation and l[ind+1] not in ["%{GREEDYDATA}"," %{GREEDYDATA}"]:
					l[ind]=l[ind]+" "
		pattern="".join(l)
		##WIP##
		ips=["%{IP}","%{IPV4}","%{IPV6}"]
		for ip in ips:
			if pattern.count(ip)==1 and all(pattern.count(address)==0 for address in ips if address != ip):
				if pattern.count(ip+"/%{INT}")==1:
					pattern=pattern.replace(ip+"/%{INT}",ip[:-1]+":source_ip}/%{INT:source_port}")
				else:
					pattern=pattern.replace(ip,ip[:-1]+":source_ip}")
		##END OF WIP##
		updated_patterns.update({pattern:updated_sub})
		if updated_sub==dict():
			updated_patterns.update({pattern:"PATTERN COMPLETE"})
		while "%{GREEDYDATA}%{GREEDYDATA}" in pattern:
			pattern=pattern.replace("%{GREEDYDATA}%{GREEDYDATA}","%{GREEDYDATA}")
		pattern_with_logs.update({pattern:pattern_def.get(str_pat).copy()})
	return(updated_patterns,pattern_with_logs)

#need to change punctuation taken into account as textual punctuation, not considered as regex element -- addition of \ (else the parsing is not working)
#issue with some greedydata (some are escaped but are not supposed to)
def punctuation_fix(pattern_with_logs):
	newdict = dict()
	for pat in pattern_with_logs:
		dgrok=dict()
		for grok in developped_grok:
			i=0
			j=0
			size=len(grok)
			while '(?:'+grok+')' in pat [j:]:
				i=pat.index('(?:'+grok+')',j)
				j=i+size+4
				dgrok.update({i:'(?:'+grok+')'})
			while grok in pat[j:]:
				i=pat.index(grok,j)
				j=i+size
				dgrok.update({i:grok})
		for grok in ['%{IPV4:source_ip}','%{IPV6:source_ip}','%{IP:source_ip}','%{INT:source_port}']:
			i=0
			j=0
			size=len(grok)
			while grok in pat[j:]:
				i=pat.index(grok,j)
				j=i+size
				dgrok.update({i:grok})
		for grok in grok_time_unleveled:
			i=0
			j=0
			size=len(grok)
			while '(?:'+grok+')' in pat [j:]:
				i=pat.index('(?:'+grok+')',j)
				j=i+size+4
				dgrok.update({i:'(?:'+grok+')'})
			while grok in pat[j:]:
				i=pat.index(grok,j)
				j=i+size
				dgrok.update({i:grok})		
		indlist=sorted(dgrok)
		i=0
		j=0
		newpattern=""
		for ind in range (len(indlist)):
			j=indlist[ind]
			newpattern+=re.escape(pat[i:j])+dgrok.get(j)
			i=j+len(dgrok.get(j))
		newpattern=newpattern.replace("\\ "," ")
		newdict.update({newpattern:pattern_with_logs.get(pat).copy()})
	return(newdict)

fcisf = open("logfiles/Cisco_Firewall.txt","r")
fcism=open("logfiles/Cisco_Meraki.txt","r")
fcisnx=open("logfiles/Cisco_NX_OS.txt","r")
fbind = open("logfiles/Bind.txt","r")
fivanti = open("logfiles/Ivanti.txt","r")
fobsd = open("logfiles/open_bsd.txt","r")
fbroad = open("logfiles/broadcom.txt","r")
fddi = open("logfiles/ddi.txt","r")
fdhcpd=open("logfiles/dhcpd.txt","r")
fibm = open("logfiles/IBM.txt","r")
fnginx=open("logfiles/nginx.txt","r")
fsquid=open("logfiles/squid.txt","r")
textcisf = fcisf.read()
textcism=fcism.read()
textcisnx=fcisnx.read()
textbind=fbind.read()
textivanti=fivanti.read()
textobsd = fobsd.read()
textbroad = fbroad.read()
textddi = fddi.read()
textdhcpd = fdhcpd.read()
textibm = fibm.read()
textnginx=fnginx.read()
textsquid=fsquid.read()

text = textcisf
start=time.time()

#Par défaut, le dictionnaire est en anglais. Reconnaissance de la langue du texte si possible
dictionnary=enchant.Dict("en_US")
langage=detect(text)
if enchant.dict_exists(langage) == True and langage != "en":
	dictionnary=enchant.Dict(langage)


ltext = text.splitlines()
while "" in ltext:
	ltext.remove("")

#Deletion of quotes
for log in ltext:
	if log[0] in ['"',"'"] and log[-1] in ["'",'"']:
		i = ltext.index(log)
		log_replaced = log[1:-1]
		ltext[i]=log_replaced
	
punct = frequent_punctuation(ltext)

logs_pairs = pairs(ltext)

#Try for each log to count how many pairs are in common with other logs
logs_count = count(ltext,logs_pairs)

#Try clusterize if at least sqrt(#pairs) in common
clusters = clustering(ltext,logs_pairs,logs_count)

pattern_temp = pattern_base(clusters)
pattern_def = pattern(clusters,pattern_temp)
pattern_def=double_check(pattern_def)[1]
# ~ we need to have double_check(pattern_def)[0]=={}
# ~ still need to work on the precision on last double_check case (rn, doesn't include punctuation in patterns)
def_dict_V2 = pattern_ordered(pattern_def)
explicit_pattern=regex_extractor(def_dict_V2)
ls,pattern_with_logs=reorder(def_dict_V2,explicit_pattern,pattern_def)
final_pattern=punctuation_fix(pattern_with_logs)
#We can retrieve the logs associated to the patterns, as def_dict_V2.keys()==pattern_def.keys(), and pattern_def.get(pat) gives the associated logs. And as we can easily get the pats with def_dict_V2...
end=time.time()
print("Time :"+str(end-start))


#Might need to add grok dates in here
grokpat_spec = {"%{IPV4}":"(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9])","%{IPV6}":"((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?","%{UUID}":"[A-Fa-f0-9]{8}-(?:[A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}","%{CISCOMAC}":"(?:(?:[A-Fa-f0-9]{4}\.){2}[A-Fa-f0-9]{4})","%{WINDOWSMAC}":"(?:(?:[A-Fa-f0-9]{2}-){5}[A-Fa-f0-9]{2})","%{COMMONMAC}":"(?:(?:[A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})","%{TTY}":"(?:/dev/(pts|tty([pq])?)(\w+)?/?(?:[0-9]+))"}

grokpat_sub = {"%{EMAILLOCALPART}":"[a-zA-Z][a-zA-Z0-9_.+-=:]+","%{HOSTNAME}":"\b(?:[0-9A-Za-z][0-9A-Za-z-]{0,62})(?:\.(?:[0-9A-Za-z][0-9A-Za-z-]{0,62}))*(\.?|\b)","%{USERNAME}":"[a-zA-Z0-9._-]+","%{INT}":"(?:[+-]?(?:[0-9]+))","%{URIPROTO}":"[A-Za-z]+(\+[A-Za-z+]+)?","%{URIPATH}":"(?:/[A-Za-z0-9$.+!*'(){},~:;=@#%_\-]*)+","%{URIPARAM}":"\?[A-Za-z0-9$.+!*'|(){},~@#%&/=:;_?\-\[\]<>]*","%{UNIXPATH}":"((?:\/[a-zA-Z0-9\.\:]+(?:_[a-zA-Z0-9\:\.]+)*(?:\-[\:a-zA-Z0-9\.]+)*)+\/?)","%{WINPATH}":'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*'}

grokpat_const_lv1 = {"%{EMAILADDRESS}":"%{EMAILLOCALPART}@%{HOSTNAME}","%{URIPATHPARAM}":"%{URIPATH}(?:%{URIPARAM})?","%{IP}":"(?:%{IPV6}|%{IPV4})","%{PATH}":"(?:%{UNIXPATH}|%{WINPATH})"}

grokpat_const_lv2 = {"%{IPORHOST}":"(?:%{IP}|%{HOSTNAME})"}

grokpat_const_lv3 = {"%{HOSTPORT}":"%{IPORHOST}:%{POSINT}","%{URIHOST}":"%{IPORHOST}(?::%{POSINT})?"}

grokpat_const_lv4 ={"%{URI}":"(?:%{URIPROTO})://(?:%{USERNAME}(?::[^@]*)?@)?(?:%{URIHOST})?(?:%{URIPATHPARAM})?"}

grokpat_date = {0:{"%{MONTHNUM}":"(?:0?[1-9]|1[0-2])","%{MONTHNUM2}":"(?:0[1-9]|1[0-2])","%{MONTHDAY}":"(?:(?:0[1-9])|(?:[12][0-9])|(?:3[01])|[1-9])","%{YEAR}":"(?>\d\d){1,2}","%{HOUR}":"(?:2[0123]|[01]?[0-9])","%{MINUTE}":"(?:[0-5][0-9])","%{SECOND}":"(?:(?:[0-5]?[0-9]|60)(?:[:.,][0-9]+)?)","%{MONTH}":"\b(?:Jan(?:uary|uar)?|Feb(?:ruary|ruar)?|M(?:a|ä)?r(?:ch|z)?|Apr(?:il)?|Ma(?:y|i)?|Jun(?:e|i)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|O(?:c|k)?t(?:ober)?|Nov(?:ember)?|De(?:c|z)(?:ember)?)\b","%{DAY}":"(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)","%{TZ}":"(?:[PMCE][SD]T|UTC)"},1:{"%{TIME}":"(?!<[0-9])%{HOUR}:%{MINUTE}(?::%{SECOND})(?![0-9])","%{DATE_US}":"%{MONTHNUM}[/-]%{MONTHDAY}[/-]%{YEAR}","%{DATE_EU}":"%{MONTHDAY}[./-]%{MONTHNUM}[./-]%{YEAR}","%{ISO8601_TIMEZONE}":"(?:Z|[+-]%{HOUR}(?::?%{MINUTE}))","%{ISO8601_SECOND}":"(?:%{SECOND}|60)","%{DATESTAMP_EVENTLOG}":"%{YEAR}%{MONTHNUM2}%{MONTHDAY}%{HOUR}%{MINUTE}%{SECOND}"},2:{"%{DATE}":"%{DATE_US}|%{DATE_EU}","%{TIMESTAMP_ISO8601}":"%{YEAR}-%{MONTHNUM}-%{MONTHDAY}[T ]%{HOUR}:?%{MINUTE}(?::?%{SECOND})?%{ISO8601_TIMEZONE}?","%{DATESTAMP_RFC2822}":"%{DAY}, %{MONTHDAY} %{MONTH} %{YEAR} %{TIME} %{ISO8601_TIMEZONE}","%{DATESTAMP_RFC822}":"%{DAY} %{MONTH} %{MONTHDAY} %{YEAR} %{TIME} %{TZ}","%{DATESTAMP_OTHER}":"%{DAY} %{MONTH} %{MONTHDAY} %{TIME} %{TZ} %{YEAR}","%{HTTPDERROR_DATE}":"%{DAY} %{MONTH} %{MONTHDAY} %{TIME} %{YEAR}","%{HTTPDATE}":"%{MONTHDAY}/%{MONTH}/%{YEAR}:%{TIME} %{INT}"},3:{"%{DATESTAMP}":"%{DATE}[- ]%{TIME}"}}

grokpat_basic = {"%{BASE10NUM}":"(?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))","%{NUMBER}":"(?:%{BASE10NUM})","%{BASE16NUM}":"(?<![0-9A-Fa-f])(?:[+-]?(?:0x)?(?:[0-9A-Fa-f]+))","%{BASE16FLOAT}":"\b(?<![0-9A-Fa-f.])(?:[+-]?(?:0x)?(?:(?:[0-9A-Fa-f]+(?:\.[0-9A-Fa-f]*)?)|(?:\.[0-9A-Fa-f]+)))\b","%{POSINT}":"\b(?:[1-9][0-9]*)\b","%{NONNEGINT}":"\b(?:[0-9]+)\b","%{WORD}":"\b\w+\b","%{NOTSPACE}":"\S+","%{SPACE}":"\s*","%{DATA}":".*?","%{GREEDYDATA}":".*"}


developped_grok=dict()
for pat_0 in grokpat_spec:
    developped_grok.update({pat_0:grokpat_spec.get(pat_0)})
for pat_0 in grokpat_sub:
    developped_grok.update({pat_0:grokpat_sub.get(pat_0)})
for pat_0 in grokpat_basic:
    developped_grok.update({pat_0:grokpat_basic.get(pat_0)})
for pat_1 in grokpat_const_lv1:
    s=grokpat_const_lv1.get(pat_1)
    for pat_0 in developped_grok:
        s=s.replace(pat_0,developped_grok.get(pat_0))
    developped_grok.update({pat_1:s})
for pat_2 in grokpat_const_lv2:
    s=grokpat_const_lv2.get(pat_2)
    for pat_1 in developped_grok:
        s=s.replace(pat_1,developped_grok.get(pat_1))
    developped_grok.update({pat_2:s})
for pat_3 in grokpat_const_lv3:
    s=grokpat_const_lv3.get(pat_3)
    for pat_2 in developped_grok:
        s=s.replace(pat_2,developped_grok.get(pat_2))
    developped_grok.update({pat_3:s})
for pat_4 in grokpat_const_lv4:
    s=grokpat_const_lv4.get(pat_4)
    for pat_3 in developped_grok:
        s=s.replace(pat_3,developped_grok.get(pat_3))
    developped_grok.update({pat_4:s})


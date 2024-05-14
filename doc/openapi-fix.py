#!/usr/bin/python

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile',help='(openapi yaml file to fix)', required=True)
parser.add_argument('-o','--outputFile',help='(output file)', required=True)
parser.add_argument('-u','--urlFile',help='(f5 url file)', required=True)
args = parser.parse_args()



with open(args.inputFile, "r") as txtFile:
    lines = [ line.rstrip() for line in txtFile ]

"""
# Fix the file coming from postman2openapi, not always perfect.
u = re.compile('(\s*)\? (/.*/$)')
for idx in range(len(lines)):
    if re.match(u, lines[idx]):
        lines[idx] = u.sub('\\1\\2:', lines[idx])
        if re.match('\s+ : .*', lines[idx+1]):
            lines[idx+1] = lines[idx+1].replace(' : ', '   ')
"""

# AssetID, uid.
i1 = re.compile('/f5/[0-9]+/(.*)') # AssetId.
i2 = re.compile('(.*)/[0-9]+/(.*)') # other id.
p2 = re.compile('(.*)\/[a-zA-z]{5}-[a-zA-Z]{16}\/(.*)[a-zA-z]{5}-[a-zA-Z]{16}\/(.*)') # ../uid/../uid/..
p1 = re.compile('(.*)\/[a-zA-z]{5}-[a-zA-Z]{16}\/(.*)') # ../uid/..

# loop the lines and replace when needed.
for idx in range(len(lines)):
    if re.match('\s+/f5/.*/:', lines[idx]): # adjust urls only.
        lines[idx] = i1.sub('/f5/someId/\\1', lines[idx])
        lines[idx] = i2.sub('\\1/someId/\\2', lines[idx])
        lines[idx] = p2.sub('\\1/uid/\\2uid/\\3', lines[idx])
        lines[idx] = p1.sub('\\1/uid/\\2', lines[idx])

# Identify the urls parameters, using the F5Urls.py file.
reUrl = re.compile("^\s+.*path\('([^']*)'.*")
urls = list()
with open(args.urlFile, "r") as urlFile:
    for line in urlFile:
        u = re.search(reUrl, line)
        if u and u.group(1): # skip root url.
            urls.append(u.group(1))

# For each url try to find a match a line in the input file and adjust that line.
# At each loop modify the url string to obtain a regex and try to match an url line of the inputFile.
reStr = re.compile('<str:([A-Za-z0-9]+)>/')
reSegmentStr = re.compile('<str:([A-Za-z0-9]+)>')
reId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>/')
reSegmentId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>')
for url in urls:
    strMatch = reStr.sub('[A-Za-z0-9]+/', url)
    urlMatch = '/f5/' + reId.sub('someId/', strMatch)


    for idx in range(len(lines)):
        if re.match('\s+/f5/.*/:', lines[idx]): # get urls only from the inputFile.
            if re.match(urlMatch, lines[idx].strip().replace(':','')): # url line example in inputFile: /f5/<int:assetId>/Partition1/pool/POOL/:.

                adjustedLineUrl = '  /' # 2 leading spaces.
                segments = url.split('/')
                if not segments[-1]:  # empty segment.
                    segments.pop(-1)
                segments.insert(0,'f5') # urls in the urlFile doesn't have the f5 prefix.

                for segment in segments:
                    if re.match(reSegmentId, segment):
                        s = reSegmentId.sub('{\\1}', segment )
                    elif re.match(reSegmentStr, segment):
                        s = reSegmentStr.sub('{\\1}', segment )
                    else:
                        s = segment
                    #print('SSSSSSSSSSSSS ' + s )
                    adjustedLineUrl += s + '/'

                lines[idx] = adjustedLineUrl + ':'

"""
for idx in range(len(lines)):
    res = re.search(r'(.*)/f5/assetId/([^/]+)/(.*)', lines[idx])
    if res:
        endUrl = res.group(3)[:-1] # remove trailing ':"
        endUrlPattern = endUrl

        if '/uid/' in endUrlPattern:
            endUrlPattern = endUrlPattern.replace('/uid/', '/<str:[a-zA-z0-9:]+[uU]id>/')
        m = ".*path\('<int:assetId>/<str:partitionName/" + endUrlPattern + "'.*"
        for u in urls:
            if re.match(m, u):
                lines[idx] = res.group(1)+ "/f5/assetId/partition/" + endUrl + ':'
"""

# When the same url for 2 http verbs is recorded in postman with 2 different uid or 2 different partition name, it results 2 identical urls in swagger. Join them.
# Example:
#
#  /checkpoint/1/POLAND/tag/8f01bedd-facf-4aca-a89b-2c0e4c46f386/:
#     get:
#     ....
#  /checkpoint/1/POLAND/tag/1ec14820-3f61-4f4f-b3b1-32a3f8e841fe/:
#     patch:
#
# The result are 2 equal entries: /checkpoint/1/POLAND/tag/uid/
# The second one should be removed the data will be automatically merged in the first one.
cleanedLines = list()
# uid
prevUrlLine = ""
for line in lines:
    if re.match('\s+/f5/.*/:', line):
        if line == prevUrlLine: # skip
            continue
        prevUrlLine = line
    cleanedLines.append(line)
"""
# domain
lines = cleanedLines
cleanedLines = []
prevUrlLine = ""
for line in lines:
    if re.match('(.*)/f5/assetId/partition/.*', line):
        if line == prevUrlLine: # skip
            continue
        prevUrlLine = line
    cleanedLines.append(line)
"""


with open(args.outputFile, 'w') as o:
    for line in cleanedLines:
        print(line, file = o)
    

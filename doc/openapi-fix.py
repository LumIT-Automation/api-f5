#!/usr/bin/python

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile',help='(openapi yaml file to fix)', required=True)
parser.add_argument('-o','--outputFile',help='(output file)', required=True)
parser.add_argument('-u','--urlFile',help='(f5 url file)', required=True)
args = parser.parse_args()



# Remove a sublist from list l starting from the element at the index pos.
def removeSubList(l: list, startPos: int, endPos: int) -> list:
    removedSubList = list()

    try:
        for i in range(startPos, endPos):
            removedSubList.append(l.pop(startPos)) # the index shift, so the position is always the same.
        return removedSubList
    except Exception as e:
        raise e



# Insert a sublist at the index pos in the list l.
def insertSubList(l: list, pos: int, sublist: list) -> None:
    for i in range(len(sublist)):
        l.insert(pos + i, sublist[i])



def getBlocksIndexes(l: list) -> (int, int):
    start = 0
    blocks = list()

    try:
        for i in range(len(l)):
            if re.match('\s+/f5/(.*/)?:', l[i]):  # line delimiting of a block or end last block.
                if not start:
                    start = i
                else:
                    blocks.append((start, i))
                    start = i
            if start and re.match('^[a-z]+:', l[i]): # end last block.
                blocks.append((start, i))
                break

        return blocks
    except Exception as e:
        raise e



def getBlockHttpMethodsIndexes(b: list, blockStartIndex: int) -> (int, int):
    httpMethods = ('get:', 'post:', 'put:', 'patch:', 'delete:')
    start = 0
    subBlocksIdx = list()

    try:
        for i in range(len(b)):
            if b[i].strip() in httpMethods:
                if not start:
                    start = i
                else:
                    subBlocksIdx.append((blockStartIndex + start, blockStartIndex + i - 1)) # end subblock.
                    start = i
        subBlocksIdx.append((blockStartIndex + start, blockStartIndex + len(b) - 1)) # last subblock.

        return subBlocksIdx
    except Exception as e:
        raise e


### Begin.
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
reStr = re.compile('<str:([A-Za-z0-9_-]+)>/')
reSegmentStr = re.compile('<str:([A-Za-z0-9_-]+)>')
reId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>/')
reSegmentId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>')
for url in urls:
    strMatch = reStr.sub('[A-Za-z0-9_-]+/', url)
    urlMatch = '/f5/' + reId.sub('[0-9]+/', strMatch)

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
                    adjustedLineUrl += s + '/'

                lines[idx] = adjustedLineUrl + ':'


# When the same url for 2 http methods is recorded in postman with 2 different parameters, it results 2 identical urls in swagger. Join them.
# Example:
#
#  /checkpoint/1/POLAND/tag/8f01bedd-facf-4aca-a89b-2c0e4c46f386/:
#     get:
#     ....
#  /checkpoint/1/POLAND/tag/1ec14820-3f61-4f4f-b3b1-32a3f8e841fe/:
#     patch:
#
# The result are 2 equal entries: /checkpoint/1/POLAND/tag/uid/
# The second url should be removed and the data should be merged in the first one.
# Find duplicated urls:
cleanedLines = lines.copy()
delta = 0 # when removing the duplicated url with the pop() function one position is subtracted.
skipAlreadyProcessed = list()
for idx in range(len(lines)):
    if idx in skipAlreadyProcessed:
        continue
    if re.match('\s+/f5/.*/:', lines[idx]): # get urls only from the inputFile.
        if lines.count(lines[idx]) > 1: # duplicated url.
            dupIndexList = list() # a list with the positions of a duplicated url.
            index = 0
            while len(dupIndexList) < lines.count(lines[idx]):
                index = lines.index(lines[idx], index+1)
                dupIndexList.append(index)

            skipAlreadyProcessed.extend(dupIndexList) # avoid to re-process.

            # For each index of the duplicated url, find the length of the block under the url, which ends at the next url.
            blocks = list() # list of dicts: (startBlockIndex, endBlockIndex).
            for startBlockIndex in dupIndexList:
                j = startBlockIndex + 1
                while not re.match('\s+/f5/.*/:', lines[j]):
                    j += 1
                blocks.append({"start": startBlockIndex, "end": j})

            # Starting from the second block, drop the url (at startBlockIndex) and put all the remaining lines under the previous block.
            for b in range(1, len(blocks)):
                blocks[b]["block"] = removeSubList(cleanedLines, blocks[b]["start"] - delta, blocks[b]["end"] - delta)
                blocks[b]["block"].pop(0) # remove url.
                delta += 1

                insertSubList(cleanedLines, blocks[0]["end"], blocks[b]["block"])




# Duplicated http method for the same url are forbidden. For each url extract the block and remove duplicate http verbs.
lines = cleanedLines
blocksIndexes = getBlocksIndexes(lines)

badSubBlocks = list()
for blockIdx in blocksIndexes:
    block = [ lines[l] for l in range(blockIdx[0], blockIdx[1]) ]
    subBlocksIndexes = getBlockHttpMethodsIndexes(block, blockIdx[0])

    httpMethods = [ lines[i[0]].strip() for i in subBlocksIndexes ] # the first line of a subblock is the http method.
    for m in httpMethods:
        if httpMethods.count(m) > 1: # duplicated http method.
            badSubIdx = list()
            #first = True # preserve the first occurrence.
            for i in subBlocksIndexes:
                if lines[i[0]].strip() == m:
                    badSubIdx.append(i)

            sortedBadSubIdx = sorted(badSubIdx, key=lambda tup: tup[0]) # sort in order to preserve the first occurrence.
            sortedBadSubIdx.pop(0)
            badSubBlocks.extend(sortedBadSubIdx)

#print(badSubBlocks)
dedupe = list(set(badSubBlocks)) # remove duplicates.
sortedBadSubBlocks = sorted(dedupe, key=lambda tup: tup[0], reverse=True)

# Remove bad subblocks lines in reverse order.
for badBlock in sortedBadSubBlocks:
    for index in reversed(range(badBlock[0], badBlock[1])):
        lines.pop(index)


with open(args.outputFile, 'w') as o:
    for line in lines:
        print(line, file = o)


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
        for i in range(startPos, endPos + 1):
            removedSubList.append(l.pop(startPos)) # the index shift, so the position is always the same.
        return removedSubList
    except Exception as e:
        raise e



# Insert a sublist at the index pos in the list l.
def insertSubList(l: list, pos: int, sublist: list) -> None:
    for i in range(len(sublist)):
        l.insert(pos + i, sublist[i])


# A "block" start with an url and end at the next url.
def getBlockEndIdx(l: list, startIdx: int):
    endIdx = startIdx

    try:
        for i in range(startIdx+1, len(l)):
            # start next block or end of last block.
            if re.match('\s+/f5/(.*/)?:', l[i]) or re.match('^[a-z]+:', l[i]):
                endIdx = i - 1
                break

        return endIdx
    except Exception as e:
        raise e



def getBlocksIndexes(l: list) -> (int, int):
    start = 0
    blocks = list()

    try:
        for i in range(len(l)):
            if re.match('\s+/f5/(.*/)?:', l[i]):  # line delimiting of a block or end last block.
                if not start:
                    start = i
                else:
                    blocks.append({
                        "idxs": (start, i-1),
                        "url": l[start]
                    })
                    start = i
            elif start and re.match('^[a-z]+:', l[i]): # end last block.
                blocks.append({
                    "idxs": (start, i-1),
                    "url": l[start]
                })
                break

        #b = list(set(blocks)) # sort
        return sorted(blocks, key=lambda d: d["idxs"][0])
    except Exception as e:
        raise e



def getSubBlocksIndexes(b: list, blockStartIndex: int) -> (int, int):
    httpMethods = ('get:', 'post:', 'put:', 'patch:', 'delete:')
    start = 0
    subBlocksIdx = list()

    try:
        for i in range(len(b)):
            if b[i].strip() in httpMethods:
                if not start:
                    start = i
                else:
                    subBlocksIdx.append({
                        "idxs": (blockStartIndex + start, blockStartIndex + i - 1),
                        "httpMethod": b[start].strip()
                    }) # end subblock.
                    start = i
        subBlocksIdx.append({
            "idxs": (blockStartIndex + start, blockStartIndex + len(b) - 1),
            "httpMethod": b[start].strip()
        }) # last subblock.

        return subBlocksIdx
    except Exception as e:
        raise e


### Begin.
with open(args.inputFile, "r") as txtFile:
    lines = [ line.rstrip() for line in txtFile ]

# Fix the file coming from postman2openapi, not always perfect. Bad lines example:
#  ...
#  ? /f5/source-asset/3/destination-asset/4/asm/source-policy/vdlgq-KAexbclPfzMgeLqQ/destination-policy/vdlgq-KAexbclPfzMgeLqQ/differences/
#  : get:
#  ...

u = re.compile('(\s*)\? (/.*/$)')
for idx in range(len(lines)):
    if re.match(u, lines[idx]):
        lines[idx] = u.sub('\\1\\2:', lines[idx])
        if re.match('\s+ : .*', lines[idx+1]):
            lines[idx+1] = lines[idx+1].replace(' : ', '   ')

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
# Also create a data structure to save the parameters info for each url.
urlsData = list()
reStr = re.compile('<str:([A-Za-z0-9_-]+)>/')
reSegmentStr = re.compile('<str:([A-Za-z0-9_-]+)>')
reId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>/')
reSegmentId = re.compile('<int:([A-Za-z0-9]*[Ii]d)>')
for url in urls:
    strMatch = reStr.sub('[A-Za-z0-9_-]+/', url)
    urlMatch = '/f5/' + reId.sub('[0-9]+/', strMatch)

    # Now we have the right regexp built from the urlFile to match an url in the inputFile.
    for idx in range(len(lines)):
        if re.match('\s+/f5/.*/:', lines[idx]): # get urls only from the inputFile.
            if re.match(urlMatch, lines[idx].strip().replace(':','')): # url line example in inputFile: /f5/<int:assetId>/Partition1/pool/POOL/:.
                urlData = dict()

                adjustedLineUrl = '  /' # 2 leading spaces.
                segments = url.split('/')
                if not segments[-1]:  # empty segment.
                    segments.pop(-1)
                segments.insert(0,'f5') # urls in the urlFile doesn't have the f5 prefix.

                for segment in segments:
                    if re.match(reSegmentId, segment):
                        paramName = reSegmentId.sub('\\1', segment )
                        urlData[paramName] = "integer"
                        s = "{" + paramName + "}"
                    elif re.match(reSegmentStr, segment):
                        paramName = reSegmentStr.sub('\\1', segment )
                        urlData[paramName] = "string"
                        s = "{" + paramName + "}"
                    else:
                        s = segment
                    adjustedLineUrl += s + '/'

                lines[idx] = adjustedLineUrl + ':'
                urlData["url"] = lines[idx]
                urlsData.append(urlData)

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
blocksIndexes = getBlocksIndexes(lines)

goodUrls = list()
badBlocks = list()
for blockUrl in blocksIndexes:
    if blockUrl["url"] not in [ url["url"] for url in goodUrls]: # the first occurrence of an url is good, the others are bad.
        goodUrls.append(blockUrl)
    else: # Example:
        # {
        #    "idxs": (10, 20) # (startIdx, endIdx)
        #    "block": ["line10", "line11", ...] # [lines]
        # }
        badB = {
            "idxs": blockUrl["idxs"],
            "block": []
        }
        for r in range(blockUrl["idxs"][0], blockUrl["idxs"][1]+1):
            badB["block"].append(lines[r])
        if not badB in badBlocks:
            badBlocks.append(badB)

# now remove the lines[] list all the blocks listed in badBlocks in reverse order.
reverseSortedBadBlocks = sorted(badBlocks, key=lambda d: d["idxs"][0], reverse=True)
for block in reverseSortedBadBlocks:
    removeSubList(lines, block["idxs"][0], block["idxs"][1])

blocksIndexes = getBlocksIndexes(lines) # the remove operation have shifted the indexes of the lines[] list.
# for each removed block strip the url, find the url in lines[] and append all others row at the good block.
for badBlock in reverseSortedBadBlocks:
    for goodBlock in blocksIndexes:
        if badBlock["block"][0].strip() == goodBlock["url"]: # the first line of a block is the url.
            insertSubList(lines, goodBlock["idxs"][1]+1, badBlock["block"][1:])
            goodBlock["idxs"] = (goodBlock["idxs"][0], goodBlock["idxs"][1] + len(badBlock["block"] -1)) # needed for > 1 inserts in the same block.


# Duplicated http method for the same url are forbidden. For each url extract the block and remove duplicate http verbs.
blocksIndexes = getBlocksIndexes(lines)
badSubBlocks = list()
for blockIdx in blocksIndexes:
    block = [ lines[l] for l in range(blockIdx["idxs"][0], blockIdx["idxs"][1]+1) ]
    # A subblock start with the http method and end at the next method. Example line:
    #    get:
    subBlocksIndexes = getSubBlocksIndexes(block, blockIdx["idxs"][0])
    """
    [
        {
            "idxs": (492, 497), 
            "httpMethod": "get:"
        }, 
        {   "idxs": (498, 530), 
            "httpMethod": "delete:"
        }
    ]
    """

    goodSubBlocks = []
    for i in subBlocksIndexes:
        if i["httpMethod"] not in [m["httpMethod"] for m in goodSubBlocks]:
            goodSubBlocks.append(i)
        else:
            badSubBlocks.append(i)

#dedupe = list(set(badSubBlocks)) # remove duplicates.
sortedBadSubBlocks = sorted(badSubBlocks, key=lambda d: d["idxs"][0], reverse=True)

# Remove bad subblocks lines in reverse order.
for badSubBlock in sortedBadSubBlocks:
    removeSubList(lines, badSubBlock["idxs"][0], badSubBlock["idxs"][1])

# Now add the parameters info for each url, previously saved in urlsData.
# First remove the duplicated, due to the (already removed) duplicated urls.
dedupe = []
for urlData in urlsData:
    if urlData["url"] not in [ uData["url"] for uData in dedupe ]:
        dedupe.append(urlData)
urlsData = dedupe

for urlData in urlsData:
    urlInfoBlock = list()
    for param in urlData.keys():
        if param != 'url':
            urlInfoBlock.extend([
                "      - name: " + param,
                "        in: path",
                "        required: true",
                "        schema:",
                "          type: " + urlData[param],
                "        description: " + param
            ])

    blockIdxs = dict()
    for idx in range(len(lines)):
        if lines[idx] == urlData["url"]:
            blockIdxs["start"] = idx
            blockIdxs["end"] = getBlockEndIdx(lines, idx)

    if blockIdxs:
        for i in range( blockIdxs["start"], blockIdxs["end"]):
            if re.match('\s+parameters:', lines[i]): # append the url parameters info under the "parameters:" line if it exists.
                # Verify that the "parameters:" have 6 leading spaces, otherwise the strings in urlInfoBlock must be adjusted.
                if lines[i].rstrip().count(' ') == 6:
                    insertSubList(lines, i+1, urlInfoBlock)
                    break


with open(args.outputFile, 'w') as o:
    for line in lines:
        print(line, file = o)


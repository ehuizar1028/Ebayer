from ebaysdk.finding import Connection
from ebaysdk.shopping import Connection as shop
import datetime
from pytz import timezone
import SQLiter
import sys

cats = {}
rightNow= datetime.datetime.now()
searchTime = datetime.datetime.now(timezone('GMT')) - datetime.timedelta(hours=1)
searchTime = searchTime.strftime("%Y-%m-%dT%H:%M:%S.000Z")
s = SQLiter.sqliter()

def getCatIds():
    api = shop(appid='', config_file=None)
    api.execute('GetCategoryInfo', {'CategoryID':'-1', "IncludeSelector":"ChildCategories"})

    CatIDs = api.response_dict().CategoryArray.Category
    ids = []
    for i in CatIDs[1:]:
        ids.append(i.CategoryID)
        cats.update({i.CategoryID:i.CategoryName})
    return ids

def getSampleData(id):
    try:
        api = Connection(appid='', config_file=None)
        response = api.execute('findCompletedItems', {
            "categoryId": "{}".format(id),
            "paginationInput": [
                {
                    "pageNumber": "1"
                }
            ],
            "itemFilter": [
                {
                    "name": "SoldItemsOnly",
                    "value": True
                },
                {
                    "name": "EndTimeFrom",
                    "value": searchTime
                }
            ]
        }
                               )
        return response.reply.searchResult.item
    except:
        pass

def insertData(itemID, Title, URL, PrimaryCat, Start, End, id):
    s.setupConnection()
    sqlCmd = 'INSERT INTO EbayItems (ItemID, Title, URL, RootCategory, PrimaryCategory, StartTime, EndTime) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(itemID, Title, URL, cats[id], PrimaryCat, Start, End)
    s.insert(sqlCmd)

def insertKeywordData(itemTitle, id):
    keywords=[]
    badKeywords = ["#", "|", "no", "vs.", "-", "the", "a", "new", "(", ")", "of", "&", "and", "old", "by", "with",
                   "plus", "for", "size", "to", "vs", "versus", "tested", "in", "/", "~", ":", "w/", "+", ",", "on"]


    keys = itemTitle.split()
    for k in keys:
        if k.lower() in badKeywords:
            pass
        else:
            k = k.replace("(", "")
            k = k.replace(")", "")
            k = k.replace(",", "")
            keywords.append(k.lower())

    for k in keywords:
        #try:
            sqlCmd = """INSERT INTO keywords (keyword, category, timestamp) VALUES ("{}", "{}", "{}");""".format(k,cats[id], rightNow)
            s.insert(sqlCmd)
        # except:
        #     e = sys.exc_info()[0]
        #     print e

def main():
    ids = getCatIds()
    for id in ids:
        try:
            sample = getSampleData(id)
            for data in sample:
                insertData(data.itemId, data.title, data.viewItemURL, data.primaryCategory.categoryName, data.listingInfo.startTime, data.listingInfo.endTime, id)
                insertKeywordData(data.title, id)
        except:
            e = sys.exc_info()[0]
            print e


main()
s.close()


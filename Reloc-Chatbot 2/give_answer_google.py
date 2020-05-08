import wolframalpha
import google

def google_search(question):
    first_page = google.search(question,1)
    print('ques: ', question)
    print('page',len(first_page))
    top_three_result = []
    i = 0
    while i<1:
        top_three_result.append(first_page[i].description)
        i+=1

    first_search = ''.join(top_three_result).encode('ascii','replace')

    print('first answer: ',first_search.decode("utf-8")[0:299])
    return first_search.decode("utf-8")[0:299]

def answer_question(question):
    try:
        app_id = "4JTE25-H9HA6YWLEQ"    # add your app id into this
        if not app_id:
            print('Please add your app id')
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        ans = str(next(res.results).text).replace('.', '.\n')
        print('Secondary DB ans: ',ans)

        if ans == 'None' or ans == '(data not available)' or ans == '(information not available)':
            print('none-google')
            ans = google_search(question)
            print('google answer: ', ans)

        return ans

    except:
        try:
            print('except-google')
            ans = google_search(question)
            print('google answ: ', ans)
            return ans
        except:
            return str('Ok, here is a link to search more: <a href=\'https://www.google.com\'>www.google.com</a>')

import os
import jinja2
import input
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

today = date.today()
yesterday = today - timedelta(days = 1)
today = str(today)
yesterday = str(yesterday)
friends = input.friendsList


def getDate(tame):
    cnv = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    cnt = 0
    mnth, year, day = '', '', ''
    for c in tame:
        if cnt==3:
            break
        if c=='/' or c==' ':
            cnt += 1
            continue
        if cnt==0:
            mnth += c
        if cnt==1:
            day += c
        if cnt==2:
            year += c
    mnth = cnv[mnth]
    return (year+'-'+mnth+'-'+day)


def getProblems(handle):

    pages = driver.find_elements(By.CLASS_NAME, 'page-index')

    total_pages = 1
    for page in pages:
        total_pages = int(page.text)
    
    submissionLink, submissionId = [], []
    problemLink, problemId = [], []
    URL = "https://codeforces.com/submissions/" + handle + "/page/"
    for num in range(total_pages+1):
        end_of_loop = 0
        new_url = URL + str(num)
        driver.get(new_url)
        sleep(1)
        lst1 = driver.find_elements(By.CLASS_NAME, 'status-small')
        lst2 = driver.find_elements(By.CLASS_NAME, 'id-cell')
        
        itr, cls = 0, 0
        temp = []
        plink = ''
        for elem in lst1:
            if cls==0:
                dt = getDate(elem.text)
                if dt==today or dt==yesterday:
                    temp.append(dt)
                else:
                    end_of_loop = 1
                    break
            elif cls==1:
                ele = driver.find_elements(By.PARTIAL_LINK_TEXT, elem.text)
                plink = ele[0].get_attribute('href')
                temp.append(elem.text)    
            elif cls==2:
                temp.append(elem.text)
                if elem.text=='Accepted' and temp[0]==yesterday:
                    problemLink.append(plink)
                    submissionId.append(str(lst2[itr].text))
                    problemId.append(temp[1])
            cls += 1
            if cls==3:
                temp.clear()
                itr += 1
                cls = 0
        for ids in submissionId:
            driver.get(new_url)
            solution = driver.find_elements(By.PARTIAL_LINK_TEXT, ids)
            solution[0].click()
            driver.implicitly_wait(10)  
            directLink = driver.find_elements(By.XPATH, '//*[@id="facebox"]/div/div/div/span/a')
            directLink = directLink[0].get_attribute('href')
            submissionLink.append(directLink)
        if end_of_loop==1:
            break
    return submissionId, submissionLink, problemId, problemLink


finalList = [[]]
finalList.clear()

for friend in friends:
    profile = "https://codeforces.com/profile/" + friend
    driver.get(profile)
    sleep(1)

    submission = driver.find_elements(By.PARTIAL_LINK_TEXT, 'SUBMISSIONS')
    submission[0].click()
    sleep(1)
    submissionId, submissionLink, problemId, problemLink = getProblems(friend)
    for [elem1, elem2, elem3, elem4] in zip(submissionId, submissionLink, problemId, problemLink):
        finalList.append([friend, profile, elem1, elem2, elem3, elem4])


driver.quit()

jinja_var = {
    'items': finalList
}

template_string = '''
<html>
    <head></head>
    <body>
        <table style="width: 100%; border: 1px solid #dddddd; border-collapse: collapse; border-spacing: 0;">
            <tr>
                <th style="border: 1px solid #dddddd; padding: 5px; text-align: center;">Handle</th>
                <th style="border: 1px solid #dddddd; padding: 5px; text-align: center;">Submission</th>
                <th style="border: 1px solid #dddddd; padding: 5px; text-align: center;">Problem</th>
            </tr>
        {% for item in items %}
        <tr>
            <td style="border: 1px solid #dddddd; padding: 5px; text-align: center;" class="c1"><a href="{{ item[1] }}">{{ item[0] }}</a></td>
            <td style="border: 1px solid #dddddd; padding: 5px; text-align: center;" class="c2"><a href="{{ item[3] }}">{{ item[2] }}</a></td>
            <td style="border: 1px solid #dddddd; padding: 5px; text-align: center;" class="c3"><a href="{{ item[5] }}">{{ item[4] }}</a></td>
        </tr>
        {% endfor %}
        </table>
    </body>
</html>
'''

template = jinja2.Template(template_string)

html = template.render(jinja_var)

me = input.myEmail
you = input.yoursEmail


message = Mail(
    from_email = input.myEmail,
    to_emails = input.yoursEmail,
    subject = "Spies Report for " + str(yesterday),
    html_content = html)


sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

response = sg.send(message)
from flask import Flask, render_template, redirect, url_for, request
import requests
from bs4 import BeautifulSoup as bs
from repl_db import *

# Configuration files
app = Flask(__name__)
app.config["DEBUG"] = True

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Leetcode topics selector
@app.route('/leetcode')
def leetcode_topics_list():
    try:
        leetcode_topics = 'https://raw.githubusercontent.com/surdebmalya/data-structure-implementation/main/leetcode/README.md'
        response = requests.get(leetcode_topics)
        data = response.text
        topic_names = data.split("\n")
        topic_names.sort()
        proper_names = {}
        for topic_name in topic_names:
            curr_topic_name = topic_name
            curr_topic_name = curr_topic_name.capitalize()
            proper_names[topic_name] = curr_topic_name
        return render_template(
            'leetcode-topic-or-questions-queue.html', 
            topic_or_question='topics',
            proper_names=proper_names,
            topic_names=topic_names)
    except:
        return redirect(url_for('error'))

# leetcode questions selector under a specific topic
@app.route('/leetcode/<topic_name>')
def leetcode_topic(topic_name):
    try:
        topic_question_lists = 'https://raw.githubusercontent.com/surdebmalya/data-structure-implementation/main/leetcode/' + topic_name + '/README.md'
        response = requests.get(topic_question_lists)
        data = response.text
        topic_question_names = data.split("\n")
        topic_question_names.sort()
        proper_topic_question_names = {}
        for each_question in topic_question_names:
            curr_question_name = each_question
            curr_question_name = curr_question_name.replace("-", " ")
            curr_question_name = curr_question_name.capitalize()
            proper_topic_question_names[each_question] = curr_question_name
        return render_template(
            'leetcode-topic-or-questions-queue.html', 
            topic_or_question='questions',
            topic_name=topic_name,
            proper_topic_question_names=proper_topic_question_names,
            topic_question_names=topic_question_names)
    except:
        return redirect(url_for('error'))

# leetcode specific question selector along with solution
@app.route('/leetcode/<topic_name>/<question_name>')
def leetcode_question(topic_name, question_name):
    try:
        solution_code_github_link = 'https://raw.githubusercontent.com/surdebmalya/data-structure-implementation/main/leetcode/' + topic_name + '/' + question_name + '.cpp'

        data = {
            "operationName":"questionData",
            "variables":
            {
                "titleSlug": question_name
            },
            "query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"
            }

        r = requests.post('https://leetcode.com/graphql', json = data).json()
        soup = bs(r['data']['question']['content'], features="html.parser")
        question_id = r['data']['question']['questionId']
        question_title = r['data']['question']['title']
        question_level = r['data']['question']['difficulty']
        question =  soup.get_text()
        question_subpath = r['data']['question']['titleSlug']
        question_link = "https://leetcode.com/problems/" + question_subpath

        return render_template(
            'leetcode.html', 
            question_id=question_id,
            question_title=question_title,
            question_level=question_level,
            question_link=question_link, 
            question=question,
            solution_code_github_link=solution_code_github_link)
    except:
        return redirect(url_for('error'))

# Video courses rendering
@app.route('/videos')
def videos():
    return render_template('video-content.html')

# Subscription backend
@app.route('/subscribe', methods=["POST", "GET"])
def subscribe():
    if request.method == 'POST':
        email = request.form['email'].replace(' ', '')
        response = create_account(email)
        if response == 200 or 409:
            return render_template('thanks.html')
        else:
            return render_template('error.html')
    else:
        return redirect(url_for('index'))

# Error page rendering
@app.route('/error')
def error():
    return render_template('error.html')

# Thank you page
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Driver code starts from here
if __name__ == '__main__':
    print_db()
    app.run(host='0.0.0.0', port=5000)
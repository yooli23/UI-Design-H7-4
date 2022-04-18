from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)
# the question images' width : height = 3 : 2 if only one needed
# if two images needed, both of them are 3 : 4
# each answer may need a image, if so, it's 3 : 2, named 'answer_imgs'
# if not, there will be another key called 'answer_texts'
test_data = [
    {
        'question_text': 'If the face within red box is the bottom, ' +
                         'which one correctly indicates the top face?',
        'question_imgs': ['test-images/test1.jpg'],
        'answer_imgs': ['test-images/test1_a.jpg',
                        'test-images/test1_b.jpg',
                        'test-images/test1_c.jpg']
    },
    {
        'question_text': 'Select all correct nets of cube from below:',
        'question_imgs': ['test-images/test2.jpg'],
        'answer_texts': ['1', '2', '3', '4', '5', '6', '7', '8']
    },
    {
        'question_text': 'Which is a possible net of this cube? \nRemark: grey means unkown.',
        'question_imgs': ['test-images/test3.jpg'],
        'answer_imgs': ['test-images/test3_a.jpg',
                        'test-images/test3_b.jpg',
                        'test-images/test3_c.jpg']
    },
    {
        'question_text': 'Given following two nets representing the same cube. \n' + 
        'Which face in the second net should be blue?',
        'question_imgs': ['test-images/test4.jpg'],
        'answer_texts': ['1', '2', '5', '6']
    }
]
# store data for learning exercises
learn_data = {
    1: {"name": "Net 1", "id": 1, "net_image": "learn-images/net1.jpg",
        "transform_gif": "learn-images/net1-transform.gif"},
    2: {"name": "Net 2", "id": 2, "net_image": "learn-images/net2.jpg",
        "transform_gif": "learn-images/net2-transform.gif"},
    3: {"name": "Net 3", "id": 3, "net_image": "learn-images/net3.jpg",
        "transform_gif": "learn-images/net3-transform.gif"},
    4: {"name": "Net 4", "id": 4, "net_image": "learn-images/net4.jpg",
        "transform_gif": "learn-images/net4-transform.gif"},
    5: {"name": "Net 5", "id": 5, "net_image": "learn-images/net5.jpg",
        "transform_gif": "learn-images/net5-transform.gif"},
    6: {"name": "Net 6", "id": 6, "net_image": "learn-images/net6.jpg",
        "transform_gif": "learn-images/net6-transform.gif"},
    7: {"name": "Net 7", "id": 7, "net_image": "learn-images/net7.jpg",
        "transform_gif": "learn-images/net7-transform.gif"}
}
# store data for visited pages
visited = dict()

# 'test_answers' will give the index or list of index of the correct answer(s).
# remark: 0-indexed, increasingly sorted for each answer
test_answers = [[2], [0, 3, 5, 6, 7], [0], [0]]
test_scores = 0

# ROUTES
@app.route('/')
def home():
    global test_scores
    test_scores = 0  # prevent jumping from test to other pages
    return render_template('home.html')

@app.route('/learn')
def learn():
    global visited
    return render_template('learn.html', visited=visited)

@app.route('/learn/<idx>')
def learn_idx(idx):
    global test_scores
    global visited  # track learning pages visited
    global learn_data
    visited[int(idx)] = 1
    test_scores = 0  # prevent jumping from test to other pages
    return render_template('learn-view.html', data=learn_data[int(idx)])

@app.route('/test')
def test():
    global visited
    return render_template('test.html')

@app.route('/test/<idx>')
def test_idx(idx):
    global test_data
    global test_scores
    test = None
    if (int(idx) < len(test_data)) and (int(idx) > 0):
        test = test_data[int(idx)]
    else:
        test_scores = 0  # start from 0 scores
        test = test_data[0]
    if len(test_data)-1 == int(idx):
        test["last"] = True
    else:
        test["last"] = False
    test["id"] = int(idx)
    return render_template('test-view.html', data=test)

@app.route('/test_finish')
def test_finish():
    global test_scores
    return render_template('test_finish.html', score=test_scores)


# possible ajex function
@app.route('/submit_answer', methods=['GET', 'POST'])
def submit_answer():
    global test_answers
    global test_scores
    json_data = request.get_json()
    # expected data structure:
    # index: int, which test it is, 0-indexed, come from /text/<index>
    # answers: list of int, telling the selection(s) of user
    test_idx = json_data['index']
    user_answers = json_data['answers']
    user_answers.sort()
    correct = 0 # default not correct
    if user_answers == test_answers[test_idx]:
        correct = 1
        test_scores += 1

    return jsonify(correct=correct, correct_answer=test_answers[test_idx])


if __name__ == '__main__':
    app.run(debug=True)

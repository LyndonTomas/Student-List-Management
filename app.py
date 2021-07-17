from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response

import sys
import os

app = Flask(__name__)
app.debug = True
# page
#index 
@app.route('/')
def index():
    record = make_response(render_template('index.html'))
    return record, url_for('index')

# page
#showStudents - done
@app.route('/showStudents')
def showStudents():
    record = make_response(render_template('showStudents.html'))
    return record, url_for('showStudents')

# page
# done
@app.route('/addStudent')
def renderInputAddStudent():
    record = make_response(render_template('addStudent.html'))
    return record, url_for('renderInputAddStudent')

# page
# done
@app.route('/removeStudent')
def renderInputDeleteStudent():
    record = make_response(render_template('deleteStudent.html'))
    return record, url_for('renderInputDeleteStudent')

# done
# page
@app.route('/findStudent')
def findStudent():
    record = make_response(render_template('findStudent.html'))
    return record, url_for('findStudent')

# done
# function
@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == "POST":
        if (os.path.isfile('./studentList.txt')==False):
            headings= ("EMPTY TABLE")
            data = ()
            return render_template("findStudent.html", headings=headings, data=data)
        else:
            # convert list into tuples
            headings= ("Student Name", "Student ID No.")
            data = ()
            listFile = open("studentList.txt", "r")
            content = listFile.readlines()
            inputNumber = request.form['studentIDNumber']
            names = content[0].replace("[", "").replace("]", "").replace("'", '').replace("\n", "").replace(" ", "")
            numbers = content[1].replace("[", "").replace("]", "").replace("'", '').replace(" ", "")
            names = names.split(",")
            numbers = numbers.split(",")
            # By this point, the data are now in a list form
            tuplerow = ()
            for x in range(len(names)):
                if inputNumber == numbers[x]:
                    newTupleData = (names[x], numbers[x])
                    tuplerow += (newTupleData,)
        data = tuplerow
        return render_template("findStudent.html", headings=headings, data=data)


# function
# done
@app.route('/show')
def show():
    if (os.path.isfile('./studentList.txt')==False):
        headings= ("Student Name", "Student ID No.")
        data = ()
        return render_template("showStudents.html", headings=headings, data=data)
    else:
        # convert list into tuples
        headings= ("Student Name", "Student ID No.")
        data = ()
        filesize = os.path.getsize("studentList.txt")
        if filesize == 0:
            data = ""
            return render_template("showStudents.html", headings=headings, data=data)
        else:
            listFile = open("studentList.txt", "r")
            content = listFile.readlines()
            names = content[0].replace("[", "").replace("]", "").replace("'", '').replace("\n", "").replace(" ", "")
            numbers = content[1].replace("[", "").replace("]", "").replace("'", '').replace(" ", "")
            names = names.split(",")
            numbers = numbers.split(",")
            # By this point, the data are now in a list form
            tuplerow = ()
            for x in range(len(names)):
                newTupleData = (names[x], numbers[x])
                tuplerow += (newTupleData,)
            data = tuplerow
            return render_template("showStudents.html", headings=headings, data=data)
    

# function
# AddStudent - done
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        # to check if file exists
        if (os.path.isfile('studentList.txt')==False):
            listFile = open('studentList.txt', 'w')
            listFile.close()
            if (os.path.getsize("studentList.txt")) == 0:
                names = []
                studentNumbers = []
                names.append(request.form['studentName'])
                studentNumbers.append(request.form['studentIDNumber'])
                names = str(names)
                studentNumbers = str(studentNumbers)
                listFile = open('studentList.txt', 'w')
                listFile.write(names)
                listFile.write("\n")
                listFile.write(studentNumbers)
                listFile.close() 
        else:
            # To check if the list is has content
            names = []
            studentNumbers = []
            names.append(request.form['studentName'])
            studentNumbers.append(request.form['studentIDNumber'])
            # Getting old file
            listFile = open('studentList.txt', 'r')
            content = listFile.readlines()
            # Formatting
            oldNames = content[0].replace("[", '').replace("]", '').replace("'", '').replace("\n", "").replace(" ", "")
            oldNumbers = content[1].replace("[", '').replace("]", '').replace("'", '').replace(" ", "")
            # String to list
            oldNames = oldNames.split(",")
            oldNumbers = oldNumbers.split(",")
            listFile.close()
            # combining new to old inputs
            oldNumbers.extend(studentNumbers)
            oldNames.extend(names)
            # saving all inputs to the new file
            listFile = open('studentList.txt', 'w+')
            oldNames = str(oldNames)
            oldNumbers = str(oldNumbers)
            listFile.write(oldNames)
            listFile.write("\n")
            listFile.write(oldNumbers)
            listFile.close()
        # returining to index page
    return redirect(url_for('index'))

# function
# done
@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == "POST":
        number = request.form['studentIDNumber']
        # getting contents of the file
        listFile = open('studentList.txt', 'r')
        content = listFile.readlines()
        oldNames = content[0].replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace(" ", "")
        oldNumbers = content[1].replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        # String to list
        oldNames = oldNames.split(",")
        oldNumbers = oldNumbers.split(",")
        listFile.close()
        # looking for the student thru a number
        if (number in oldNumbers):
            for x in range(len(oldNumbers)):
                if number == oldNumbers[x]:
                    oldNumbers.pop(x)
                    oldNames.pop(x)
                    listFile = open('studentList.txt', 'w+')
                    oldNames = str(oldNames)
                    oldNumbers = str(oldNumbers)
                    listFile.write(oldNames)
                    listFile.write("\n")
                    listFile.write(oldNumbers)
                    listFile.close()
                    return redirect(url_for('index'))
        else:
            return "<h3>NO STUDENT MATCH</h3>"

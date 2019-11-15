
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session, url_for
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://sgt2118:2876@35.243.220.243/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.


engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM circuit")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/school')
def school():
  cursor = g.conn.execute("SELECT name, state FROM school")
  names = []
  for result in cursor:
    names.append(result[0] + " " + result[1])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("school.html", **context)

@app.route('/student')
def student():
  cursor = g.conn.execute("SELECT name FROM students")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("student.html", **context)


@app.route('/viewstudent')
def viewstudent():
  cursor = g.conn.execute("SELECT name FROM students")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("viewstudent.html", **context)

@app.route('/team')
def team():
  cursor = g.conn.execute("SELECT team_name FROM team")
  names = []
  for result in cursor:
    names.append(result['team_name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("team.html", **context)

@app.route('/viewteam')
def viewteam():
  cursor = g.conn.execute("SELECT team_name, cid FROM team")
  names = []
  for result in cursor:
    names.append(result['team_name'] + "," + str(result['cid']))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("viewteam.html", **context)

@app.route('/insertParticipants')
def insertParticipants():
  cursor = g.conn.execute("SELECT name, sid FROM students")
  names = []
  for result in cursor:
    names.append(result['name'] + "," + str(result['sid'])) # can also be accessed using result[0]
  cursor.close() 
  context = dict(data = names)
  return render_template("insertParticipants.html", **context)

@app.route('/registerStudentIntoTeam')
def registerStudentIntoTeam():
    string = request.args.get('query')
    data = string.split(",")
    school_name, school_state = None, None
    cursor2 = g.conn.execute("SELECT DFEI.school_state, DFEI.school_name FROM Students, DebatesFor_EnrollsIn DFEI WHERE DFEI.sid = Students.sid AND Students.sid = %s", data[1])
    for result in cursor2:
        school_name = "'"+ result['school_name'] + "'"
        school_state = "'" +result['school_state'] + "'"
    sql = "INSERT INTO DebatesFor_EnrollsIn(cid, team_name, sid, school_state, school_name) VALUES(%s, %s, " + data[1] + ", " + school_state + ", " + school_name +")"
    session['my_var'] = sql
    session['cid'] = data[1]
    cursor = g.conn.execute("SELECT team_name, cid FROM team")
    names = []
    for result in cursor:
      names.append(result['team_name'] + "," + str(result['cid']))  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    print(session['my_var'], session['cid'])
    return render_template("registerTeam.html", **context)

@app.route('/registerIntoTeam')
def registerIntoTeam():
  data = session.get('my_var', None)
  print("OVER HERE")
  print(data)
  string = request.args.get('query')
  print("HEREEEE")
  print(string)

  query = string.split(",")
  cid = query[1]
  team_name = query[0] 
  g.conn.execute(data, cid, team_name)
  cursor = g.conn.execute("SELECT team_name, cid FROM team")
  names = []
  for result in cursor:
    names.append(result['team_name'] + "," + str(result['cid']))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("viewteam.html", **context)

@app.route('/insertStudents', methods=['POST'])
def insertStudents():
  name = request.form['name']
  sid = request.form['sid']
  gender = request.form['gender']
  g.conn.execute("INSERT INTO Students (sid, name, gender) VALUES (%s, %s, %s);", sid, name, gender)
  cursor = g.conn.execute("SELECT name FROM students")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close() 
  context = dict(data = names)
  return render_template("insertParticipants.html", **context)

@app.route('/insertTeam', methods=['POST'])
def insertTeam():
    team_name = request.form['name']
    cid = session.get('cid', None)
    g.conn.execute("INSERT INTO Team(team_name, cid) VALUES(%s, %s)", team_name, cid)
    cursor = g.conn.execute("SELECT team_name, cid FROM team")
    names = []
    for result in cursor:
      names.append(result['team_name'] + "," + str(result['cid']))  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("registerTeam.html", **context)

@app.route('/insertJudges')
def insertJudges():
  cursor = g.conn.execute("SELECT name FROM judge")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close() 
  context = dict(data = names)
  return render_template("insertJudges.html", **context)

@app.route('/insertJudging', methods=['POST'])
def insertJudging():
  name = request.form['name']
  sid = request.form['sid']
  gender = request.form['gender']
  g.conn.execute("INSERT INTO Judge(j_id, name, gender) VALUES (%s, %s, %s);", sid, name, gender)
  cursor = g.conn.execute("SELECT name FROM judge")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close() 
  context = dict(data = names)
  return render_template("insertJudges.html", **context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

@app.route('/schoolByWins', methods=['POST'])
def schoolByWins():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  cursor = g.conn.execute("SELECT AR.school_name, AR.school_state, ROUND(AVG(AR.won::INT),3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.school_name, AR.school_state ORDER BY AVG(AR.won::INT) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('school.html', **context)

@app.route('/schoolByPoints', methods=['POST'])
def schoolByPoints():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  print(circuit_name, circuit_region)
  cursor = g.conn.execute("SELECT AR.school_name, AR.school_state, ROUND(AVG(AR.speaker_points)::numeric,3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.school_name, AR.school_state ORDER BY AVG(AR.speaker_points) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('school.html', **context)

#students

@app.route('/studentByWins', methods=['POST'])
def studentByWins():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  cursor = g.conn.execute("SELECT AR.sid, AR.student_name, ROUND(AVG(AR.won::INT),3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.sid, AR.student_name ORDER BY AVG(AR.won::INT) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('student.html', **context)

@app.route('/studentByPoints', methods=['POST'])
def studentByPoints():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  cursor = g.conn.execute("SELECT AR.sid, AR.student_name, ROUND(AVG(AR.speaker_points)::numeric,3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.sid, AR.student_name ORDER BY AVG(AR.speaker_points) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('student.html', **context)

#teams

@app.route('/teamByWins', methods=['POST'])
def teamByWins():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  cursor = g.conn.execute("SELECT AR.cid, AR.team_name, ROUND(AVG(AR.won::INT),3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.cid, AR.team_name ORDER BY AVG(AR.won::INT) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('team.html', **context)

@app.route('/teamByPoints', methods=['POST'])
def teamByPoints():
  circuit_region = request.form['circuit_region']
  circuit_name = request.form['circuit_name']
  cursor = g.conn.execute("SELECT AR.cid, AR.team_name, ROUND(AVG(AR.speaker_points)::numeric,3) FROM Aggregate_Rounds AR WHERE AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.cid, AR.team_name ORDER BY AVG(AR.speaker_points) DESC;", circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('team.html', **context)

#RECORDS
#student


@app.route('/findStudentID', methods=['POST'])
def findStudentID():
  student_name = '%' + request.form['student_name'] + '%'
  cursor = g.conn.execute("SELECT DISTINCT AR.student_name, AR.school_name, AR.sid, AR.circuit_name, AR.region FROM Aggregate_Rounds AR WHERE AR.student_name LIKE %s", student_name)  
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2], result[3], result[4]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('student2.html', **context)


@app.route('/studentID', methods=['GET', 'POST'])
def studentID():
  string = request.args.get('query')
  def parse_string(string):
    split_list = string[1:-1].split(",")
    for i, element in enumerate(split_list):
       split_list[i] = element.lstrip().replace("'","")
    return split_list  
  data = parse_string(string)
  print(data)
  print(data[2], data[3], data[4])
  student_id = data[2]
  circuit_name = data[3]
  circuit_region = data[4]
  cursor = g.conn.execute("WITH Student_Rank As(SELECT AR.sid, AR.student_name, ROUND(AVG(AR.speaker_points)::numeric, 3) AVG FROM Aggregate_rounds AR GROUP BY AR.sid, AR.student_name ORDER BY AVG(AR.speaker_points) DESC) select count(*) + 1 from Student_Rank WHERE Student_Rank.AVG > (select Student_Rank.AVG from Student_Rank WHERE Student_Rank.sid = %s);",student_id)
  cursor2 = g.conn.execute("WITH Student_Rank As(SELECT AR.sid, AR.student_name, ROUND(AVG(AR.speaker_points)::numeric, 3) AVG FROM Aggregate_rounds AR WHERE  AR.circuit_name LIKE %s AND AR.region LIKE %s GROUP BY AR.sid, AR.student_name ORDER BY AVG(AR.speaker_points) DESC) select count(*) + 1 from Student_Rank WHERE Student_Rank.AVG > (select Student_Rank.AVG from Student_Rank WHERE Student_Rank.sid = %s);",circuit_name, circuit_region, student_id) 
  names = []
  names.append("Rankings for :" + data[0])
  for result in cursor:
      names.append("OVERALL RANK: " + str(result[0])) 
  cursor.close()
  for result in cursor2:
      names.append("CIRCUIT RANK: " + str(result[0]))
  cursor2.close()
  context = dict(data = names)
  return render_template('student.html', **context)


@app.route('/teamInRounds', methods=['GET','POST'])
def teamInRounds():
  string = request.args.get('query')
  def parse_string(string):
    split_list = string[1:-1].split(",")
    for i, element in enumerate(split_list):
       split_list[i] = element.lstrip().replace("'","")
    return split_list  
  data = parse_string(string)
  print(data)
  print(data[2], data[3], data[4])
  student_id = data[2]
  circuit_name = data[3]
  circuit_region = data[4]
  cursor = None
  cursor = g.conn.execute("SELECT PIRW.team_name, PIRW.speaker_points, PIRW.won, PIRW.t_name, PIRW.number FROM ParticipatesIn_RegisteredWith as PIRW WHERE PIRW.cid = %s AND PIRW.circuit_name = %s AND PIRW.region = %s", student_id, circuit_name, circuit_region)
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2], result[3], result[4]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('team.html', **context)


@app.route('/findStudentIDTeams', methods=['POST'])
def findStudentIDTeams():
  student_name = '%' + request.form['student_name'] + '%'
  cursor = g.conn.execute("SELECT DISTINCT AR.student_name, AR.school_name, AR.sid, AR.circuit_name, AR.region FROM Aggregate_Rounds AR WHERE AR.student_name LIKE %s", student_name)  
  names = []
  for result in cursor:
      names.append((result[0], result[1], result[2], result[3], result[4]))  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template('team2.html', **context)


@app.route('/viewStudentsInTeam', methods=['GET', 'POST'])
def viewStudentsInTeam():
    data = request.args.get('query')
    string = data.split(",")
    print(string)
    cursor = g.conn.execute("SELECT Students.name, Students.sid FROM Students, DebatesFor_EnrollsIn DFEI WHERE DFEI.cid = %s AND DFEI.team_name = %s AND DFEI.sid = Students.sid", string[1], string[0])
    names = []
    names.append("All of the students in team " + string[0])
    for result in cursor:
        names.append(result[0])
    print(names)
    cursor.close()
    context = dict(data = names)
    return render_template('viewstudent.html', **context)
#School

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()

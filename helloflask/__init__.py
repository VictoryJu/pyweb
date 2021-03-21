from flask import Flask, g, request, Response, make_response, session
from flask import render_template, Markup
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True
# app.jinja_env.trim_blocks = True # 공백이나 개행을 없애고싶을때는 -을 사용하는것을 권장한다.

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31일 동안 유지되고 삭제된다.
)

@app.route('/main')
def main():
  return render_template('main.html',title="THIS MAIN")


class Nav:
  def __init__(self, title, url='#', children=[]):
    self.title = title
    self.url = url
    self.children = children


@app.route('/tmpl3')
def tmpl3():
  py = Nav("파이썬","https://www.naver.com/")
  java = Nav("자바","https://www.naver.com/")
  t_prg = Nav("프로그래밍언어","https://www.naver.com/",[py,java])
  
  jinja = Nav("Jinja","https://www.naver.com/")
  gc = Nav("Genshi, Cheetah","https://www.naver.com/")
  flask = Nav("플라스크","https://www.naver.com/",[jinja,gc])
  
  spr = Nav("스프링","https://www.naver.com/")
  ndjs = Nav("노드JS","https://www.naver.com/")
  t_webf = Nav("웹 프레임워크","https://www.naver.com/",[flask,spr,ndjs])
  
  my = Nav("나의 일상","https://www.naver.com/")
  issue = Nav("이슈게시판","https://www.naver.com/")
  t_others = Nav("기타","https://www.naver.com/",[my,issue])

  return render_template("index.html", navs=[t_prg,t_webf,t_others])


@app.route('/tmpl2')
def tmpl2():
  a = (1, "만남1", "김건모", False, [])
  b = (2, "만남2", "노사연", True, [a])
  c = (3, "만남3", "익명", False, [a,b])
  d = (4, "만남4", "익명", False, [a,b,c])

  return render_template("index.html", lst2=[a,b,c,d])



@app.route("/tmpl")
def t():
  
  
  tit = Markup("<strong>Title</strong>") #마크업 객체 생성 title은 마크업객체가 된다.
  mu = Markup("<h1>iii = <i>%s</i></h1>") # 반복되는 html을 컴포넌트화 시켜놓을수있음
  h = mu % "Italic"
  lst = [ ("만남1", "김건모",True), ("만남2", "노사연",False), ("만남3", "노사봉",True) ]
  return render_template('index.html',title=tit,mu=h,lst=lst) 

@app.route('/wc') # cookie 생성
def wc():
  key = request.args.get('key')
  val = request.args.get('val')
  res = Response("SET COOKIE")
  res.set_cookie(key,val)
  session['Token'] = '123X'
  return make_response(res)

@app.route('/rc')
def rc():
  key = request.args.get('key') #token 이름 
  val = request.cookies.get(key)
  return "cookie['" + key + "] = " + val + " , " + session.get('Token')

@app.route('/delsess')
def delsess():
  if session.get('Token'):
    del session['Token']
  return "Session이 삭제되었습니다!"

@app.route('/reqenv')
def reqenv():
  return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
        'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
        'PATH_INFO: %(PATH_INFO) s <br>'
        'QUERY_STRING: %(QUERY_STRING) s <br>'
        'SERVER_NAME: %(SERVER_NAME) s <br>'
        'SERVER_PORT: %(SERVER_PORT) s <br>'
        'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
        'wsgi.version: %(wsgi.version) s <br>'
        'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
        'wsgi.input: %(wsgi.input) s <br>'
        'wsgi.errors: %(wsgi.errors) s <br>'
        'wsgi.multithread: %(wsgi.multithread) s <br>'
        'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
        'wsgi.run_once: %(wsgi.run_once) s') % request.environ

def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

@app.route('/rp')
def rp():
  # q = request.args.get('q')
  q = request.args.getlist('q') # 값을 여러개 받아야 할때
  return "q = %s" % str(q)


@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), 
					('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)

@app.route('/res1')
def res1():
  custom_res = Response("Custom Response", 201, {'test': 'ttt'})
  return make_response(custom_res)

# @app.before_request
# def before_request():
#   print("before_request")
#   g.str = "한글"

# @app.route("/gg")
# def hellowordl2():
#   return "Hello World!" + getattr(g,'str','111')

@app.route("/")
def helloworld():
  return "Hello Flask World!"


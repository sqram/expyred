import web
import re
from mako.template import Template
import os.path

urls = (
	'/permalink', 'Permalink',
	'/(.*)/', 'Redirect',
	'/([0-9]+)', 'Index',
	'/', 'Index'
)


# Database credentials
db = web.database(
	dbn='mysql',
	host='localhost',
	user='root',
	pw='',
	db='expyred'
)



class View(object):
	def main_page(self, extra_placeholders = None):
		# The following placeholder(s) is the same everytime.
		# Extra ones are passed as params and get appended
		# when this method is called
		placeholders = {
			'site_name' : 'Expyred' ,
			'title' : 'Expyred - A python regex editor' ,
			'regex' : '',
			'string' : '',
			'options' : ''
		}

		# If we passed placeholders vars, replace the default values
		if extra_placeholders != None:
			for k, v in extra_placeholders.iteritems():
				placeholders[k] = v

		web.header('Content-Type','text/html; charset=utf-8', unique=True)

		filename = os.path.dirname (__file__) + '/static/layout.html'
		mytemplate = Template (filename=filename)
		return mytemplate.render (**placeholders)





class Index:
	def GET(self, id = None):
		''' Outputs main layout. If id is present, select from db '''

		if id == None:
			# Render index page with blank fields
			view = View()
			return view.main_page()
		else:
			# Render index page with form fields populated
			try:
				myvar = dict(id=id)
				values = db.select(
					"permalinks",
					myvar,
					where="linkID = $id",
					limit=1,
					_test = False)[0]

				extra_placeholders = {
					'regex' : values['regex'],
					'string' : values['string'],
					'options' : values['options']
				}
				view = View()
				return view.main_page(extra_placeholders)
			except:
				# linkID is out of range(does not exist in db)
				return self.GET()


	# Ajax'd
	def POST(self):
		''' Get POST vars '''
		data = web.input()
		options = data.options
		regex = data.regex
		string = data.string
		return self.replace_regex (regex, string, options)


	# Ajax'd
	def replace_regex(self, regex, string, options):
		''' Process the regex '''
		try:
			if options:
				options = "(?"+options+")"

			pattern = re.compile (options+regex)
			if( pattern.search(string) ):
				new = pattern.sub (r"<span class='match'>\g<0></span>", string)
				new = re.sub ("\n", "<br />", new)
				new = re.sub ("\t", "<span class='tab'>tab</span>", new)
				return "{ result : 'match',  string : '%s' }" % re.escape(new)
			else:
				return "{ result : 'no-match' }"
		except re.error, e:
			return "{ result : 'failure',  error : '%s' }" % e


# Ajax'd
class Permalink:
	def POST(self):
		''' Create permalink entry in db '''

		data = web.input()
		'' if data.options == None else data.options
		'' if data.regex == None else data.regex
		'' if data.string == None else data.string
		try:
			insert = db.insert(
			'permalinks',
			regex = data.regex,
			string = data.string,
			options = data.options,
			date = web.SQLLiteral ("NOW()") )
			return "{ result : 'success', text : %s }" % insert
		except:
			return "{ result : 'failure', text : 'Oops. Something bad happened' }"



class Redirect(object):
	def GET(self, path):
		''' Redirect to index if url ends with /'''
		web.seeother('/%s' % path)


# mod_wsgi needs the *application* variable to serve our app
application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
	app.run()

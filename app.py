from chalice import Chalice, Response
from chalicelib.middleman import do_milb
import icalendar

app = Chalice(app_name='icsMiddleman')


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/milb/{teamtoken}')
def get_milb(teamtoken):
	return Response(body=do_milb(teamtoken),
		status_code=200,
		headers={'Content-Type': 'text/calendar'})

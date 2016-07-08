from flask import render_template, request, make_response
from app import app
from app import db
from models import Video, Company, Company_List, Single_Report_View, Current_Month_Stats
from forms import VideoByNameForm, VideoEditForm , CompanyByNameForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/search/video', methods=['GET', 'POST'])
def search_title():

    form = VideoByNameForm()
    results = None

    if form.validate_on_submit():
        title = '%' + form.title.data + '%'
        results = Video.query.filter(Video.V_Title.ilike(title.encode("utf-8"))).all()
        for r in results:
            print r
    return render_template('video_search.html',results=results,form=form)


@app.route('/edit/video/<key>', methods=['POST'])
def get_video(key):
    video = Video.query.get(key)
    form = VideoEditForm(request.form)
    form.populate_obj(video)

    return render_template('video_edit.html',form=form)


@app.route('/search/company', methods=['GET', 'POST'])
def search_company():

    form = CompanyByNameForm()
    results = None

    if form.validate_on_submit():
        company_name = '%' + form.CName.data + '%'
        results = Company_List.query.filter(Company_List.CName.ilike(company_name.encode("utf-8"))).all()
        for r in results:
            print r
    return render_template('company_search.html',results=results,form=form)

@app.route('/edit/company/<key>', methods=['POST'])
def get_company(key):
    company = Company.query.get(key)
    form = VideoEditForm(request.form)
    #form.populate_obj(video)
    print 'ready to render template'

    return render_template('video_edit.html',form=form)

#
#  get video_id for single report
#
@app.route('/search/single_report', methods=['GET', 'POST'])
def get_single_report():
    form = VideoByNameForm()
    results = None

    if form.validate_on_submit():
        title = '%' + form.title.data + '%'
        results = Video.query.filter(Video.V_Title.ilike(title.encode("utf-8"))).order_by(Video.V_Title).all()
        for r in results:
            print r
    return render_template('single_report_search.html',results=results,form=form)
#
#  produce single report
#
@app.route('/reports/single_report/<int:video_id>', methods=['POST'])
def produce_single_report(video_id):
    summary = dict()

    results = Single_Report_View.query.filter_by(V_ID = video_id).order_by(Single_Report_View.month_id).all()

    #get current month stats from database
    current_month_stats = Current_Month_Stats.query.all()

    if not current_month_stats:
        return render_template('error.html')

    current_month = current_month_stats[0].month_name
    current_year =  current_month_stats[0].month_year

    #loop through results set to find current month

    for result_row in results:
        if result_row.SPeriod == current_month and result_row.SYear == current_year :

            summary['total_views'] = result_row.total_views
            summary['total_viewing_duration'] = 0.00
            summary['video_duration'] = 0.0
            summary['average_view'] = 0.0

    #summary['total_views'] = '1,295'
    #summary['total_viewing_duration'] = '32.4'
    #summary['video_duration'] = '2.2'
    #summary['average_view'] = '1.5'

    url = 'https://www.assettv.com/sites/default/files/video/images/etfsfeb2016.jpg'
    url_caption = ['Charles Schwab, ', 'Morgan Stanley, ','Thornburg, ','New York Life, ','J.P. Morgan']

    url_video = 'https://www.assettv.com/video/masterclass-exchange-traded-funds-february-2016?chid=61'


    header = dict()
    header['report_name'] = 'EXCHANGE TRADED FUNDS'
    header['published_date'] = 'PUBLISHED | December 7, 1941'
    header['report_date'] = 'VIEWING REPORT | 6/1/2016'
    header['masterclass'] = False
    header['single'] = True
    header['commpany_name'] = 'CAMBRIDE ASSOCIATES'

    top_companies = ('Merril Lynch','Morgan Stanly','RBC', 'Ameriprise',
    'LPL Financial', 'MetLife','Jannry', 'Transamerica','Stifel','Commonwealth')

    return render_template('graph.html',summary=summary, url=url,header = header, url_caption = url_caption,
                           top_companies = top_companies, url_video = url_video)

@app.route('/graph', methods=['POST'])
def graph():
    summary = dict()
    summary['total_views'] = '2,714'
    summary['total_viewing_duration'] = '836.6'
    summary['video_duration'] = '59.4'
    summary['average_view'] = '18.5'

    url = 'https://www.assettv.com/sites/default/files/video/images/etfsfeb2016.jpg'
    url_caption = ['Charles Schwab, ', 'Morgan Stanley, ','Thornburg, ','New York Life, ','J.P. Morgan']

    url_video = 'https://www.assettv.com/video/masterclass-exchange-traded-funds-february-2016?chid=61'


    header = dict()
    header['report_name'] = 'EXCHANGE TRADED FUNDS'
    header['published_date'] = 'PUBLISHED | December 7, 1941'
    header['report_date'] = 'VIEWING REPORT | 6/1/2016'
    header['masterclass'] = True
    header['single'] = False
    header['commpany_name'] = 'CAMBRIDE ASSOCIATES'

    top_companies = ('Merril Lynch','Morgan Stanly','RBC', 'Ameriprise',
    'LPL Financial', 'MetLife','Jannry', 'Transamerica','Stifel','Commonwealth')

    return render_template('graph.html',summary=summary, url=url,header = header, url_caption = url_caption,
                           top_companies = top_companies, url_video = url_video)


@app.route('/graph2', methods=['GET'])
def graph2():
    summary = dict()
    summary['total_views'] = '1,295'
    summary['total_viewing_duration'] = '32.4'
    summary['video_duration'] = '2.2'
    summary['average_view'] = '1.5'

    url = 'https://www.assettv.com/sites/default/files/video/images/etfsfeb2016.jpg'
    url_caption = ['Charles Schwab, ', 'Morgan Stanley, ','Thornburg, ','New York Life, ','J.P. Morgan']

    url_video = 'https://www.assettv.com/video/masterclass-exchange-traded-funds-february-2016?chid=61'


    header = dict()
    header['report_name'] = 'EXCHANGE TRADED FUNDS'
    header['published_date'] = 'PUBLISHED | December 7, 1941'
    header['report_date'] = 'VIEWING REPORT | 6/1/2016'
    header['masterclass'] = False
    header['single'] = True
    header['commpany_name'] = 'CAMBRIDE ASSOCIATES'

    top_companies = ('Merril Lynch','Morgan Stanly','RBC', 'Ameriprise',
    'LPL Financial', 'MetLife','Jannry', 'Transamerica','Stifel','Commonwealth')

    return render_template('graph.html',summary=summary, url=url,header = header, url_caption = url_caption,
                           top_companies = top_companies, url_video = url_video)

@app.route('/graph3', methods=['GET'])
def graph3():

    # use J.P Morgan Asset Management
    return render_template('channel.html')

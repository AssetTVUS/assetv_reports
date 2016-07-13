from flask import render_template, request, make_response
from sqlalchemy import desc
from app import app
from app import db
from models import Video, Company, Company_List, Single_Report_View, Current_Month_Stats
from models import Video_Tag, TopCompany, ReportMonth, CurrentMonth,VideoTopCompany
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
    summary = {}

    results = Single_Report_View.query.filter_by(V_ID = video_id).order_by(Single_Report_View.month_id).all()

    # did we get reporting data? If not, complain
    if not results:
        return render_template('no_report_data.html')

    #get current month stats from database
    current_month_stats = Current_Month_Stats.query.all()

    # unable to retrieve the current reportng month/year, show error page
    if not current_month_stats:
        return render_template('error.html',error_message='Unable to retrieve the current reportng month/year, check database')

    current_month = current_month_stats[0].month_name
    current_year =  current_month_stats[0].month_year
    current_month_number  = current_month_stats[0].month_number

    # is this a single or masterclass video?
    masterclass = True
    single = False
    if results[0].VType == 'SINGLE':
        masterclass = False
        single = True

    #loop through results set to find current month

    audience_profile = [] # pie chart needs a list

    for result_row in results:
        if result_row.SPeriod == current_month and result_row.SYear == current_year :

            summary['total_views'] = result_row.total_views
            summary['total_viewing_duration'] = 0.00  #TODO
            summary['video_duration'] = 0.0           #TODO
            summary['average_view'] = 0.0             #TODO

            point=['Wirehouse Advisors' , result_row.Wirehouse_Advisors*100]
            audience_profile.append(point)

            point=['Independent B/D' ,result_row.Independent_BD*100 ]
            audience_profile.append(point)

            point = ['RIA' , result_row.RIA*10 ]
            audience_profile.append(point)

            point = ['Investment Consultant' , result_row.Investment_Consultant*100 ]
            audience_profile.append(point)

            point = [ 'Plan Sponsor' , result_row.Plan_Sponsor*100 ]
            audience_profile.append(point)

            point = ['Asset Manager' , result_row.Asset_Manager*100 ]
            audience_profile.append(point)

            point = [ 'Other' ,result_row.Other*100 ]
            audience_profile.append(point)

            url = result_row.V_ImageURL

            #get the video caption(s) from the database
            caption_results = Video_Tag.query.filter_by(video_id = video_id ,tag_type='Companies')\
                .order_by(Video_Tag.tag_name).all()
            caption = ''
            if caption_results:
                for c in caption_results:
                    caption = caption + c.tag_name  + ', '
                caption = caption.rstrip(', ') # remove last comma

            # URL for video link
            url_video = result_row.V_VideoLink


            header = {}

            header['published_date'] = 'PUBLISHED | ' +  result_row.V_DatePublished.strftime('%B %d,%Y')
            header['report_date'] = 'VIEWING REPORT | ' + str(current_month_number) + '/1/' + str(current_year)
            header['masterclass'] = masterclass
            header['single'] = single



            if masterclass:
                temp = result_row.V_Title.strip('MASTERCLASS:')
                dash = temp.find('-',1) -1 #back up 1 position in fron of dash
                header['report_name'] =  temp[1: dash]
            else:
                header['report_name'] = result_row.V_Title

            if single:
                header['commpany_name'] = 'CAMBRIDE ASSOCIATES' #TODO


            #op_companies_result = TopCompanyVideo.query.join(ReportMonth,(ReportMonth.month_name == TopCompanyVideo.TCPeriod,
            #                                            ReportMonth.month_year == TopCompanyVideo.TCYear))\
            #                      .filter(CurrentMonth,(CurrentMonth.month_number == ReportMonth.month_number,
            #                                          CurrentMonth.month_year == ReportMonth.month_year))\
            #                      .filter(TopCompanyVideo == video_id).order_by(desc(TopCompanyVideo.TCViews)).limit(10)

            #top_companies_result = VideoTopCompany.query.filter(VideoTopCompany.VTCVID== video_id)\
            #    .filter(VideoTopCompany.VTCVID == video_id) \
            #   .join(ReportMonth, (ReportMonth.month_name == VideoTopCompany.VTCPeriod,\
            #            ReportMonth.month_year == VideoTopCompany.VTCYear))\
            #    .order_by(desc(VideoTopCompany.VTCViews)).limit(10)

            #top_companies = []
            #top_companies_result = VideoTopCompany.query.filter(VideoTopCompany.VTCVID== video_id)\
            #   .join(ReportMonth)\
            #   .order_by(desc(VideoTopCompany.VTCViews)).limit(10)

            #for tc in  top_companies_result:
            #    top_companies.append(tc.VTCCompany)

            top_companies = ('Merril Lynch', 'Morgan Stanly', 'RBC', 'Ameriprise',
                             'LPL Financial', 'MetLife', 'Jannry', 'Transamerica', 'Stifel', 'Commonwealth')  # TODO

            barchart_data = [
                [0, 1885], # 1 - Mar
                [1, 2479],# 1 - Apr
                [2, 2637], # 1 - May
                [3, 2714], # 1 - June
                [4, 0], # 1 - Jul
                [5, 0] #1 - Aug
            ]

            barchart_ticks = [
                [0, "1-Mar"], [1, "1-Apr"], [2, "1-May"], [3, "1-Jun"],
                [4, "1-Jul"], [5, "1-Aug"]
            ]



            return render_template('graph.html',summary=summary, url=url,header = header, caption = caption,
                top_companies = top_companies, url_video = url_video, audience_profile = audience_profile,
                barchart_data  = barchart_data ,barchart_ticks = barchart_ticks)

    return render_template('error.html',
                           error_message='data for the current reporting period, check database')
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

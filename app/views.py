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
        results = Video.query.filter(Video.V_Title.ilike(title.encode("utf-8"))).filter(Video.V_Type != None)\
            .order_by(Video.V_Title).all()
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


    #
    # get the data for the bar chart
    #
    barchart_data = []
    barchart_ticks = []

    for index in range(len(results)):
        # make ticks in the format of 1-JAN, 1-MAR
        barchart_ticks.append([index,'1-' + results[index].month_short_name.encode("utf-8")])
        barchart_data.append([index,results[index].total_views])


    # pie chart needs a list
    audience_profile = []

    #dictionary for report header
    header = {}

    if single:

        # loop through results set to find current month

        for result_row in results:
           if result_row.SPeriod == current_month and result_row.SYear == current_year :

               summary['total_views'] = result_row.total_views
               summary['total_viewing_duration'] = result_row.Total_Hours
               summary['video_duration'] = result_row.V_Duration
               summary['average_view'] = result_row.Avgerage_Minutes             #TODO

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


               # URL for Image and Video links
               url_video = result_row.V_VideoLink
               url = result_row.V_ImageURL

               #get the video caption(s) and Company Name  from the database
               caption_results = Video_Tag.query.filter_by(video_id = video_id )\
                   .order_by(Video_Tag.tag_name).all()

               caption = ''
               if caption_results:
                   for c in caption_results:
                       if c.tag_type =='People':
                           caption = caption + c.tag_name  + ', '
                           caption = caption.rstrip(', ') # remove last comma

                       if c.tag_type == 'Companies':
                           header['commpany_name'] =  c.tag_name  # add Company Name to Header dict






               header['published_date'] = 'PUBLISHED | ' +  result_row.V_DatePublished.strftime('%B %d,%Y')
               header['report_date'] = 'VIEWING REPORT | ' + str(current_month_number) + '/1/' + str(current_year)
               header['masterclass'] = masterclass
               header['single'] = single
               header['report_name'] = result_row.V_Title


               top_companies =[]
               top_companies_result = TopCompany.query.filter_by(VTCVID = video_id).order_by(desc(TopCompany.VTCViews))

               for tc in  top_companies_result:
                   top_companies.append(tc.VTCCompany)

               return render_template('graph.html',summary=summary, url=url,header = header, caption = caption,
                   top_companies = top_companies, url_video = url_video, audience_profile = audience_profile,
                   barchart_data  = barchart_data ,barchart_ticks = barchart_ticks)

        return render_template('error.html',
                error_message='data for the current reporting period, check database')


    else:
        point = {}
        summary['total_views'] = 0
        summary['total_viewing_duration'] = 0
        summary['video_duration'] = 0
        summary['average_view'] = 0

        point['Wirehouse Advisors'] = 0
        point['Independent B/D'] = 0
        point['RIA'] = 0
        point['Investment Consultant'] = 0
        point['Plan Sponsor'] = 0
        point['Asset Manager'] = 0
        point['Other'] = 0

        for result_row in results:
            summary['total_views'] = summary['total_views'] + result_row.total_views
            summary['total_viewing_duration'] = summary['total_viewing_duration'] + result_row.Total_Hours
            ###summary['video_duration'] = summary['video_duration']  + result_row.V_Duration
            summary['average_view'] = summary['average_view'] + result_row.Avgerage_Minutes  # TODO

            point['Wirehouse Advisors'] =  point['Wirehouse Advisors']  +  (result_row.Wirehouse_Advisors * 100)
            point['Independent B/D'] =  point['Independent B/D'] + ( result_row.Independent_BD * 100)
            point['RIA'] = point['RIA'] + (result_row.RIA * 10)
            point['Investment Consultant'] = point['Investment Consultant'] + (result_row.Investment_Consultant * 100)
            point['Plan Sponsor'] =   point['Plan Sponsor'] + (result_row.Plan_Sponsor * 100)
            point['Asset Manager'] = point['Asset Manager'] + (result_row.Asset_Manager * 100)
            point ['Other'] =   point ['Other'] + (result_row.Other * 100)

        audience_profile.append(point['Wirehouse Advisors'])
        audience_profile.append(point['Independent B/D'])
        audience_profile.append(point['RIA'])
        audience_profile.append(point['Investment Consultant'])
        audience_profile.append(point['Plan Sponsor'])
        audience_profile.append(point['Asset Manager'])
        audience_profile.append(point['Other'])

        url_video = results[0].V_VideoLink
        url = results[0].V_ImageURL
        summary['video_duration'] = results[0].V_Duration

        # get the video caption(s) and Company Name  from the database
        caption_results = Video_Tag.query.filter_by(video_id=video_id) \
            .order_by(Video_Tag.tag_name).all()

        caption = ''
        if caption_results:
            for c in caption_results:
                if c.tag_type == 'People':
                    caption = caption + c.tag_name + ', '
                    caption = caption.rstrip(', ')  # remove last comma

                #if c.tag_type == 'Companies':
                #    header['commpany_name'] = c.tag_name  # add Company Name to Header dict

        header['published_date'] = 'PUBLISHED | ' + results[0].V_DatePublished.strftime('%B %d,%Y')
        header['report_date'] = 'VIEWING REPORT | ' + str(current_month_number) + '/1/' + str(current_year)
        header['masterclass'] = masterclass
        header['single'] = single
        header['report_name'] = results[0].V_Title

        # chop MASTERCLASS TITLE
        temp = results[0].V_Title.strip('MASTERCLASS:')
        dash = temp.find('-', 1) - 1  # back up 1 position in fron of dash
        header['report_name'] = temp[1: dash]

        top_companies = []
        top_companies_result = TopCompany.query.filter_by(VTCVID=video_id).order_by(desc(TopCompany.VTCViews))

        for tc in top_companies_result:
            top_companies.append(tc.VTCCompany)

        return render_template('graph.html', summary=summary, url=url, header=header, caption=caption,
                               top_companies=top_companies, url_video=url_video, audience_profile=audience_profile,
                               barchart_data=barchart_data, barchart_ticks=barchart_ticks)


@app.route('/graph', methods=['GET'])
def graph():
    summary = dict()
    summary['total_views'] = 2714
    summary['total_viewing_duration'] = 836.6
    summary['video_duration'] = 59.4
    summary['average_view'] = 18.5

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
    audience_profile = [] # pie chart needs a list

    point=['Wirehouse Advisors' , 20]
    audience_profile.append(point)

    point=['Independent B/D' ,20]
    audience_profile.append(point)

    point = ['RIA' , 10 ]
    audience_profile.append(point)

    point = ['Investment Consultant' , 5 ]
    audience_profile.append(point)

    point = [ 'Plan Sponsor' , 5]
    audience_profile.append(point)

    point = ['Asset Manager' , 5 ]
    audience_profile.append(point)

    point = [ 'Other' ,35 ]
    audience_profile.append(point)

    return render_template('graph.html',summary=summary, url=url,header = header, url_caption = url_caption,
                top_companies = top_companies, url_video = url_video,
                audience_profile = audience_profile,
                barchart_data  = barchart_data ,barchart_ticks = barchart_ticks)


@app.route('/graph2', methods=['GET'])
def graph2():
    summary = dict()
    summary['total_views'] = 1295
    summary['total_viewing_duration'] = 32.4
    summary['video_duration'] = 2.2
    summary['average_view'] = 1.5

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

    audience_profile = [] # pie chart needs a list

    point=['Wirehouse Advisors' , 27]
    audience_profile.append(point)

    point=['Independent B/D' ,26]
    audience_profile.append(point)

    point = ['RIA' , 14 ]
    audience_profile.append(point)

    point = ['Investment Consultant' , 5 ]
    audience_profile.append(point)

    point = [ 'Plan Sponsor' , 6]
    audience_profile.append(point)

    point = ['Asset Manager' , 5 ]
    audience_profile.append(point)

    point = [ 'Other' ,2 ]
    audience_profile.append(point)
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
    return render_template('graph.html',summary=summary, url=url,header = header, url_caption = url_caption,
                           top_companies = top_companies, url_video = url_video,
                           audience_profile=audience_profile,
                           barchart_data=barchart_data, barchart_ticks=barchart_ticks)

@app.route('/graph3', methods=['GET'])

def graph3():
    body = {}
    footer = {}

    body['most_watched_video'] = "https://www.assettv.com/sites/default/files/video/images/importanceofsavingfor.jpg"
    body['most_watched_video_title'] = "The  importance of saving for retirement"
    body['most_watched_video_views'] = '2937'
    body['most_watched_video_hours'] = 73


    body['total_views'] = 21114
    body['second_most_watched_video'] = 'https://www.assettv.com/sites/default/files/video/images/helpingmillennialswith.jpg'
    body['second_most_watched_video_title'] = 'Helping millennials with innovative DC plan design'
    body['second_most_watched_video_views'] =  2896
    body['second_most_watched_video_hours'] = 109
    body['total_time_hours'] = 2340
    body['top_companies'] = ['Merrill Lynch Wealth Management','Morgan Stanley Wealth Management','LPL Financial',
                             'Wells Fargo Advisors','Raymond James','RBC','Lincoln Financial Group',
                             'UBS','Mercer','Commonwealth Fiancial']
    body['average_time_minutes'] = 6.7
    body['new_videos_published'] = 9
    body['average_video_engagement'] = .7
    footer['month_name'] = 'FEBRUARY 2016'
    footer['month_views'] = 5548
    footer['hours_watched'] = 778

    # use J.P Morgan Asset Management
    #return render_template('channel.html')
    return render_template('channel_report_page_2.html',body = body, footer = footer)

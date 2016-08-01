from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin import menu
from wtforms.validators import InputRequired,NumberRange,URL

# create the application object
app = Flask(__name__)

#get our configuration object
app.config.from_object('config')

#start up SQLAlchemy and Bootstrap
db = SQLAlchemy(app)
Bootstrap(app)


admin = Admin(app, name='Dashboard', template_mode='bootstrap3')
from models import Video,VideoTopCompany,Blog,BlogStats
from models import AudienceProfile, Email, EmailStats
from models import TopCompany, Whitepaper, WhitepaperStats,company_view
from models import AudienceProfile,VideoStats
from flask_admin.model import typefmt
from datetime import date


def date_format(view, value):
    return value.strftime('%d/%m/%Y')

def thousand_format(view,value):
    return '{0:,}'.format(value)

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        int: thousand_format,
        float: thousand_format,
        date: date_format
    })


class AudienceProfileModelView(ModelView):
    column_searchable_list = ['APCID']
    column_labels = dict(APWirehouseAdvisors = 'Wirehouse Advisors',
                         APindependent_BD='Independent BD', APRIA='RIA',
                         APInsurance_CPAs_BankTrust = 'Insurance CPAs BankTrust',
                         APInvestmentConsultant = 'Investment Consultant',
                         APEndowment_Foundation = 'Endowment Foundation',
                         APPlanSponsor = 'Plan Sponsor',
                         APAssetManager = 'Asset Manager',
                         APPrivateBank_WM = 'PrivateBank WM',
                         APIFA = 'IFA',
                         APOther ='APOther',
                         APArea = 'APArea'
                         )

class BlogModelView(ModelView):
    column_searchable_list = ['BTitle']


    column_labels = dict(BCID='Company Table is messed up',
                         BTitle='Blog Title',BDatePublished='Date Published'
    )
    form_ajax_refs = {
         'BCID': QueryAjaxModelLoader('company_view', db.session, company_view, fields=['company_name'], page_size=10)
    }
class BlogStatsModelView(ModelView):
    column_default_sort = 'blog.BTitle'
    column_searchable_list = ['blog.BTitle']
    column_labels = dict(BBID='Blog',
                         BMonth='Month',BViews='Views'
    )
    form_ajax_refs = {
        'BBID': QueryAjaxModelLoader('blog', db.session, Blog, fields=[Blog.BTitle], page_size=10)
    }
class EmailModelView(ModelView):
    column_default_sort = 'ETitle'
    column_searchable_list = [Email.ETitle]
    column_labels = dict(ECID='Company Issues',
                         ETitle='Title',EDate='Date'
    )
class EmailStatsModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_default_sort = 'EEID'
    column_searchable_list = ['emails.ETitle']
    column_labels = dict(ESends='Sends',
                         EOpens='Opens', ECTR='ECTR',
                         EWirehouseAdvisors='Wirehouse Advisors',
                         EIndepentBD='Independent BD',
                         ERIA='RIA',
                         EInsuranceCPAsBankTrust='Insurance CPAs BankTrust',
                         EInvestmentConsultant='Investment Consultant',
                         EEndowmentFoundation='Endowment Foundation',
                         EPlanSponsor='Plan Sponsor',
                         EAssetManager='Asset Manager',
                         EOther='Other',
                         EArea='Area'
                         )


class TopCompanyModelView(ModelView):
    column_default_sort = 'TCCID'
    column_exclude_list = ['TCPeriod','TCYear' ]
    column_labels = dict(
        TCCID = 'Company',  TCMonth = 'Month', TCCompany= 'Company', TCViews  = 'Views', TCArea ='Area'
    )
class VideoStatsModelView(ModelView):
    column_default_sort = 'vs_video.V_Title'
    column_sortable_list  = ('V_ID',('vs_video', 'vs_video.V_Title'))
    column_exclude_list = ['SPeriod', 'SYear']
    column_labels = dict(WirehouseAdvisors='Wirehouse Advisors',
                     Independent_BD='Independent BD',
                     RIA='RIA',
                     Insurance_CPAs_BankTrust='Insurance CPAs BankTrust',
                     Investment_Consultant='Investment Consultant',
                     Endowment_Foundation='Endowment Foundation',
                     Plan_Sponsor='Plan Sponsor',
                     Asset_Manager='Asset Manager',
                     PrivateBank_WM='PrivateBank WM',
                     IFA='IFA',
                     Other='Other',
                     VSMonth='Month',
                     VSArea ='Area',
                     Total_Views='Total Views',
                     Avgerage_Minutes = 'Average Minutes',
                     Total_Hours = 'Total Hours',
                     Completed_Views = 'Completed Views',
                     Terminal_Views = 'Terminal Views'
                     )
    column_choices = { 'VType' :[('Interactive','Interactive'),('INHOTSEAT','INHOTSEAT'),('MASTERCLASS','MASTERCLASS'),
                                 ('SINGLE','SINGLE'),('',' ')]
    }

class VideoTopCompanyModelView(ModelView):
    column_searchable_list = ['video.V_Title']
    column_exclude_list = ['VTCPeriod', 'VTCYear']
    column_labels = dict(VTCVID='Video Title',VTCCompany='Company',VTCViews ='Views',
            VTCArea='Area',VTCMonth='IDK'
    )
    form_ajax_refs = {
         'VTCVID': QueryAjaxModelLoader('video', db.session, Video, fields=[Video.V_Title], page_size=10)
    }

class VideoModelView(ModelView):
    column_default_sort = 'V_Title'
    column_exclude_list = ('V_DateFilmed')
    column_searchable_list = ['V_Title']
    column_labels = dict(V_Title='Video Title', V_Duration='Duration',
            V_VideoLink='Video URL',V_ImageURL='Thumbnail URL',
            V_Report_Finished ='Reporting Completed?',
            V_DatePublished='Date Published',
            V_Type='Video Type',
            V_DateFilmed ='Date Filmed'
            )
    form_choices = {
    'V_Type': [
        ('SINGLE', 'SINGLE'),
        ('MASTERCLASS', 'MASTERCLASS'),
        ('NULL', 'None')
    ]
    }
    form_args = dict(
        V_DatePublished = dict(validators=[InputRequired(message='Please provide Video Published Date')]),
        V_Title = dict(validators=[InputRequired(message='Please provide Video Title')]),
        V_Duration = dict(validators=[InputRequired(message='Please provide Video Duration'),
                                      NumberRange(min=0, max=999999, message='Please enter a valid duration')]),
        V_VideoLink = dict(validators=[URL(message = 'Please provide a valid URL'),InputRequired(message='Please provide a valid URL')]),
        V_ImageURL = dict(validators=[URL(message = 'Please provide a valid URL'),InputRequired(message='Please provide a valid URL')]),
    )
class WhitepaperModelView(ModelView):
    column_searchable_list = ['WTitle']

    column_labels = dict(WCID='Company Table Issues',WTitle= 'Title',
            WDatePublished= 'Date Published'
    )

class WhitepaperStatsModelView(ModelView):
    column_searchable_list = ['whitepaper.WTitle']

    column_labels = dict(WWID='White Paper',
            WViews='Views'
    )
real_home = menu.MenuLink(name='Back to Application',url='/')
admin.add_link(real_home)
admin.add_view(AudienceProfileModelView(AudienceProfile,db.session))
admin.add_view(BlogModelView(Blog,db.session))
admin.add_view(BlogStatsModelView(BlogStats,db.session))
admin.add_view(EmailModelView(Email,db.session))
admin.add_view(EmailStatsModelView(EmailStats,db.session))
admin.add_view(TopCompanyModelView(TopCompany, db.session))
admin.add_view(VideoModelView(Video, db.session))
admin.add_view(VideoStatsModelView(VideoStats,db.session))
admin.add_view(VideoTopCompanyModelView(VideoTopCompany, db.session))
admin.add_view(WhitepaperModelView(Whitepaper, db.session))
admin.add_view(WhitepaperStatsModelView(WhitepaperStats, db.session))





from app import views, models
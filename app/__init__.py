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
from models import TopCompany, Whitepaper, WhitepaperStats


class BlogModelView(ModelView):
    column_searchable_list = ['BTitle']


    column_labels = dict(BCID='Company Table is messed up',
                         BTitle='Blog Title',BDatePublished='Date Published'
    )
    #form_ajax_refs = {
    #     'VTCVID': QueryAjaxModelLoader('video', db.session, Video, fields=[Video.V_Title], page_size=10)
    #}
class BlogStatsModelView(ModelView):
    column_searchable_list = ['blog.BTitle']



    column_labels = dict(BBID='Blog',
                         BMonth='Month',BViews='Views'
    )
    form_ajax_refs = {
        'BBID': QueryAjaxModelLoader('blog', db.session, Blog, fields=[Blog.BTitle], page_size=10)
    }
class EmailModelView(ModelView):
    column_searchable_list = [Email.ETitle]
    column_labels = dict(ECID='Company Issues',
                         ETitle='Title',EDate='Date'
    )
#class EmailStats:

class TopCompanyModelView(ModelView):
    column_labels = dict(
        TCCID = 'Company', TCPeriod = 'Period', TCMonth = 'Month',TCYear  = 'Year',
          TCCompany= 'Company', TCViews  = 'Views', TCArea ='Area'
    )
class VideoTopCompanyModelView(ModelView):
    column_searchable_list = ['video.V_Title']
    column_labels = dict(VTCVID='Video Title',
                         VTCPeriod='Month',
            VTCYear='Year',
            VTCCompany='Company',
            VTCViews ='Views',
            VTCArea='Area',
            VTCMonth='IDK'
            )


    form_ajax_refs = {
         'VTCVID': QueryAjaxModelLoader('video', db.session, Video, fields=[Video.V_Title], page_size=10)
    }

class VideoModelView(ModelView):
    column_exclude_list = ('V_DateFilmed')
    column_searchable_list = ['V_Title']
    column_labels = dict(V_Title='Video Title', V_Duration='Duration',
            V_VideoLink='Video URL',V_ImageURL='Thumbnail URL',
            V_Report_Finished ='Reporting Completed?',
            V_DatePublished='Date Published',
            V_Type='Video Type'
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
        V_VideoLink = dict(validators=[URL(message = 'Please provide a valid URL')]),
        V_ImageURL = dict(validators=[URL(message = 'Please provide a valid URL')]),
    )
class WhitepaperModelView(ModelView):
    column_searchable_list = ['WTitle']

    column_labels = dict(WCID='Company Table Issues',WTitle= 'Title',
            WDatePublished= 'Date Published'
    )

class WhitepaperStatsModelView(ModelView):
    column_searchable_list = ['whitepaper.WTitle']

    column_labels = dict(WWID='White Paper', WMonth = 'Date',
            WViews='Views'
    )


real_home = menu.MenuLink(name='Back to Application',url='/')
admin.add_link(real_home)
admin.add_view(BlogModelView(Blog,db.session))
admin.add_view(BlogStatsModelView(BlogStats,db.session))
admin.add_view(EmailModelView(Email,db.session))
admin.add_view(TopCompanyModelView(TopCompany, db.session))
admin.add_view(VideoModelView(Video, db.session))
admin.add_view(VideoTopCompanyModelView(VideoTopCompany, db.session))
admin.add_view(WhitepaperModelView(Whitepaper, db.session))
admin.add_view(WhitepaperStatsModelView(WhitepaperStats, db.session))





from app import views, models
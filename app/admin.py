'''

admin.py - this is the module is used to generate the table maint. pages

'''

from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin import menu


from models import Video,VideoTopCompany,Blog,BlogStats
from models import AudienceProfile, Email, EmailStats
from models import TopCompany, Whitepaper, WhitepaperStats,company_view
from models import AudienceProfile,VideoStats
from flask_admin.model import typefmt
from datetime import date
from wtforms.validators import InputRequired,NumberRange,URL,DataRequired,ValidationError,StopValidation

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')


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



class BlogModelView(ModelView):
    column_searchable_list = ['BTitle']
    column_filters = ['companies.CName']

    column_labels = dict(companies='Company',
                         BTitle='Blog Title',BDatePublished='Date Published'
    )

    form_args = dict(
        BDatePublished= dict(validators=[InputRequired(message='Please provide Blog Published Date')]),
        BTitle = dict(validators=[InputRequired(message='Please provide Blog Title')]),
        #companies = dict(validators=[InputRequired(message='Please Select a Company')])
    )
    form_args['companies'] = dict(validators=[InputRequired(message='Please Select a Company'),
                                              DataRequired(message='Please Select a Company')])

    form_excluded_columns = ['blogs']



class BlogStatsModelView(ModelView):
    column_default_sort = 'blog.BTitle'
    column_searchable_list = ['blog.BTitle']
    column_labels = dict(BBID='Blog',
                         BMonth='Month',BViews='Views'
    )
    form_ajax_refs = {
        'BBID': QueryAjaxModelLoader('blog', db.session, Blog, fields=[Blog.BTitle], page_size=10)
    }

    form_args = dict(

        BBID = dict(validators=[InputRequired(message='Please provide Blog Title')]),
        BViews=dict(validators=[InputRequired(message='Please provide the  number of Blog Views'),
                                    NumberRange(min=0, max=999999, message='Please enter the number of views')]),
        month = dict(validators=[InputRequired(message='Please a month')])
    )

    #form_args = {'blog.BTitle': dict(validators=[InputRequired(message='Please provide Blog Title')])}
class EmailModelView(ModelView):
    column_default_sort = 'ETitle'
    column_searchable_list = [Email.ETitle]
    column_labels = dict(companies='Company',
                         ETitle='Title',EDate='Date')
    form_excluded_columns = ['emails']
    form_args = dict(

        EDate = dict(validators=[InputRequired(message='Please provide an Email Date')]),
        ETitle=dict(validators=[InputRequired(message='Please provide a Title')]),
        companies=dict(validators=[InputRequired(message='Please Select a Company'),
                                   DataRequired(message='Please Select a Company')]),
        company = dict(validators=[InputRequired(message='Please Select a Company'),
                                     DataRequired(message='Please Select a Company')])
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
    column_sortable_list = ('company','month_tc')
    column_exclude_list = ['TCPeriod','TCYear' ]
    column_labels = dict( month_tc = 'Month',TCCompany= 'Top 10 Company', TCViews  = 'Views',
                          TCArea ='Area'
    )
    column_filters = ['company']
    column_searchable_list = ['company.CName']
    form_excluded_columns = ['TCPeriod','TCYear']
    form_args = dict(

        month_tc = dict(validators=[InputRequired(message='Please select a month'),
                                       DataRequired(message='Pleasea select a month')]),
        TCViews = dict(validators=[InputRequired(message='Please provide the number of Views'),
                                      NumberRange(min=0, max=999999, message='Please enter a valid duration')]),
        TCArea =  dict(validators=[InputRequired(message='Please provide the number of Views'),
                                      NumberRange(min=0, max=5, message='Please enter a valid area')]),
        TCCompany = dict(validators=[InputRequired(message='Please select a company'),
                                       DataRequired(message='Pleasea select a company')]),
        company = dict(validators=[InputRequired(message='Please Select a Company'),
                               DataRequired(message='Please Select a Company')])
    )

class VideoStatsModelView(ModelView):
    column_filters = ['vs_months']
    column_searchable_list = ['vs_video.V_Title']
    column_default_sort = 'vs_video.V_Title'
    column_sortable_list  = ('V_ID',('vs_video', 'vs_video.V_Title'))
    column_exclude_list = ['SPeriod', 'SYear']
    form_excluded_columns = ['SPeriod', 'SYear']
    form_widget_args = {
        'VType': {
            'disabled': True
        }
    }
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
                     vs_months='Month',
                     VSArea ='Area',
                     Total_Views='Total Views',
                     Avgerage_Minutes = 'Average Minutes',
                     Total_Hours = 'Total Hours',
                     Completed_Views = 'Completed Views',
                     Terminal_Views = 'Terminal Views',
                     vs_video = 'Video Title',
                     VType = 'Type'

                     )
    column_choices = { 'VType' :[('Interactive','Interactive'),('INHOTSEAT','INHOTSEAT'),('MASTERCLASS','MASTERCLASS'),
                                 ('SINGLE','SINGLE'),('',' ')]
    }

    legit_number = dict(validators=[ NumberRange(min=0, max=999999, message='Please enter a valid number')])
    form_args = dict(

        Total_Views = legit_number,
        Avgerage_Minutes = legit_number,
        Total_Hours = legit_number,
        Completed_Views = legit_number,
        Terminal_Views  = legit_number,
        Wirehouse_Advisors = legit_number,
        Independent_BD =  legit_number,
        RIA = legit_number,
        Insurance_CPAs_BankTrust = legit_number,
        Investment_Consultant = legit_number,
        Endowment_Foundation = legit_number,
        Plan_Sponsor= legit_number,
        Asset_Manager= legit_number,
        PrivateBank_WM = legit_number,
        IFA = legit_number,
        Other = legit_number,
        Finished = legit_number,
        VSArea = legit_number

    )
    form_args['vs_video'] = dict(validators=[DataRequired(message='Please select a video title')])
    form_args['vs_months'] =  dict(validators=[InputRequired(message='Please select a month'),
                                       DataRequired(message='Pleasea select a month')])

    def on_model_change(self, form, model):
        total = 0

        if  form.Wirehouse_Advisors.data :
            total = total + form.Wirehouse_Advisors.data

        if  form.Independent_BD.data:
            total = total +  form.Independent_BD.data

        if  form.RIA.data:
             total = total + form.RIA.data

        if form.Insurance_CPAs_BankTrust.data:
             total = total + form.Insurance_CPAs_BankTrust.data

        if form.Investment_Consultant.data:
             total = total + form.Investment_Consultant.data

        if form.Endowment_Foundation.data:
            total = total + form.Endowment_Foundation.data

        if form.Plan_Sponsor.data:
            total = total + form.Plan_Sponsor.data

        if form.Asset_Manager.data:
            total = total + form.Asset_Manager.data

        if form.PrivateBank_WM.data:
            total = total + form.PrivateBank_WM.data

        if  form.IFA.data:
            total = total + form.IFA.data

        if  form.Other.data:
            total = total +  form.Other.data


        print '=======> ' + str(total) + ' <======='
        if (total == 0) | (total == 1):
            pass
            #super(form, model, is_created)._on_model_change()
        else:
            raise ValidationError(message='Invalid: These should add up to 1.0')


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
    '''
    vstats = VideoStatsModelView(VideoStats,db.session)
    column_labels = vstats.column_labels
    legit_number = vstats.legit_number
    form_args = vstats.form_args
    form_excluded_columns = vstats.form_excluded_columns
    column_exclude_list = vstats.column_exclude_list

    def on_model_change(self,form,model):
        vstats.on_model_change(sef,form,model)
    '''

class VideoTopCompanyModelView(ModelView):
    column_filters = ['VTCCompany','video.V_Title']
    form_excluded_columns = ['VTCYear','VTCPeriod']
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
    form_excluded_columns = ['vs_video','videos']

class WhitepaperModelView(ModelView):
    column_default_sort = 'WCID'
    column_sortable_list = ('company', 'WTitle')
    column_searchable_list = ['WTitle']

    column_labels = dict(WCID='Company Table Issues',WTitle= 'Title',
            WDatePublished= 'Date Published'
    )
    form_excluded_columns = ['whitepapers']
    form_args = dict(
        WTitle = dict(validators=[InputRequired(message='Please provide a Whitepaper Title')]),
        WDatePublished = dict(validators=[InputRequired(message='Please provide Published Date')]),
        company=dict(validators=[InputRequired(message='Please Select a Company'),
                                 DataRequired(message='Please Select a Company')])
    )

class WhitepaperStatsModelView(ModelView):
    column_default_sort = 'whitepapers.WTitle'
    column_searchable_list = ['whitepapers.WTitle']
    column_sortable_list = ('whitepapers','whitepapers.WTitle')
    column_labels = dict(WWID='White Paper',
            WViews='Views', whitepaper_month='Month'
    )
    form_args = dict(
        whitepapers = dict(validators=[InputRequired(message='Please Select a whitepaper'),
                                 DataRequired(message='Please Select a whitepaper')]),
        whitepaper_month = dict(validators=[InputRequired(message='Please select a month'),
                                       DataRequired(message='Pleasea select a month')]),
        WViews = dict(validators=[DataRequired(message='Please provide Video Duration'),
                                             NumberRange(min=0, max=999999, message='Please enter the number of views')])
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






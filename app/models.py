from app import db


class Video(db.Model):
    __tablename__ = "Video"
    V_ID = db.Column(db.Integer, primary_key=True)
    V_Title = db.Column(db.String(200))
    V_DateFilmed = db.Column(db.DateTime)
    V_DatePublished = db.Column(db.DateTime)
    V_Duration = db.Column(db.Float)
    V_VideoLink = db.Column(db.String(500))
    V_Type = db.Column(db.String(1))
    V_ImageURL = db.Column(db.String(500))
    #videos = db.relationship("TagList", backref="video")

    def __repr__(self):
        return '<Video (%r) - %r>' % (self.V_ID,self.V_Title.encode('utf-8'))
    def __str__(self):
        return self.V_Title

class Tag(db.Model):
    __tablename__='Tag'
    T_ID = db.Column(db.Integer, primary_key=True)
    T_TAG = db.Column(db.String(200))
    T_Type = db.Column(db.String(50))

    def __repr__(self):
        return '<Tag (%r) - %r>' % (self.T_ID,self.T_Tag)

class TagList(db.Model):
    __tablename__ = 'TagList'
    TL_ID =  db.Column(db.Integer, primary_key=True)
    TL_VID = db.Column(db.Integer,db.ForeignKey('Video.V_ID'))
    TL_TID = db.Column(db.Integer,db.ForeignKey('Tag.T_ID'))
    #video = db.relationship("Video", foreign_keys="Video.V_ID")
    tag_name = db.relationship("Tag", foreign_keys="Tag.T_ID", \
                               primaryjoin="and_(Tag.T_ID==TagList.TL_TID)")

class Company(db.Model):
    CID = db.Column(db.Integer, primary_key=True)
    CName = db.Column(db.String(100))
    CReportSinceMonth = db.Column(db.Integer)         #TODO
    CReportSinceYear  = db.Column(db.Integer)             #TODO
    CType = db.Column(db.Integer)                     #TODO

    def __repr__(self):
        return '<Company (%r) - %r>' % (self.CID, self.CName)

class Company_List(db.Model):
    __tablename__ = "VW_COMPANY_LIST"
    CID = db.Column(db.Integer, primary_key=True)
    CName = db.Column(db.String(100))
    month_name = db.Column(db.Integer)         #TODO
    CReportSinceYear  = db.Column(db.Integer)             #TODO
    company_type = db.Column(db.Integer)                     #TODO

    def __repr__(self):
        return '<Company (%r) - %r>' % (self.CID, self.CName)

class YTD_Results(db.Model):
    __tablename__ = "VW_YTD_Results_Detailed"
    CID = db.Column(db.Integer, primary_key=True)
    V_ID = db.Column(db.Integer, primary_key=True)
    V_Title = db.Column(db.String(200))
    V_DatePublished = db.Column(db.String(20))
    V_Duration = db.Column(db.Float)
    View_Stats =  db.Column(db.Integer)
    View_Completes = db.Column(db.Integer)
    Average_Completion_Rate = db.Column(db.Float)
    Average_Time = db.Column(db.Float)
    Total_Time = db.Column(db.Float)
    Bloomberg_Terminal_Views = db.Column(db.Integer)

class Single_Report_View(db.Model):
    __tablename__ = "VW_SINGLE_REPORT"
    month_id =  db.Column(db.Integer)
    V_ID  =  db.Column(db.Integer)
    SPeriod = db.Column(db.String(20))
    SYear = db.Column(db.Integer)
    month_short_name = db.Column(db.String(3))
    V_Title = db.Column(db.String(200))
    V_ImageURL = db.Column(db.String(500))
    V_VideoLink = db.Column(db.String(500))
    V_DatePublished = db.Column(db.DateTime)
    VType  = db.Column(db.String(20))
    total_views = db.Column(db.Integer)
    Completed_Views  = db.Column(db.Integer)
    Avgerage_Minutes  = db.Column(db.Float)
    Total_Hours  = db.Column(db.Float)
    V_Duration  = db.Column(db.Float)
    Wirehouse_Advisors = db.Column(db.Float)
    Independent_BD = db.Column(db.Float)
    Insurance_CPAs_BankTrust = db.Column(db.Float)
    RIA  = db.Column(db.Float)
    Investment_Consultant =  db.Column(db.Float)
    Plan_Sponsor =  db.Column(db.Float)
    Endowment_Foundation =  db.Column(db.Float)
    Asset_Manager =  db.Column(db.Float)
    Other  =  db.Column(db.Float)
    VS_ID = db.Column(db.Integer, primary_key=True)

class Current_Month_Stats(db.Model):
    __tablename__ = 'VW_Current_Month'
    month_number =  db.Column(db.Integer, primary_key=True)
    month_year =  db.Column(db.Integer)
    month_id =  db.Column(db.Integer)
    month_name  = db.Column(db.String(20))
    month_short_name  = db.Column(db.String(3))

class Video_Tag(db.Model):
    __tablename__ = 'VW_VIDEO_TAG_COMPANIES'
    TL_ID = db.Column(db.Integer,primary_key = True)
    video_id = db.Column(db.Integer)
    tag_name = db.Column(db.String(200))
    tag_type = db.Column(db.String(20))

class CurrentMonth(db.Model):
    __tablename__ = 'Month_current'
    month_key = db.Column(db.Integer, primary_key = True)
    month_number = db.Column(db.Integer)
    month_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Month (%r) - %r>' % (self.month_number, self.month_year)



class TopCompany(db.Model):
    __tablename__ = 'VW_TOP_COMPANIES'
    VTCID = db.Column(db.Integer, primary_key = True)
    VTCVID = db.Column(db.Integer)
    VTCCompany = db.Column(db.String(255))
    VTCViews = db.Column(db.Integer)


class VideoTopCompany(db.Model):
    __tablename__ = 'VideoTopCompany'

    #__table_args__ = (
    #    db.ForeignKeyConstraint(
    #        ['VTCPeriod', 'VTCYear'],
    #        ['Month_report.month_name', 'Month_report.month_year'],
    #    ),
    #)
    VTCID = db.Column(db.Integer, primary_key = True)
    VTCVID = db.Column(db.Integer,db.ForeignKey('Video.V_ID'))
    VTCPeriod = db.Column(db.String(255))
    VTCYear  = db.Column(db.Integer)
    VTCArea  = db.Column(db.String(255))
    VTCCompany = db.Column(db.String(255))
    VTCViews = db.Column(db.Integer)
    video = db.relationship(
        Video,
        backref="videos"
    )

    #report_month = db.relationship('ReportMonth', lazy='joined',
    #                                primaryjoin='report_month.month_name==VideoTopCompany.VTCPeriod')
    #report_year =  db.relationship('ReportMonth', lazy='joined', primaryjoin='report_month.month_year==VideoTopCompany.VTCYear')

class Month_Report(db.Model):
    __tablename__ = 'Month_report'
    month_id = db.Column(db.Integer, primary_key = True)
    month_short_name = db.Column(db.String(3))
    month_name = db.Column(db.String(20))
    month_number = db.Column(db.Integer)
    month_year = db.Column(db.Integer)

month_table = db.Table('Month', db.metadata,
                        db.Column('month',db.Integer),
                        db.Column('month_name', db.String(20))
)

Masterclass_Top_Companies = db.Table('VW_TOP_COMPANIES_MASTERCLASS',db.metadata,
                                  db.Column("VTCVID",db.Integer),
                                  db.Column("SUM_VIEWS",db.Integer),
                                  db.Column("VTCCompany",db.String(100)))

Channel_Reports = db.Table('VW_Video_Company_Tag_Stats', db.metadata,
                        db.Column('TL_TID',db.Integer),
                        db.Column('V_Title', db.String(200)),
                        db.Column('V_DatePublished',db.Date),
                        db.Column('V_Duration',db.Float),
                        db.Column('V_VideoLink',db.String(500)),
                        db.Column('V_ImageURL',db.String(500)),
                        db.Column('VS_ID',db.Integer),
                        db.Column('V_ID',db.Integer),
                        db.Column('VType', db.String(20)),
                        db.Column('SPeriod', db.String(20)),
                        db.Column('SYear',db.Integer),
                        db.Column('Total_Views',db.Integer),
                        db.Column('Avgerage_Minutes',db.Integer),
                        db.Column('Total_Hours',db.Float),
                        db.Column('Completed_Views', db.Integer),
                        db.Column('Terminal_Views', db.Integer),
                        db.Column('Wirehouse_Advisors',db.Float),
                        db.Column('Independent_BD',db.Float),
                        db.Column('RIA',db.Float),
                        db.Column('Insurance_CPAs_BankTrust',db.Float),
                        db.Column('Investment_Consultant',db.Float),
                        db.Column('Endowment_Foundation',db.Float),
                        db.Column('Plan_Sponsor',db.Float),
                        db.Column('Asset_Manager',db.Float),
                        db.Column('PrivateBank_WM', db.Float),
                        db.Column('IFA',db.Float),
                        db.Column('Other',db.Float),
                        db.Column('Finished',db.Integer),
                        db.Column('VSMonth', db.Integer),
                        db.Column('VSArea',db.Integer)
)

Channel_Reports_Page1 = db.Table('VW_CHANNEL_REPORTS', db.metadata,
                        db.Column('T_ID',db.Integer),
                        db.Column('T_TAG',db.String(200)),
                        db.Column('Sum_Total_Views', db.Integer),
                        db.Column('Sum_Total_Hours',db.Float),
                        db.Column('Sum_Completed_Views',db.Integer)
)

Channel_Reports_Last_Month = db.Table('VW_CHANNEL_REPORTS_LAST_MONTH',db.metadata,
                        db.Column('month_id',db.Integer),
                        db.Column('T_ID', db.Integer),
                        db.Column('T_TAG', db.Integer),
                        db.Column('Sum_Total_Views', db.Integer),
                        db.Column('Sum_Total_Hours',db.Float),
                        db.Column('Wirehouse_Advisors', db.Float),
                        db.Column('Independent_BD', db.Float),
                        db.Column('RIA', db.Float),
                        db.Column('Insurance_CPAs_BankTrust', db.Float),
                        db.Column('Investment_Consultant', db.Float),
                        db.Column('Endowment_Foundation', db.Float),
                        db.Column('Plan_Sponsor', db.Float),
                        db.Column('Asset_Manager', db.Float),
                        db.Column('PrivateBank_WM', db.Float),
                        db.Column('IFA',db.Float),
                        db.Column('Other', db.Float)
)

CHANNEL_YTD_Audience_Category  = db.Table('VW_CHANNEL_YTD_Audience_Category',db.metadata,
                        db.Column('T_ID',db.Integer),
                        db.Column('Wirehouse_Advisors',db.Float),
                        db.Column('Independent_BD',db.Float),
                        db.Column('RIA',db.Float),
                        db.Column('Insurance_CPAs_BankTrust',db.Float),
                        db.Column('Investment_Consultant',db.Float),
                        db.Column('Endowment_Foundation',db.Float),
                        db.Column('Plan_Sponsor',db.Float),
                        db.Column('Asset_Manager',db.Float),
                        db.Column('PrivateBank_WM',db.Float),
                        db.Column('IFA', db.Float),
                        db.Column('Other',db.Float)
)
CHANNEL_YTD_Reports = db.Table('VW_YTD_CHANNEL_REPORTS', db.metadata,
                                         db.Column('T_ID', db.Integer),
                                         db.Column('T_TAG', db.Integer),
                                         db.Column('V_ID',db.Integer),
                                         db.Column('V_DatePublished', db.Date),
                                         db.Column('V_Title',db.String(200)),
                                         db.Column('V_Duration',db.Float),
                                         db.Column('YTD_Views',db.Integer),
                                         db.Column('YTD_Avg_Min', db.Float),
                                         db.Column('YTD_Total_Hours',db.Float),
                                         db.Column('YTD_Completed_Views',db.Integer),
                                         db.Column('YTD_Wirehouse_Advisors', db.Float),
                                         db.Column('YTD_Independent_BD', db.Float),
                                         db.Column('YTD_Insurance_CPAs_BankTrust', db.Float),
                                         db.Column('YTD_RIA', db.Float),
                                         db.Column('YTD_Investment_Consultant', db.Float),
                                         db.Column('YTD_Plan_Sponsor', db.Float),
                                         db.Column('YTD_Endowment_Foundation', db.Float),
                                         db.Column('YTD_Asset_Manager', db.Float),
                                         db.Column('YTD_Other', db.Float),
                                         db.Column('YTD_PrivateBank_WM', db.Float),
                                         db.Column('YTD_IFA', db.Float)
)
Last_Month = db.Table('VW_LAST_REPORT_MONTH',db.metadata,
                        db.Column('month_id',db.Integer),
                        db.Column('month_short_name',db.String(20)),
                        db.Column('month_name',db.String(20)),
                        db.Column('month_number',db.Integer),
                        db.Column('month_year', db.Integer)
)

Channel_last_month_Detail = db.Table('VW_CHANNEL_REPORTS_LAST_MONTH_DETAIL',db.metadata,
                        db.Column('month_id',db.Integer),
                        db.Column('T_ID', db.Integer),
                        db.Column('T_Tag',db.String(200)),
                        db.Column('V_Title',db.String(200)),
                        db.Column('V_DatePublished', db.Date),
                        db.Column('V_Duration', db.Float),
                        db.Column('Total_Views',db.Integer),
                        db.Column('Total_Hours',db.Integer),
                        db.Column('Wirehouse_Advisors',db.Float),
                        db.Column('Independent_BD',db.Float),
                        db.Column('RIA', db.Float),
                        db.Column('Insurance_CPAs_BankTrust',db.Float),
                        db.Column('Investment_Consultant', db.Float),
                        db.Column('Endowment_Foundation', db.Float),
                        db.Column('Plan_Sponsor', db.Float),
                        db.Column('Asset_Manager', db.Float),
                        db.Column('PrivateBank_WM', db.Float),
                        db.Column('IFA', db.Float),
                        db.Column('Other', db.Float)


)

channel_report_all_time_2 = db.Table('VW_CHANNEL_REPORTS_ALL_TIME_2',db.metadata,
                        db.Column('T_ID',db.Integer),
                        db.Column('T_Tag',db.String(200)),
                        db.Column('V_DatePublished',db.Date),
                        db.Column('V_Title',db.String(200)),
                        db.Column('V_Duration',db.Float),
                        db.Column('Total_Views', db.Integer),
                        db.Column('Average_Minutes',db.Float),
                        db.Column('Total_Hours', db.Float),
                        db.Column('Engagement', db.Float)

)

channel_email_stats = db.Table('VW_Channel_EMail_Stats',db.metadata,
                        db.Column('ECID',db.Integer),
                        db.Column('ETitle',db.String(200)),
                        db.Column('EDate',db.Date),
                        db.Column('ESends',db.Integer),
                        db.Column('EOpens',db.Integer),
                        db.Column('ECTR',db.Integer),
                        db.Column('EWirehouseAdvisors',db.Float),
                        db.Column('EIndepentBD',db.Float),
                        db.Column('ERIA',db.Float),
                        db.Column('EInvestmentConsultant',db.Float),
                        db.Column('EPlanSponsor',db.Float),
                        db.Column('EAssetManager',db.Float),
                        db.Column('EOther',db.Float)
)


class VideoStats(db.Model):
    __tablename__ = 'VideoStats'
    VS_ID = db.Column(db.Integer, primary_key = True)
    V_ID = db.Column(db.Integer)
    VType = db.Column(db.String(20))
    SPeriod = db.Column(db.String(20))
    SYear  = db.Column(db.Integer)
    Total_Views  = db.Column(db.Integer)
    Avgerage_Minutes = db.Column(db.Float)
    Total_Hours = db.Column(db.Float)
    Completed_Views = db.Column(db.Integer)
    Terminal_Views  = db.Column(db.Integer)
    Wirehouse_Advisors = db.Column(db.Float)
    Independent_BD = db.Column(db.Float)
    RIA = db.Column(db.Float)
    Insurance_CPAs_BankTrust = db.Column(db.Float)
    Investment_Consultant = db.Column(db.Float)
    Endowment_Foundation = db.Column(db.Float)
    Plan_Sponsor = db.Column(db.Float)
    Asset_Manager = db.Column(db.Float)
    PrivateBank_WM = db.Column(db.Float)
    IFA = db.Column(db.Float)
    Other = db.Column(db.Float)
    Finished  = db.Column(db.Integer)
    VSMonth  = db.Column(db.Integer)
    VSArea  = db.Column(db.Integer)

class AudienceProfile(db.Model):
    __tablename__ = 'AudienceProfile'
    APID  = db.Column(db.Integer, primary_key = True)
    APCID   = db.Column(db.Integer)
    APPeriod  = db.Column(db.String(255))
    APYear  = db.Column(db.Integer)
    APWirehouseAdvisors   = db.Column(db.Float)
    APindependent_BD   = db.Column(db.Float)
    APRIA = db.Column(db.Float)
    APInsurance_CPAs_BankTrust  = db.Column(db.Float)
    APInvestmentConsultant  = db.Column(db.Float)
    APEndowment_Foundation  = db.Column(db.Float)
    APPlanSponsor  = db.Column(db.Float)
    APAssetManager  = db.Column(db.Float)
    APPrivateBank_WM  = db.Column(db.Float)
    APIFA  = db.Column(db.Float)
    APOther  = db.Column(db.Float)
    APArea  = db.Column(db.Integer)

class Blog(db.Model):
    __tablename__ =  'blog'
    BID = db.Column(db.Integer, primary_key = True)
    BCID = db.Column(db.Integer)
    BTitle = db.Column(db.String(200))
    BDatePublished = db.Column(db.Date)
    def __str__(self):
        return self.BTitle

class BlogStats(db.Model):
    __tablename__= 'blog_stats'
    BSID = db.Column(db.Integer, primary_key = True)
    BBID =  db.Column(db.Integer,db.ForeignKey(Blog.BID))
    BMonth = db.Column(db.Integer,db.ForeignKey(Month_Report.month_id))
    BViews = db.Column(db.Integer)
    blog = db.relationship(
        Blog,
        backref="blogs")
    month =  db.relationship(Month_Report,backref='months')

class Email(db.Model):
    __tablename__ = 'email'
    EID = db.Column(db.Integer, primary_key = True)
    ECID = db.Column(db.Integer)
    ETitle = db.Column(db.String(200))
    EDate = db.Column(db.Date)

class EmailStats(db.Model):
    __tablename='email_stats'
    ESID = db.Column(db.Integer, primary_key = True)
    EEID = db.Column(db.Integer)
    EMonth = db.Column(db.Integer)
    ESends = db.Column(db.Integer)
    EOpens = db.Column(db.Integer)
    ECTR = db.Column(db.Integer)
    EWirehouseAdvisors = db.Column(db.Float)
    EIndepentBD = db.Column(db.Float)
    ERIA  = db.Column(db.Float)
    EInsuranceCPAsBankTrust  = db.Column(db.Float)
    EInvestmentConsultant  = db.Column(db.Float)
    EEndowmentFoundation  = db.Column(db.Float)
    EPlanSponsor  = db.Column(db.Float)
    EAssetManager  = db.Column(db.Float)
    EOther  = db.Column(db.Float)
    EArea = db.Column(db.String(10))

class Whitepaper(db.Model):
    __tablename__ = 'whitepaper'
    WID = db.Column(db.Integer, primary_key=True)
    WCID = db.Column(db.Integer)
    WTitle = db.Column(db.String(200))
    WDatePublished = db.Column(db.Date)
    def __str__(self):
        return self.WTitle

class WhitepaperStats(db.Model):
    __tablename__='whitepaper_stats'
    WSID = db.Column(db.Integer, primary_key = True)
    WWID = db.Column(db.Integer,db.ForeignKey(Whitepaper.WID))
    WMonth = db.Column(db.Integer)
    WViews  = db.Column(db.Integer)
    whitepaper =  db.relationship(Whitepaper,backref='whitepapers')

class TopCompany_Table(db.Model):
    __tablename__ = 'TopCompany'
    TCID = db.Column(db.Integer, primary_key = True)
    TCCID = db.Column(db.Integer)
    TCCID  = db.Column(db.Integer)
    TCPeriod = db.Column(db.String(255))
    TCYear  = db.Column(db.Integer)
    TCCompany= db.Column(db.String(255))
    TCViews  = db.Column(db.Integer)
    TCMonth  = db.Column(db.Integer)
    TCArea  = db.Column(db.Integer)


'''
class TagList(db.Model):
    TL_ID = db.Column(db.Integer, primary_key=True)
    TL_VID =  db.Column(db.Integer,db.ForeignKey('Video.V_ID'))
    TL_TID = db.Column(db.Integer,db.ForeignKey('Tag.T_ID'))
    tags = db.relationship("TagList", backref="tag")

    def __repr__(self):
        return '<TagList Video Id:(%r) - Tag Id:(%r)>' % (self.TL_VID,self.TL_TID)
'''
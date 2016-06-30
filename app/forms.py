from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField, DateField, DecimalField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms.validators import URL, NumberRange
from wtforms import ValidationError
from models import Video


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class VideoByNameForm(Form):
    #title = StringField('Video Name',[DataRequired, Length(min=3,max=50)])
    title = StringField('Video Name')
    submit = SubmitField('Search')

class VideoEditForm(Form):
    V_ID = IntegerField('Key')
    V_Title = StringField('Video Title', [DataRequired, Length(min=3,max=200)])
    V_DateFilmed = DateField("Date Filmed", [DataRequired])
    V_DatePublished = DateField("Date Published", [DataRequired])
    V_Duration = DecimalField("Duration", [DataRequired, NumberRange(min=0.01666666, max=200)])
    V_VideoLink = StringField("Video Link", [DataRequired, URL])
    V_Type = StringField('Video Type')
    V_ImageURL = StringField("Image URL", [DataRequired, URL])
    def populate_obj(self,video):
        self.V_ID = video.V_ID
        self.Title = video.V_Title.encode('UTF-8')
        self.V_DateFilmed =  video.V_DateFilmed
        self.V_DatePublished = video.V_DatePublished
        self.V_Duration =  video.V_Duration
        self.V_VideoLink = video.V_VideoLink
        self.V_Type = video.V_Type
        self.V_ImageURL = video.V_ImageURL
        print "populate done for " + self.Title

class CompanyByNameForm(Form):
    #CID = IntegerField('Key')
    CName = StringField('Company Name')   #TODO
    #CName = StringField('Company Name', [DataRequired, Length(min=2,max=100)])
    #CType = StringField('Company Type', [Length(min=2,max=10)])
    submit = SubmitField('Search')
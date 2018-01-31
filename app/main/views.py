from flask import flash, render_template, url_for, request
from flask_login import login_required, current_user
from flask_wtf import Form
from wtforms.fields import TextAreaField, SubmitField, SelectField, DecimalField
from . import main
from ..models import EditableHTML, Question, Answer, Club, ClubCategory


@main.route('/')
def index():
    clubs = Club.query.filter_by(is_confirmed=True).all()
    questions = Question.query.all()
    categories = ClubCategory.query.all()
    all_c = []
    for c in clubs:
        club_obj = {
            'id': c.id,
            'description': c.description,
            'img_link': c.img_link,
            'name': c.name,
            'categories': c.categories
        }
        for a in c.answers:
            if a.question is not None:
                if a.question.content not in club_obj:
                    club_obj[a.question.content] = []
                club_obj[a.question.content].append(a.rating)
        for q in club_obj:
            if type(club_obj[q]) is list:
                club_obj[q] = sum(club_obj[q]) / len(club_obj[q])
        all_c.append(club_obj)
    return render_template(
        'main/index.html',
        all_c=all_c,
        questions=questions,
        categories=categories)


@main.route('/submit-review/<int:club_id>', methods=['GET', 'POST'])
@login_required
def submit_review(club_id):
    class F(Form):
        pass

    for field in Question.query.all():
        if field.type == 'Rating':
            setattr(F, '{}_q'.format(field.id),
                    SelectField(
                        '{}. Pick from {} to {}'.format(field.content, 1,
                                                        5),
                        description=field.description,
                        choices=[('{}'.format(x + 1), x + 1)
                                 for x in range(5)]))
        elif field.type == 'Numerical':
            setattr(F, '{}_q'.format(field.id),
                    DecimalField(
                        '{}'.format(field.content),
                        description=field.description))
        if field.free_response:
            setattr(F, '{}_resp'.format(field.id),
                    TextAreaField('Please feel free to elaborate'))
    setattr(F, 'submit', SubmitField('Submit Rating'))
    form = F()
    if form.validate_on_submit():
        for x in form:
            if x.name.find('_q') > -1:
                if (x.name.find('_q')):
                    q_id = x.name.split('_')[0]
                    answer = form['{}_resp'.format(
                        q_id)].data if '{}_resp'.format(q_id) in form else ''
                    rating = x.data
                Answer.newAnswer(answer, rating, current_user.id, q_id,
                                 club_id)

        flash('Club Review successfully added', 'form-success')
    return render_template('main/submit-review.html', form=form)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)

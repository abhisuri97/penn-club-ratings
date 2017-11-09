from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_rq import get_queue

from .forms import (ChangeAccountTypeForm, ChangeUserEmailForm, InviteUserForm,
                    NewUserForm, NewQuestionForm)
from . import admin
from .. import db
from ..decorators import admin_required
from ..email import send_email
from ..models import Role, User, EditableHTML, Question, Answer


def bool(str):
    if str == 'True':
        return True
    if str == 'False':
        return False


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link, )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'
              .format(user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'
              .format(user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route('/_update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200

# All stuff dealing with adding, editing, and removing questions


@admin.route('/new-question', methods=['GET', 'POST'])
@login_required
@admin_required
def new_question():
    """Create a new question."""
    form = NewQuestionForm()
    if form.validate_on_submit():
        question = Question(
            content=form.content.data,
            max_rating=form.max_rating.data,
            free_response=bool(form.free_response.data))
        db.session.add(question)
        db.session.commit()
        flash('Question {} successfully created'.format(question.content),
              'form-success')
    return render_template('admin/new_question.html', form=form)


@admin.route('/questions')
@login_required
@admin_required
def questions():
    """View all registered users."""
    questions = Question.query.all()
    return render_template(
        'admin/questions.html', questions=questions)


@admin.route('/question/<int:question_id>')
@admin.route('/question/<int:question_id>/info')
@login_required
@admin_required
def question_info(question_id):
    """View a question."""
    question = Question.query.filter_by(id=question_id).first()
    answers = question.answers
    if question is None:
        abort(404)
    return render_template('admin/manage_question.html', question=question, answers=answers)


@admin.route('/question/<int:question_id>/change-question-details', methods=['GET', 'POST'])
@login_required
@admin_required
def change_question_details(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        abort(404)
    form = NewQuestionForm()
    if form.validate_on_submit():
        question.content = form.content.data
        question.max_rating = form.max_rating.data
        print(bool(form.free_response.data))
        question.free_response = bool(form.free_response.data)
        db.session.add(question)
        db.session.commit()
        flash('Question successfully edited', 'form-success')
    form.content.data = question.content
    form.max_rating.data = question.max_rating
    form.free_response.data = str(question.free_response)
    return render_template('admin/manage_question.html', question=question, form=form)


@admin.route('/question/<int:question_id>/delete')
@login_required
@admin_required
def delete_question_request(question_id):
    """Request deletion of a question"""
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        abort(404)
    return render_template('admin/manage_question.html', question=question)


@admin.route('/question/<int:question_id>/_delete')
@login_required
@admin_required
def delete_question(question_id):
    """Delete a question."""
    question = Question.query.filter_by(id=question_id).first()
    db.session.delete(question)
    db.session.commit()
    flash('Successfully deleted question %s.' % question.content, 'success')
    return redirect(url_for('admin.questions'))


@admin.route('/answer/<int:answer_id>/_delete')
@login_required
@admin_required
def delete_answer(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    db.session.delete(answer)
    db.session.commit()
    flash('Successfully deleted answer', 'success')
    return redirect(request.referrer)

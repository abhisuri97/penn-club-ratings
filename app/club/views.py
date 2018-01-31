from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from flask_rq import get_queue
from ..email import send_email
from .forms import (NewClubForm, EditClubForm)
from . import club
from .. import db
from ..decorators import admin_required
from ..models import Club, Role, User
from ..helpers import bool


@club.route('/new-club', methods=['GET', 'POST'])
@login_required
def new_club():
    """Create a new club."""
    form = NewClubForm()
    if form.validate_on_submit():
        club = Club(
            name=form.name.data,
            img_link=form.img_link.data,
            website=form.website.data,
            description=form.desc.data,
            recruitment_info=form.recruitment_info.data,
            is_confirmed=current_user.is_admin(),
            categories=form.categories.data)
        db.session.add(club)
        db.session.commit()
        link = url_for(
            'club.change_club_details', club_id=club.id, _external=True)
        if (current_user.is_admin() == False):
            for r in Role.query.filter_by(name='Administrator').all():
                for a in r.users:
                    get_queue().enqueue(
                        send_email,
                        recipient=a.email,
                        subject='A new club was suggested by {}'.format(
                            current_user.first_name),
                        template='club/email/suggested_club',
                        club=club,
                        link=link)
        action = 'created' if current_user.is_admin() else 'suggested'
        flash('Club {} successfully {}'.format(club.name, action),
              'form-success')
    return render_template('club/new_club.html', form=form)


@club.route('/clubs')
@login_required
@admin_required
def clubs():
    """View all registered users."""
    clubs = Club.query.all()
    return render_template('club/clubs.html', clubs=clubs)


@club.route('/<int:club_id>')
@club.route('/<int:club_id>/info')
def club_info(club_id):
    """View a club."""
    club = Club.query.filter_by(id=club_id).first()
    return render_template('club/manage_club.html', club=club)


@club.route('/<int:club_id>/change-club-details', methods=['GET', 'POST'])
@login_required
def change_club_details(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is None:
        abort(404)
    if (current_user.id != club.admin_id) and (current_user.is_admin() is False):
        print(current_user.is_admin())
        abort(403)
    form = EditClubForm()
    if form.validate_on_submit():
        club.name=form.name.data
        club.img_link=form.img_link.data
        club.website=form.website.data
        print(form.owner.data)
        club.admin_id=form.owner.data.id
        club.description=form.desc.data
        club.recruitment_info=form.recruitment_info.data
        club.categories = form.categories.data
        club.is_confirmed = bool(form.is_confirmed.data)
        db.session.add(club)
        db.session.commit()
        flash('Club successfully edited', 'form-success')
    form.name.data=club.name
    form.img_link.data=club.img_link
    form.website.data=club.website
    form.recruitment_info.data=club.recruitment_info
    form.owner.data = User.query.get(club.admin_id) if club.admin_id else None
    form.categories.data = club.categories
    form.desc.data = club.description
    form.is_confirmed.data = str(club.is_confirmed)
    return render_template('club/manage_club.html', club=club, form=form)


@club.route('/<int:club_id>/delete')
@login_required
@admin_required
def delete_club_request(club_id):
    """Request deletion of a club"""
    club = Club.query.filter_by(id=club_id).first()
    if club is None:
        abort(404)
    return render_template('club/manage_club.html', club=club)


@club.route('/<int:club_id>/_delete')
@login_required
@admin_required
def delete_club(club_id):
    """Delete a club."""
    club = Club.query.filter_by(id=club_id).first()
    db.session.delete(club)
    db.session.commit()
    flash('Successfully deleted club %s.' % club.name, 'success')
    return redirect(url_for('club.clubs'))

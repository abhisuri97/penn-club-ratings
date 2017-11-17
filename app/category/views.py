from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required

from .forms import (NewClubCategoryForm)
from . import category
from .. import db
from ..decorators import admin_required
from ..models import ClubCategory


@category.route('/new-category', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    """Create a new category."""
    form = NewClubCategoryForm()
    if form.validate_on_submit():
        category = ClubCategory(
            category_name=form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash('ClubCategory {} successfully created'.format(category.category_name),
              'form-success')
    return render_template('category/new_category.html', form=form)


@category.route('/categories')
@login_required
@admin_required
def categories():
    """View all registered users."""
    categories = ClubCategory.query.all()
    return render_template(
        'category/categories.html', categories=categories)


@category.route('/<int:category_id>')
@category.route('/<int:category_id>/info')
@login_required
@admin_required
def category_info(category_id):
    """View a category."""
    category = ClubCategory.query.filter_by(id=category_id).first()
    return render_template('category/manage_category.html', category=category)


@category.route('/<int:category_id>/change-category-details', methods=['GET', 'POST'])
@login_required
@admin_required
def change_category_details(category_id):
    category = ClubCategory.query.filter_by(id=category_id).first()
    if category is None:
        abort(404)
    form = NewClubCategoryForm()
    if form.validate_on_submit():
        category.category_name = form.category_name.data
        db.session.add(category)
        db.session.commit()
        flash('ClubCategory successfully edited', 'form-success')
    form.category_name.data = category.category_name
    return render_template('category/manage_category.html', category=category, form=form)


@category.route('/<int:category_id>/delete')
@login_required
@admin_required
def delete_category_request(category_id):
    """Request deletion of a category"""
    category = ClubCategory.query.filter_by(id=category_id).first()
    if category is None:
        abort(404)
    return render_template('category/manage_category.html', category=category)


@category.route('/<int:category_id>/_delete')
@login_required
@admin_required
def delete_category(category_id):
    """Delete a category."""
    category = ClubCategory.query.filter_by(id=category_id).first()
    db.session.delete(category)
    db.session.commit()
    flash('Successfully deleted category %s.' % category.category_name, 'success')
    return redirect(url_for('category.categories'))

from flask import abort,flash,redirect,render_template,url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm
from .. import db
from ..models import Department, Role

def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/departments', methods=['GET','POST'])
@login_required
def list_departments():
    
    check_admin()
    departments = Department.query.all()

    return render_template('admin/departments/departments.html',departments=departments,title='Departments')

@admin.route('/departments/add', methods=['GET','POST'])
@login_required
def add_department():

    check_admin()
    add_department=True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)

        try:
            db.session.add(department)
            db.session.commit()
            flash("Department successfully added.")
        except:
            flash("Error: department name already in use")

        return redirect(url_for('admin.list_departments'))

    return render_template('admin/departments/department.html',action="Add",add_department=add_department,form=form,title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_department(id):
    
    check_admin()
    add_department = False
    
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('Department successfully edited')

        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",add_department=add_department,form=form,department=department,title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET','Post'])
@login_required
def delete_department(id):
    
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('Department successfully deleted')
    
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

@admin.route('/roles')
@login_required
def list_roles():

    roles = Role.query.all()
    return render_template('admin/roles/roles.html',roles=roles,title='Roles')

@admin.route('/roles/add',methods=['GET','POST'])
@login_required
def add_role():
    
    check_admin()
    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            db.session.add(role)
            db.session.commit()
            flash('Role successfully added')
        except:
            flash('Error: role name already exists.')

        return redirect(url_for('admin.list_roles'))

    return render_template('admin/roles/role.html',add_role=add_role,form=form,title='Add Role')

@admin.route('/roles/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_role(id):
    
    check_admin()
    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('Role successfully edited')

        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html',add_role=add_role,form=form,title="Edit Roloe")

@admin.route('/roles/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_role(id):
    
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Role successfully deleted')

    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


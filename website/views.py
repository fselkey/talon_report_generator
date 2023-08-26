
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_session import Session

from flask_login import login_required, current_user
from .models import Note, Report
from . import db
import json
from datetime import datetime
from sqlalchemy import update

import webbrowser

import settings
import src.reader.reader_section as reader_section
import src.reader.reader_tdata as reader_tdata
import src.reader.reader as reader

import src.writer.writer as writer

views = Blueprint('views', __name__)

report_url = ''



## HOME PAGE
## ENTER SO NUMBER
@views.route('/', methods=['GET', 'POST'])
@login_required
def home() :
    quick_msg = ''

    username = session.get('user')
    password = session.get('pass')
    print('type session username: ', type(username))
    print('session username: ', username)
    print('type session password: ', type(password))
    print('session password: ', password)
    if username == 'None' or password == 'None' or username == '' or password == '' :
        return redirect(url_for('auth.login'))

    
    if request.method == 'POST' :
        so_num = request.form.get('so_num')

        session['so_num'] = so_num
        print('SESSION SO_NUM: ', session['so_num'])

        if so_num and len(so_num) < 1 :
            flash('so_num is too short!', category='error')
        else:

            print("Checking SO number.... ", so_num)
            reader_section.read_sections()
            print("Finished checking SO number.... ", so_num)

            section_name = ''
            if session.get("section_name") is not None :
                section_name=session['section_name']
            else :
                section_name = ''
            print('set section name: ', section_name)
            
            return render_template("section-form.html",
                user=current_user,
                soNum=session['so_num'],
                report_id=session['report_id'],
                sections=session['sections'],
                section_name=section_name)

    else :

        session['report_sections'] = []
        session['summary_sect_id'] = ''
        session['summary_row_id'] = []
        section=session['section'] = ''
        sect_id=session['sect_id'] = ''
        #session['section_name'] = ''
        session['sections'] = []

        session['so_num'] = ''
        session['report_id'] = ''
        session['iqty'] = 0
        session['pqty'] = 0
        session['fqty'] = 0
        session['quick_msg'] = ''
        session['quick_msgs'] = []
        session['original_quick_msgs'] = []
        session['image_templates'] = []
        session['test_templates'] = []

        session['img_urls'] = []
        session['img_ids'] = []
        session['img_files'] = []
        session['img_sectids'] = []
        session['img_dords'] = []
        session['img_cols'] = []
        session['img_titles'] = []
        session['img_descriptions'] = []
        session['equipment_template'] = ''
        session['test_template'] = ''

        return render_template("home.html", user=current_user)

## SELECT TEST SECTION
@views.route('/section', methods=['POST'])
@login_required
def section_form() :

    username = session.get('user')
    password = session.get('pass')
    print('type session username: ', type(username))
    print('session username: ', username)
    print('type session password: ', type(password))
    print('session password: ', password)
    if username == 'None' or password == 'None' or username == '' or password == '' :
        return redirect(url_for('auth.login'))

    if request.method == 'POST' :

        print('SESSION SO_NUM: ', session['so_num'])

        section_index = request.form.get('section')
        print("USER SELECTED SECTION: ", section_index)
        section = session['sections'][int(section_index)]
        session['section'] = section
        session['section_id'] = section[0]
        session['section_number'] = str(int(section[3])+1)

        print('section: ', session['section'])

        reader_tdata.generate_test_rows()

        ## Make sure images have been updated in talon
        ## do this before searching for new image files
        writer.save_new_images()

        templates = settings.test_templates
        session['test_templates'] = templates
        test_templates = session['test_templates']

        template_titles = []
        for template in test_templates :
            template_titles.append(template.name)

        print('SETTINGS.TEST_TEMPLATES: ', test_templates)


        return render_template("test-form.html",
            user=current_user,
            template_titles=template_titles,
            test_templates=test_templates,
            test_rows=session['test_rows'],
            soNum=session['so_num'],
            reportid=session['report_id'])

    else :
        return render_template("home.html", user=current_user)

## SELECT TEST NAME
@views.route('/test', methods=['POST'])
@login_required
def test_form() :
    quick_msg = ''

    username = session.get('user')
    password = session.get('pass')
    print('type session username: ', type(username))
    print('session username: ', username)
    print('type session password: ', type(password))
    print('session password: ', password)
    if username == 'None' or password == 'None' or username == '' or password == '' :
        return redirect(url_for('auth.login'))

    if request.method == 'POST' :

        print('SESSION SO_NUM: ', session['so_num'])

        test_name = request.form.get('test_name')
        test_template = request.form.get('test_template')

        print('USER INPUT TEST NAME: ', test_name)
        print('USER INPUT TEST TEMPLATE: ', test_template)

        session['test_name'] = test_name
        session['test_template'] = test_template

        reader.generate_tdata()

        return render_template("report.html",
            user=current_user,
            equipment_template=session['equipment_template'],
            test_template=['test_template'],
            image_templates=session['image_templates'],
            quick_msgs=session['quick_msgs'],
            so_num=session['so_num'],
            report_id=session['report_id'],
            iqty=session['iqty'],
            pqty=session['pqty'],
            fqty=session['fqty'],
            quick_msg=session['quick_msg'],
            report_sections=session['report_sections'],
            summary_sect_id=session['summary_sect_id'],
            section=session['section'],
            sect_id=session['sect_id'],
            section_name=session['section_name'],
            sections=session['sections'],
            img_ids=session['img_ids'],
            img_files=session['img_files'],
            img_urls=session['img_urls'],
            img_titles=session['img_titles'],
            img_sectids=session['img_sectids'],
            img_cols=session['img_cols'],
            img_dords=session['img_dords'],
            img_descriptions=session['img_descriptions'])

    else :
        return render_template("home.html", user=current_user)

@views.route('/report', methods=['POST'])
@login_required
def report() :

    username = session.get('user')
    password = session.get('pass')
    print('type session username: ', type(username))
    print('session username: ', username)
    print('type session password: ', type(password))
    print('session password: ', password)
    if username == 'None' or password == 'None' or username == '' or password == '' :
        return redirect(url_for('auth.login'))

    if request.method == 'POST' :

        #summary section of report
        iQty = request.form.get('iqty')
        pQty = request.form.get('pqty')
        fQty = request.form.get('fqty')
        quick_msg = request.form.get('summary_textarea')
        asset_tags = request.form.get('asset_tags')

        session['iqty'] = iQty
        session['pqty'] = pQty
        session['fqty'] = fQty
        session['quick_msg'] = quick_msg
        session['asset_tags'] = asset_tags

        print('iQty: ', iQty)
        print('pQty: ', pQty)
        print('fQty: ', fQty)
        print('quick_msg: ', quick_msg)
        print('asset_tags: ', asset_tags)

        print('image titles before: ', session['img_titles'])
        print('image descriptions before: ', session['img_descriptions'])

        img_sectids = []
        img_dords = []
        img_cols = []
        img_titles = []
        img_descriptions = []

        for idx, image in enumerate(session['img_files']) :

            img_sectid = request.form.get('img_sectid'+str(idx))
            img_dord = request.form.get('img_dord'+str(idx))
            img_col = request.form.get('img_col'+str(idx))
            img_title = request.form.get('img_title'+str(idx))
            img_description = request.form.get('img_description_'+str(idx))

            ## Images section of report
            print('IMAGE TITLE IDX: ', idx)
            print('IMAGE SECT ID: ', img_sectid)
            print('IMAGE DORD: ', img_dord)
            print('IMAGE COL: ', img_col)
            print('IMAGE TITLE: ', img_title)
            print('IMAGE DESCRIPTION: ', img_description)

            img_sectids.append(img_sectid)
            img_dords.append(img_dord)
            img_cols.append(img_col)
            img_titles.append(img_title)
            img_descriptions.append(img_description)


        print('IMAGE TITLES: ', img_titles)
        print('IMAGE DESCRIPTIONS: ', img_descriptions)

        session['img_sectids'] = img_sectids
        session['img_dords'] = img_dords
        session['img_cols'] = img_cols
        session['img_titles'] = img_titles
        session['img_descriptions'] = img_descriptions

        writer.file_report()

        report_url = settings.base_url+'gets/report_view.php?reportid='+str(session['report_id'])

        webbrowser.open(str(report_url))

        return redirect('/')

    else :
        return render_template("home.html", user=current_user,)
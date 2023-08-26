
from flask import session
from flask_session import Session

import time
import cursor
import settings

img_urls = []
img_ids = []
img_files = []
img_sectids = []
img_dords = []
img_cols = []
img_titles = []
img_descriptions = []

def process_img_rows(rows) :

    global img_urls, img_ids, img_files, img_sectids, img_dords, img_cols, img_titles, img_descriptions

    img_urls = []
    img_ids = []
    img_files = []
    img_sectids = []
    img_dords = []
    img_cols = []
    img_titles = []
    img_descriptions = []

    img_urls = session['img_urls']
    img_ids = session['img_ids']
    img_files = session['img_files']
    img_sectids = session['img_sectids']
    img_dords = session['img_dords']
    img_cols = session['img_cols']
    img_titles = session['img_titles']
    img_descriptions = session['img_descriptions']


    for idx, img in enumerate(rows) :
        
        img_id = img[0]
        img_ids.append(img_id)

        img_file = img[2]
        img_files.append(img_file)

       ##AUTOMATICALLY FILL IN TEMPLATE IMAGE INFORMATION
        test_template = session['test_template']
        test_template = str(test_template)

        if test_template != '' and img_file[0].isdigit() and not img_file[1].isdigit() :

            index = int(img_file[0])
            image_templates = settings.image_templates

            for image_template in image_templates :

                test_template = session['test_template']

                if str(image_template.tag) == str(test_template) :

                    print('READER TIMG TEMPLATE NAME MATCHES TEST TEMPLATE')

                    if int(image_template.dord) == int(index) :

                        print('READER TIMG FOUND IMAGE TEMPLATE')
                        #img_sectids[int(index)-1] = session['img_sectid']
                        print('READER TIMG index', index)
                        #print('READER TIMG session[img_dords]', session['img_dords'])

                        img_title = img[19]
                        if img_title == 'NULL' or img_title == '' : 
                            img_title = img[2].replace(".JPG","").replace(".PNG","").title()

                        if img_title[0].isdigit() and not img_title[1].isdigit() :
                            img_title = img_title[1:].strip()

                        if image_template.title != '' :
                            img_title = image_template.title
                        img_titles.append(img_title)

                        img_sectid = session['summary_sect_id']
                        img_sectids.append(img_sectid)

                        img_dord = image_template.dord
                        img_dords.append(img_dord)
                        #print('READER TIMG img_dords[int(index)-1] ', img_dords[int(index)-1])

                        img_col = image_template.col
                        img_cols.append(img_col)

                        #print('READER TIMG img_cols[int(index)-1]', img_cols[int(index)-1])

                        img_description = image_template.description
                        img_descriptions.append(img_description)

                        #print('READER TIMG img_descriptions[int(index)-1]', img_descriptions[int(index)-1])

        else :

            img_title = img[19]
            if img_title == 'NULL' or img_title == '' : 
                img_title = img[2].replace(".JPG","").replace(".PNG","").title()

            if img_title[0].isdigit() and not img_title[1].isdigit() :
                img_title = img_title[1:].strip()
            img_titles.append(img_title)

            img_sectid = img[10]
            img_sectids.append(img_sectid)

            img_dord = img[17]
            img_dords.append(img_dord)

            img_col = img[18]
            img_cols.append(img_col)

            img_description = img[20]
            if img_description == 'NULL' :
                img_description = 'We found no associated description. This image requires a description.'
            img_descriptions.append(img_description)
        
        


        file_path = img_file.replace('#','%23')
        img_url = settings.base_url + 'gets/SO/' + str(session['so_num']) + '/' + str(file_path)
        img_urls.append(img_url)

        print('TIMG URL: ', img_url)

        session['img_urls'] = img_urls
        session['img_ids'] = img_ids
        session['img_files'] = img_files
        session['img_sectids'] = img_sectids
        session['img_dords'] = img_dords
        session['img_cols'] = img_cols
        session['img_titles'] = img_titles
        session['img_descriptions'] = img_descriptions

 



def clear_session_images() :

    session['img_urls'] = []
    session['img_ids'] = []
    session['img_files'] = []
    session['img_sectids'] = []
    session['img_dords'] = []
    session['img_cols'] = []
    session['img_titles'] = []
    session['img_descriptions'] = []

def get_images() :

    global img_urls, img_ids, img_files, img_sectids, img_dords, img_cols, img_titles, img_descriptions

    img_urls = []
    img_ids = []
    img_files = []
    img_sectids = []
    img_dords = []
    img_cols = []
    img_titles = []
    img_descriptions = []


    session['img_urls'] = []
    session['img_ids'] = []
    session['img_files'] = []
    session['img_sectids'] = []
    session['img_dords'] = []
    session['img_cols'] = []
    session['img_titles'] = []
    session['img_descriptions'] = []

    clear_session_images()

    summary_sect_id = session['summary_sect_id']

    print('GET IMAGES summary_sect_id: ', summary_sect_id)

    report_id = session['report_id']

    print('FIND TIMG REPORT_ID: ', str(report_id))
    print('FIND TIMG summary_sect_id: ', str(summary_sect_id))

    #time.sleep(1)

    cmdStr = "SELECT * FROM gets.timg WHERE reportid='"+str(report_id)+"' AND sectid='0' ORDER BY imgid DESC LIMIT 50;"
    print('CMD STRING: ', cmdStr)
    cursor.cur.execute(cmdStr)
    img_rows = cursor.cur.fetchall()
    cursor.con.commit()
    print('FOUND IMAGE ROWS: ', img_rows)

    image_rows = []
    for idx, img_row in enumerate(img_rows) :
        image_rows.append(img_row)

    #process_img_rows(img_rows)

    time.sleep(1)

    cmdStr = "SELECT * FROM gets.timg WHERE reportid='"+str(report_id)+"' AND sectid='"+str(summary_sect_id)+"' ORDER BY imgid DESC LIMIT 50;"
    print('CMD STRING: ', cmdStr)
    cursor.cur.execute(cmdStr)
    img_rows = cursor.cur.fetchall()
    cursor.con.commit()
    print('FOUND IMAGE ROWS: ', img_rows)
    
    for idx, img_row in enumerate(img_rows) :
        image_rows.append(img_row)

    process_img_rows(image_rows)

    #time.sleep(1)

prod_url = 'http://192.168.150.1/'
dev_url = 'http://192.168.150.11/'

base_url = ''
prod = True


prod_port = 5050
dev_port = 5000


host = 'localhost'
port = 5000

section_names = []

class test_template :
    def __init__(self, tag, name, section, asset, summary) :
        self.tag = tag
        self.name = name
        self.section = section
        self.asset = asset
        self.summary = summary


class img_template :
    def __init__(self, tag, name, section, title, col, dord, description) :
        self.tag = tag
        self.name = name
        self.section = section
        self.title = title
        self.col = col
        self.dord = dord
        self.description = description


test_templates = []
image_templates = []


def init() :

    global base_url, port, section_names, test_templates, image_templates


    if prod == True :
        base_url = prod_url
        port = prod_port
    else :
        base_url = prod_url
        port = dev_port

    section_names.append('electrical')

    ## Test Templates
    ### No Template make best guess
    tag = 'None'
    name = 'None'
    section = 'None'
    asset = ''
    summary = ''
    test_templates.append( test_template(tag, name, section, asset, summary) )

    ### Curve Tracer Test Template
    tag = 'ct'
    name = 'curve tracer'
    section = 'electrical'
    asset = '161'
    summary = "Tested 10 via pin correlation at 25C using Curve Tracer method. \nPassed: 10. \nPower's applied to DUT to check for current surge at 25C."
    test_templates.append( test_template(tag, name, section, asset, summary) )

    ### ABI Test Template
    tag = 'abi'
    name = 'abi'
    section = 'electrical'
    asset = '161,41'
    summary = "Tested 10 via pin correlation at 25C using Sentry Counterfeit Detection method. \nPassed: 10. \nPower's applied to DUT to check for current surge at 25C."
    test_templates.append( test_template(tag, name, section, asset, summary) )
    
    ### Logic Test Template
    tag = 'lt'
    name = 'logic'
    section = 'electrical'
    asset = '68'
    summary = "Tested 10 functionally at 25C via verify the DUT's truth table. \nPassed: 10."
    test_templates.append( test_template(tag, name, section, asset, summary) )



    ## Curve Tracer Image Templates
    tag = 'ct'
    name = 'curve tracer'
    section = 'electrical'
    title = ''
    description = "DUT pin diagram."
    col = 2
    dord = 1
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )
    
    tag = 'ct'
    name = 'curve tracer'
    section = 'electrical'
    title = ''
    description = "Applied power to DUT to check for current surge at 25C. \nPASS!"
    col = 2
    dord = 2
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'ct'
    name = 'curve tracer'
    section = 'electrical'
    title = ''
    description = "Non-existed internal connection from DUT via pins correlation test at 25˚C by Curve Trace method. \nPASS!"
    col = 2
    dord = 3
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )


    ## ABI Image Templates
    tag = 'abi'
    name = 'abi'
    section = 'electrical'
    title = ''
    description = "DUT pin diagram."
    col = 2
    dord = 1
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'abi'
    name = 'abi'
    section = 'electrical'
    title = ''
    description = "Applied power to DUT to check for current surge at 25C. \nPASS!"
    col = 2
    dord = 2
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'abi'
    name = 'abi'
    section = 'electrical'
    title = ''
    description = "Non-existed internal connection from DUT via pins correlation test at 25˚C by Curve Trace method. \nPASS!"
    col = 2
    dord = 3
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'abi'
    name = 'abi'
    section = 'electrical'
    title = ''
    description = "DUT signatures tested using Sentry Counterfeit Detection method. \nPASS!"
    col = 2
    dord = 4
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )



    ## Logic Test Image Templates
    tag = 'lt'
    name = 'logic'
    section = 'electrical'
    title = 'PINOUT'
    col = 2
    dord = 1
    description = "DUT pin diagram."
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'lt'
    name = 'logic'
    section = 'electrical'
    title = 'REFERENCE'
    col = 2
    dord = 2
    description = "Truth table reference illustrating the function logic."
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )

    tag = 'lt'
    name = 'logic'
    section = 'electrical'
    title = 'RESULT'
    col = 2
    dord = 3
    description = "Result of vector test. \nPass!"
    image_templates.append( img_template(tag, name, section, title, col, dord, description) )
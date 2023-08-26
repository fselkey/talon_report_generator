function deleteNote(note_id) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ note_id: note_id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteOrder(order_id) {
  fetch("/delete-order", {
    method: "POST",
    body: JSON.stringify({ order_id: order_id }),
  }).then((_res) => {
    window.location.href = "/orders";
  });
}

function deleteTrack(track_id) {
  fetch("/delete-track", {
    method: "POST",
    body: JSON.stringify({ track_id: track_id }),
  }).then((_res) => {
    window.location.href = "/tracks";
  });
}



function setAllColumns(img_files, section, column) {

  numColumn = parseInt(column) - 1;
  numSection = parseInt(section) - 1;

  console.log('set all sections called: ', numSection);
  console.log('set all columns called: ', numColumn);

  console.log('set all columns img_files: ', img_files);

  let files = img_files.replace("[", '');
  console.log('replace [ all columns files: ', files);

  files = files.replace("]", '');
  console.log('replace ] all columns files: ', files);

  files = files.replaceAll("'", '');
  console.log('replace quotes all columns files: ', files);

  files = files.split(', ');
  console.log('split all columns files , : ', files);

  console.log('length of img files to set columns: ', files.length);
  console.log('Setting number of columns: ', numColumn);


  for(let i=0; i<files.length; i++) {

    let sectId = 'img_sectid'+i;
    console.log('Setting section element id: ', sectId);

    let colId = 'img_col'+i;
    console.log('Setting columns element id: ', colId);

    var section_element = document.getElementById(sectId);
    section_element.options[numSection].selected = true;

    var column_element = document.getElementById(colId);
    column_element.options[numColumn].selected = true;
  }

}


function check_image(imageId) {

  console.log('check image id: ', imageId);

  let checkId = 'img'+imageId;
  let sectId = 'img_sectid'+imageId;
  let colId = 'img_col'+imageId;


  var check_element = document.getElementById(checkId);
  //console.log('CHECKBOX VALUE: ', check_element.value);
  console.log('CHECKBOX CHECKED: ', check_element.checked);
  if(check_element==true) {
    conformImage(sectId, )
  }

}

function deselectImage(sectId, colId, dordId, textareaId) {

  var section_element = document.getElementById(sectId);
  section_element.options[0].selected = true;
  
  var column_element = document.getElementById(colId);
  column_element.options[0].selected = true;

  var dord_element = document.getElementById(dordId);
  dord_element.value = 1;

  var textarea_element = document.getElementById(textareaId);
  textarea_element.value = 'None'
}

function setImageColumn(colId, column) {

  numColumn = column - 1;

  console.log('image column selected by ID: ', colId);
  console.log('setting number of columns: ', column);

  var column = document.getElementById(colId);
  column.options[numColumn].selected = true;

}

function conformImage(sectId, section, colId, column) {

  console.log('conform image called.');

  numSection = parseInt(section) - 1;
  numColumn = parseInt(column) - 1;

  console.log('conform image section: ', section);

  console.log('image section selected by ID: ', sectId);
  console.log('setting section number: ', numSection);

  console.log('image column selected by ID: ', colId);
  console.log('setting number of numColumn: ', column);

  var section_element = document.getElementById(sectId);
  section_element.options[numSection].selected = true;
  
  var column_element = document.getElementById(colId);
  column_element.options[numColumn].selected = true;
}


function swap_img_template(image_index, description_index, section, column, order) {

  console.log('swap img template section number: ', section);
  console.log('swap img template column: ', column);
  console.log('swap img template order dorder: ', order)
  numSection = parseInt(section) - 1;
  numColumn = parseInt(column) - 1;
  //numOrder = parseInt(order);


  console.log('SWAP IMG SUMMARY IMAGE: ', image_index);

  //description_index = description_index - 1;
  console.log('SWAP IMG SUMMARY WITH TEMPLATE: ', description_index);

  var img_textarea_id = 'img_description_'+image_index;
  img_textarea_id.toString();
  var img_textarea_element = document.getElementById(img_textarea_id);
  
  var img_template_id = 'img_template_'+description_index;
  img_template_id.toString();
  var img_template_element = document.getElementById(img_template_id);
  img_textarea_element.value = '';
  img_textarea_element.value = img_template_element.value;

  var img_sect_id = 'img_sectid' + image_index;
  img_sect_id.toString();
  var img_sect_element = document.getElementById(img_sect_id);
  img_sect_element.options[numSection].selected = true;

  var img_col_id = 'img_col' + image_index;
  img_col_id.toString();
  var img_col_element = document.getElementById(img_col_id);
  img_col_element.options[numColumn].selected = true;
  
  var img_dord_id = 'img_dord' + image_index;
  img_dord_id.toString();
  var img_dord_element = document.getElementById(img_dord_id);
  img_dord_element.value = order;

}

function swap_summary(index) {

  console.log('SWAP SUMMARY WITH QUICK MSG: ', index);

  var summary_textarea_id = 'summary_textarea';
  var summary_textarea_element = document.getElementById(summary_textarea_id);
  
  var quick_message_id = 'msg';
  quick_message_id = quick_message_id+index;

  console.log('SWAP SUMMARY QUICK MESSAGE ID', quick_message_id);

  var quick_message_element = document.getElementById(quick_message_id);
  summary_textarea_element.value = '';
  summary_textarea_element.value = quick_message_element.value;
}

function swap_original_summary(index) {

  console.log('SWAP SUMMARY WITH QUICK MSG: ', index);

  var summary_textarea_id = 'summary_textarea';
  var summary_textarea_element = document.getElementById(summary_textarea_id);
  
  var quick_message_id = 'oqmsg';
  quick_message_id = quick_message_id+index;

  console.log('SWAP SUMMARY QUICK MESSAGE ID', quick_message_id);
  
  var quick_message_element = document.getElementById(quick_message_id);
  summary_textarea_element.value = '';
  summary_textarea_element.value = quick_message_element.value;
}



function autoSelectTemplate(row, templates) {
  console.log('ATTEMPTING TO AUTO SELECT YOUR TEMPLATE', templates);
  console.log('typeof(templates)', typeof(templates));

  templates = templates.replace('[', '').replace(']', '').replaceAll("'", "").replaceAll('"', '').replaceAll('&#39;', '');
  console.log('templates replace: ', templates);
  templates = templates.split(', ');

  console.log('ATTEMPTING TO AUTO SELECT YOUR TEMPLATE', templates);
  console.log('typeof(templates)', typeof(templates));

  for (index=0; index<templates.length; index++) {

    console.log('ROW templates[index]: ', templates[index]);
    console.log('ROW typeof templates[index]: ', typeof(templates[index]));

    console.log('ROW ', row);
    console.log('ROW: ', typeof(row));

    row = row.toString().toLowerCase();

    if (row.includes(templates[index].toString().toLowerCase())) {

      console.log('FOUND TEMPLATE: ', templates[index]);

      template_id = 'test_template'
      template_element = document.getElementById(template_id)
      template_element.options[index].selected = true;
    }
  }
}


function testFunction() {

  if (document.title == 'Report') {

    console.log('TEST FUNCTION WORKS!!');
    
  }
}

function oneClickProtection() {

  var submit_button_element = document.getElementById("submit-button");
  submit_button_element.disabled = true;
}

window.onload = testFunction();
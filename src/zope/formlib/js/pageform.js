function toggleFormFieldHelp(ob,state) {
  // ob is the label element
  var field = findWidgetDiv(ob);
  if (field) {
    field.style.visibility = state && 'hidden' || 'visible';
    var help = document.getElementById("field-help-for-" + ob.htmlFor);
    if (help) {
      help.style.visibility = state && 'visible' || 'hidden';
    }
  }
}

function findWidgetDiv(label) {
  var element = findFormField(label);
  while (element) {
    element = element.parentNode;
    if (element.tagName == 'DIV' && element.getAttribute('class') == 'widget')
      return element;
  }
}

function findFormField(label) {
  var name = label.htmlFor;
  var field = label.form[name];
  // Multiple fields with the same name, such as radiobuttons
  if (field) {
    if (field.length)
      field = field[0];
    return field;
  }
  // No field with the exact name; find one that starts with the name
  for (var i = 0; field = label.form[i++];) {
    if (field.name.substr(0, name.length) == name)
      return field;
  }
}

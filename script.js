// word\t(left,top,width,height)\n


function js_function(value) {
    let output = window.location.href + '\n';
    let spans = document.getElementsByTagName('span');
    for(i = 0; i < spans.length; i++) {
        if (spans[i].innerText.match(/^[a-zA-Z0-9]+/)) {
            let word = spans[i].innerText
            let rect = spans[i].getBoundingClientRect()
            output += word + '\t(' + rect.left + ',' + rect.top + ',' + rect.width + ',' + rect.height + ')\n'
        }
        
    }
    py_function(output, js_callback);
}
function js_callback(value, py_callback) {
    py_callback('');
}
// Hide unwanted elements
(function() {
    let spans = document.getElementsByTagName("span");
    for (i = 0; i < spans.length; i++) {
        if (!spans[i].innerText.match(/^[a-zA-Z0-9]+/)) {
            continue;
        }
        let spanRect = spans[i].getBoundingClientRect()
        let divRect = spans[i].parentNode.parentNode.getBoundingClientRect()
        if (!(spanRect.top <= divRect.top + divRect.height &&
            spanRect.left <= divRect.left + divRect.width &&
            spanRect.top + spanRect.height <= divRect.top + divRect.height &&
            spanRect.left + spanRect.width <= divRect.left + divRect.width)) {
                spans[i].setAttribute("style", "display: none;");
        }
    }
})();


// word\t(left,top,width,height)\n
function get_data_txt() {
    let output = window.location.href + '\n';
    let spans = document.getElementsByTagName('span');
    for(i = 0; i < spans.length; i++) {
        let spanRect = spans[i].getBoundingClientRect()
        let divRect = spans[i].parentNode.parentNode.getBoundingClientRect()
        if (spans[i].style.display !== 'none' &&
            spans[i].innerText.match(/^[a-zA-Z0-9]+/)) {
                let word = spans[i].innerText
                output += word + '\t(' + Math.round(spanRect.left) + ',' + Math.round(spanRect.top) + ',' + Math.round(spanRect.width) + ',' + Math.round(spanRect.height) + ')\n'
        }
    }
    save_data(output);
    // console.log(output);
}

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
        // console.log(divRect);
        if (spanRect.top <= divRect.top + divRect.height &&
            spanRect.left <= divRect.left + divRect.width &&
            spanRect.top + spanRect.height <= divRect.top + divRect.height &&
            spanRect.left + spanRect.width <= divRect.left + divRect.width &&
            spans[i].innerText.match(/^[a-zA-Z0-9]+/)) {
                let word = spans[i].innerText
                output += word + '\t(' + Math.round(spanRect.left) + ',' + Math.round(spanRect.top) + ',' + Math.round(spanRect.width) + ',' + Math.round(spanRect.height) + ')\n'
        }
    }
    save_data(output);
    // console.log(output);
}

function get_data_csv() {

    let output = ''

    // reduce Path to relevant info
    let pathList = window.location.href.split('/');
    let htmlIndex = Number.MAX_SAFE_INTEGER;
    let path = ''
    for(i = 0; i < pathList.length; i++) {
        if (pathList[i] === 'html')
            htmlIndex = i;
        if (i > htmlIndex)
            path += pathList[i].endsWith('.html') ? pathList[i].replace('.html', '') : pathList[i] + '/'
    }
    // retrieve the data
    let spans = document.getElementsByTagName('span');
    for(i = 0; i < spans.length; i++) {
        let rect = spans[i].getBoundingClientRect()
        if (rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth) &&
            spans[i].innerText.match(/^[a-zA-Z0-9]+/)) {

            output += path
            output += ','
            output += spans[i].innerText
            output += ','
            output += Math.round(rect.left)
            output += ','
            output += Math.round(rect.top)
            output += ','
            output += Math.round(rect.width)
            output += ','
            output += Math.round(rect.height)
            output += '\n'
        }
    }
    save_data(output);
}
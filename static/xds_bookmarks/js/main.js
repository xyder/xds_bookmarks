function cancel(e) {
    if (e.preventDefault) e.preventDefault(); // required by FF + Safari
    e.dataTransfer.dropEffect = 'copy'; // tells the browser what drop effect is allowed here
    return false; // required by IE
}

function addEvent(to, type, fn) {
    if (document.addEventListener) {
        to.addEventListener(type, fn, false);
    } else if (document.attachEvent) {
        to.attachEvent('on' + type, fn);
    } else {
        to['on' + type] = fn;
    }
}

class Panel {
    constructor(title, height, width) {
        this.height = typeof height === 'undefined' ? 100 : height;
        this.width = typeof width === 'undefined' ? 100 : width;

        this.title = typeof title === 'undefined' ? '' : title;

        this.create_element();
    }

    create_element() {
        this.$panel = $('<div>', {class: 'panel panel-default'});
        this.$panel_head = $('<div>', {class: 'panel-heading'});
        this.$panel_body = $('<div>', {class: 'panel-body'});
        this.$panel_footer = $('<div>', {class: 'panel-footer'});
        this.$panel_title = $('<h3>', {class: 'panel-title'});

        this.$panel_title.html(this.title);
        this.$panel_head.append(this.$panel_title);
        this.$panel
            .append(this.$panel_head)
            .append(this.$panel_body)
            .append(this.$panel_footer);
    }
}

function main() {
    var drop = document.querySelector('#drop');

    // enable 'drop' on this target
    addEvent(drop, 'dragover', cancel);
    addEvent(drop, 'dragenter', cancel);

    addEvent(drop, 'drop', function (e) {
        if (e.preventDefault) e.preventDefault(); // stop browser from redirecting to text

        drop.innerHTML = '<ul></ul>';

        var li = document.createElement('li');

        if (e.dataTransfer.types) {
            li.innerHTML = '<ul>';

            [].forEach.call(e.dataTransfer.types, function (type) {
                li.innerHTML += '<li>' + e.dataTransfer.getData(type)
                    + ' (content-type: ' + type + ')' + '</li>';
            });
            li.innerHTML += '</ul>';
        } else {
            // IE doesn't have .types property
            li.innerHTML = e.dataTransfer.getData('Text');
        }
        var ul = drop.querySelector('ul');

        if (ul.firstChild) {
            ul.insertBefore(li, ul.firstChild);
        } else {
            ul.appendChild(li);
        }

        return false;
    });
}

// start things off
$(document).ready(main);

var lessons = {};

var items = document.querySelectorAll('[data-tags]');
for (var i = 0; i < items.length; i++) {
    var tags = items[i].getAttribute('data-tags').split(' ');

    lessons[items[i].id] = tags;
}

function fuzzyFromString(str) {
    var fuse = new Fuse(Object.keys(lessons).map(function(key) {
        return {
            item: key,
            tags: lessons[key]
        };
    }), {
        keys: ['tags']
    });

    return fuse.search(str);
}

var search = document.getElementById('search');

search.addEventListener('input', function() {
    if (search.value === '') {
        var items = document.querySelectorAll('[data-tags]');
        for (var i = 0; i < items.length; i++) {
            items[i].style.display = 'block';
        }

        return;
    }

    var results = fuzzyFromString(search.value);

    var ids = results.map(function(result) {
        return result.item.item;
    });

    var items = document.querySelectorAll('[data-tags]');
    for (var i = 0; i < items.length; i++) {
        if (ids.indexOf(items[i].id) !== -1) {
            items[i].style.display = 'block';
            continue;
        }

        items[i].style.display = 'none';
    }
});
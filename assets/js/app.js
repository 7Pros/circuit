(function () {
    $.material.init();
})();

Vue.config.delimiters = ['(%', '%)'];

var PostCreate = new Vue({
    el: '#post_create',
    data: {
        content: null
    }
});

var users = [
    { value: 'MetalMatze', data: '1' },
    { value: 'Gjum', data: '2' },
    { value: 'Juan', data: '3' }
];

$('.autocomplete').autocomplete({
    lookup: users,
    onSelect: function (suggestion) {
        alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }
});

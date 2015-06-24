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

$('.autocomplete').autocomplete({
     serviceUrl: '/users/search',
    onSelect: function (suggestion) {
        alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }
});

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


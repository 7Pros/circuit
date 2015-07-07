var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');

gulp.task('default', [
    'copy',
    'css',
    'js'
]);

gulp.task('css', function () {
    return gulp.src([
        './assets/less/app.less',
        './assets/vendor/animate-css/animate.css'
    ])
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('./circuit/static/css'));
});

gulp.task('css', ['less'], function () {
    return gulp.src([
        './circuit/static/css/app.css',
        './assets/vendor/wow/css/libs/animate.css'
    ])
        .pipe(concat('app.css'))
        .pipe(gulp.dest('./circuit/static/css'))
});

gulp.task('js', function () {
    return gulp.src([
        './assets/vendor/jquery/dist/jquery.js',
        './assets/vendor/bootstrap/dist/js/bootstrap.js',
        './assets/vendor/bootstrap-material-design/dist/js/material.js',
        './assets/vendor/bootstrap-material-design/dist/js/ripples.js',
        './assets/vendor/vue/dist/vue.js',
        './assets/vendor/devbridge-autocomplete/dist/jquery.autocomplete.js',
        './assets/js/app.js',
        './assets/vendor/wow/dist/wow.js'
    ])
        .pipe(concat('app.js'))
        .pipe(concat('wow.js'))
        .pipe(gulp.dest('./circuit/static/js'))
});

gulp.task('copy', function () {
    return gulp.src('assets/vendor/bootstrap-material-design/fonts/*')
        .pipe(gulp.dest('./circuit/static/fonts'));
});

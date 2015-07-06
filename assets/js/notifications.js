// Ask the browser for permission to show notifications
// Taken from https://developer.mozilla.org/en-US/docs/Web/API/Notification/Using_Web_Notifications
//window.addEventListener('load', function () {
//    Notification.requestPermission(function (status) {
//        // This allows to use Notification.permission with Chrome/Safari
//        if (Notification.permission !== status) {
//            Notification.permission = status;
//        }
//    });
//});


// Subscribe once swampdragon is connected
swampdragon.open(function () {
    var userId = $("#user_id").val();
    swampdragon.subscribe('notifications', 'notifications');
});

// This is the list of notifications
var notificationsList = document.getElementById("notifications");


// New channel message received
swampdragon.onChannelMessage(function (channels, message) {
    var userId = $("#user_id").val();
    console.log(userId, message.data.user);
    console.log(message.action);
    if (message.action === "created" && message.data.user == userId) {
        console.log('inside if');
        // Update badges
        upgradeBadge();
        // Add the notification
        addNotification((message.data));
    }
});

function upgradeBadge() {
    var badgeValue = document.getElementById('badge');
    badgeValue.innerHTML = parseInt(badgeValue.innerHTML) + 1;
};

function formatDate(date) {
    var month = ['',
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'];
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return month[date.getMonth() + 1] + " " + date.getDate() + ", " + date.getFullYear() + ", " + strTime;
};

// Add new notifications
function addNotification(notification) {

    // If we have permission to show browser notifications
    // we can show the notifiaction
    // TODO: fix double notifications
    //if (window.Notification && Notification.permission === "granted") {
    //    new Notification(notification.message);
    //} else {
        console.log('hier pnotify');
        // TODO: personalize
            var browserNotification = new PNotify({
                text: notification.message,
                type: 'info',
                styling: 'bootstrap3',
                hide: 'false',
                delay: '5000',
                opacity: .6
            });
        browserNotification.get().click(function (e) {
            if ($(e.target).is('.ui-pnotify-closer *, .ui-pnotify-sticker *')) {
                return;
            }
            window.location.replace('/users/notification/' + notification.pk + '/see/');
        });
    //}

    console.log('hier notification');
    // Add the new notification elements
    var buttonNotification = document.createElement("button"),
        divRowUp = document.createElement("div"),
        divRowDown = document.createElement("div"),
        divStatus = document.createElement("div"),
        spanLabel = document.createElement("span"),
        hr = document.createElement("hr"),
        smallCreatedAt = document.createElement("small"),
        pCreatedAt = document.createElement("p"),
        divContent = document.createElement("div");

    var creationDateUnformatted = new Date(notification.created_at),
        creationDateFormatted = formatDate(creationDateUnformatted);

    //setting attributes to text content
    divContent.setAttribute('class', 'col-xs-10');
    divContent.innerHTML = notification.message;

    //setting attributes to label
    spanLabel.setAttribute('class', 'badge label-info');
    spanLabel.innerHTML = '·';

    //setting attributes to status label's col and adding label to it
    divStatus.setAttribute('class', 'col-xs-1');
    divStatus.insertBefore(spanLabel, divStatus.firstChild);

    //setting attributes to row and adding content and status label
    divRowUp.setAttribute('class', 'row bg-info');
    divRowUp.insertBefore(divContent, divRowUp.firstChild);
    divRowUp.insertBefore(divStatus, divRowUp.firstChild);


    pCreatedAt.innerHTML = creationDateFormatted;
    pCreatedAt.setAttribute('class', 'bg-info');
    //adding p to small for the creation date
    smallCreatedAt.setAttribute('class', 'col-xs-offset-2 col-xs-10 text-right');
    smallCreatedAt.insertBefore(pCreatedAt, smallCreatedAt.firstChild);

    divRowDown.setAttribute('class', 'row bg-info');
    divRowDown.insertBefore(smallCreatedAt, divRowDown.firstChild);

    //setting attributes to button and adding elements
    buttonNotification.setAttribute('class', 'list-group-item list-group-item-info');
    buttonNotification.setAttribute('type', 'button');
    buttonNotification.setAttribute('onclick', 'window.location.replace("/users/notification/' + notification.pk + '/see/")');

    //insert everything to the right place
    buttonNotification.insertBefore(divRowDown, buttonNotification.firstChild);
    buttonNotification.insertBefore(divRowUp, buttonNotification.firstChild);

    hr.style.marginTop = '0px';
    hr.style.marginBottom = '0px';
    notificationsList.insertBefore(hr, notificationsList.children[2]);
    notificationsList.insertBefore(buttonNotification, notificationsList.children[2]);

    // Remove excess notifications
    while (notificationsList.getElementsByTagName("button").length > 42) {
        notificationsList.getElementsByTagName("button")[41].remove();
        notificationsList.getElementsByTagName("button")[40].remove();
    }
}
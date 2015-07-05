// Ask the browser for permission to show notifications
// Taken from https://developer.mozilla.org/en-US/docs/Web/API/Notification/Using_Web_Notifications
window.addEventListener('load', function () {
    Notification.requestPermission(function (status) {
        // This allows to use Notification.permission with Chrome/Safari
        if (Notification.permission !== status) {
            Notification.permission = status;
        }
    });
});


// Subscribe once swampdragon is connected
swampdragon.open(function () {
    swampdragon.subscribe('notifications', 'notifications');
});

// This is the list of notifications
var notificationsList = document.getElementById("notifications");


// New channel message received
swampdragon.onChannelMessage(function (channels, message) {
    if (message.action === "created") {
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

// Add new notifications
function addNotification(notification) {

    // If we have permission to show browser notifications
    // we can show the notifiaction
    if (!(window.Notification && Notification.permission === "granted")) {
        new Notification(notification.message);
    } else {
        // TODO: personalize
        var stack_topright = {"dir1": "down", "dir2": "left"},
            browserNotification = new PNotify({
                text: notification.message,
                type: 'info',
                styling: 'bootstrap3',
                hide: 'true',
                delay: '5000',
                opacity: .6,
                addclass: 'stack-topright',
                stack: stack_topright,
            });
        browserNotification.get().click(function(e){
            if ($(e.target).is('.ui-pnotify-closer *, .ui-pnotify-sticker *')) {
                 return;
            }
            window.location.replace('/users/notification/'+notification.pk+'/see/');
        });
    }

    // Add the new notification elements
    var buttonNotification = document.createElement("button"),
        divRow = document.createElement("div"),
        divStatus = document.createElement("div"),
        spanLabel = document.createElement("span"),
        hr = document.createElement("hr"),
        smallCreatedAt = document.createElement("small"),
        pCreatedAt = document.createElement("p"),
        divContent = document.createElement("div");

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
    divRow.setAttribute('class', 'row bg-info');
    divRow.insertBefore(divContent, divRow.firstChild);
    divRow.insertBefore(divStatus, divRow.firstChild);

    pCreatedAt.innerHTML = notification.created_at;
    pCreatedAt.setAttribute('class', 'bg-info');
    //adding p to small for the creation date
    smallCreatedAt.insertBefore(pCreatedAt, smallCreatedAt.firstChild);

    //setting attributes to button and adding elements
    buttonNotification.setAttribute('class', 'list-group-item list-group-item-info');
    buttonNotification.setAttribute('type', 'button');
    buttonNotification.setAttribute('onclick', 'window.location.replace("/users/notification/'+notification.pk+'/see/")');

    //insert everything to the right place
    buttonNotification.insertBefore(divRow, buttonNotification.firstChild);

    notificationsList.insertBefore(hr, notificationsList.nodeValue[3]);
    notificationsList.insertBefore(smallCreatedAt, notificationsList.nodeValue[3]);
    notificationsList.insertBefore(buttonNotification, notificationsList.nodeValue[3]);

    // Not needing this yet
    //// Remove excess notifications
    //while (notificationsList.getElementsByTagName("li").length > 5) {
    //    notificationsList.getElementsByTagName("li")[5].remove();
    //}
}
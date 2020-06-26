function getRandom(max) {
    return Math.floor(Math.random() * Math.floor(max))
}

function getRandomColor() {
    number = getRandom(6);
    switch (number) {
        case 0:
            return ""
        case 1:
            return "success"
        case 2:
            return "danger"
        case 3:
            return "warning"
        case 4:
            return "info"
        case 5:
            return "secondary"
    }
}

function start_long_task() {
    div = $(
      `<div class="task"><div class="row mx-1 justify-content-between"><h5>Task starting</h5><h6>Status: starting</h6></div><div class="progress"><divclass="progress-bar progress-bar-striped bg-${getRandomColor()}" role="progressbar" style="width: 0%;"></div></div></div><hr>`,
    );
    $(".task-list").append(div)

    $.ajax({
        type: "POST",
        url: window.location.pathname,
        success: function(data, status, request) {
            status_url = request.getResponseHeader('location')
            update_progress(status_url)
        }

    })
}

function update_progress(status_url) {
    $.getJSON(status_url, function(data) {
        percent = parseInt(data['current'])
        
    })
}
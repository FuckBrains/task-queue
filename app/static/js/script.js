// html task 
export function getTaskDiv() {
  return $(
    `<div class="task">
            <div class="row mx-1 justify-content-between">
                <h6>Task: <span class="small">unknown</span></h6>
                <h6>Status: <span class="small">starting</span></h6>
            </div>
            <div class="progress">
                <div class="progress-bar progress-bar-striped bg-${getRandomColor()}" role="progressbar" style="width: 0%;">
                </div>
            </div>
            <div class="row justify-content-center">0%</div>
        </div>
        <hr>`,
  );
}

// get random number
export function getRandom(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

// get random color
export function getRandomColor() {
  let number = getRandom(6);
  switch (number) {
    case 0:
      return "";
    case 1:
      return "success";
    case 2:
      return "danger";
    case 3:
      return "warning";
    case 4:
      return "info";
    case 5:
      return "secondary";
  }
}

// update progress of progress bars
export function updateProgress(status_url, status_div) {
  $.getJSON(status_url, function (data) {
    console.log(data)
    let percent = parseInt(data["current"]);
    // status
    $(status_div.children[0].children[1].children[0]).text(data["status"]);
    // id
    $(status_div.children[0].children[0].children[0]).text(data["id"]);
    // percents
    $(status_div.children[2]).text(percent + "%");
    // progress bar
    $(status_div.children[1].children[0]).css("width", percent + "%");

    if (data["state"] != "PENDING" && data["state"] != "PROGRESS") {
    } else {
      setTimeout(() => {
        updateProgress(status_url, status_div);
      }, 1000);
    }
  });
}


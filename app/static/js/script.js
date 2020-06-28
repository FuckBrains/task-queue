if (localStorage.getItem("sendEmail") == null) {
  localStorage.setItem("sendEmail", "[]");
}
let sendEmailArray = JSON.parse(localStorage.getItem("sendEmail"));

if (sendEmailArray != null) {
  sendEmailArray.forEach((url) => {
    div = getTaskDiv();
    updateProgress(url, div[0]);
    $(".task-list").prepend(div);
  });
}

function getTaskDiv() {
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

function getRandom(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function getRandomColor() {
  number = getRandom(6);
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

function updateProgress(status_url, status_div) {
  $.getJSON(status_url, function (data) {
    percent = parseInt(data["current"]);
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

function startEmailSendTask(submit) {
  div = getTaskDiv();
  emailArray = [];
  $(".task-list").prepend(div);
  $(".email-list")
    .children()
    .each(function (index) {
      emailArray.push($(this).val());
      $(this).val("");
    });

  $.ajax({
    type: "POST",
    url: window.location.pathname,
    data: {
      email: emailArray,
      submit: $(`#${submit}`).val(),
      message: $("#message-textarea").val(),
    },
    success: function (data, status, request) {
      $("#message-textarea").val("");
      status_url = request.getResponseHeader("location");
      sendEmailArray.push(status_url);
      localStorage.setItem("sendEmail", JSON.stringify(sendEmailArray));
      updateProgress(status_url, div[0]);
    },
    error: function (request, status, error) {
      alert(request.status + " " + error);
    },
  });
}

function removeEmail() {
  if ($(".email-list").children().length > 1) {
    $(".email-list").children().last().remove();
  }
}

function addEmail() {
  if ($(".email-list").children().length < 5) {
    $(".email-list").append(
      "<input type='email' class='form-control mb-2' name='email' placeholder='Example: user@domain.com'/>",
    );
  }
}

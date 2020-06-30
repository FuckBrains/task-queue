import { getTaskDiv, updateProgress } from "./script.js";

// init local storage
if (localStorage.getItem("sendEmail") == null) {
  localStorage.setItem("sendEmail", "{}");
}

// get local storage task list
let sendEmailDict = JSON.parse(localStorage.getItem("sendEmail"));


// display all previous tasks
if (Object.keys(sendEmailDict) != null) {
  Object.keys(sendEmailDict).forEach((url) => {
    let div = getTaskDiv();
    updateProgress(url, div[0]);
    $(".task-list").prepend(div);
  });
}

// function to start sending email
function startEmailSendTask(submit) {
  let div = getTaskDiv();
  let emailArray = [];
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
      let status_url = request.getResponseHeader("location");
      sendEmailDict[status_url] = null;
      localStorage.setItem("sendEmail", JSON.stringify(sendEmailDict));
      updateProgress(status_url, div[0]);
    },
    error: function (request, status, error) {
      alert(request.status + " " + error);
    },
  });
}

// on click send email instantly
$("#submitIns").click(() => {
  startEmailSendTask("submitIns")
})

// on click send email after 1 minute
$("#submitMin").click(() => {
  startEmailSendTask("submitMin");
});

// on clock remove email field
$("#removeEmail").click(() => {
  if ($(".email-list").children().length > 1) {
    $(".email-list").children().last().remove();
  }
});

// on click add email field
$("#addEmail").click(() => {
  if ($(".email-list").children().length < 5) {
    $(".email-list").append(
      "<input type='email' class='form-control mb-2' name='email' placeholder='Example: user@domain.com'/>",
    );
  }
});

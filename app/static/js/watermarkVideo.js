import { getTaskDiv, updateProgress } from "./script.js";

// init local storage
if (localStorage.getItem("processVideo") == null) {
  localStorage.setItem("processVideo", "[]");
}

// get local storage task list
let processVideoArray = JSON.parse(localStorage.getItem("processVideo"));

// display all previous tasks
if (processVideoArray != null) {
  processVideoArray.forEach((url) => {
    let div = getTaskDiv();
    updateProgress(url, div[0]);
    $(".task-list").prepend(div);
  });
}

$(".custom-file-input").change((e) => {
  let fileName = $("#inputGroupFile02").val().split("\\").pop();
  $(".custom-file-label").text(fileName);
});

$("#inputGroupFileAddon04").click(() => {
  let div = getTaskDiv();
   $(".task-list").prepend(div);

  var formData = new FormData($("#upload-video")[0]);

  $.ajax({
    type: "POST",
    url: window.location.pathname,
    data: formData,
    processData: false,
    contentType: false,
    cache: false,
    success: function (data, status, request) {
      let status_url = request.getResponseHeader("location");
      processVideoArray.push(status_url);
      localStorage.setItem("processVideo", JSON.stringify(processVideoArray));
      updateProgress(status_url, div[0]);
    },
    error: function (request, status, error) {
      alert(request.status + " " + error);
    },
  });
});

document.addEventListener("DOMContentLoaded", () => {

const user = "temp" // Replace this when user auth gets added
const submitAddButton = document.getElementById("submitAdd")

if (!submitAddButton) return

submitAddButton.addEventListener("click", handleSubmit)

function handleSubmit(event) {
    event.preventDefault()

    const taskName = document.getElementById("taskName").value
    const taskDesc = document.getElementById("taskDesc").value
    const dateStart = document.getElementById("dateStart").value
    const dateEnd = document.getElementById("dateEnd").value
    const timeStart = document.getElementById("timeStart").value
    const timeEnd = document.getElementById("timeEnd").value

    const toJson = { // All values as JSON
      "user": user,
      "taskName": taskName,
      "taskDesc": taskDesc,
      "dateStart": dateStart,
      "dateEnd": dateEnd,
      "timeStart": timeStart,
      "timeEnd": timeEnd
    }

    fetch(`${window.location.origin}/api/add/`, {
      method: "POST", // Post API call
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(toJson) // Send JSON
    })
    console.log("Sent")
  }
})
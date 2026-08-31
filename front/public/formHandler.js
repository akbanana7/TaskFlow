document.addEventListener("DOMContentLoaded", () => {

const user = "temp" // Replace this when user auth gets added
const taskName = document.getElementById("taskName")
const taskDesc = document.getElementById("taskDesc")
const dateStart = document.getElementById("dateStart")
const dateEnd = document.getElementById("dateEnd")
const timeStart = document.getElementById("timeStart")
const timeEnd = document.getElementById("timeEnd")
const submitAddButton = document.getElementById("submitAdd")

if (!submitAddButton) return

submitAddButton.addEventListener("click", handleSubmit)

function handleSubmit(event) {
    event.preventDefault()
    fetch(`http://localhost:8000/add/?user=${user}&timeStart=${timeStart.value}&timeEnd=${timeEnd.value}&timeZone=0&dateStart=${dateStart.value}&dateEnd=${dateEnd.value}`)
    console.log("Sent")
  }
})



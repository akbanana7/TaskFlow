document.addEventListener("DOMContentLoaded", () => {
    const user = "temp" // Replace when auth added
    const taskName = document.getElementById("taskSearch")
    const submitButton = document.getElementById("submitRead")

    if (!submitButton) return


submitButton.addEventListener("click", handleSubmit)

function handleSubmit(event) {
    event.preventDefault()
    fetch(`http://localhost:8000/find/?user=${user}&taskName=${taskName.value}`)

}
})
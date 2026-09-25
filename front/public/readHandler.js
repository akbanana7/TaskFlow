document.addEventListener("DOMContentLoaded", () => { // Loads all required HTML elements from the page
    const user = "temp" // Replace when auth added
    const taskName = document.getElementById("taskSearch")
    const submitButton = document.getElementById("submitRead")

    // For displaying task details

    const taskReadName = document.getElementById("taskReadName")
    const taskReadDesc = document.getElementById("taskReadDesc")
    const taskReadDateStart = document.getElementById("taskReadDateStart")
    const taskReadTimeStart = document.getElementById("taskReadTimeStart")
    const taskReadDateEnd = document.getElementById("taskReadDateEnd")
    const taskReadTimeEnd = document.getElementById("taskReadTimeEnd")
    if (!submitButton) return

let array = []
submitButton.addEventListener("click", handleSubmit) // When button, clicked do

async function handleSubmit(event) {
    event.preventDefault()
    const response = await fetch(`http://localhost:8000/find/?user=${user}&taskName=${taskName.value}`)
    if (response.ok) {
        const data = await response.json()
        console.log(data)
        const rawRecord = data.record // Turns it from the http response BS to a "tuple"
        console.log(rawRecord)
        console.log(rawRecord[0],rawRecord[1])
        console.log(typeof(rawRecord)) // Apparently is now a string. Sound
        array = rawRecord.split(",") // Turns recieved data into a JS array
        console.log(array)
        let index = 0
        for (i in array) { // Essentially trim and format recieved data inside of the array
            array[index] = array[index].replace(/[\[\]']/g, "").trim()
            index++
        }
        console.log(array)

        // Set the recieved data to the values of HTML DOM content
        taskReadName.textContent = array[1]
        taskReadDesc.textContent = array[2]
        taskReadDateStart.textContent = array[6]
        taskReadDateEnd.textContent = array[7]
        taskReadTimeStart.textContent = array[3]
        taskReadTimeEnd.textContent = array[4]

    }
}
})
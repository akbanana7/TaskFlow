document.addEventListener("DOMContentLoaded", () => { // Loads all required HTML elements from the page
    const user = "temp" // Replace when auth added
    const taskName = document.getElementById("taskSearch")
    const submitButton = document.getElementById("submitRead")

    const taskReadDiv = document.getElementById("taskDetails")

    if (!submitButton) return

let array = []
submitButton.addEventListener("click", handleSubmit) // When button, clicked do

async function handleSubmit(event) {
    event.preventDefault()
    
    taskReadDiv.replaceChildren()
    const response = await fetch(`${window.location.origin}/api/find/?user=${encodeURIComponent(user)}&taskName=${encodeURIComponent(taskName.value)}`)
    if (response.ok) {
        const data = await response.json()
        console.log(data)
        const record = data.body // Turns it from the http response BS to a tuple
        const finArr = [] // Needed to essentially create a big array to actively and easily chuck stuff out

        
        
        for (i of record) { // Loops through each returned record
            console.log(i)
            const newDiv = document.createElement("div")
            taskReadDiv.appendChild(newDiv)
            let index = 0
            for (j of i) { // Loops through each element of indivdual record
                if (index == 0){ // Basically prevents top element (username) from being displayed.
                    index ++
                }
                else{
                    const toAdd = document.createElement("p") // Creates P element in which element is placed into
                    toAdd.textContent = String(j)
                    newDiv.appendChild(toAdd) // Adds to the div that gets added
                }
            }
        }
        
        console.log("Finished printing to scrn")
    }
}
})
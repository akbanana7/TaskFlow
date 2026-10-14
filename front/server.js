const express = require("express")
const app = express()
const port = 8080 // Please for the love of god figure out a better port

app.use(express.static("public"))


app.listen(port, "0.0.0.0", () => { // make sure it is
    console.log(`Node.js exposed on port ${port}`)
})
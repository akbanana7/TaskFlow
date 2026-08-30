const express = require("express")
const app = express()
const port = 8080 // Please for the love of god figure out a better port

app.use(express.static("public"))

app.get("/", (req,res) =>{
    res.status(200)
})

app.listen(port, () => {
    console.log(`Node.js exposed on port ${port}`)
})
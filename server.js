const express = require("express");
const session = require("express-session");
const { MongoClient, ObjectId } = require("mongodb");

const app = express();
const PORT = 3000;

// MongoDB setup
const url = "mongodb://127.0.0.1:27017";
const client = new MongoClient(url);
let db;

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: "student-secret",
    resave: false,
    saveUninitialized: true
}));

// Start server
async function startServer() {
    try {
        await client.connect();
        db = client.db("SchoolDB");
        console.log("Connected to SchoolDB");

        app.listen(PORT, () => {
            console.log(`Student Portal: http://localhost:${PORT}/student`);
        });
    } catch (err) {
        console.error("Connection error:", err);
    }
}

startServer();

// Display + Form
app.get("/student", async (req, res) => {
    const students = await db.collection("student").find().toArray();

    let rows = students.map(s => `
        <tr>
            <td>${s.rollNo}</td>
            <td>${s.name}</td>
            <td>${s.grade}</td>
            <td>
                <form action="/delete-student/${s._id}" method="POST" style="display:inline;">
                    <button type="submit" style="background:none;border:none;color:red;cursor:pointer;">
                        [Delete]
                    </button>
                </form>
            </td>
        </tr>
    `).join("");

    res.send(`
        <style>
            body {
                font-family: Arial;
                padding: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .form-box {
                margin-bottom: 20px;
            }
            input {
                padding: 8px;
                margin: 5px;
                border: 1px solid #ccc;
            }
            button {
                padding: 8px 12px;
                cursor: pointer;
            }
        </style>

        <h1>Student Management System</h1>

        <div class="form-box">
            <form action="/add-student" method="POST">
                <input name="rollNo" placeholder="Roll Number" required>
                <input name="name" placeholder="Full Name" required>
                <input name="grade" placeholder="Grade" required>
                <button type="submit">Add Student</button>
            </form>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Roll No</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `);
});

// Add student
app.post("/add-student", async (req, res) => {
    const { rollNo, name, grade } = req.body;

    await db.collection("student").insertOne({
        rollNo,
        name,
        grade
    });

    res.redirect("/student");
});

// Delete student
app.post("/delete-student/:id", async (req, res) => {
    const id = req.params.id;

    await db.collection("student").deleteOne({
        _id: new ObjectId(id)
    });

    res.redirect("/student");
});
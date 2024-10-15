const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path"); // Ensure this is imported
const app = express();
const port = 3001; // Use a different port from the frontend (Next.js)

// Enable CORS to allow requests from frontend
app.use(cors());

// Endpoint to serve flagged user reports
app.get("/api/flagged-user", (req, res) => {
  fs.readFile("user_reports_with_flags.json", "utf8", (err, data) => {
    if (err) {
      return res.status(500).send("Error reading report");
    }
    res.json(JSON.parse(data));
  });
});

// Endpoint to get aggregated category scores
app.get("/api/category-report", (req, res) => {
  const filePath = path.join(__dirname, "user_toxicity_report.json"); // Adjust the path as necessary

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error("Error reading file:", err);
      return res.status(500).send("Internal Server Error");
    }

    const userReports = JSON.parse(data);

    // Initialize aggregated scores
    const aggregatedScores = {
      toxic: 0,
      severe_toxic: 0,
      obscene: 0,
      threat: 0,
      insult: 0,
      identity_hate: 0,
    };

    // Loop through each user report to aggregate scores
    userReports.forEach((user) => {
      const { category_scores } = user;
      aggregatedScores.toxic += category_scores.toxic || 0;
      aggregatedScores.severe_toxic += category_scores.severe_toxic || 0;
      aggregatedScores.obscene += category_scores.obscene || 0;
      aggregatedScores.threat += category_scores.threat || 0;
      aggregatedScores.insult += category_scores.insult || 0;
      aggregatedScores.identity_hate += category_scores.identity_hate || 0;
    });

    // Convert the aggregated scores into an array for easier pie chart usage
    const aggregatedCategoryScores = [
      { category: "toxic", total_score: aggregatedScores.toxic },
      { category: "severe_toxic", total_score: aggregatedScores.severe_toxic },
      { category: "obscene", total_score: aggregatedScores.obscene },
      { category: "threat", total_score: aggregatedScores.threat },
      { category: "insult", total_score: aggregatedScores.insult },
      {
        category: "identity_hate",
        total_score: aggregatedScores.identity_hate,
      },
    ];

    // Send aggregated scores as a JSON response
    res.json(aggregatedCategoryScores);
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

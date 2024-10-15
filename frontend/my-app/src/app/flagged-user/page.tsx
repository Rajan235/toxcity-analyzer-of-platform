"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion"; // Adjust the import path if needed

interface Comment {
  comment_id: string;
  content: string;
  categories?: {
    toxic?: number;
    severe_toxic?: number;
    obscene?: number;
    threat?: number;
    insult?: number;
    identity_hate?: number;
  };
}

interface UserReport {
  author_id: string;
  user_id: string;
  toxic_score: number;
  total_toxic_score: number; // Added for the total toxic score
  num_comments: number;
  flag: boolean;
  category_scores: {
    toxic?: number;
    severe_toxic?: number;
    obscene?: number;
    threat?: number;
    insult?: number;
    identity_hate?: number;
  };
  comments: Comment[];
}

const FlaggedUsersPage: React.FC = () => {
  const [userReports, setUserReports] = useState<UserReport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserReports = async () => {
      try {
        const response = await axios.get(
          "http://localhost:3001/api/flagged-user"
        );
        setUserReports(response.data);
      } catch (error) {
        console.error("Error fetching user reports:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserReports();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Handle loading state
  }

  if (!userReports.length) {
    return <div>No flagged users found.</div>; // Handle case when no reports are found
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Flagged Users</h1>
      <Accordion type="multiple">
        {userReports.map((report) => (
          <AccordionItem key={report.author_id} value={report.author_id}>
            <AccordionTrigger>
              <div className="flex justify-between w-full">
                <span>{report.user_id}</span> {/* Display user_id */}
                <span className="font-semibold">
                  Total Toxic Score: {report.total_toxic_score.toFixed(2)}
                </span>
                <span className="font-semibold">
                  Total number of comments: {report.num_comments.toFixed(2)}
                </span>
              </div>
            </AccordionTrigger>
            <AccordionContent>
              <div className="mb-4">
                <h2 className="font-bold">Category Scores:</h2>
                <ul className="list-disc pl-5">
                  <li>
                    Toxic: {report.category_scores?.toxic?.toFixed(2) ?? "N/A"}
                  </li>
                  <li>
                    Severe Toxic:{" "}
                    {report.category_scores?.severe_toxic?.toFixed(2) ?? "N/A"}
                  </li>
                  <li>
                    Obscene:{" "}
                    {report.category_scores?.obscene?.toFixed(2) ?? "N/A"}
                  </li>
                  <li>
                    Threat:{" "}
                    {report.category_scores?.threat?.toFixed(2) ?? "N/A"}
                  </li>
                  <li>
                    Insult:{" "}
                    {report.category_scores?.insult?.toFixed(2) ?? "N/A"}
                  </li>
                  <li>
                    Identity Hate:{" "}
                    {report.category_scores?.identity_hate?.toFixed(2) ?? "N/A"}
                  </li>
                </ul>

                <h2 className="font-bold mt-4">Comments:</h2>
                <ul className="list-disc pl-5">
                  {report.comments && report.comments.length > 0 ? (
                    report.comments.map((comment) => (
                      <li key={comment.comment_id} className="mb-2">
                        <p>
                          <strong>Comment:</strong>{" "}
                          {comment.content ?? "No content available"}
                        </p>
                        <p>
                          <strong>Toxicity Categories:</strong>
                        </p>
                        {comment.categories ? (
                          <ul className="list-inside list-disc">
                            <li>
                              Toxic:{" "}
                              {comment.categories.toxic?.toFixed(2) ?? "N/A"}
                            </li>
                            <li>
                              Severe Toxic:{" "}
                              {comment.categories.severe_toxic?.toFixed(2) ??
                                "N/A"}
                            </li>
                            <li>
                              Obscene:{" "}
                              {comment.categories.obscene?.toFixed(2) ?? "N/A"}
                            </li>
                            <li>
                              Threat:{" "}
                              {comment.categories.threat?.toFixed(2) ?? "N/A"}
                            </li>
                            <li>
                              Insult:{" "}
                              {comment.categories.insult?.toFixed(2) ?? "N/A"}
                            </li>
                            <li>
                              Identity Hate:{" "}
                              {comment.categories.identity_hate?.toFixed(2) ??
                                "N/A"}
                            </li>
                          </ul>
                        ) : (
                          <p>No categories available for this comment.</p>
                        )}
                      </li>
                    ))
                  ) : (
                    <p>No comments available.</p>
                  )}
                </ul>
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};

export default FlaggedUsersPage;

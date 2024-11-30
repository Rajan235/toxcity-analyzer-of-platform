// src/app/page.tsx
"use client";

import { useState, FormEvent } from "react";
import axios from "axios";

// Component to handle comment submission
export default function CommentForm() {
  const [comment, setComment] = useState<string>(""); // State for comment input
  const [userId, setUserId] = useState<string>(""); // State for userId
  const [responseMessage, setResponseMessage] = useState<string>(""); // State for response message

  // Function to handle form submission
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent page refresh on form submit

    try {
      // Send a POST request to the Express backend
      const response = await axios.post("http://localhost:3001/api/comments", {
        comment,
        userId,
      });

      // Handle the response
      if (response.status === 200) {
        setResponseMessage("Comment submitted successfully!");
        setComment(""); // Clear form fields
        setUserId("");
      } else {
        setResponseMessage("Failed to submit comment.");
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        setResponseMessage(`Error: ${error.response?.data || error.message}`);
      } else {
        setResponseMessage("An unknown error occurred.");
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="comment">Comment:</label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            required
          ></textarea>
        </div>
        <div>
          <label htmlFor="userId">User ID:</label>
          <input
            type="text"
            id="userId"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

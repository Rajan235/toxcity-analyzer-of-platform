"use client"; // Mark this component as a client component

import React, { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts"; // Ensure recharts is installed

interface CategoryScore {
  category: string;
  total_score: number;
}

const ToxicityCategoryPieChart: React.FC = () => {
  const [data, setData] = useState<CategoryScore[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:3001/api/category-report"
        );
        const result = await response.json();

        // Format and set data correctly
        const formattedData = result.map((item: any) => ({
          category: item.category, // Map to meaningful category name
          total_score: item.total_score,
        }));

        setData(formattedData);
      } catch (error) {
        console.error("Error fetching category report:", error);
      }
    };

    fetchData();
  }, []);

  // Colors for each category
  const COLORS = [
    "#0088FE", // Blue
    "#00C49F", // Green
    "#FFBB28", // Yellow
    "#FF8042", // Orange
    "#FF45E5", // Pink
    "#FF0099", // Magenta
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">
        Toxicity Category Distribution
      </h2>
      <PieChart width={400} height={400}>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ index }) =>
            `${data[index].category}: ${(
              (data[index].total_score /
                data.reduce((sum, entry) => sum + entry.total_score, 0)) *
              100
            ).toFixed(0)}%`
          }
          outerRadius={80}
          dataKey="total_score"
        >
          {data.map((entry, index) => (
            <Cell key={entry.category} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default ToxicityCategoryPieChart;

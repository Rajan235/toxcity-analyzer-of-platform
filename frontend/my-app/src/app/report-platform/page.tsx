// src/app/report-platform/page.tsx

import React from "react";
import ToxicityCategoryPieChart from "./ToxicityCategoryPieChart"; // Adjust path if necessary

const ReportPlatformPage: React.FC = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Report Platform</h1>
      <ToxicityCategoryPieChart />
    </div>
  );
};

export default ReportPlatformPage;

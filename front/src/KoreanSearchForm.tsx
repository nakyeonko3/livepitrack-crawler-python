import { useState, useEffect } from "react";
import { generateDiseaseDocsFile, getOptions } from "./api";

interface convertFormat {
  dateType: string;
  startDate: string;
  endDate: string;
  region: string;
  disease: string;
  legalGrade: string;
  livestock: string;
}

const convertFormat = (input: convertFormat) => {
  return {
    turmGubun: input.dateType,
    occrFromDt: input.startDate,
    occrToDt: input.endDate,
    ctprvn: input.region,
    dissCl: input.disease,
    lstkspCl: input.livestock,
    legalIctsdGradSe: input.legalGrade,
  };
};

const KoreanSearchForm = () => {
  // Form state
  const [startDate, setStartDate] = useState("2024-03-13");
  const [endDate, setEndDate] = useState("2025-03-13");
  const [dateType, setDateType] = useState("01");
  const [region, setRegion] = useState(""); // Empty string represents '전체'
  const [disease, setDisease] = useState("");
  const [legalGrade, setLegalGrade] = useState("");
  const [livestock, setLivestock] = useState("");
  const [loading, setLoading] = useState(false);

  // Options state
  const [options, setOptions] = useState({
    ctprvn: {},
    dissCl: {},
    legalIctsdGradSe: {},
    lstkspCl: {},
  });

  // Fetch options from API
  useEffect(() => {
    const fetchOptions = async () => {
      const options = await getOptions();
      setOptions(options);
    };
    fetchOptions();
  }, []);

  // Handle form submission
  const handleSubmit = async () => {
    // Prepare data to send
    const formData = {
      dateType,
      startDate,
      endDate,
      region,
      disease,
      legalGrade,
      livestock,
    };

    console.log("Sending request with data:", formData);

    const params = convertFormat(formData);
    setLoading(true);
    const response = await generateDiseaseDocsFile(params);
    setLoading(false);
    console.log("Response:", response);
  };

  const renderOptions = (
    optionsObj: Record<string, string>,
    firstKey: string
  ) => {
    const entries = Object.entries(optionsObj);
    const firstEntry = entries.find(([key]) => key === firstKey);
    const restEntries = entries.filter(([key]) => key !== firstKey);
    return [
      <option key={firstKey} value={firstKey}>
        {firstEntry ? firstEntry[1] : "전체"}
      </option>,
      ...restEntries.map(([key, value]) => (
        <option key={key} value={key}>
          {value}
        </option>
      )),
    ];
  };

  return (
    <div className="w-full max-w-4xl p-4 bg-gray-100 rounded">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        {/* Radio button group */}
        <div className="flex items-center gap-1 mr-2">
          <span className="text-gray-600 mr-1">•</span>
          <span className="text-gray-600">조회기간</span>
          <div className="flex items-center ml-1">
            <input
              type="radio"
              id="range1"
              name="dateRange"
              checked={dateType === "01"}
              onChange={() => setDateType("01")}
              className="mr-1"
            />
            <label htmlFor="range1" className="mr-2">
              진단일
            </label>

            <input
              type="radio"
              id="range2"
              name="dateRange"
              checked={dateType === "02"}
              onChange={() => setDateType("02")}
              className="mr-1"
            />
            <label htmlFor="range2" className="mr-2">
              발생일
            </label>
          </div>
        </div>

        {/* Date inputs */}
        <div className="flex items-center">
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border border-gray-300 px-1 py-0.5 rounded"
          />
          <span className="mx-1">~</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border border-gray-300 px-1 py-0.5 rounded"
          />
        </div>

        {/* Disease dropdown */}
        <div className="flex items-center ml-2">
          <span className="text-gray-600 mr-1">•</span>
          <span className="text-gray-600 mr-1">질병명</span>
          <select
            value={disease}
            onChange={(e) => setDisease(e.target.value)}
            className="border border-gray-300 rounded px-2 py-0.5"
          >
            {renderOptions(options.dissCl, "")}
          </select>
        </div>

        {/* Second dropdown row */}
        <div className="flex flex-wrap items-center gap-2 mt-2">
          <div className="flex items-center">
            <span className="text-gray-600 mr-1">•</span>
            <span className="text-gray-600 mr-1">지역선택</span>
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="border border-gray-300 rounded px-2 py-0.5 w-32"
            >
              {renderOptions(options.ctprvn, "")}
            </select>
          </div>

          <div className="flex items-center ml-2">
            <span className="text-gray-600 mr-1">•</span>
            <span className="text-gray-600 mr-1">축 중</span>
            <select
              value={livestock}
              onChange={(e) => setLivestock(e.target.value)}
              className="border border-gray-300 rounded px-2 py-0.5 w-24"
            >
              {renderOptions(options.lstkspCl, "")}
            </select>
          </div>

          <div className="flex items-center ml-2">
            <span className="text-gray-600 mr-1">•</span>
            <span className="text-gray-600 mr-1">법정전염병별</span>
            <select
              value={legalGrade}
              onChange={(e) => setLegalGrade(e.target.value)}
              className="border border-gray-300 rounded px-2 py-0.5 w-24"
            >
              {renderOptions(options.legalIctsdGradSe, "")}
            </select>
          </div>

          {/* Search button */}
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white px-4 py-1 rounded ml-auto hover:bg-blue-600 disabled:bg-gray-400 disabled:text-gray-600 disabled:cursor-not-allowed"
            disabled={loading}
          >
            다운로드
          </button>
        </div>

        {loading && <Loading />}

        {/* Color indicators */}
        <div className="flex items-center ml-auto mt-2">
          <span className="text-gray-600">법정전염병별 :</span>
          <div className="flex items-center ml-2">
            <div className="w-4 h-4 bg-pink-200 rounded mr-1"></div>
            <span className="text-gray-600 mr-2">1종</span>

            <div className="w-4 h-4 bg-yellow-200 rounded mr-1"></div>
            <span className="text-gray-600 mr-2">2종</span>

            <div className="w-4 h-4 bg-blue-200 rounded mr-1"></div>
            <span className="text-gray-600">3종</span>
          </div>
        </div>
      </div>
    </div>
  );
};
const Loading = () => {
  return (
    <div
      className="fixed top-0 left-0 w-full h-full flex items-center justify-center z-50"
      style={{
        backgroundColor: `rgba(255, 255, 255, 0.2)`,
        backdropFilter: "blur(2px)",
      }}
    >
      <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-gray-700"></div>
    </div>
  );
};

export default KoreanSearchForm;

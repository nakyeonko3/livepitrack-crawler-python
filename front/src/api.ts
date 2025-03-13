const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export const getOptions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/options`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching options:", error);
  }
};

interface generateDiseaseDocsFileParams {
  turmGubun: string; // 01: , 02:
  occrFromDt: string; //
  occrToDt: string; //
  ctprvn: string; //
  dissCl: string; //
  lstkspCl: string; //
  legalIctsdGradSe: string; //
}

export const generateDiseaseDocsFile = async (
  data: generateDiseaseDocsFileParams
) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/animal-disease-report`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    // 응답이 성공적인지 확인
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 파일 다운로드 처리
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    // Content-Disposition 헤더에서 파일 이름을 가져오거나 기본값 설정
    const filename =
      response.headers
        .get("content-disposition")
        ?.split("filename=")[1]
        ?.trim() || "livestock_disease_data.xlsx";
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);

    return { success: true };
  } catch (error) {
    console.error("Error generating file:", error);
    return { success: false, error };
  }
};

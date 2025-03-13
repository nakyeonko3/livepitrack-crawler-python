const API_BASE_URL = "http://localhost:5000";

export const getOptions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/options`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching options:", error);
  }
};

export const generateParams = async (data: any) => {
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
    return await response.json();
  } catch (error) {
    console.error("Error generating params:", error);
  }
};

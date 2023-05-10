import axios from "axios";

export const sql_tool = async () => {
  const pplQuery = `source=opensearch_dashboards_sample_data_logs | where timestamp >= '2023-05-09 17:49:46' and timestamp <= '2023-05-09 18:04:46' | stats count() by host`;
  // console.log("got pplQuery ################", pplQuery);
  await axios.default
    .post(
      "http://127.0.0.1:5601/api/ppl/search",
      {
        query: pplQuery,
        format: "jdbc",
      },
      {
        headers: { "osd-xsrf": true },
        auth: {
          username: process.env.OS_USERNAME || "",
          password: process.env.OS_PASSWORD || "",
        },
      }
    )
    .then((res: any) => {
      // console.log("got response hjere ################");
      return JSON.stringify(res.jsonData);
    });
  return "Error while making a request for PPL Query";
};

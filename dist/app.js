// import { OpenAI } from "langchain/llms/openai";
// import { initializeAgentExecutorWithOptions } from "langchain/agents";
// import { DynamicTool } from "langchain/tools";
// import { sql_tool } from "./tool.js";
// import { ConsoleCallbackHandler } from "langchain/callbacks";
// export const run = async () => {
//   const model = new OpenAI({ temperature: 0 });
//   const pplQuery = `source=opensearch_dashboards_sample_data_logs | where timestamp >= '2023-05-09 17:49:46' and timestamp <= '2023-05-09 18:04:46' | stats count() by host`;
//   const tools = [
//     new DynamicTool({
//       name: "PPL Query Tool",
//       description: "use this tool to make a PPL Query in an OpenSearch cluster",
//       func: () => sql_tool(pplQuery),
//     }),
//   ];
//   const executor = await initializeAgentExecutorWithOptions(tools, model, {
//     agentType: "zero-shot-react-description",
//     verbose: true,
//     callbacks: [new ConsoleCallbackHandler()], // add a console callback handler
//   });
//   console.log("Loaded agent.");
//   const input = `Can you execute a PPL query and summarize the response?`;
//   console.log(`Executing with input "${input}"...`);
//   const result = await executor.call({ input });
//   console.log(`Got output ${result.output}`);
// };
// run();
// console.log("Welcome to the LangChain.js tutorial by LangChainers.");
import { OpenAI } from "langchain/llms/openai";
const model = new OpenAI({
    temperature: 0.9,
    modelName: "gpt-3.5-turbo",
    openAIApiKey: "sk-nMUTm9o0r9Ly7oAaaUqTT3BlbkFJgZxEcW0iuCXzmOoO54b", // In Node.js defaults to process.env.OPENAI_API_KEY
});
const res = await model.call("What would be a good company name a company that makes colorful socks?");
console.log({ res });

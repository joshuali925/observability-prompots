import { OpenAI } from "langchain/llms/openai";
import { initializeAgentExecutorWithOptions } from "langchain/agents";
import { DynamicTool } from "langchain/tools";
import { sql_tool } from "./tool.js";
import { ConsoleCallbackHandler } from "langchain/callbacks";
import * as dotenv from "dotenv"; // see https://github.com/motdotla/dotenv#how-do-i-use-dotenv-with-import
dotenv.config();

export const run = async () => {
  const model = new OpenAI({ temperature: 0 });

  const tools = [
    new DynamicTool({
      name: "PPL Query Tool",
      description:
        "use this tool to execute a PPL Query in an OpenSearch cluster",
      func: () => sql_tool(),
    }),
  ];

  const executor = await initializeAgentExecutorWithOptions(tools, model, {
    agentType: "zero-shot-react-description",
    verbose: true,
    callbacks: [new ConsoleCallbackHandler()], // add a console callback handler
    maxIterations: 2,
  });

  console.log("Loaded agent.");

  const input = `Can you execute a PPL query and summarize the response?`;

  console.log(`Executing with input "${input}"...`);

  const result = await executor.call({ input });

  console.log(`Got output ${result.output}`);
};
run();
// console.log("Welcome to the LangChain.js tutorial by LangChainers.");

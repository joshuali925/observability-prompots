const fs = require("fs");

const dataDir = `${__dirname}/data`;
const outputDir = `${__dirname}/output`;

const writeFile = (obj) => {
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(`${outputDir}/ppl_samples.json`, JSON.stringify(obj, null, 2));
};

const lines = fs
  .readFileSync(`${dataDir}/jaeger.txt`, "utf8")
  .split(/\r?\n/)
  .filter((line) => line.trim() !== "");

const samples = [];

tag = "jaeger-span";

context = {
  "jaeger-span": `
index name: 'jaeger-span-*'

field for error: 'tag.error'
field for latency, response time, duration: 'duration'
field for spans: 'spanId'
field for service: 'process.serviceName'

Accounting Service: 'accountingservice'
Ad Service: 'adservice'
Cache: 'cache'
Cart Service: 'cartservice'
Checkout Service: 'checkoutservice'
Currency Service: 'currencyservice'
Email Service: 'emailservice'
Fraud Detection Service: 'frauddetectionservice'
Frontend: 'frontend'
Frontend Proxy: 'frontendproxy'
Load Generator: 'loadgenerator'
Payment Service: 'paymentservice'
Product Catalog Service: 'productcatalogservice'
Quote Service: 'quoteservice'
Recommendation Service: 'recommendationservice'
Shipping Service: 'shippingservice'
Feature Flag Service: 'featureflagservice'
Feature Flag Store: 'featureflagstore'
Queue: 'queue'
`.trim(),
};

for (let i = 0; i < lines.length; i += 2) {
  const description = lines[i];
  const query = lines[i + 1];
  samples.push({
    tag,
    description,
    context: context[tag],
    query,
  });
}

console.info("❗samples:", samples);

writeFile(samples)

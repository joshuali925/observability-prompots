

Here are some sample questions and the PPL query to retrieve the information. Format:

a. Question
b. PPL query with sample schema
c. PPL query with placeholder variables

[index] is a placeholder for index name.
[field] is a placeholder for a field name.
[value] is a placeholder for a field value.

Examples:

What is the throughput of each service?
source=<index> | stats count() by <field>
source=jaeger-span* | stats count() by process.serviceName

What is the number of spans of service 'loadgenerator'?
source=<index> | where <field> = '<value>' | stats count()
source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count()

What is the number of spans per second for the load generator service?
source=<index> | where <field> = '<value>' | stats count() by span('<field>', 1s)
source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count() by span('startTime', 1s)

What is the average latency of spans in each service?
source=<index> | stats avg(<field>) by <field>
source=jaeger-span* | stats avg(duration) by process.serviceName

What is the current average latency of spans in each service?
source=<index> | where <field> >= 'now-5m' | stats avg(<field>) by <field>
source=jaeger-span* | where startTime >= 'now-5m' | stats avg(duration) by process.serviceName

What is the average latency of spans by service and operation name?
source=<index> | stats avg(<field>) by <field>, <field>
source=jaeger-span* | stats avg(duration) by process.serviceName, operationName

What is the average latency of spans in every 5 minutes intervals?
source=<index> | stats avg(<field>) by span('<field>', 5m)
source=jaeger-span* | stats avg(duration) by span('startTime', 5m)

What is the average latency of spans of frontend service?
source=<index> | where <field> = '<value>' | stats avg(<field>)
source=jaeger-span* | where process.serviceName = 'frontend' | stats avg(duration)

What are some services with latency over 1 second?
source=<index> | where <field> > 1000000 | stats count() by <field>
source=jaeger-span* | where duration > 1000000 | stats count() by process.serviceName

What are some spanIDs with latency over 1 second for the load generator service
source=<index> | where <field> > 1000000 and <field> = '<value>' | fields <field>
source=jaeger-span* | where duration > 1000000 and process.serviceName = 'loadgenerator' | fields spanID

What are some services with errors?
source=<index> | where <field> > 0 | stats count() by <field>
source=jaeger-span* | where status.code > 0 | stats count() by process.serviceName

What are some spans with errors for the accounting service
source=<index> | where <field> > 0 and <field> = '<value>' | fields <field>
source=jaeger-span* | where status.code > 0 and process.serviceName = 'accounting' | fields SpanID

What are the top 5 services with errors?
source=<index> | where <field> > 0 | stats count() as errors by <field> | sort - errors
source=jaeger-span* | where status.code > 0 | stats count() as errors by process.serviceName | sort - errors

What are the top 5 spans with least latency?
source=<index> | sort <field> | head 5 | fields <field>
source=jaeger-span* | sort duration | head 5 | fields spanID

---------------

Before you write the query, use tools to replace placeholder values. A tool can only be used once
You have access to the following tools:

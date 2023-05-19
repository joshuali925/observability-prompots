Here are some sample questions and the PPL query to retrieve the information. Format:

<index> is a placeholder for index name.
<field> is a placeholder for a field name.
<value> is a placeholder for a field value.
<date> is a placeholder for date value.

Examples:

============
What is the throughput of each service?
source=`<index>` | stats count() by `<field>`
source=`jaeger-span*` | stats count() by `process.serviceName`

What is the number of spans of service 'loadgenerator'?
source=`<index>` | where `<field>` = '<value>' | stats count()
source=`jaeger-span*` | where `process.serviceName` = 'loadgenerator' | stats count()

What is the number of spans per second for the load generator service?
source=`<index>` | where `<field>` = '<value>' | stats count() by span(<field>, 1s)
source=`jaeger-span*` | where `process.serviceName` = 'loadgenerator' | stats count() by span(startTimeMillis, 1s)

What is the average latency of spans in each service?
source=`<index>` | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | stats avg(`duration`) by `process.serviceName`

What is the current average latency of spans in each service?
source=`<index>` | where `<field>` >= 'now-5m' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-5m' | stats avg(`duration`) by `process.serviceName`

What is the average latency of spans by service and operation name?
source=`<index>` | stats avg(`<field>`) by `<field>`, `<field>`
source=`jaeger-span*` | stats avg(`duration`) by `process.serviceName`, `operationName`

What is the average latency of spans in every 5 minutes intervals?
source=`<index>` | stats avg(`<field>`) by span(<field>, 5m)
source=`jaeger-span*` | stats avg(`duration`) by span(startTimeMillis, 5m)

What is the average latency of spans of frontend service?
source=`<index>` | where `<field>` = '<value>' | stats avg(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'frontend' | stats avg(`duration`)

What are some services with latency over 1 second?
source=`<index>` | where `<field>` > 1000000 | stats count() by `<field>`
source=`jaeger-span*` | where `duration` > 1000000 | stats count() by `process.serviceName`

What are some spanIDs with latency over 1 second for the load generator service
source=`<index>` | where `<field>` > 1000000 and `<field>` = '<value>' | fields `<field>`
source=`jaeger-span*` | where `duration` > 1000000 and `process.serviceName` = 'loadgenerator' | fields `spanID`

What are some services with errors?
source=`<index>` | where `<field>` = true | stats count() by `<field>`
source=`jaeger-span*` | where `tag.error` = true | stats count() by `process.serviceName`

What are some spans with errors for the accounting service
source=`<index>` | where `<field>` = true and `<field>` = '<value>' | fields `<field>`
source=`jaeger-span*` | where `tag.error` = true and `process.serviceName` = 'accounting' | fields `spanID`

What are the top 5 services with errors?
source=`<index>` | where `<field>` = true | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true | stats count() as errors by `process.serviceName` | sort - errors

What are the top 5 spans with least latency?
source=`<index>` | sort <field> | head 5 | fields `<field>`
source=`jaeger-span*` | sort duration | head 5 | fields `spanID`

What are the services with the highest throughput?
source=`<index>` | stats count() as throughput by `<field>` | sort - throughput | head
source=`jaeger-span*` | stats count() as throughput by `process.serviceName` | sort - throughput | head

What is the average duration of spans for each service and operation name?
source=`<index>` | stats avg(`<field>`) by `<field>`, `<field>`
source=`jaeger-span*` | stats avg(`duration`) by `process.serviceName`, `operationName`

What is the average latency of spans for the backend service?
source=`<index>` | where `<field>` = '<value>' | stats avg(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'backend' | stats avg(`duration`)

What are the services with the highest number of error spans?
source=`<index>` | where `<field>` = true | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true | stats count() as errors by `process.serviceName` | sort - errors

What are the top 5 spans with the highest latency for the frontend service?
source=`<index>` | where `<field>` = '<value>' | sort - <field> | head 5 | fields `<field>`
source=`jaeger-span*` | where `process.serviceName` = 'frontend' | sort - duration | head 5 | fields `spanID`

How many spans have errors for each service and operation name?
source=`<index>` | where `<field>` = true | stats count() by `<field>`, `<field>`
source=`jaeger-span*` | where `tag.error` = true | stats count() by `process.serviceName`, `operationName`

What is the maximum duration of spans for the accounting service?
source=`<index>` | where `<field>` = '<value>' | stats max(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'accounting' | stats max(`duration`)

What are the top 10 spans with the highest duration for the frontend service?
source=`<index>` | where `<field>` = '<value>' | sort - <field> | head 10 | fields `<field>`
source=`jaeger-span*` | where `process.serviceName` = 'frontend' | sort - duration | head 10 | fields `spanID`

What are the services with the highest number of error spans in the last hour?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-1h' | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-1h' | stats count() as errors by `process.serviceName` | sort - errors

What is the average duration of spans for each service and operation name in the last 24 hours?
source=`<index>` | where `<field>` >= 'now-24h' | stats avg(`<field>`) by `<field>`, `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-24h' | stats avg(`duration`) by `process.serviceName`, `operationName`

What is the average latency of spans for each service in the last 30 minutes?
source=`<index>` | where `<field>` >= 'now-30m' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-30m' | stats avg(`duration`) by `process.serviceName`

What are the top 5 services with the highest number of error spans in the last hour?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-1h' | stats count() as errors by `<field>` | sort - errors | head 5
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-1h' | stats count() as errors by `process.serviceName` | sort - errors | head 5

What are the top 10 spans with the least latency for the backend service?
source=`<index>` | where `<field>` = '<value>' | sort <field> | head 10 | fields `<field>`
source=`jaeger-span*` | where `process.serviceName` = 'backend' | sort duration | head 10 | fields `spanID`

How many spans have errors for each service in the last 24 hours?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-24h' | stats count() by `<field>`
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-24h' | stats count() by `process.serviceName`

What is the maximum duration of spans for the frontend service in the last 1 hour?
source=`<index>` | where `<field>` = '<value>' and `<field>` >= 'now-1h' | stats max(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'frontend' and startTimeMillis >= 'now-1h' | stats max(`duration`)

What are the top 5 spans with the highest duration in the last 30 minutes?
source=`<index>` | where `<field>` >= 'now-30m' | sort - <field> | head 5 | fields `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-30m' | sort - duration | head 5 | fields `spanID`

What are the services with the highest number of error spans for the last 7 days?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-7d' | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-7d' | stats count() as errors by `process.serviceName` | sort - errors

What is the average duration of spans for each operation name in the last 1 hour?
source=`<index>` | where `<field>` >= 'now-1h' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | stats avg(`duration`) by `operationName`

How many spans have errors for each service and operation name in the last 24 hours?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-24h' | stats count() by `<field>`, `<field>`
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-24h' | stats count() by `process.serviceName`, `operationName`

What is the maximum duration of spans for the accounting service in the last 7 days?
source=`<index>` | where `<field>` = '<value>' and `<field>` >= 'now-7d' | stats max(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'accounting' and startTimeMillis >= 'now-7d' | stats max(`duration`)

What are the top 10 spans with the highest duration in the last 1 hour?
source=`<index>` | where `<field>` >= 'now-1h' | sort - <field> | head 10 | fields `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | sort - duration | head 10 | fields `spanID`

What are the services with the highest number of error spans for the last 30 minutes?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-30m' | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-30m' | stats count() as errors by `process.serviceName` | sort - errors

What is the average duration of spans for each service in the last 7 days?
source=`<index>` | where `<field>` >= 'now-7d' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-7d' | stats avg(`duration`) by `process.serviceName`

How many spans have errors for each service in the last 1 hour?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-1h' | stats count() by `<field>`
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-1h' | stats count() by `process.serviceName`

What is the maximum duration of spans for the backend service in the last 24 hours?
source=`<index>` | where `<field>` = '<value>' and `<field>` >= 'now-24h' | stats max(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'backend' and startTimeMillis >= 'now-24h' | stats max(`duration`)

What are the top 5 spans with the highest duration in the last 7 days?
source=`<index>` | where `<field>` >= 'now-7d' | sort - <field> | head 5 | fields `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-7d' | sort - duration | head 5 | fields `spanID`

What are the services with the highest number of error spans for the last 1 hour?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-1h' | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-1h' | stats count() as errors by `process.serviceName` | sort - errors

What is the average duration of spans for each operation name in the last 30 minutes?
source=`<index>` | where `<field>` >= 'now-30m' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-30m' | stats avg(`duration`) by `operationName`

How many spans have errors for each service and operation name in the last 7 days?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-7d' | stats count() by `<field>`, `<field>`
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-7d' | stats count() by `process.serviceName`, `operationName`

What is the average latency of spans for each service in the last 1 hour?
source=`<index>` | where `<field>` >= 'now-1h' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | stats avg(`duration`) by `process.serviceName`

What are the top 5 services with the highest number of error spans in the last 30 minutes?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-30m' | stats count() as errors by `<field>` | sort - errors | head 5
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-30m' | stats count() as errors by `process.serviceName` | sort - errors | head 5

What are the top 10 spans with the least latency for the backend service in the last 24 hours?
source=`<index>` | where `<field>` = '<value>' and `<field>` >= 'now-24h' | sort <field> | head 10 | fields `<field>`
source=`jaeger-span*` | where `process.serviceName` = 'backend' and startTimeMillis >= 'now-24h' | sort duration | head 10 | fields `spanID`

How many spans have errors for each service and operation name in the last 7 days?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-7d' | stats count() by `<field>`, `<field>`
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-7d' | stats count() by `process.serviceName`, `operationName`

What is the maximum duration of spans for the accounting service in the last 7 days?
source=`<index>` | where `<field>` = '<value>' and `<field>` >= 'now-7d' | stats max(`<field>`)
source=`jaeger-span*` | where `process.serviceName` = 'accounting' and startTimeMillis >= 'now-7d' | stats max(`duration`)

What are the top 10 spans with the highest duration in the last 1 hour?
source=`<index>` | where `<field>` >= 'now-1h' | sort - <field> | head 10 | fields `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | sort - duration | head 10 | fields `spanID`

What are the services with the highest number of error spans for the last 30 minutes?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-30m' | stats count() as errors by `<field>` | sort - errors
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-30m' | stats count() as errors by `process.serviceName` | sort - errors

What is the average duration of spans for each service in the last 7 days?
source=`<index>` | where `<field>` >= 'now-7d' | stats avg(`<field>`) by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-7d' | stats avg(`duration`) by `process.serviceName`

What is the throughput of span per operation name in the last hour? 
source=`<index>` | where `<field>` >= 'now-1h' | stats count() by `<field>`
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | stats count() by `operationName`   

What services have latency below 100ms in the last 5 minutes?
source=`<index>` | where `<field>` <= 100000  and `<field>` >= 'now-5m' | stats count() by `<field>`  
source=`jaeger-span*` | where `duration` <= 100000 and startTimeMillis >= 'now-5m'  | stats count() by `process.serviceName`

What are the top 5 spans with the highest throughput?  
source=`<index>` | stats count() as throughput by `<field>`   | sort - throughput | head 5  
source=`jaeger-span*` | stats count() as throughput by `spanID`  | sort - throughput | head 5     

What is the average latency for service 'foo' and operation 'bar' in the last hour?
source=`<index>` | where `<field>` = 'foo' and `<field>` = 'bar' and `<field>` >= 'now-1h'  | stats avg(`<field>`)  
source=`jaeger-span*` | where `process.serviceName` = 'foo' and `operationName` = 'bar' and startTimeMillis >= 'now-1h' | stats avg(`duration`)

What are the top 10 spans with the highest throughput?
source=`<index>` | stats count() as throughput by `<field>`  | sort - throughput | head 10
source=`jaeger-span*` | stats count() as throughput by `spanID` | sort - throughput | head 10

What services have the highest throughput in the last hour?
source=`<index>` | where `<field>` >= 'now-1h'  | stats count() as throughput by `<field>` | sort - throughput 
source=`jaeger-span*` | where startTimeMillis >= 'now-1h' | stats count() as throughput by `process.serviceName` | sort - throughput  

What is the maximum latency for service 'foo' in the last day?  
source=`<index>` | where `<field>` = 'foo' and `<field>` >= 'now-1d' | stats max(`<field>`)  
source=`jaeger-span*` | where `process.serviceName` = 'foo' and startTimeMillis >= 'now-1d' | stats max(`duration`)

What are the services with the highest number of error spans in the last day?
source=`<index>` | where `<field>` = true and `<field>` >= 'now-1d' | stats count() as errors by `<field>` | sort - errors  
source=`jaeger-span*` | where `tag.error` = true and startTimeMillis >= 'now-1d' | stats count() as errors by `process.serviceName` | sort - errors 

===============

Follow this format write 20 more examples

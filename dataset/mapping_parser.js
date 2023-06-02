const mapping = {
  body: {
    jaeger: {
      mappings: {
        dynamic_templates: [
          {
            span_tags_map: {
              path_match: "tag.*",
              mapping: {
                ignore_above: 256,
                type: "keyword",
              },
            },
          },
          {
            process_tags_map: {
              path_match: "process.tag.*",
              mapping: {
                ignore_above: 256,
                type: "keyword",
              },
            },
          },
        ],
        properties: {
          duration: {
            type: "long",
          },
          flags: {
            type: "integer",
          },
          logs: {
            type: "nested",
            dynamic: "false",
            properties: {
              fields: {
                type: "nested",
                dynamic: "false",
                properties: {
                  key: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  tagType: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  value: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                },
              },
              timestamp: {
                type: "long",
              },
            },
          },
          operationName: {
            type: "keyword",
            ignore_above: 256,
          },
          parentSpanID: {
            type: "keyword",
            ignore_above: 256,
          },
          process: {
            properties: {
              serviceName: {
                type: "keyword",
                ignore_above: 256,
              },
              tag: {
                properties: {
                  "container@id": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "host@arch": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "host@name": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "os@description": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "os@name": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "os@type": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "os@version": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@command": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@command_args": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@command_line": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@executable@name": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@executable@path": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@owner": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@pid": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@runtime@description": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@runtime@name": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "process@runtime@version": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "service@instance@id": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "service@namespace": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "telemetry@auto@version": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "telemetry@sdk@language": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "telemetry@sdk@name": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  "telemetry@sdk@version": {
                    type: "keyword",
                    ignore_above: 256,
                  },
                },
              },
              tags: {
                type: "nested",
                dynamic: "false",
                properties: {
                  key: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  tagType: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                  value: {
                    type: "keyword",
                    ignore_above: 256,
                  },
                },
              },
            },
          },
          references: {
            type: "nested",
            dynamic: "false",
            properties: {
              refType: {
                type: "keyword",
                ignore_above: 256,
              },
              spanID: {
                type: "keyword",
                ignore_above: 256,
              },
              traceID: {
                type: "keyword",
                ignore_above: 256,
              },
            },
          },
          spanID: {
            type: "keyword",
            ignore_above: 256,
          },
          startTime: {
            type: "long",
          },
          startTimeMillis: {
            type: "date",
            format: "epoch_millis",
          },
          tag: {
            properties: {
              "app@ads@ad_request_type": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@ads@ad_response_type": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@ads@category": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@ads@contextKeys": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@ads@contextKeys@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@ads@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@cart@items@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@currency@conversion@from": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@currency@conversion@to": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@email@recipient": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@featureflag@enabled": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@featureflag@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@filtered_products@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@filtered_products@list": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@order@amount": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@order@id": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@order@items@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@payment@amount": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@payment@card_type": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@payment@card_valid": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@payment@charged": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@product@id": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@product@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@product@quantity": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@products@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@products_recommended@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@quote@cost@total": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@quote@items@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@recommendation@cache_enabled": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@session@id": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@shipping@amount": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@shipping@cost@total": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@shipping@items@count": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@shipping@tracking@id": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@shipping@zip_code": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@synthetic_request": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@user@currency": {
                type: "keyword",
                ignore_above: 256,
              },
              "app@user@id": {
                type: "keyword",
                ignore_above: 256,
              },
              busy_ns: {
                type: "keyword",
                ignore_above: 256,
              },
              "code@filepath": {
                type: "keyword",
                ignore_above: 256,
              },
              "code@function": {
                type: "keyword",
                ignore_above: 256,
              },
              "code@lineno": {
                type: "keyword",
                ignore_above: 256,
              },
              "code@namespace": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@instance": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@redis@database_index": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@redis@flags": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@statement": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@system": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@type": {
                type: "keyword",
                ignore_above: 256,
              },
              "db@url": {
                type: "keyword",
                ignore_above: 256,
              },
              decode_time_microseconds: {
                type: "keyword",
                ignore_above: 256,
              },
              error: {
                type: "keyword",
                ignore_above: 256,
              },
              "http@client_ip": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@flavor": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@host": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@method": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@request_content_length": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@request_content_length_uncompressed": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@response_content_length": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@route": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@scheme": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@status_code": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@status_text": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@target": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@url": {
                type: "keyword",
                ignore_above: 256,
              },
              "http@user_agent": {
                type: "keyword",
                ignore_above: 256,
              },
              idle_ns: {
                type: "keyword",
                ignore_above: 256,
              },
              idle_time_microseconds: {
                type: "keyword",
                ignore_above: 256,
              },
              "internal@span@format": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@destination": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@destination@kind": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@destination@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@destination_kind": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@kafka@message@offset": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@kafka@partition": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@kafka@source@partition": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@message@payload_size_bytes": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@message_id": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@message_payload_size_bytes": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@operation": {
                type: "keyword",
                ignore_above: 256,
              },
              "messaging@system": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@host@ip": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@host@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@host@port": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@peer@ip": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@peer@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@peer@port": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@sock@peer@addr": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@sock@peer@port": {
                type: "keyword",
                ignore_above: 256,
              },
              "net@transport": {
                type: "keyword",
                ignore_above: 256,
              },
              "otel@library@name": {
                type: "keyword",
                ignore_above: 256,
              },
              "otel@library@version": {
                type: "keyword",
                ignore_above: 256,
              },
              "otel@status_code": {
                type: "keyword",
                ignore_above: 256,
              },
              "otel@status_description": {
                type: "keyword",
                ignore_above: 256,
              },
              "peer@ipv4": {
                type: "keyword",
                ignore_above: 256,
              },
              "peer@service": {
                type: "keyword",
                ignore_above: 256,
              },
              "phoenix@action": {
                type: "keyword",
                ignore_above: 256,
              },
              "phoenix@plug": {
                type: "keyword",
                ignore_above: 256,
              },
              query_time_microseconds: {
                type: "keyword",
                ignore_above: 256,
              },
              queue_time_microseconds: {
                type: "keyword",
                ignore_above: 256,
              },
              "rpc@grpc@status_code": {
                type: "keyword",
                ignore_above: 256,
              },
              "rpc@method": {
                type: "keyword",
                ignore_above: 256,
              },
              "rpc@service": {
                type: "keyword",
                ignore_above: 256,
              },
              "rpc@system": {
                type: "keyword",
                ignore_above: 256,
              },
              "rpc@user_agent": {
                type: "keyword",
                ignore_above: 256,
              },
              "sinatra@template_name": {
                type: "keyword",
                ignore_above: 256,
              },
              source: {
                type: "keyword",
                ignore_above: 256,
              },
              "span@kind": {
                type: "keyword",
                ignore_above: 256,
              },
              "thread@id": {
                type: "keyword",
                ignore_above: 256,
              },
              "thread@name": {
                type: "keyword",
                ignore_above: 256,
              },
              total_time_microseconds: {
                type: "keyword",
                ignore_above: 256,
              },
            },
          },
          tags: {
            type: "nested",
            dynamic: "false",
            properties: {
              key: {
                type: "keyword",
                ignore_above: 256,
              },
              tagType: {
                type: "keyword",
                ignore_above: 256,
              },
              value: {
                type: "keyword",
                ignore_above: 256,
              },
            },
          },
          traceID: {
            type: "keyword",
            ignore_above: 256,
          },
        },
      },
    },
  },
  statusCode: 200,
  headers: {
    "x-opaque-id": "1b50cf27-1efe-4690-9ebe-d3de7457a9d3",
    "content-type": "application/json; charset=UTF-8",
    "content-length": "9454",
  },
  meta: {
    context: null,
    request: {
      params: {
        method: "GET",
        path: "/jaeger/_mapping",
        body: null,
        querystring: "",
        headers: {
          "user-agent":
            "opensearch-js/2.2.1 (linux 5.4.241-160.348.amzn2int.x86_64-x64; Node.js v18.15.0)",
          "x-opensearch-product-origin": "opensearch-dashboards",
          "x-opaque-id": "1b50cf27-1efe-4690-9ebe-d3de7457a9d3",
        },
        timeout: 30000,
      },
      options: {},
      id: 1,
    },
    name: "opensearch-js",
    connection: {
      url: "http://localhost:9200/",
      id: "http://localhost:9200/",
      headers: {},
      deadCount: 0,
      resurrectTimeout: 0,
      _openRequests: 0,
      status: "alive",
      roles: {
        data: true,
        ingest: true,
      },
    },
    attempts: 0,
    aborted: false,
  },
};


const properties = mapping.body[Object.keys(mapping.body)[0]].mappings.properties

const parseProperties = (keys, prefix, properties) => {
  for (const key in properties) {
    if (!properties.hasOwnProperty(key)) continue;
    const value = properties[key];
    if (value.properties) {
      parseProperties(keys, prefix + "." + key, value.properties);
    } else {
      keys.push({
        field: (prefix ? prefix.slice(1) + '.' : '') + key,
        type: value.type,
      });
    }
  }
};



const arr = []
parseProperties(arr, '', properties)

for (let i = 0; i < arr.length; i++) {
  const element = arr[i];
  console.info('❗element:', element);
}

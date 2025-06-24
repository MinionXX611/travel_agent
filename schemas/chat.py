from jsonschema import Draft7Validator

# 请求 Schema
ASK_REQUEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "聊天请求参数",
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1000,
            "pattern": "^[\\s\\S]*$",
            "description": "用户输入的聊天内容"
        },
        "conversation_id": {
            "type": ["string", "null"],
            "pattern": "^[a-zA-Z0-9_-]*$",
            "maxLength": 100,
            "description": "会话ID，首次请求可为空"
        }
    },
    "required": ["text"],
    "additionalProperties": False
}

# 响应 Schema (用于验证Dify API返回的数据)
DIFY_RESPONSE_SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Dify SSE Event Schema",
  "description": "Schema for validating Dify API Server-Sent Events stream",
  "type": "object",
  "properties": {
    "event": {
      "type": "string",
      "enum": [
        "message",
        "message_file",
        "message_end",
        "tts_message",
        "tts_message_end",
        "message_replace",
        "workflow_started",
        "node_started",
        "node_finished",
        "workflow_finished",
        "error",
        "ping"
      ]
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "任务 ID，用于请求跟踪"
    },
    "message_id": {
      "type": "string",
      "format": "uuid",
      "description": "消息唯一 ID"
    },
    "conversation_id": {
      "type": "string",
      "format": "uuid",
      "description": "会话 ID"
    },
    "workflow_run_id": {
      "type": "string",
      "description": "workflow 执行 ID"
    },
    "answer": {
      "type": "string",
      "description": "LLM 返回文本内容"
    },
    "created_at": {
      "type": "integer",
      "description": "创建时间戳"
    },
    "finished_at": {
      "type": "integer",
      "description": "结束时间戳"
    },
    "audio": {
      "type": "string",
      "description": "Base64 编码的音频数据"
    },
    "id": {
      "type": "string",
      "description": "对象唯一ID"
    },
    "data": {
      "type": "object",
      "anyOf": [
        {
          "properties": {
            "id": { "type": "string" },
            "workflow_id": { "type": "string" },
            "sequence_number": { "type": "integer", "minimum": 1 },
            "created_at": { "type": "integer" }
          }
        },
        {
          "properties": {
            "id": { "type": "string" },
            "node_id": { "type": "string" },
            "node_type": { "type": "string" },
            "title": { "type": "string" },
            "index": { "type": "integer" },
            "predecessor_node_id": { "type": ["string", "null"] },
            "inputs": { "type": ["object", "null"] },
            "created_at": { "type": "integer" }
          }
        },
        {
          "properties": {
            "id": { "type": "string" },
            "node_id": { "type": "string" },
            "status": { "enum": ["running", "succeeded", "failed", "stopped"] },
            "outputs": { "type": "object" },
            "error": { "type": ["string", "null"] },
            "elapsed_time": { "type": "number" },
            "execution_metadata": {
              "type": "object",
              "properties": {
                "total_tokens": { "type": "integer" },
                "total_price": { "type": "string" },
                "currency": { "type": "string" }
              }
            },
            "created_at": { "type": "integer" }
          }
        },
        {
          "properties": {
            "id": { "type": "string" },
            "workflow_id": { "type": "string" },
            "status": { "enum": ["running", "succeeded", "failed", "stopped"] },
            "outputs": { "type": "object" },
            "error": { "type": ["string", "null"] },
            "elapsed_time": { "type": "number" },
            "total_tokens": { "type": "integer" },
            "total_steps": { "type": ["string","integer"] },
            "created_at": { "type": "integer" },
            "finished_at": { "type": "integer" }
          }
        }
      ]
    },
    "metadata": {
      "type": "object",
      "properties": {
        "usage": {
          "type": "object",
          "properties": {
            "prompt_tokens": { "type": "integer" },
            "completion_tokens": { "type": "integer" },
            "total_tokens": { "type": "integer" },
            "total_price": { "type": "string" },
            "currency": { "type": "string" }
          }
        },
        "retriever_resources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "position": { "type": "integer" },
              "dataset_id": { "type": "string", "format": "uuid" },
              "document_id": { "type": "string", "format": "uuid" },
              "content": { "type": "string" }
            }
          }
        }
      }
    },
    "status": {
      "type": "integer",
      "description": "HTTP 状态码"
    },
    "code": {
      "type": "string",
      "description": "错误码"
    },
    "message": {
      "type": "string",
      "description": "错误消息"
    },
    "type": {
      "type": "string",
      "enum": ["image"],
      "description": "文件类型"
    },
    "url": {
      "type": "string",
      "format": "uri",
      "description": "文件访问地址"
    },
    "belongs_to": {
      "type": "string",
      "enum": ["user", "assistant"],
      "description": "文件归属"
    }
  },
  "required": ["event"],
  "oneOf": [
    {
      "properties": {
        "event": { "const": "message" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "conversation_id": { "type": "string" },
        "answer": { "type": "string" },
        "created_at": { "type": "integer" }
      }
    },
    {
      "properties": {
        "event": { "const": "message_file" },
        "id": { "type": "string" },
        "type": { "type": "string" },
        "belongs_to": { "type": "string" },
        "url": { "type": "string" },
        "conversation_id": { "type": "string" }
      }
    },
    {
      "properties": {
        "event": { "const": "message_end" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "conversation_id": { "type": "string" },
        "metadata": { "$ref": "#/properties/metadata" }
      }
    },
    {
      "properties": {
        "event": { "const": "tts_message" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "audio": { "type": "string" },
        "created_at": { "type": "integer" }
      }
    },
    {
      "properties": {
        "event": { "const": "tts_message_end" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "audio": { "const": "" },
        "created_at": { "type": "integer" }
      }
    },
    {
      "properties": {
        "event": { "const": "message_replace" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "conversation_id": { "type": "string" },
        "answer": { "type": "string" },
        "created_at": { "type": "integer" }
      }
    },
    {
      "properties": {
        "event": { "const": "workflow_started" },
        "task_id": { "type": "string" },
        "workflow_run_id": { "type": "string" },
        "data": { "$ref": "#/properties/data/anyOf/0" }
      }
    },
    {
      "properties": {
        "event": { "const": "node_started" },
        "conversation_id": { "type": "string" },
        "message_id": { "type": "string" },
        "created_at": { "type": "integer" },
        "task_id": { "type": "string" },
        "workflow_run_id": { "type": "string" },
        "data": { "$ref": "#/properties/data/anyOf/1" }
      }
    },
    {
      "properties": {
        "event": { "const": "node_finished" },
        "task_id": { "type": "string" },
        "workflow_run_id": { "type": "string" },
        "data": { "$ref": "#/properties/data/anyOf/2" }
      }
    },
    {
      "properties": {
        "event": { "const": "workflow_finished" },
        "task_id": { "type": "string" },
        "workflow_run_id": { "type": "string" },
        "data": { "$ref": "#/properties/data/anyOf/3" }
      }
    },
    {
      "properties": {
        "event": { "const": "error" },
        "task_id": { "type": "string" },
        "message_id": { "type": "string" },
        "status": { "type": "integer" },
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    },
    {
      "properties": {
        "event": { "const": "ping" }
      }
    }
  ]
}


# 预编译验证器（提升性能）
ask_request_validator = Draft7Validator(ASK_REQUEST_SCHEMA)
dify_response_validator = Draft7Validator(DIFY_RESPONSE_SCHEMA)